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
            MenuItem {
                text: "Exit"
            }
        }
    }

    Comparison {
        id: comparison
    }

    Rectangle {
        width: parent.width; height: parent.height

        ListView {
            id: experiments_list
            anchors.fill: parent
            model: ListModel { id: experiments_listModel }
            delegate: Component {
                Item {
                    width: parent.width
                    height: 40
                    Column {
                        Text { text: 'Name:' + name }
                        Text { text: 'Number:' + number }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: experiments_list.currentIndex = index
                    }
                }
            }
            highlight: Rectangle {
                color: 'grey'
            }
            focus: true
            onCurrentItemChanged: console.log(model.get(experiments_list.currentIndex).name + ' selected')
        }
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
            experiments_listModel.append({name: "pera", number: 822})
            experiments_listModel.append(comparison.experiments_title)
        }
    }
}
