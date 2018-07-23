import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

import ifl_downloader as dl
from ifl_infomanager import InformationManager
from ifl_guimodules import *
import ifl_system


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
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    with open("stylesheet.qss", 'r') as f:
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

    w = QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("1.ico"), parent=w, inf_man=inf_man, downloader=down_man)

    trayIcon.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()