import time
import sm_helpers as sm
start = time.perf_counter()
ID = sm.ID()  # init ID class

blueprint = sm.Blueprint(ID)  # init Blueprint class

blueprint.load()

IDs = {}

for i in range(len(blueprint.childs)):
    if "controller" in blueprint.childs[i].keys():
        if "controllers" in blueprint.childs[i]["controller"].keys():
            if blueprint.childs[i]["controller"]["controllers"] is not None:
                print(blueprint.childs[i])
                for id in blueprint.childs[i]["controller"]["controllers"]:
                    print(id)
                    id = str(id["id"])
                    if id in IDs.keys():
                        IDs[id] += 1
                    else:
                        IDs[id] = 1


print(time.perf_counter()-start)