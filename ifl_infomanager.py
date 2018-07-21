import yaml
import pickle

class InformationManager():
    screensize = "2560x1080"
    imageFolder = "./wallpapers"
    thumbnailFolder = "./thumbs"
    tempFolder = "./temp"
    dataFile = "./wallpaper_info.dat"
    settingsFile = "./config.yaml"

    blacklist = []          # Just a list of IDs which are blacklisted (disliked). We don't want to download these again
    wallpaper_info = []     # A list of Tuples. Each tuple contains:
                                # 0: The ID
                                # 1: The title of the wallpaper
                                # 2: The name of the photographer
                                # 3: The filename on disk

    def write_settings(self):
        with open(self.settingsFile, 'w') as f:
            contents = {'imageFolder': self.imageFolder,
                        'thumbnailFolder': self.thumbnailFolder,
                        'tempFolder': self.tempFolder,
                        'dataFile': self.dataFile}
            yaml.dump(contents, stream=f, default_flow_style=False)

    def load_settings(self):
        try:
            f = open(self.settingsFile, 'w')
            contents = yaml.load(f)
            self.imageFolder = contents['imageFolder']
            self.thumbnailFolder = contents['thumbnailFolder']
            self.tempFolder = contents['tempFolder']
            self.dataFile = contents['dataFile']
            f.close()
        except IOError:
            # Settings-File doesn't exist
            print("Settings-File doesn't exist")
            self.write_settings()

    def write_wallpaper_info(self):
        with open(self.dataFile, 'w') as f:
            pickle.dump((self.wallpaper_info, self.blacklist), f)

    # Load the information about the already downloaded wallpapers and the blacklist
    def load_wallpaper_info(self):
        try:
            f = open(self.dataFile, 'r')
            (self.wallpaper_info, self.blacklist) = pickle.load(f)
            f.close()
        except IOError:
            # File doesn't exist
            print("Database-File doesn't exist")
        except pickle.PickleError:
            # Error in reading the pickle information
            print("Could not read pickle-file")

    def __init__(self):
        self.load_settings()
        self.load_wallpaper_info()
        pass