
// Uranium is released under the terms of the LGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Controls 2.15

import UM 1.5 as UM
import Cura 1.1 as Cura

import ".."

Item
{
    id: base
    width: childrenRect.width
    height: childrenRect.height


    property var extrudersModel: CuraApplication.getExtrudersModel()
    UM.I18nCatalog { id: catalog; name: "cura"}

    Column
    {
        id: items
        anchors.top: parent.top;
        anchors.left: parent.left;
        color: "black";


        spacing: UM.Theme.getSize("default_margin").height

        Row
        {
            id: duplicationButtons
            spacing: UM.Theme.getSize("default_margin").width

            UM.ToolbarButton
            {
                id: normalButton
                text: catalog.i18nc("@label", "Dual")
                toolItem: UM.ColorImage
                {
                    source: UM.Theme.getIcon("dualicon")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable: true
                checked: Cura.PrintersManagerService.getPrintMode() == "dual"
                onClicked:{
                 Cura.PrintersManagerService.setPrintMode("dual")
                 CuraActions.setExtruderForSelection(extrudersModel.getItem(0).id)
                }
                z: 5
            }
            UM.ToolbarButton
            {
                id: singleT0Button
                text: catalog.i18nc("@label", "Single 1")
                toolItem: UM.ColorImage
                {
                    source: UM.Theme.getIcon("single1")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable: true
                checked: Cura.PrintersManagerService.getPrintMode() == "singleT0"
                onClicked: {
                 Cura.PrintersManagerService.setPrintMode("singleT0");
                 CuraActions.setExtruderForSelection(extrudersModel.getItem(0).id)
                    }
                z: 4
            }

            UM.ToolbarButton
            {
                id: singleT1Button
                text: catalog.i18nc("@label", "Single 2")
                toolItem: UM.ColorImage
                {
                    source: UM.Theme.getIcon("single2")
                    color: UM.Theme.getColor("icon")
                }                
                property bool needBorder: true
                checkable: true
                checked: Cura.PrintersManagerService.getPrintMode() == "singleT1"
                onClicked:{
                 Cura.PrintersManagerService.setPrintMode("singleT1")
                 CuraActions.setExtruderForSelection(extrudersModel.getItem(1).id)
                }
                z: 3
            }
            UM.ToolbarButton
            {
                id: duplication
                text: catalog.i18nc("@label", "Duplication")
                toolItem: UM.ColorImage
                {
                    source: UM.Theme.getIcon("duplicationicon")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable: true
                checked: Cura.PrintersManagerService.getPrintMode() == "duplication"
                onClicked:{
                 Cura.PrintersManagerService.setPrintMode("duplication")
                 CuraActions.setExtruderForSelection(extrudersModel.getItem(0).id)

                }
                z: 2
            }
            UM.ToolbarButton
            {
                id: mirrorButton
                text:  catalog.i18nc("@label", "Mirror")
                toolItem: UM.ColorImage
                {
                    source: UM.Theme.getIcon("mirroricon")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable: true
                checked: Cura.PrintersManagerService.getPrintMode() == "mirror"
                onClicked:{
                 Cura.PrintersManagerService.setPrintMode("mirror")
                 CuraActions.setExtruderForSelection(extrudersModel.getItem(0).id)

                }
                z: 1
            }
        }

        UM.Label
        {
            id: printModeLabel
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            height: UM.Theme.getSize("setting").height
            verticalAlignment: Text.AlignVCenter
        }


    }

}
