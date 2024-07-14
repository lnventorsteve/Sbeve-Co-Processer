import time
import block_list
import sm_helpers as sm
import CPU_Components as cc
import color_list
import os
import compiler
start = time.perf_counter()
ID = sm.ID()  # init ID class


blueprint = sm.Blueprint(ID)  # init Blueprint class


blocks = block_list.blocks()  # list of usable blocks
objects = block_list.objects()  # list of usable objects
colors = color_list.colors()

sm.Timer(blueprint,ID,0,1,(0,0,0),"east","up")
sm.Timer(blueprint,ID,0,1,(2,0,0),"north","up")
sm.Timer(blueprint,ID,0,1,(4,0,0),"west","up")
sm.Timer(blueprint,ID,0,1,(6,0,0),"south","up")

blueprint.place_object(objects.Duct_Holder,(0,0,0),"up","right")
blueprint.place_object(objects.Duct_Holder,(2,0,0),"up","right")
blueprint.place_object(objects.Duct_Holder,(4,0,0),"up","right")
blueprint.place_object(objects.Duct_Holder,(6,0,0),"up","right")



blueprint.export_blueprint()

print(time.perf_counter()-start)