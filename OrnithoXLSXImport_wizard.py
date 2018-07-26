# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OrnithoXLSXImportDialog
                                 A QGIS plugin
 Importiert XLXS aus Ornitho.de in ein GeoPackage
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-07-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Johannes Kilian
        email                : hoppfrosch@gmx.de
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

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWizard, QLineEdit, QToolButton, \
    QFileDialog, QComboBox, QLabel  # , QWizardPage
# from PyQt5 import QtGui
# from PyQt5.QtGui import QPaintEvent, QIcon, QPixmap,

from PyQt5.QtCore import QSettings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'OrnithoXLSXImport_wizard_base.ui'))


def dump(obj):
    """Dump object"""

    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


class OrnithoXLSXImportWizard(QtWidgets.QWizard, FORM_CLASS):
    """Import Wizard"""

    def __init__(self, parent=None):
        """Constructor."""

        # Read the settings
        self.fileXLSX = None
        self.fileGPKG = None
        self.readSettings()
        self.NextButtonEnabled = False

        super(OrnithoXLSXImportWizard, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # dump(self)

        # Set initial values
        # Fill in the predefine values
        self.wizardPageXSLX.findChild(
            QLineEdit, "lineEditXLSXFile").setText(self.fileXLSX)
        self.wizardPageGeopackage.findChild(
            QLineEdit, "lineEditGeopackageFile").setText(self.fileGPKG)

        self.wizardPageGeopackage.findChild(
            QLineEdit, "lineEditGeopackageFile").setText(self.fileGPKG)

        # Set up the signals
        tb = self.wizardPageXSLX.findChild(QToolButton, "toolButtonXSLXFile")
        tb.clicked.connect(self.clickedToolButtonXSLXFile)
        tb = self.wizardPageGeopackage.findChild(
            QToolButton, "toolButtonGeopackageFile")
        tb.clicked.connect(self.clickedToolButtonGeopackageFile)

    def paintEvent(self, event):
        """Event fuer Neuzeichnen des Wizards"""
        pageId = self.currentId()
        # https://python-forum.io/Thread-Disable-Enter-Key-PyQt5-Wizard?pid=51388
        if pageId == 0:
            self.validateXLSXFile()
        elif pageId == 1:
            self.validateGPKGFile()
        elif pageId == 3:
            self.validateLayername()

        self.button(QWizard.NextButton).setEnabled(self.NextButtonEnabled)
        super(OrnithoXLSXImportWizard, self).paintEvent(event)

    def populateLayerDropdown(self):
        """Populate the Layer Dropdown with layers from current geopackage"""

        cb = self.wizardPageLayername.findChild(
            QComboBox, "comboBoxGeopackageLayer")
        cb.clear()
        layerList = []
        layerList.append(os.path.splitext(os.path.basename(self.fileGPKG))[0])

        layerList.sort()
        cb.addItems(layerList)

    def showEvent(self, event):
        """Show-Event"""
        self.button(QWizard.NextButton).setDefault(False)
        super(OrnithoXLSXImportWizard, self).showEvent(event)

    def clickedToolButtonXSLXFile(self):
        """Select the XLSX-File to be imported"""

        filename = QFileDialog.getOpenFileName(
            None, 'Waehle XLXS-Export Datei aus Ornitho:', self.fileXLSX,
            "Excel-File (*.xlsx)")
        self.fileXLSX = filename[0]
        if self.fileXLSX == "":
            return
        # Fill in the lineEdit containing filename
        self.wizardPageXSLX.findChild(
            QLineEdit, "lineEditXLSXFile").setText(self.fileXLSX)

    def clickedToolButtonGeopackageFile(self):
        """Select the Geopackage-File to be exported"""

        filename = QFileDialog.getSaveFileName(
            None, 'Waehle zu exportierende Geopackage-Datei:', self.fileGPKG,
            "Geopackage-File (*.gpkg)")
        self.fileGPKG = filename[0]
        if self.fileGPKG == "":
            return
        # Fill in the lineEdit containing filename
        self.wizardPageGeopackage.findChild(
            QLineEdit, "lineEditGeopackageFile").setText(self.fileGPKG)

    def validateXLSXFile(self):
        """Validierung des ausgewaehlten XLSX-Files"""
        self.NextButtonEnabled = False

        if os.path.exists(self.fileXLSX):
            if os.path.isfile(self.fileXLSX):
                self.NextButtonEnabled = True

    # TODO: Ueberpruefen ob XLSX-Inhalt auch tatsaechlich ein Ornitho-Export ist

        return False

    def validateGPKGFile(self):
        """Validierung des ausgewaehlten XLSX-Files"""
        self.NextButtonEnabled = False

        if not os.path.exists(self.fileGPKG):
            self.NextButtonEnabled = True
            self.populateLayerDropdown()
            self.wizardPageLayername.findChild(
                QLabel, "labelGeopackageFileName").setText(self.fileGPKG)

        return self.NextButtonEnabled

    def validateLayername(self):
        """Validierung des ausgewaehlten Layernamens"""
        self.NextButtonEnabled = False

        # Wenn die GPKG-Datei noch nicht existiert, kann der Layername frei
        # gewaehlt werden
        if not os.path.exists(self.fileGPKG):
            self.NextButtonEnabled = True

        return self.NextButtonEnabled

    def storeSettings(self):
        """Store the settings into global QGIS-Settings"""
        s = QSettings()
        s.setValue("OrnithoXLSXImport/fileXLSX", self.fileXLSX)
        s.setValue("OrnithoXLSXImport/fileGPKG", self.fileGPKG)
        s.setValue("OrnithoXLSXImport/layerGPKG", self.layerGPKG)

    def readSettings(self):
        """Restore the settings from global QGIS-Settings"""
        defaultPath = os.path.join(os.path.join(os.path.expanduser('~')))
        defaultXLSX = os.path.join(defaultPath, "export.xlsx")
        defaultGPKG = os.path.join(defaultPath, "ornitho.gpkg")
        defaultLayerGPKG = os.path.splitext(os.path.basename(defaultXLSX))[0]

        s = QSettings()
        self.fileXLSX = s.value("OrnithoXLSXImport/fileXLSX", defaultXLSX)
        self.fileGPKG = s.value("OrnithoXLSXImport/fileGPKG", defaultGPKG)
        self.layerGPKG = s.value(
            "OrnithoXLSXImport/layerGPKG", defaultLayerGPKG)

    def clearSettings(self):
        """Delete the settings from global QGIS-Settings"""
        s = QSettings()
        s.remove("OrnithoXLSXImport/fileXLSX")
        s.remove("OrnithoXLSXImport/fileGPKG")
        s.remove("OrnithoXLSXImport/layerGPKG")

    def nextId(self):
        """Skip wizardpages if everything is OK"""
        currId = self.currentId()
        if currId == 1:
            if self.validateGPKGFile():
                return 3
            else:
                return 2
        elif currId == 3:
            if self.validateLayername():
                return 5
            else:
                return 4
        return currId+1
