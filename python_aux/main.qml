import QtQuick 2.11
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.4
import QtQuick.Window 2.0
import QtQuick.Controls.Material 2.1
import Qt.labs.platform 1.0 as QLP

import Comparison 1.0
import PlotAxes 1.0

ApplicationWindow {
    id: window
    height: 240
    width: 320
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Blue
    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem {
                text: "Open..."
                onTriggered: openFile.visible = true
            }
            MenuItem {
                text: "Close Plots"
                onTriggered: plotAxes.close_plots()
            }
            MenuItem {
                text: "Exit"
                onTriggered: {
                    plotAxes.close_plots()
                    window.close(); 
                }
            }
        }
        Menu {
            title: "Help"
            MenuItem {
                text: "About"
                onTriggered: {
                    about.open()
                }
            }
            
        }
        
    }

    Dialog {
        id: about
        contentWidth: view.implicitWidth
        contentHeight: view.implicitHeight
        x: Math.round((window.width - width) / 2)
        y: Math.round((window.height - height) / 2)
        opacity: 0.0
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        Column {
            Text {
                text: "About CEMplot\n"
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }
            Text {
                text: "<a href='https://github.com/lsmanoel/CEM_2'>https://github.com/lsmanoel/CEM_2</a>"
                horizontalAlignment: Text.AlignHCenter
                width: parent.width
                wrapMode: Text.WordWrap
                onLinkActivated: Qt.openUrlExternally(link)
                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.NoButton
                    cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
                }
            }
            Text {
                text: "\n\
This program is distributed in the hope that it will be useful,\n\
but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n\
GNU General Public License for more details."
                horizontalAlignment: Text.AlignHCenter
                onLinkActivated: Qt.openUrlExternally(link)
                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.NoButton
                    cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
                }
            }
        }
        standardButtons: Dialog.Ok
        
        exit: Transition {
            NumberAnimation { property: "opacity"; from: 1.0; to: 0.0 }
        }
        enter: Transition {
            NumberAnimation { property: "opacity"; from: 0.0; to: 1.0 }
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
            highlightMoveDuration : 300
            highlightMoveVelocity : -1
            model: ListModel { id: experiments_listModel }
            delegate: Component {
                Item {
                    width: window.width
                    height: 80
                    Column {
                        spacing: 2
                        padding: 5
                        Text {
                            width: window.width
                            wrapMode: Text.WordWrap
                            text: (index + 1) + '. ' + info_dict.Title
                            font.bold: true
                            font.capitalization: Font.AllUppercase
                        }
                        Text {
                            width: window.width
                            wrapMode: Text.WordWrap
                            text: 'Descrição: ' + info_dict.Description
                            font.italic: true
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
                color: 'lightblue'
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
