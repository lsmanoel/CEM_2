import QtQuick 2.11
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.1
import Qt.labs.platform 1.0 as QLP

import Comparison 1.0

ApplicationWindow {
    id: window
    height: 480
    width: 480
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Blue

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem {
                text: "Open..."
                onTriggered: openFile.visible = true
            }
        }
    }

    Comparison{
        id: comparison
    }

    NewFileDialog {
        id: openFile
        title: "Please select a file"
        nameFilters: ["CSV Files (*.csv *.CSV)"]
        fileMode: QLP.FileDialog.OpenFile
        onOutputChanged: {
            if(!output) {
                return;
            }
            print('Opening file', output)
            comparison.load(output)
        }
    }
}
