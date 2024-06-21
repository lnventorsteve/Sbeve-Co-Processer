import time
import block_list
import sm_helpers as sm
import CPU_Components as cc
import os
import compiler

ID = sm.ID()  # init ID class
if os.name == "posix":
    path = (r"/home/dyaln/.local/share/Steam/steamapps/compatdata/387990/pfx/dosdevices/c:/users/steamuser/"
            r"AppData/Roaming/Axolot Games/Scrap Mechanic/User/User_76561198331351809/Blueprints/")
if os.name == "nt":
    path = r"C:\Users\Dylan\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198331351809\Blueprints/"


blueprint = sm.Blueprint(ID, path, r"0d1ecb3e-a836-40c0-a35b-bfd22f6812ae")  # init Blueprint class


blocks = block_list.blocks()  # list of useable blocks
objects = block_list.objects()  # list of useable objects

blueprint.fill_block(blocks.Plastic_Block,(0,-1,0),(16,1,1))
blueprint.fill_block(blocks.Plastic_Block,(0,0,0),(6,1,1))
blueprint.fill_block(blocks.Plastic_Block,(8,3,0),(8,2,1))
switches_1 = cc.switches(blueprint,ID,16,(0,0,1))
switches_2 = cc.switches(blueprint,ID,8,(0,4,1))

disk = cc.disk(blueprint,ID,16,8,1048,(0,1,0))

disk.connect_address(switches_1.switches)

switches_2.switches.reverse()

blueprint.connect_ID(switches_2.switches,disk.input_gates)


"""


ram = cc.Ram(blueprint,ID,6,8,(0,0,0))

inputs = cc.switches(blueprint,ID,ram.bitness_out,(0,-1,1),"y,x,z")
inputs.switches.reverse()
blueprint.connect_ID(inputs.switches,ram.input_and)


address = cc.switches(blueprint,ID,ram.bitness_in,(0,2,1),"y,x,z")
address.switches.reverse()
blueprint.connect_ID(address.switches,ram.input_nors)
blueprint.connect_ID(address.switches,ram.input_ors)


buttons = cc.buttons(blueprint,ID,2,(0,-1,1),"x,y,z")
blueprint.connect_IDS(buttons.buttons[1],[ram.write])
blueprint.connect_IDS(buttons.buttons[0],[ram.read])

blueprint.fill_block(blocks.Plastic_Block,(-1,-1,0),(1,8,1))
"""

blueprint.export_blueprint()