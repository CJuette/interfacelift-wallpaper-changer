import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

import ifl_downloader as dl
from ifl_infomanager import InformationManager

fixedWidthTray = 200
fixedWidthDialog = 400

def openLink(event):
    print("openLink called")

def nextWallpaper():
    print("nextWallpaper called")

def update():
    print("update called")
    dialog = LikeDislikeDialog()
    result = dialog.exec_()
    if result == QDialog.Accepted:
        liked = True
    else:
        liked = False

    print(liked)

def dislike():
    print("dislike called")

class LikeDislikeDialog(QDialog):
    gridLayout = None
    buttonLike = None
    buttonDislike = None
    labelTitle = None
    labelArtist = None
    imageLabel = None
    image = None

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.gridLayout = QGridLayout()
        self.buttonDislike = QPushButton(QtGui.QIcon("thumbs_down.png"), "")
        self.buttonDislike.setObjectName("buttonDislike")

        self.buttonLike = QPushButton(QtGui.QIcon("thumbs_up.png"), "")
        self.buttonLike.setObjectName("buttonLike")
        self.buttonLike.setDefault(True)

        self.imageLabel = QLabel()
        self.labelTitle = QLabel("Foto")
        self.labelTitle.setObjectName("labelTitle")
        self.labelArtist = QLabel("Mensch")
        self.labelArtist.setObjectName("labelArtist")

        self.labelTitle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.labelArtist.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.imageLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.imageLabel, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.labelTitle, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.labelArtist, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.buttonDislike, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.buttonLike, 3, 1, 1, 1)

        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.setLayout(self.gridLayout)

        self.image = QtGui.QPixmap("preview_test.jpg")
        #self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setPixmap(self.image.scaledToWidth(fixedWidthDialog, QtCore.Qt.SmoothTransformation))

        self.labelTitle.mousePressEvent = openLink
        self.labelArtist.mousePressEvent = openLink
        self.imageLabel.mousePressEvent = openLink

        self.buttonLike.clicked.connect(self.accept)
        self.buttonDislike.clicked.connect(self.reject)



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

    def __init__(self, icon, parent=None):
        QWidget.__init__(self, parent)

        self.gridLayout = QGridLayout()
        self.buttonExit = QPushButton("Exit")
        self.buttonUpdate = QPushButton("Check for new wallpapers")
        self.buttonNext = QPushButton("Next random wallpaper")
        self.buttonDislike = QPushButton(QtGui.QIcon("thumbs_down.png"), "")
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
        self.imageLabel.setPixmap(self.image.scaledToWidth(fixedWidthTray, QtCore.Qt.SmoothTransformation))

        self.buttonExit.clicked.connect(qApp.quit)
        self.buttonDislike.clicked.connect(dislike)
        self.buttonNext.clicked.connect(nextWallpaper)
        self.buttonUpdate.clicked.connect(update)

        self.labelTitle.mousePressEvent = openLink
        self.labelArtist.mousePressEvent = openLink
        self.imageLabel.mousePressEvent = openLink


class SystemTrayIcon(QSystemTrayIcon):

    window = None
    wa = None

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.window = SystemTrayWindow(parent)
        self.wa = QWidgetAction(parent)
        self.wa.setDefaultWidget(self.window)
        menu.setFixedWidth(fixedWidthTray)
        menu.addAction(self.wa)
#        exitAction = menu.addAction("Exit")
#        exitAction.triggered.connect(qApp.quit)
        self.setContextMenu(menu)

def main():
    app = QApplication(sys.argv)

    with open("stylesheet.qss", 'r') as f:
        stylesheet = f.read()

    app.setStyleSheet(stylesheet)
    app.setQuitOnLastWindowClosed(False)

    # Initialize information manager
    inf_man = InformationManager()
    down_man = dl.IFLDownloader(inf_man)

    w = QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("1.ico"), w)

    trayIcon.show()



    sys.exit(app.exec_())

if __name__ == '__main__':
    main()