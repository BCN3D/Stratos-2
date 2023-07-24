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