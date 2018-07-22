import sys
from screeninfo import get_monitors
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

import ifl_downloader as dl
from ifl_infomanager import InformationManager
from ifl_guimodules import *
import ifl_system

def nextWallpaper():
    print("nextWallpaper called")

def update():
    print("update called")

def dislike():
    print("dislike called")

class SystemTrayWindow(QWidget):
    gridLayout = None
    buttonExit = None
    buttonUpdate = None
    buttonNext = None
    buttonDislike = None
    imageLabel = None
    image = None
    labelTitle = None
    labelArtist = None

    im: InformationManager = None

    def __init__(self, parent=None, inf_man=None):
        QWidget.__init__(self, parent)

        self.gridLayout = QGridLayout()
        self.buttonExit = QPushButton("Exit")
        self.buttonUpdate = QPushButton("Check for new wallpapers")
        self.buttonNext = QPushButton("Next random wallpaper")
        self.buttonDislike = QPushButton("\U0001F44E")
        self.buttonDislike.setObjectName("buttonDislike")
        self.imageLabel = QLabel()
        self.labelTitle = QLabel("Foto")
        self.labelTitle.setObjectName("labelTitle")
        self.labelArtist = QLabel("Mensch")
        self.labelArtist.setObjectName("labelArtist")

        self.labelTitle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.labelArtist.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.imageLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.imageLabel, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.labelTitle, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.labelArtist, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.buttonDislike, 1, 2, 2, 1)
        self.gridLayout.addWidget(self.buttonNext, 3, 0, 1, 3)
        self.gridLayout.addWidget(self.buttonUpdate, 4, 0, 1, 3)
        self.gridLayout.addWidget(self.buttonExit, 5, 0, 1, 3)

        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setLayout(self.gridLayout)

        self.image = QtGui.QPixmap("preview_test.jpg")
        #self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        pixelRatio = self.devicePixelRatioF()
        self.image.setDevicePixelRatio(pixelRatio)
        self.imageLabel.setPixmap(self.image.scaledToWidth(fixedWidthTray*pixelRatio, QtCore.Qt.SmoothTransformation))

        self.buttonExit.clicked.connect(qApp.quit)
        self.buttonDislike.clicked.connect(dislike)
        self.buttonNext.clicked.connect(nextWallpaper)
        self.buttonUpdate.clicked.connect(update)

        self.labelTitle.mousePressEvent = ifl_system.openLink
        self.labelArtist.mousePressEvent = ifl_system.openLink
        self.imageLabel.mousePressEvent = ifl_system.openLink

        self.im = inf_man


class SystemTrayIcon(QSystemTrayIcon):

    window = None
    wa = None

    def __init__(self, icon, parent=None, inf_man=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.window = SystemTrayWindow(parent=parent, inf_man=inf_man)
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
    down_man = dl.IFLDownloader(inf_man)

    w = QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("1.ico"), parent=w, inf_man=inf_man)

    trayIcon.show()

    down_man.update()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()