import math

import sm_helpers as sm


ID = sm.ID()  # init ID class
blueprint = sm.Blueprint(ID, r"C:\Users\dylan\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198331351809\Blueprints\e37c1c7a-119b-44d8-a44b-8b511519fb46")  # put blue print path here

blueprint.load()

IDs = {}

for i in range(len(blueprint.childs)):
    if "controller" in blueprint.childs[i].keys():
        if "controllers" in blueprint.childs[i]["controller"].keys():
            if blueprint.childs[i]["controller"]["controllers"] is not None:
                for id in blueprint.childs[i]["controller"]["controllers"]:
                    id = str(id["id"])
                    if id in IDs.keys():
                        IDs[id] += 1
                    else:
                        IDs[id] = 1


max_value = math.log(sorted(IDs.values())[-1])

print(IDs)
print(max_value)

for i in range(len(blueprint.childs)):
    if "controller" in blueprint.childs[i].keys():
        if "controllers" in blueprint.childs[i]["controller"].keys():
            id = str(blueprint.childs[i]["controller"]["id"])
            if id in IDs:

                data = IDs[id]
                print(data)
                data = math.log(data)
            else:
                data = 0
            color = int(data * 255 / max_value)
            print(data,color)

            if blueprint.childs[i]["controller"]["controllers"] is not None:
                gray = len(blueprint.childs[i]["controller"]["controllers"])*10
                blueprint.childs[i]["color"] = sm.rgb_hex((color,gray,gray))
            else:
                blueprint.childs[i]["color"] = sm.rgb_hex((color,0,0))

blueprint.export_blueprint()