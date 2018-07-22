from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

import ifl_system

fixedWidthTray = 200
fixedWidthDialog = 400

class ProgressDialog(QProgressDialog):

    def __init__(self, parent=None):
        QProgressDialog.__init__(self, parent)

        self.setWindowTitle("Downloading new wallpapers...")
        self.setWindowIcon(QtGui.QIcon("1.ico"))

class LikeDislikeDialog(QDialog):
    gridLayout = None
    buttonLike = None
    buttonDislike = None
    labelTitle = None
    labelArtist = None
    imageLabel = None
    image = None

    id = None
    URL_PATH = "http://interfacelift.com/wallpaper/details/"

    def openLink(self, event):
        print("Call to LikeDislikeDialog.openLink")
        ifl_system.openLink(self.URL_PATH+self.id+'/')

    def __init__(self, photographer, title, previewImage, id, parent=None):
        QDialog.__init__(self, parent)

        self.id = id

        pixelRatio = self.devicePixelRatioF()

        self.gridLayout = QGridLayout()
        self.buttonDislike = QPushButton("\U0001F44E")
        self.buttonDislike.setObjectName("buttonDislike")

        self.buttonLike = QPushButton("\U0001F44D")
        self.buttonLike.setObjectName("buttonLike")
        self.buttonLike.setDefault(True)

        self.imageLabel = QLabel()
        self.labelTitle = QLabel(title)
        self.labelTitle.setObjectName("labelTitle")
        self.labelArtist = QLabel(photographer)
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

        self.image = QtGui.QPixmap(previewImage)
        self.image.setDevicePixelRatio(pixelRatio)
        self.imageLabel.setPixmap(self.image.scaledToWidth(fixedWidthDialog * pixelRatio, QtCore.Qt.SmoothTransformation))

        self.labelTitle.mousePressEvent = self.openLink
        self.labelArtist.mousePressEvent = self.openLink
        self.imageLabel.mousePressEvent = self.openLink

        self.buttonLike.clicked.connect(self.accept)
        self.buttonDislike.clicked.connect(self.reject)

        self.setWindowTitle("New Wallpaper found!")
        self.setWindowIcon(QtGui.QIcon("1.ico"))