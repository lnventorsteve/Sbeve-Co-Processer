import sm_helpers as sm
import os
if os.name == "posix":
    path = (r"/home/dyaln/snap/steam/common/.local/share/Steam/steamapps/compatdata/387990/pfx/drive_c/users/"
            r"steamuser/AppData/Roaming/Axolot Games/Scrap Mechanic/User/User_76561198331351809/Blueprints/")
if os.name == "nt":
    path = r"C:\Users\Dylan\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198331351809\Blueprints/"

ID = sm.ID()  # init ID class
blueprint = sm.Blueprint(ID, path,r"225d3588-e26d-4972-ac5c-fdcb295d60f8")  # init Blueprint class

blueprint.load()

positions = []

for i in range(len(blueprint.childs)):
    dit_pos = blueprint.childs[i]["pos"]
    pos = dit_pos["x"],dit_pos["y"],dit_pos["z"]
    while pos in positions:
        print(blueprint.childs[i])
        blueprint.childs[i]["pos"]["z"] = pos[2]+1
        pos = pos[0],pos[1],pos[2]+1
    positions.append(pos)

blueprint.export_blueprint()
