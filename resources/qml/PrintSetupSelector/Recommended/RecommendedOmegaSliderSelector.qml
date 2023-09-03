// Copyright (c) 2022 UltiMaker
// Cura is released under the terms of the LGPLv3 or higher.

import QtQuick 2.7
import QtQuick.Layouts 1.3

import UM 1.5 as UM
import Cura 1.7 as Cura

Item {
    height: childrenRect.height

    property int leftColumnWidth: Math.floor(width * 0.35)
    property string selectorText : ""
    property string quality_key: ""
    property string backgroundTextLeftText: ""
    property string backgroundTextRightText: ""
    property string tooltipText: ""
    property string sourceIcon: ""




    // We use a binding to make sure that after manually setting omegaQualitySlider.value it is still bound to the property provider
   Binding
    {
        target: omegaQualitySlider
        property: "value"
        value: {
            return parseInt(omegaQuality.properties.value)
        }
    }

    Cura.IconWithText
    {
        id: qualityRowTitle
        text: catalog.i18nc("@label", selectorText)
        width: leftColumnWidth
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        source: UM.Theme.getIcon(sourceIcon)
        spacing: UM.Theme.getSize("default_margin").width
        iconSize: UM.Theme.getSize("medium_button_icon").width
        iconColor: UM.Theme.getColor("text")
        font: UM.Theme.getFont("medium_bold")
    }

    Item
    {
        id: omegaQualitySliderContainer
        height: childrenRect.height

        anchors
        {
            left: qualityRowTitle.right
            right: omegaQualitySlider.right
            verticalCenter: qualityRowTitle.verticalCenter
        }

        Text
        {
            id: backgroundTextLeft
            text: backgroundTextLeftText
            font.pixelSize: 8
            color:"white"
            anchors{
                right: omegaQualitySlider.left + 10
                verticalCenter: qualityRowTitle.verticalCenter

            }
        }

        Text
        {
            id: backgroundTextRight
            text: backgroundTextRightText
            color:"white"
            font.pixelSize: 8
            anchors{
                right: omegaQualitySlider.right
                verticalCenter: qualityRowTitle.verticalCenter

            }
        }


        CustomSlider {
            id: omegaQualitySlider
            from: 1
            to: 4
            stepSize: 1

            // set initial value from stack
            value: parseInt(omegaQuality.properties.value)

            onValueChanged:
            {
                if (!omegaQuality.properties.value || parseInt(omegaQuality.properties.value) == omegaQualitySlider.value)
                {
                    return
                }        

                //omegaQualitySlider.value = omegaQuality.properties.value

                // Otherwise if I change the value in the Custom mode the Recomended view will try to repeat
                // same operation
                var active_mode = UM.Preferences.getValue("cura/active_mode")

                if (active_mode == 0 || active_mode == "simple")
                {
                    Cura.MachineManager.setSettingForAllExtruders( quality_key, "value", omegaQualitySlider.value )
                }
            }
        }
    }

    property var omegaQuality : UM.SettingPropertyProvider
    {
        id: omegaQuality
        containerStack: Cura.MachineManager.activeStack
        key: quality_key
        watchedProperties: [ "value" ]
    }

}
