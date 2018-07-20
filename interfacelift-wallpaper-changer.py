import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

fixedWidth = 200

def openLink(event):
    print("openLink called")

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
        self.labelTitle.setOpenExternalLinks(True)
        self.labelArtist.setOpenExternalLinks(True)

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
        self.imageLabel.setPixmap(self.image.scaledToWidth(fixedWidth, QtCore.Qt.SmoothTransformation))

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
        menu.setFixedWidth(fixedWidth)
        menu.addAction(self.wa)
#        exitAction = menu.addAction("Exit")
#        exitAction.triggered.connect(qApp.quit)
        self.setContextMenu(menu)

def main():
    app = QApplication(sys.argv)

    with open("stylesheet.qss", 'r') as f:
        stylesheet = f.read()

    app.setStyleSheet(stylesheet)

    w = QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("1.ico"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()