from typing import Optional, Any

from UM.Application import Application
from UM.Logger import Logger
from UM.Settings.PropertyEvaluationContext import PropertyEvaluationContext
from UM.Settings.SettingFunction import SettingFunction
from typing import Any, Dict, List

##put BCN first in material list
def putBcn3dFirstInMaterials(brand_item_list : List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    position = 0
    switch = False
    for item in brand_item_list:
        if item['name'] == "BCN3D Filaments":
            switch = item
            break
        position +=1
    if switch:
        brand_item_list.pop(position)
        brand_item_list.insert(0, item)

    return brand_item_list

def checkMaterialcompatibility(active_quality_group, global_container_stack):
    checkMaterial =  Application.getInstance().getPreferences().getValue("cura/check_material_compatibility")
    if not checkMaterial:
        return active_quality_group.is_available
    materialcompatibility = {}
    materialcompatibility['PLA'] = ['PLA', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA','PVA', 'BVOH', 'TPU', 'TPU 64D',]
    materialcompatibility['Tough PLA'] = ['PLA', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA','PVA', 'BVOH', 'TPU', 'TPU 64D',]
    materialcompatibility['PVA'] = ['PLA', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA','PVA', 'TPU', 'TPU 64D', 'PAHT CF15', 'PET CF15']
    materialcompatibility['BVOH'] = ['PLA', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA', 'BVOH', 'ABS', 'TPU','TPU 64D', 'PA', 'PAHT CF15', 'PET CF15']
    materialcompatibility['ABS'] = ['BVOH', 'ABS', 'PC ABS FR', 'Matterhackers ABS', 'TPU','TPU 64D','PAHT CF15', 'PET CF15']
    materialcompatibility['PET-G'] = ['PET-G',  'Fillamentum PET-G','Matterhackers PET-G', 'PET CF15']
    materialcompatibility['TPU'] = ['PLA', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA', 'BVOH', 'PVA', 'ABS', 'TPU','TPU 64D', 'PET CF15']
    materialcompatibility['PA'] = ['BVOH', 'PA']
    materialcompatibility['PP'] = ['PP']
    materialcompatibility['PAHT CF15'] = ['PVA', 'BVOH', 'ABS', 'PC ABS FR', 'Matterhackers ABS', 'PAHT CF15']
    materialcompatibility['PP GF30'] = ['PP GF30']
    materialcompatibility['PET CF15'] = [ 'PVA', 'BVOH', 'ABS', 'PC ABS FR', 'Matterhackers ABS', 'PET-G',  'Fillamentum PET-G','Matterhackers PET-G', 'TPU','TPU 64D','PET CF15']
    materialcompatibility['17-4PH'] = ['17-4PH', 'Ultrafuse Support Layer']
    materialcompatibility['316L'] = ['316L', 'Ultrafuse Support Layer']
    materialcompatibility['Ultrafuse ASA'] = ['Ultrafuse ASA']
    materialcompatibility['Ultrafuse PET'] = ['Ultrafuse PET']
    materialcompatibility['Ultrafuse rPET'] = ['Ultrafuse rPET']
    materialcompatibility['Ultrafuse TPU 85A'] = ['Ultrafuse TPU 85A']
    materialcompatibility['Ultrafuse TPS 90A'] = ['Ultrafuse TPS 90A']
    materialcompatibility['Tech-X 316L HMs'] = ['Tech-X 316L HMs']
    materialcompatibility['Tech-X H13 HMs'] = ['Tech-X H13 HMs']
    materialcompatibility['Tech-X 17-4PH HMs'] = ['Tech-X 17-4PH HMs']
    materialcompatibility['Tech-X Inconel 625 HMs'] = ['Tech-X Inconel 625 HMs']
    materialcompatibility['Essentium HTN'] = ['Essentium HTN']
    materialcompatibility['Essentium PACF'] = ['Essentium PACF']
    materialcompatibility['Essentium PCTG Z'] = ['Essentium PCTG Z']
    materialcompatibility['Essentium PCTG'] = ['Essentium PCTG']
    materialcompatibility['Essentium PETCF'] = ['Essentium PETCF']
    materialcompatibility['Fillamentum NonOilen'] = ['Fillamentum NonOilen']
    materialcompatibility['Matterhackers PET-G'] = ['PET-G',  'Fillamentum PET-G','Matterhackers PET-G', 'PET CF15']
    materialcompatibility['Matterhackers PLA'] = ['PLA', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA','PVA', 'BVOH', 'TPU']
    materialcompatibility['Matterhackers Nylon'] = ['Matterhackers Nylon']
    materialcompatibility['Matterhackers ABS'] = ['BVOH', 'ABS', 'PC ABS FR', 'Matterhackers ABS', 'TPU','TPU 64D','PAHT CF15', 'PET CF15' 'Matterhackers ABS']
    materialcompatibility['Fillamentum PLA'] = ['PLA', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA','PVA', 'BVOH', 'TPU']
    materialcompatibility['PC ABS FR'] = ['BVOH', 'ABS', 'PC ABS FR', 'Matterhackers ABS', 'TPU','PAHT CF15', 'PET CF15']
    materialcompatibility['TPU 64D'] = ['PLA', 'TPU 64D', 'Fillamentum PLA', 'Matterhackers PLA', 'Tough PLA', 'BVOH', 'PVA', 'ABS', 'TPU', 'PET CF15']
    materialcompatibility['PA6 GF30'] = ['PA6 GF30']
    materialcompatibility['Fillamentum PET-G'] = ['PET-G', 'Fillamentum PET-G', 'Matterhackers PET-G', 'PET CF15']
    materialcompatibility['Fillamentum CPE'] = ['Fillamentum CPE']
    materialcompatibility['Ultrafuse Support Layer'] = ['Ultrafuse Support Layer', '316L', '17-4PH']

    ext0 = global_container_stack.extruderList[0]
    ext1 = global_container_stack.extruderList[1]
    if (ext0 and ext0.isEnabled ) and (ext1 and ext1.isEnabled):
        material1 = ext0.material.metaData['material']
        material2 = ext1.material.metaData['material']
        if material1 == material2:
            return True
        for material in materialcompatibility:
            if material == material1:
                for chekingMaterial in materialcompatibility[material]:
                    if chekingMaterial == material2:
                        return True
                return False
    return active_quality_group.is_available
