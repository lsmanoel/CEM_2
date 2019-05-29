import QtQuick 2.11
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.1
import Qt.labs.platform 1.0 as QLP

import Comparison 1.0
import PlotAxes 1.0

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

    PlotAxes {
        id: plotAxes
    }

    Rectangle {
        width: parent.width; height: parent.height

        ListView {
            id: experiments_list
            property var selected: null
            anchors.fill: parent
            model: ListModel { id: experiments_listModel }
            delegate: Component {
                Item {
                    width: parent.width
                    height: 80
                    ColumnLayout {
                        Text {
                            text: 'Title:' + info_dict.Title
                        }
                        Text { 
                            text: 'Observation:' + info_dict.Observation
                        }
                        Text { 
                            wrapMode: Text.WordWrap
                            text: 'Description:' + info_dict.Description
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            experiments_list.currentIndex = index
                        }
                        onDoubleClicked: {
                            console.log("Opening selected experiment...")
                            var files = experiments_list.selected.file_list
                            plotAxes.plot_file(files)
                        }
                    }

                }
            }
            highlight: Rectangle {
                color: 'grey'
            }
            focus: true
            onCurrentItemChanged: {
                console.log(model.get(experiments_list.currentIndex).info_dict.Title + ' selected')
                experiments_list.selected = experiments_listModel.get(experiments_list.currentIndex)
            }
        }
    }

    NewFileDialog {
        id: openFile
        title: "Please select a file"
        nameFilters: ["CSV Files (*.csv *.CSV)"]
        fileMode: QLP.FileDialog.OpenFile
        onOutputChanged: {
            if(!output) {
                return
            }
            console.log('Opening file', output)
            comparison.load(output)
            experiments_listModel.append(JSON.parse(comparison.experiments_title))
            console.log(JSON.parse(comparison.experiments_title)[0].file_list)
        }
    }
}
