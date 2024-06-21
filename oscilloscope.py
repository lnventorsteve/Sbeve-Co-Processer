import block_list
import sm_helpers as sm
import CPU_Components as cc

ID = sm.ID()  # init ID class
blueprint = sm.Blueprint(ID, r"C:\Users\Dylan\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198331351809\Blueprints\b70f09e1-13b7-42ab-8528-8583f323d23e")  # init Blueprint class

blocks = block_list.blocks()    # list of useable blocks
objects = block_list.objects()  # list of useable objects

resolution = (32,8)

blueprint.fill_block(blocks.Plastic_Block,(0,0,0),(resolution[0]+2,1,1),sm.rgb_hex((166,155,149)))
blueprint.fill_block(blocks.Plastic_Block,(0,0,resolution[1]+1),(resolution[0]+2,1,1),sm.rgb_hex((166,155,149)))
blueprint.fill_block(blocks.Plastic_Block,(0,0,1),(1,1,resolution[1]),sm.rgb_hex((166,155,149)))
blueprint.fill_block(blocks.Plastic_Block,(resolution[0]+1,0,1),(1,1,resolution[1]),sm.rgb_hex((166,155,149)))
blueprint.fill_block(blocks.Plastic_Block,(0,1,0),(resolution[0]+2,1,resolution[1]+2),sm.rgb_hex((166,155,149)))

channel_1 = ID.get_next()
channel_2 = ID.get_next()
channel_3 = ID.get_next()
channel_4 = ID.get_next()


for x in range(resolution[0]):
    for y in range(resolution[1]):
        blueprint.logic_gate(ID.get_next(),"or",(1+resolution[0]-x,1,1+y),"south","left",sm.rgb_hex((166,155,149)))
        if x <= resolution[0]-2:
            blueprint.addId(ID.current_ID,ID.current_ID + 8)


blueprint.export_blueprint()