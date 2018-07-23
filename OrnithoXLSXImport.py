# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OrnithoXLSXImport
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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction, QWizard, QWizardPage, QLineEdit

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the Wizard
from .OrnithoXLSXImport_wizard import OrnithoXLSXImportWizard
import os.path

__version__ = "0.1.0alpha004"


class OrnithoXLSXImport:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'OrnithoXLSXImport_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Read the settings
        self.readSettings()

        # Create the Wizard (after translation) and keep reference
        self.wiz = OrnithoXLSXImportWizard()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&OrnithoXLSXImport')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'OrnithoXLSXImport')
        self.toolbar.setObjectName(u'OrnithoXLSXImport')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('OrnithoXLSXImport', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Ornitho_XLSX_Importer/res/goose.svg'
        self.add_action(
            icon_path,
            text=self.tr(u'OrnithoXLSXImport'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&OrnithoXLSXImport'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""

        # Fill in the predefine values
        self.wiz.wizardPageXSLX.findChild(
            QLineEdit, "lineEditXLSXFile").setText(self.fileXLSX)

        # show the Wizard
        self.wiz.show()
        # Run the Wizard event loop
        result = self.wiz.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def storeSettings(self):
        """Store the settings into global QGIS-Settings"""
        s = QSettings()
        s.setValue("OrnithoXLSXImport/fileXLSX", self.fileXLSX)
    #    s.setValue("OrnithoXLSXImport/fileGPKG", self.fileGPKG)
    #    s.setValue("OrnithoXLSXImport/layerGPKG", self.layerGPKG)

    def readSettings(self):
        """Restore the settings from global QGIS-Settings"""
        defaultPath = os.path.join(os.path.join(os.path.expanduser('~')))
        defaultXLSX = os.path.join(defaultPath, "export.xlsx")
    #    defaultGPKG = os.path.join(defaultPath, "ornitho.gpkg")
    #    defaultLayerGPKG = os.path.splitext(os.path.basename(defaultXLSX))[0]

        s = QSettings()
        self.fileXLSX = s.value("OrnithoXLSXImport/fileXLSX", defaultXLSX)
    #    self.fileGPKG = s.value("OrnithoXLSXImport/fileGPKG", defaultGPKG)
    #    self.layerGPKG = s.value("OrnithoXLSXImport/layerGPKG", defaultLayerGPKG)

    def clearSettings(self):
        """Delete the settings from global QGIS-Settings"""
        s = QSettings()
        s.remove("OrnithoXLSXImport/fileXLSX")
        # s.remove("OrnithoXLSXImport/fileGPKG")
        # s.remove("OrnithoXLSXImport/layerGPKG")
