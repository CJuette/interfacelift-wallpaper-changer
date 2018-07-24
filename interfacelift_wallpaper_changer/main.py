import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

from interfacelift_wallpaper_changer.infomanager import InformationManager
from interfacelift_wallpaper_changer.guimodules import *
from interfacelift_wallpaper_changer import system, downloader as dl


class SystemTrayIcon(QSystemTrayIcon):

    window = None
    wa = None

    def __init__(self, icon, parent=None, inf_man=None, downloader=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.window = SystemTrayWindow(parent=parent, inf_man=inf_man, downloader=downloader)
        self.wa = QWidgetAction(parent)
        self.wa.setDefaultWidget(self.window)
        menu.setFixedWidth(fixedWidthTray)
        menu.addAction(self.wa)
#        exitAction = menu.addAction("Exit")
#        exitAction.triggered.connect(qApp.quit)
        self.setContextMenu(menu)

def main():
    print("Welcome to Interfacelift-wallpaper-changer! Starting update.")

    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Interfacelift-Wallpaper-Changer")
    app.setApplicationName("Interfacelift-Wallpaper-Changer")

    with open("res/stylesheet.qss", 'r') as f:
        stylesheet = f.read()

    app.setStyleSheet(stylesheet)
    app.setQuitOnLastWindowClosed(False)

    # Initialize information manager
    inf_man = InformationManager()
    down_man = dl.DownloadManager(inf_man)

    if down_man.update():
        inf_man.set_latest_wallpaper()
    else:
        inf_man.set_fresh_random_wallpaper()

    print("Updating finished.")

    w = QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("res/1.ico"), parent=w, inf_man=inf_man, downloader=down_man)

    trayIcon.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()