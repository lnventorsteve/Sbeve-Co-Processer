import json
import os
object_list = {}
block_list = {}

banned_objects = ["Piston","Handbook","Spud_Gun","Lift","Connect_Tool","Off_Road_Suspension","Sport_Suspension","Paint_Tool","Sledgehammer","Weld_Tool"]

creative_shapesets = os.listdir("E:/SteamLibrary/steamapps/common/Scrap Mechanic/Data/Objects/Database/ShapeSets")
survival_shapesets = os.listdir("E:/SteamLibrary/steamapps/common/Scrap Mechanic/Survival/Objects/Database/ShapeSets")

colors = {}

partslist = {}

for file in creative_shapesets:
    with open(f"E:/SteamLibrary/steamapps/common/Scrap Mechanic/Data/Objects/Database/ShapeSets/{file}","r") as file_json:
        blocks = json.loads(file_json.read())
        try:
            if "blocks" in file:
                for each in blocks["blockList"]:
                    partslist[each["uuid"]] = {}
                    partslist[each["uuid"]]["name"] = each["name"]
                    partslist[each["uuid"]]["color"] = each["color"]
            else:
                for each in blocks["partList"]:
                    partslist[each["uuid"]] = {}
                    partslist[each["uuid"]]["name"] = each["name"]
                    partslist[each["uuid"]]["color"] = each["color"]
        except:
            print("error",each)

for file in survival_shapesets:
    with open(f"E:/SteamLibrary/steamapps/common/Scrap Mechanic/Survival/Objects/Database/ShapeSets/{file}","r") as file_json:
        blocks = json.loads(file_json.read())
        try:
            if "blocks" in file:
                for each in blocks["blockList"]:
                    partslist[each["uuid"]] = {}
                    partslist[each["uuid"]]["name"] = each["name"]
                    partslist[each["uuid"]]["color"] = each["color"]
            else:
                for each in blocks["partList"]:
                    partslist[each["uuid"]] = {}
                    partslist[each["uuid"]]["name"] = each["name"]
                    partslist[each["uuid"]]["color"] = each["color"]
        except:
            print("error",each)



with open("E:/SteamLibrary/steamapps/common/Scrap Mechanic/Data/Gui/Language/English/InventoryItemDescriptions.json","r") as survival_items:
    items = json.loads(survival_items.read())
    for each in items:
        block = items[each]["title"]
        block = block.replace(" ", "_")
        block = block.replace("-", "_")
        block = block.replace("'","")
        block = block.replace(":","")
        block = block.replace("(","")
        block = block.replace(")","")
        block = block.replace(".","_")
        try:
            if "_Block" in block or block == "Net_Fence":
                block_list[block] = {}
                block_list[block]["uuid"] = each
                block_list[block]["color"] = partslist[each]["color"]
                partslist[each]["name"] = block
                print(partslist[each])
            elif block not in banned_objects:
                object_list[block] = {}
                object_list[block]["uuid"] = each
                object_list[block]["color"] = partslist[each]["color"]
                partslist[each]["name"] = block
                print(partslist[each])
        except:
            print("error",block)

with open("E:/SteamLibrary/steamapps/common/Scrap Mechanic/Survival/Gui/Language/English/inventoryDescriptions.json","r") as survival_items:
    items = json.loads(survival_items.read())
    for each in items:
        block = items[each]["title"]
        block = block.replace(" ", "_")
        block = block.replace("-", "_")
        block = block.replace("'","")
        block = block.replace(":","")
        block = block.replace("(","")
        block = block.replace(")","")
        block = block.replace(".","_")
        try:
            if "_Block" in block or block == "Net_Fence":
                block_list[block] = {}
                block_list[block]["uuid"] = each
                block_list[block]["color"] = partslist[each]["color"]
                partslist[each]["name"] = block
                print(partslist[each])
            elif block not in banned_objects:
                object_list[block] = {}
                object_list[block]["uuid"] = each
                object_list[block]["color"] = partslist[each]["color"]
                partslist[each]["name"] = block
                print(partslist[each])
        except:
            print("error",block)

with open("block_list.py", "w") as block_list_json:
    block_list_json.write('class objects:\n')
    block_list_json.write('    def __init__(self):\n')
    for block in object_list:
        block_list_json.write(f'        self.{block} = {object_list[block]}\n')
    block_list_json.write('class blocks:\n')
    block_list_json.write('    def __init__(self):\n')
    for block in block_list:
        block_list_json.write(f'        self.{block} = {block_list[block]}\n')


with open("logic rotations.json", "r") as blueprint_json:
    blueprint = json.loads(blueprint_json.read())
    bodies = blueprint["bodies"][0]
    childs = bodies["childs"]

    for block in childs:
        ID = block["controller"]["id"]
        x = block["pos"]["x"]-ID
        y = block["pos"]["y"]
        z = block["pos"]["z"]
        xaxis = block["xaxis"]
        zaxis = block["zaxis"]
        print((x,y,z),(xaxis,zaxis))




