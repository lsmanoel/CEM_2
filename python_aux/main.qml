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
                            console.log("Click in Experiments List")
                            experiments_list.currentIndex = index
                        }
                        onDoubleClicked: {
                            console.log("Double Click in Experiments List")
                            // PlotAxesList(experiments_list.selected.file_list).plot_axes_list() // nao funciona
                            // plotAxesList.plot_axes_list() // tenta plotar None
                            // plotAxesList.testbench() // o exemplo funciona

                            // plotAxes.plot_axes(
                            //     plotAxes.files2axes(
                            //         // experiments_list.selected.file_list,
                            //         plotAxes.files_example(), 
                            //         1), 
                            //     'freq_dB'
                            // )
                            // plotAxes.plot_file(experiments_list.selected.file_list)
                            // plotAxes.plot_file(plotAxes.files_example())
                            // plotAxes.plot_file(PlotAxes.files_example)
                            // var files = plotAxes.files_example()
                            // var files = 
                            
                            print(JSON.stringify(experiments_list.selected.file_list))


                            // var axes = plotAxes.files2axes()
                            // plotAxes.plot_axes(axes)
                            // plotAxes.show()



                            // PlotAxes.plot_file()
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
                console.log(experiments_list.selected)
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
            print('Opening file', output)
            comparison.load(output)
            experiments_listModel.append(JSON.parse(comparison.experiments_title))
        }
    }
}
