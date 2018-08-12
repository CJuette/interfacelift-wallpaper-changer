import os

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

from interfacelift_wallpaper_changer import system
from interfacelift_wallpaper_changer.resources import *
import sys

fixedWidthTray = 200
fixedWidthDialog = 400

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
        system.openLink(self.URL_PATH + self.id + '/')

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

        self.setWindowTitle("InterfaceLift Wallpaper Changer - New Wallpaper found!")
        self.setWindowIcon(QtGui.QIcon(iconFile))


class QuestionDialog(QMessageBox):

    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)

        self.setWindowTitle("InterfaceLift Wallpaper Changer")
        self.setWindowIcon(QtGui.QIcon(iconFile))
        self.setStyleSheet("")
        self.addButton(QMessageBox.Yes)
        self.addButton(QMessageBox.No)
        self.setIcon(QMessageBox.Question)

class InfoDialog(QMessageBox):

    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)

        self.setWindowTitle("InterfaceLift Wallpaper Changer")
        self.setWindowIcon(QtGui.QIcon(iconFile))
        self.setStyleSheet("")
        self.addButton(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.setIcon(QMessageBox.Information)

class ProgressDialog(QProgressDialog):

    def __init__(self, parent=None):
        QProgressDialog.__init__(self, parent)

        self.setWindowTitle("InterfaceLift Wallpaper Changer")
        self.setWindowIcon(QtGui.QIcon(iconFile))

import interfacelift_wallpaper_changer.downloader as dl

class BlacklistItem(QWidget):
    gridLayout = None
    buttonLike = None
    labelID = None
    id = None
    blacklistDiag = None

    def like(self):
        self.blacklistDiag.like(self.id, self)

    def __init__(self, parent=None, id=None, blacklistDia=None):
        QListWidgetItem.__init__(self, None)
        self.id = id
        self.gridLayout = QGridLayout()
        self.blacklistDiag = blacklistDia

        self.buttonLike = QPushButton("\U0001F44D")
        self.buttonLike.setObjectName("buttonLike")
        self.labelID = QLabel(str(id))
        self.labelID.setObjectName("labelTitle")

        self.buttonLike.clicked.connect(self.like)

        self.gridLayout.addWidget(self.labelID, 0, 0)
        self.gridLayout.addWidget(self.buttonLike, 0, 1)

        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setFixedHeight(50)
        self.setFixedWidth(400)

        #self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.setLayout(self.gridLayout)


class BlacklistDialog(QDialog):
    from interfacelift_wallpaper_changer.infomanager import InformationManager

    im: InformationManager = None
    dm: dl.DownloadManager = None
    gridLayout = None
    closeButton = None
    scrollArea = None
    scrollAreaWidget = None

    def like(self, id, widget: QWidget):
        self.im.delete_from_blacklist(id)
        widget.hide()

    def beforeClose(self):
        self.im.write_wallpaper_info()
        self.close()
        self.dm.update()

    def __init__(self, parent=None, inf_man=None, down_man=None):
        QDialog.__init__(self, parent)
        self.im = inf_man
        self.dm = down_man

        self.gridLayout = QGridLayout()
        self.setWindowTitle("InterfaceLift Wallpaper Changer - Blacklist")
        self.setWindowIcon(QtGui.QIcon(iconFile))

        self.scrollArea = QScrollArea()
        self.scrollAreaWidget = QWidget()

        self.scrollArea.setFixedWidth(500)
        self.scrollArea.setFixedHeight(500)

        sAgrid = QGridLayout()

        for i, id in enumerate(self.im.blacklist):
            sAgrid.addWidget(BlacklistItem(parent=self.scrollAreaWidget, id=id, blacklistDia=self))

        self.scrollAreaWidget.setLayout(sAgrid)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollArea.show()
        self.scrollAreaWidget.show()

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.beforeClose)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.closeButton, 1, 0, 1, 1)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)

        #self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.setLayout(self.gridLayout)


class SystemTrayWindow(QWidget):
    from interfacelift_wallpaper_changer.infomanager import InformationManager

    gridLayout = None
    buttonExit = None
    buttonUpdate = None
    buttonNext = None
    buttonDislike = None
    buttonBlacklist = None
    imageLabel = None
    image = None
    labelTitle = None
    labelArtist = None

    im: InformationManager = None
    dm: dl.DownloadManager = None

    URL_PATH = "http://interfacelift.com/wallpaper/details/"
    id = ""

    pixelRatio = 0

    def openLink(self, event):
        print("Call to SystemTrayWindow.openLink")
        system.openLink(self.URL_PATH + self.id + '/')

    def set_wallpaper_info(self, wallpaper):
        """
        wallpaper: Tuple from wallpaper-info in InformationManager
        """
        self.id = wallpaper[0]
        self.labelTitle.setText(wallpaper[1])
        self.labelArtist.setText(wallpaper[2])

        self.image = QtGui.QPixmap(os.path.join(self.im.thumbnailFolder, wallpaper[5]))
        self.image.setDevicePixelRatio(self.pixelRatio)
        self.imageLabel.setPixmap(self.image.scaledToWidth(fixedWidthTray*self.pixelRatio, QtCore.Qt.SmoothTransformation))

    def update(self):
        print("Update called")
        if self.dm.update(silent=False):
            self.im.set_latest_wallpaper()
            self.set_wallpaper_info(self.im.get_current_wallpaper())

    def dislike(self):
        print("Dislike called")
        dialog = QuestionDialog()
        dialog.setText("Do you really want to dislike this image?")
        dialog.setInformativeText("The image will be removed from your computer, and added to a blacklist, so that it will not be downloaded again.")

        result = dialog.exec_()

        if result == QMessageBox.Yes:
            print("Deleting the image...")
            self.im.dislike_current()
            self.set_wallpaper_info(self.im.get_current_wallpaper())
        else:
            print("Dislike rejected.")

    def show_blacklist(self):
        blacklistDiag = BlacklistDialog(parent=self, inf_man=self.im, down_man=self.dm)
        blacklistDiag.show()

    def next(self):
        print("Next called")
        self.im.set_random_wallpaper()
        self.set_wallpaper_info(self.im.get_current_wallpaper())

    def __init__(self, parent=None, inf_man=None, downloader=None):
        QWidget.__init__(self, parent)

        self.pixelRatio = self.devicePixelRatioF()

        self.im = inf_man
        self.dm = downloader

        self.gridLayout = QGridLayout()
        self.buttonBlacklist = QPushButton("Blacklist")
        self.buttonExit = QPushButton("Exit")
        self.buttonUpdate = QPushButton("Check for new wallpapers")
        self.buttonNext = QPushButton("Next random wallpaper")
        self.buttonDislike = QPushButton("\U0001F44E")
        self.buttonDislike.setObjectName("buttonDislike")

        self.imageLabel = QLabel()
        self.labelTitle = QLabel("Title")
        self.labelArtist = QLabel("Mensch")
        self.labelTitle.setFixedWidth(fixedWidthTray * 2 / 3)
        self.labelArtist.setFixedWidth(fixedWidthTray * 2 / 3)
        self.labelTitle.setObjectName("labelTitle")
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
        self.gridLayout.addWidget(self.buttonBlacklist, 5, 0, 1, 3)
        self.gridLayout.addWidget(self.buttonExit, 6, 0, 1, 3)

        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setLayout(self.gridLayout)

        self.buttonExit.clicked.connect(sys.exit)
        self.buttonDislike.clicked.connect(self.dislike)
        self.buttonNext.clicked.connect(self.next)
        self.buttonUpdate.clicked.connect(self.update)
        self.buttonBlacklist.clicked.connect(self.show_blacklist)

        self.labelTitle.mousePressEvent = self.openLink
        self.labelArtist.mousePressEvent = self.openLink
        self.imageLabel.mousePressEvent = self.openLink

        self.set_wallpaper_info(self.im.get_current_wallpaper())
