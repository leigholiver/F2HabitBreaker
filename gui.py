# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_guiDialog(object):
    def setupUi(self, guiDialog):
        guiDialog.setObjectName("guiDialog")
        guiDialog.resize(241, 202)
        guiDialog.setAutoFillBackground(False)
        self.overlayGroupBox = QtWidgets.QGroupBox(guiDialog)
        self.overlayGroupBox.setGeometry(QtCore.QRect(10, 40, 221, 111))
        self.overlayGroupBox.setObjectName("overlayGroupBox")
        self.overlayWidthLabel = QtWidgets.QLabel(self.overlayGroupBox)
        self.overlayWidthLabel.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.overlayWidthLabel.setObjectName("overlayWidthLabel")
        self.overlayYLabel = QtWidgets.QLabel(self.overlayGroupBox)
        self.overlayYLabel.setGeometry(QtCore.QRect(120, 50, 31, 21))
        self.overlayYLabel.setObjectName("overlayYLabel")
        self.overlayHeightLabel = QtWidgets.QLabel(self.overlayGroupBox)
        self.overlayHeightLabel.setGeometry(QtCore.QRect(120, 20, 31, 21))
        self.overlayHeightLabel.setObjectName("overlayHeightLabel")
        self.overlayXLabel = QtWidgets.QLabel(self.overlayGroupBox)
        self.overlayXLabel.setGeometry(QtCore.QRect(10, 50, 31, 21))
        self.overlayXLabel.setObjectName("overlayXLabel")
        self.overlayColorLabel = QtWidgets.QLabel(self.overlayGroupBox)
        self.overlayColorLabel.setGeometry(QtCore.QRect(10, 80, 31, 21))
        self.overlayColorLabel.setObjectName("overlayColorLabel")
        self.overlayColorButton = QtWidgets.QPushButton(self.overlayGroupBox)
        self.overlayColorButton.setGeometry(QtCore.QRect(160, 80, 51, 23))
        self.overlayColorButton.setObjectName("overlayColorButton")
        self.overlayColorWidget = QtWidgets.QWidget(self.overlayGroupBox)
        self.overlayColorWidget.setGeometry(QtCore.QRect(50, 80, 51, 22))
        self.overlayColorWidget.setAutoFillBackground(True)
        self.overlayColorWidget.setStyleSheet("")
        self.overlayColorWidget.setObjectName("overlayColorWidget")
        self.overlayWidthSpinBox = QtWidgets.QSpinBox(self.overlayGroupBox)
        self.overlayWidthSpinBox.setGeometry(QtCore.QRect(50, 20, 51, 22))
        self.overlayWidthSpinBox.setMinimum(1)
        self.overlayWidthSpinBox.setMaximum(2147483647)
        self.overlayWidthSpinBox.setProperty("value", 80)
        self.overlayWidthSpinBox.setObjectName("overlayWidthSpinBox")
        self.overlayXSpinBox = QtWidgets.QSpinBox(self.overlayGroupBox)
        self.overlayXSpinBox.setGeometry(QtCore.QRect(50, 50, 51, 22))
        self.overlayXSpinBox.setMinimum(-2147483647)
        self.overlayXSpinBox.setMaximum(2147483647)
        self.overlayXSpinBox.setProperty("value", 20)
        self.overlayXSpinBox.setObjectName("overlayXSpinBox")
        self.overlayHeightSpinBox = QtWidgets.QSpinBox(self.overlayGroupBox)
        self.overlayHeightSpinBox.setGeometry(QtCore.QRect(160, 20, 51, 22))
        self.overlayHeightSpinBox.setMinimum(1)
        self.overlayHeightSpinBox.setMaximum(2147483647)
        self.overlayHeightSpinBox.setProperty("value", 50)
        self.overlayHeightSpinBox.setObjectName("overlayHeightSpinBox")
        self.overlayYSpinBox = QtWidgets.QSpinBox(self.overlayGroupBox)
        self.overlayYSpinBox.setGeometry(QtCore.QRect(160, 50, 51, 22))
        self.overlayYSpinBox.setPrefix("")
        self.overlayYSpinBox.setMinimum(-2147483647)
        self.overlayYSpinBox.setMaximum(2147483647)
        self.overlayYSpinBox.setProperty("value", 500)
        self.overlayYSpinBox.setObjectName("overlayYSpinBox")
        self.bottomButtonBox = QtWidgets.QDialogButtonBox(guiDialog)
        self.bottomButtonBox.setGeometry(QtCore.QRect(10, 160, 221, 32))
        self.bottomButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.bottomButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Reset)
        self.bottomButtonBox.setCenterButtons(False)
        self.bottomButtonBox.setObjectName("bottomButtonBox")
        self.monitorLabel = QtWidgets.QLabel(guiDialog)
        self.monitorLabel.setGeometry(QtCore.QRect(10, 10, 47, 21))
        self.monitorLabel.setObjectName("monitorLabel")
        self.monitorComboBox = QtWidgets.QComboBox(guiDialog)
        self.monitorComboBox.setGeometry(QtCore.QRect(60, 10, 171, 22))
        self.monitorComboBox.setObjectName("monitorComboBox")

        self.retranslateUi(guiDialog)
        QtCore.QMetaObject.connectSlotsByName(guiDialog)
        guiDialog.setTabOrder(self.monitorComboBox, self.overlayWidthSpinBox)
        guiDialog.setTabOrder(self.overlayWidthSpinBox, self.overlayHeightSpinBox)
        guiDialog.setTabOrder(self.overlayHeightSpinBox, self.overlayXSpinBox)
        guiDialog.setTabOrder(self.overlayXSpinBox, self.overlayYSpinBox)
        guiDialog.setTabOrder(self.overlayYSpinBox, self.overlayColorButton)

    def retranslateUi(self, guiDialog):
        _translate = QtCore.QCoreApplication.translate
        guiDialog.setWindowTitle(_translate("guiDialog", "F2 Habit Breaker"))
        self.overlayGroupBox.setTitle(_translate("guiDialog", "Overlay"))
        self.overlayWidthLabel.setText(_translate("guiDialog", "Width"))
        self.overlayYLabel.setText(_translate("guiDialog", "Y Pos"))
        self.overlayHeightLabel.setText(_translate("guiDialog", "Height"))
        self.overlayXLabel.setText(_translate("guiDialog", "X Pos"))
        self.overlayColorLabel.setText(_translate("guiDialog", "Color"))
        self.overlayColorButton.setText(_translate("guiDialog", "Set"))
        self.monitorLabel.setText(_translate("guiDialog", "Monitor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    guiDialog = QtWidgets.QDialog()
    ui = Ui_guiDialog()
    ui.setupUi(guiDialog)
    guiDialog.show()
    sys.exit(app.exec_())

