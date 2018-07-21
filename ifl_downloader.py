from urllib.request import urlopen, Request

import os
import sys
import re   # Regular expressions
from ifl_infomanager import InformationManager

# Merge dictionaries. Used for merging resolutions.
# Necessary workaround for Python 2.x   :(
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

HOST = 'http://interfacelift.com'
RES_WIDESCREEN_16_10 = {
    # widescreen 16:10
    '6400x4000': '/wallpaper/downloads/date/wide_16:10/6400x4000/',
    '5120x3200': '/wallpaper/downloads/date/wide_16:10/5120x3200/',
    '3840x2400': '/wallpaper/downloads/date/wide_16:10/3840x2400/',
    '3360x2100': '/wallpaper/downloads/date/wide_16:10/3360x2100/',
    '2880x1800': '/wallpaper/downloads/date/wide_16:10/2880x1800/',
    '2560x1600': '/wallpaper/downloads/date/wide_16:10/2560x1600/',
    '2304x1440': '/wallpaper/downloads/date/wide_16:10/2304x1440/',
    '2048x1280': '/wallpaper/downloads/date/wide_16:10/2048x1280/',
    '1920x1200': '/wallpaper/downloads/date/wide_16:10/1920x1200/',
    '1680x1050': '/wallpaper/downloads/date/wide_16:10/1680x1050/',
    '1440x900': '/wallpaper/downloads/date/wide_16:10/1440x900/',
    '1280x800': '/wallpaper/downloads/date/wide_16:10/1280x800/',
    '1152x720': '/wallpaper/downloads/date/wide_16:10/1152x720/',
    '1024x640': '/wallpaper/downloads/date/wide_16:10/1024x640/',
}
RES_WIDESCREEN_16_9 = {
    # widescreen 16:9
    '5120x2880': '/wallpaper/downloads/date/wide_16:9/5120x2880/',
    '3840x2160': '/wallpaper/downloads/date/wide_16:9/3840x2160/',
    '3200x1800': '/wallpaper/downloads/date/wide_16:9/3200x1800/',
    '2880x1620': '/wallpaper/downloads/date/wide_16:9/2880x1620/',
    '2560x1440': '/wallpaper/downloads/date/wide_16:9/2560x1440/',
    '1920x1080': '/wallpaper/downloads/date/wide_16:9/1920x1080/',
    '1600x900': '/wallpaper/downloads/date/wide_16:9/1600x900/',
    '1366x768': '/wallpaper/downloads/date/wide_16:9/1366x768/',
    '1280x720': '/wallpaper/downloads/date/wide_16:9/1280x720/',
}
RES_WIDESCREEN_21_9 = {
    # widescreen 21:9
    '2560x1080': '/wallpaper/downloads/date/wide_21:9/2560x1080/',
    '3440x1440': '/wallpaper/downloads/date/wide_21:9/3440x1440/',
    '6400x3600': '/wallpaper/downloads/date/wide_21:9/6400x3600/',
}
RES_DUAL_MONITORS = {
    # dual monitors
    '5120x1600': '/wallpaper/downloads/date/2_screens/5120x1600/',
    '5120x1440': '/wallpaper/downloads/date/2_screens/5120x1440/',
    '3840x1200': '/wallpaper/downloads/date/2_screens/3840x1200/',
    '3840x1080': '/wallpaper/downloads/date/2_screens/3840x1080/',
    '3360x1050': '/wallpaper/downloads/date/2_screens/3360x1050/',
    '3200x1200': '/wallpaper/downloads/date/2_screens/3200x1200/',
    '2880x900': '/wallpaper/downloads/date/2_screens/2880x900/',
    '2560x1024': '/wallpaper/downloads/date/2_screens/2560x1024/',
}
RES_TRIPLE_MONITORS = {
    # triple monitors
    '7680x1600': '/wallpaper/downloads/date/3_screens/7680x1600/',
    '7680x1440': '/wallpaper/downloads/date/3_screens/7680x1440/',
    '5760x1200': '/wallpaper/downloads/date/3_screens/5760x1200/',
    '5760x1080': '/wallpaper/downloads/date/3_screens/5760x1080/',
    '5040x1050': '/wallpaper/downloads/date/3_screens/5040x1050/',
    '4800x1200': '/wallpaper/downloads/date/3_screens/4800x1200/',
    '4800x900': '/wallpaper/downloads/date/3_screens/4800x900/',
    '4320x900': '/wallpaper/downloads/date/3_screens/4320x900/',
    '4200x1050': '/wallpaper/downloads/date/3_screens/4200x1050/',
    '4096x1024': '/wallpaper/downloads/date/3_screens/4096x1024/',
    '3840x1024': '/wallpaper/downloads/date/3_screens/3840x1024/',
    '3840x960': '/wallpaper/downloads/date/3_screens/3840x960/',
    '3840x720': '/wallpaper/downloads/date/3_screens/3840x720/',
    '3072x768': '/wallpaper/downloads/date/3_screens/3072x768/',
}
RES_IPHONE = {
    # iPhone
    'iphone_6_plus': '/wallpaper/downloads/date/iphone/iphone_6_plus/',
    'iphone_6': '/wallpaper/downloads/date/iphone/iphone_6/',
    'iphone_5s': '/wallpaper/downloads/date/iphone/iphone_5s,_5c,_5/',
    'iphone_5c': '/wallpaper/downloads/date/iphone/iphone_5s,_5c,_5/',
    'iphone_5': '/wallpaper/downloads/date/iphone/iphone_5s,_5c,_5/',
    'iphone_4': '/wallpaper/downloads/date/iphone/iphone_4,_4s/',
    'iphone_4s': '/wallpaper/downloads/date/iphone/iphone_4,_4s/',
    'iphone': '/wallpaper/downloads/date/iphone/iphone,_3g,_3gs/',
    'iphone_3g': '/wallpaper/downloads/date/iphone/iphone,_3g,_3gs/',
    'iphone_3gs': '/wallpaper/downloads/date/iphone/iphone,_3g,_3gs/',
}
RES_IPAD = {
    # iPad
    'ipad_air': '/wallpaper/downloads/date/ipad/ipad_air,_4,_3,_retina_mini/',
    'ipad_4': '/wallpaper/downloads/date/ipad/ipad_air,_4,_3,_retina_mini/',
    'ipad_3': '/wallpaper/downloads/date/ipad/ipad_air,_4,_3,_retina_mini/',
    'ipad_retina_mini': '/wallpaper/downloads/date/ipad/ipad_air,_4,_3,_retina_mini/',
    'ipad_mini': '/wallpaper/downloads/date/ipad/ipad_mini,_ipad_1,_2/',
    'ipad_1': '/wallpaper/downloads/date/ipad/ipad_mini,_ipad_1,_2/',
    'ipad_2': '/wallpaper/downloads/date/ipad/ipad_mini,_ipad_1,_2/',
}
RES_PATHS = merge_dicts(
    RES_WIDESCREEN_16_10,
    RES_WIDESCREEN_16_9,
    RES_WIDESCREEN_21_9,
    RES_DUAL_MONITORS,
    RES_TRIPLE_MONITORS,
    RES_IPHONE,
    RES_IPAD,
)

class IFLDownloader:

    IMG_PATH_PATTERN = re.compile(r'<a href=\"(?P<path>.+)\"><img.+?src=\"/img_NEW/button_download')
    IMG_FILE_PATTERN = re.compile(r'[^/]*$')

    RES_PATH = RES_PATHS["1920x1080"]

    im: InformationManager = None   # The information manager

    # Downloads the given url and write it to the given directory
    def download_file(self, url, saveDir):
        # interfacelift returns a 403 forbidden unless you include a referer.
        headers = { 'User-Agent' : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
                    'Referer': url}
        req = Request(url, None, headers)
        filename = self.IMG_FILE_PATTERN.search(url).group()
        saveFile = os.path.join(saveDir, filename)
        with open(saveFile, 'wb') as f:
            try:
                res = urlopen(req)
                f.write(res.read())
                print('[+] Downloaded %s' % filename)
            except Exception as e:
                print(e)
                try: os.remove(saveFile)
                except: pass

    # Returns the path of the specified page number
    def get_page_path(self, pageNumber):
        return '%sindex%d.html' % (self.RES_PATH, pageNumber)

    # Returns the full URL of the specified path
    def get_url_from_path(self, path):
        return '%s/%s' % (HOST, path)

    # Returns the full URL of the specified page number
    def get_page_url(self, pageNumber):
        return self.get_url_from_path(self.get_page_path(pageNumber))

    # Returns True if next page exists, else False
    # CURRENTLY ONLY ONE PAGE IS SUPPORTED
    # def has_next_page(pageContent, currentPage):
    #     return True if pageContent.find(get_page_path(currentPage+ 1)) > -1 else False

    # Opens the specified page and returns the page's HTML content
    def open_page(self, pageNumber):
        url = self.get_page_url(pageNumber)
        # interfacelift returns a 403 forbidden unless you include a referer.
        headers = { 'User-Agent' : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
                    'Referer': url}
        try:
            req = Request(url, None, headers)
            f = urlopen(req)
        except IOError as e:
            print('Failed to open', url)
            if hasattr(e, 'code'):
                print('Error code:', e.code)
        return f.read().decode(errors='ignore')

    def set_resolution(self, res):
        if res not in list(self.RES_PATHS.keys()):
            print('Invalid specified resolution (%s)' % res)
            print('List available resolutions: %s --list' % os.path.basename(__file__))
            # sys.exit(1)
        else:
            self.RES_PATH = RES_PATHS["1920x1080"]

    def update(self):

        # Create directory if not exist
        if not os.path.exists(self.im.imageFolder):
            os.makedirs(self.im.imageFolder)

        if not os.path.exists(self.im.tempFolder):
            os.makedirs(self.im.tempFolder)

        if not os.path.exists(self.im.thumbnailFolder):
            os.makedirs(self.im.thumbnailFolder)

        # Add image URLs to queue
        page = 1
        pageContent = self.open_page(page)
        links = self.IMG_PATH_PATTERN.finditer(pageContent)
        for link in links:
            url = self.get_url_from_path(link.group('path'))
            filename = self.IMG_FILE_PATTERN.search(url).group()
            saveFile = os.path.join(self.im.imageFolder, filename)
            self.download_file(url, self.im.imageFolder)


#            else:
#                print('[-] Skipped %s (already exists)' % filename)

    def __init__(self, inf_man):
        """

        :type inf_man: InformationManager
        """
        self.inf_man = inf_man
        pass