import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

from interfacelift_wallpaper_changer.infomanager import InformationManager
from interfacelift_wallpaper_changer.guimodules import *
import interfacelift_wallpaper_changer.downloader as dl
from interfacelift_wallpaper_changer.resources import *

class SystemTrayIcon(QSystemTrayIcon):

    window = None
    wa = None

    def initialize_window(self, inf_man, downloader):
        menu = QMenu(self.parent())
        self.window = SystemTrayWindow(parent=self.parent(), inf_man=inf_man, downloader=downloader)
        self.wa = QWidgetAction(self.parent())
        self.wa.setDefaultWidget(self.window)
        menu.setFixedWidth(fixedWidthTray)
        menu.addAction(self.wa)
        #        exitAction = menu.addAction("Exit")
        #        exitAction.triggered.connect(qApp.quit)
        self.setContextMenu(menu)
        self.setToolTip("Interfacelift Wallpaper Changer")

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("Updating wallpaper database...")

def main():
    print("Welcome to Interfacelift-wallpaper-changer! Starting update.")

    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Interfacelift-Wallpaper-Changer")
    app.setApplicationName("Interfacelift-Wallpaper-Changer")

    with open(stylesheetFile, 'r') as f:
        stylesheet = f.read()

    app.setStyleSheet(stylesheet)
    app.setQuitOnLastWindowClosed(False)

    screen_rect = app.desktop().screenGeometry()
    screensize = str(screen_rect.width()) + 'x' + str(screen_rect.height())
    print("Screensize: " + screensize)

    w = QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(iconFile), parent=w)
    trayIcon.show()

    # Initialize information manager
    inf_man = InformationManager(screensize)
    down_man = dl.DownloadManager(inf_man)

    # inf_man.set_latest_wallpaper()

    if down_man.update():
        inf_man.set_latest_wallpaper()
    else:
        inf_man.set_fresh_random_wallpaper()

    trayIcon.initialize_window(inf_man, down_man)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()