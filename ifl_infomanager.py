import os

import yaml
import pickle
import datetime
import ifl_system
import random

class InformationManager():
    screensize = "2560x1080"
    imageFolder = "./wallpapers"
    thumbnailFolder = "./thumbs"
    freshDays = 2                   # Number of days after download, that a new wallpaper is still considered fresh and
                                    # will be preferred over a random wallpaper at the start.
    startupMode = "latest"          # Which wallpaper to set at startup
                                    # latest: The latest wallpaper that was downloaded
                                    # random: Just a random wallpaper
                                    # fresh_random: The latest wallpaper, if it was downloaded within a timeframe of a number of days
    dataFile = "./wallpaper_info.dat"
    settingsFile = "./config.yaml"
    currentWallpaper = None         # The wallpaper that is currently set (Tuple)

    blacklist = []          # Just a list of IDs which are blacklisted (disliked). We don't want to download these again
    wallpaper_info = []     # A list of Tuples. Each tuple contains:
                                # 0: The ID
                                # 1: The title of the wallpaper
                                # 2: The name of the photographer
                                # 3: The filename on disk
                                # 4: The date when the wallpaper was downloaded
                                # 5: The corresponding thumbnail-filename

    randomList = []         # List of indices to the wallpaper_info list.
    randomIndex = 0         # current position in the randomList. Generate a new randomList on overflow.

    def get_current_wallpaper(self):
        return self.currentWallpaper

    def set_fresh_random_wallpaper(self):
        largest_id = 0
        wp = None
        for i, el in enumerate(self.wallpaper_info):
            if int(el[0]) > largest_id:
                largest_id = int(el[0])
                wp = el

        if wp:
            # Compare date to the current date
            if (wp[4] - datetime.date.today()).days <= 2:
                self.currentWallpaper = wp
                ifl_system.set_wallpaper(self.imageFolder + "/" + self.currentWallpaper[3], True)
                return self.currentWallpaper
            else:
                self.set_random_wallpaper()

    def set_latest_wallpaper(self):
        largest_id = 0
        wp = None
        for i, el in enumerate(self.wallpaper_info):
            if int(el[0]) > largest_id:
                largest_id = int(el[0])
                wp = el

        if wp:
            self.currentWallpaper = wp
            ifl_system.set_wallpaper(self.imageFolder + "/" + self.currentWallpaper[3], True)
            return self.currentWallpaper

    def set_random_wallpaper(self):
        if len(self.wallpaper_info) > 1:

            while True:
                random_wp = self.wallpaper_info[self.randomList[self.randomIndex]]
                self.randomIndex += 1
                if self.randomIndex >= len(self.randomList):
                    random.shuffle(self.randomList)
                    self.randomIndex = 0

                if random_wp[0] != self.currentWallpaper[0]:
                    break

            self.currentWallpaper = random_wp
            ifl_system.set_wallpaper(self.imageFolder + "/" + self.currentWallpaper[3], True)
            return self.currentWallpaper

    def dislike_current(self):
        try:
            os.remove(os.path.join(self.imageFolder, self.currentWallpaper[3]))
            os.remove(os.path.join(self.thumbnailFolder, self.currentWallpaper[5]))
        except FileNotFoundError:
            print("Wallpapers / Thumb could not be deleted or was not found.")
            
        self.delete_wallpaper_entry(self.currentWallpaper[0])
        self.add_to_blacklist(id)
        self.write_wallpaper_info()
        self.initialize_random_list()
        self.set_random_wallpaper()

    def initialize_random_list(self):
        self.randomList = list(range(0, len(self.wallpaper_info)))
        random.shuffle(self.randomList)
        self.randomIndex = 0

    def check_download_id(self,id):
        """ Check if the image with the given id needs to be downloaded.
        It should not be downloaded, if it is on the blacklist or in the info list.
        """
        if id in self.blacklist:
            return False

        for el in self.wallpaper_info:
            if el[0] == id:
                return False

        return True

    def add_to_blacklist(self, id):
        self.blacklist.append(id)

    def add_to_blacklist_flush(self, id):
        self.add_to_blacklist(id)
        self.write_wallpaper_info()

    def add_wallpaper_entry(self, id, title, photographer, filename, thumbfilename):
        self.wallpaper_info.append((id, title, photographer, filename, datetime.date.today(), thumbfilename))
        self.initialize_random_list()

    def add_wallpaper_entry_flush(self, id, title, photographer, filename, thumbfilename):
        self.add_wallpaper_entry(id, title, photographer, filename, thumbfilename)
        self.write_wallpaper_info()

    def delete_wallpaper_entry(self, id):
        for i, el in enumerate(self.wallpaper_info):
            if el[0] == id:
                self.wallpaper_info.pop(i)
                break

    def write_settings(self):
        with open(self.settingsFile, 'w') as f:
            contents = {'imageFolder': self.imageFolder,
                        'thumbnailFolder': self.thumbnailFolder,
                        'dataFile': self.dataFile,
                        'freshDays': self.freshDays}
            yaml.dump(contents, stream=f, default_flow_style=False)

    def load_settings(self):
        try:
            f = open(self.settingsFile, 'r')
            contents = yaml.load(f)
            self.imageFolder = contents.get('imageFolder', self.imageFolder)
            self.thumbnailFolder = contents.get('thumbnailFolder', self.thumbnailFolder)
            self.dataFile = contents.get('dataFile', self.dataFile)
            self.freshDays = contents.get('freshDays', self.freshDays)
            f.close()
        except IOError:
            # Settings-File doesn't exist
            print("Settings-File doesn't exist or is corrupt.")
            self.write_settings()

    def write_wallpaper_info(self):
        with open(self.dataFile, 'wb') as f:
            pickle.dump((self.wallpaper_info, self.blacklist), f)

    # Load the information about the already downloaded wallpapers and the blacklist
    def load_wallpaper_info(self):
        try:
            f = open(self.dataFile, 'rb')
            (self.wallpaper_info, self.blacklist) = pickle.load(f)
            f.close()
        except IOError:
            # File doesn't exist
            print("Database-File doesn't exist")
        except pickle.PickleError:
            # Error in reading the pickle information
            print("Could not read pickle-file")

    def __init__(self):
        self.screensize = ifl_system.get_resolution()
        self.load_settings()
        self.load_wallpaper_info()
        self.initialize_random_list()