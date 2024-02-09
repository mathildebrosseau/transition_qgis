# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TransitionDockWidget
                                 A QGIS plugin
 truc
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-02-03
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Transition
        email                : Transition
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import sys

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from .import_path import return_lib_path
sys.path.append(return_lib_path())
from test_api import call_api

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'transition_qgis_dockwidget_base.ui'))


class TransitionDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(TransitionDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Connect the buttons
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.resetButton.clicked.connect(self.on_resetButton_clicked)

    def on_pushButton_clicked(self):
        # Call the API
        result = call_api()
        self.plainTextEdit.setPlainText(result)
        print("API called")

    def on_resetButton_clicked(self):
        self.plainTextEdit.clear()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

