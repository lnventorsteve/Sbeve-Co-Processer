import sm_helpers as sm

ID = sm.ID()  # init ID class
blueprint = sm.Blueprint(ID)  # init Blueprint class

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
