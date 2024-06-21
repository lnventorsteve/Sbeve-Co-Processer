import time
import block_list
import sm_helpers as sm
import CPU_Components as cc
import os
import compiler

ID = sm.ID()  # init ID class

if os.name == "posix":
    path = (r"/home/dyaln/snap/steam/common/.local/share/Steam/steamapps/compatdata/387990/pfx/drive_c/users/"
            r"steamuser/AppData/Roaming/Axolot Games/Scrap Mechanic/User/User_76561198331351809/Blueprints/")
elif os.name == "nt":
    path = r"C:\Users\Dylan\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198331351809\Blueprints/"
else:
    print("unknown os")
    exit(1)

blueprint = sm.Blueprint(ID, path, r"e37c1c7a-119b-44d8-a44b-8b511519fb46")  # init Blueprint class

blocks = block_list.blocks()    # list of useable blocks
objects = block_list.objects()  # list of useable objects

#
clock = cc.Clock(blueprint,ID,7,5,(7,37,0))

# pipe line
fetch = cc.Fetch(blueprint,ID,(26,2,0))
stage_1 = cc.PipeLine(blueprint,ID,(26,4,0))
stage_2 = cc.PipeLine(blueprint,ID,(26,7,0))

memory_bridge = cc.MemoryBridge(blueprint,ID,8,(26,0,0))


Main_bus = cc.Bus(blueprint,ID,8,(17,0,0),"d02525")         # 8-bit main bus

Address_bus = cc.Bus(blueprint,ID,16,(0,0,0),"0a3ee2")      # 16-bit address bus

Transfer_bus = cc.Bus(blueprint,ID,16,(0,36,0),"eeeeee")     # 16-bit transfer bus

ALU_LHS_bus = cc.Bus(blueprint,ID,8,(26,41,0),"2ce6e6")     # 8-bit ALU input bus right hand side shift
ALU_RHS_bus = cc.Bus(blueprint,ID,8,(26,42,0),"cf11d2")     # 8-bit ALU input bus left hand side bitwise

GPR_A = cc.GPR8Bit(blueprint,ID,(17,37,0))              # 8-bit general purpose register A
GPR_B = cc.GPR8Bit(blueprint,ID,(17,31,0))              # 8-bit general purpose register B
GPR_C = cc.GPR8Bit(blueprint,ID,(17,25,0))              # 8-bit general purpose register C
GPR_D = cc.GPR8Bit(blueprint,ID,(17,19,0))              # 8-bit general purpose register D

constant = cc.Register(blueprint,ID,8,(17,15,0))           # 8-bit register for loading values from program memory

Transfer_RHS = cc.Transfer8Bit(blueprint,ID,(17,1,0))   # 8-bit Transfer register right hand side
Transfer_LHS = cc.Transfer8Bit(blueprint,ID,(17,8,0))   # 8-bit Transfer register left hand side


pc = cc.Address16Bit(blueprint,ID,(0,29,0))               # 16-bit program counter
ra = cc.Address16Bit(blueprint,ID,(0,22,0))               # 16-bit return address
sp = cc.Address16Bit(blueprint,ID,(0,15,0))               # 16-bit stack pointer
di = cc.Address16Bit(blueprint,ID,(0,8,0))               # 16-bit destination index
si = cc.Address16Bit(blueprint,ID,(0,1,0))                # 16-bit source index


bitwise = cc.Bitwise(blueprint,ID,8,(26,34,0))
bitwise_reg = cc.RegisterNoOutput(blueprint,ID,9,(26,31,0))

shift = cc.Shift(blueprint,ID,9,(26,28,0))
shift_reg = cc.RegisterNoOutput(blueprint,ID,9,(26,25,0))


cla = cc.CLA(blueprint,ID,8,(26,11,0))

opcodes = cc.OpCodes(blueprint,ID,8,(0,0,1))

ram = cc.Ram(blueprint,ID,7,8,(-10,2,0),"-y,x,z",)

memory_map = cc.MemoryMap(blueprint,ID,16**2,8**2,8,(0,-8,0),"000000")

IO = cc.IO(blueprint,ID,8,(-9,-16,0))

# clock connections
clock.connect_rising(pc.decrement_clock)
clock.connect_rising(pc.increment_clock)
clock.connect_rising(ra.decrement_clock)
clock.connect_rising(ra.increment_clock)
clock.connect_rising(sp.decrement_clock)
clock.connect_rising(sp.increment_clock)
clock.connect_rising(di.decrement_clock)
clock.connect_rising(di.increment_clock)
clock.connect_rising(si.decrement_clock)
clock.connect_rising(si.increment_clock)
clock.connect_rising(IO.clock_high)


clock.connect_falling(pc.write_enable_clock)
clock.connect_falling(ra.write_enable_clock)
clock.connect_falling(sp.write_enable_clock)
clock.connect_falling(di.write_enable_clock)
clock.connect_falling(si.write_enable_clock)

clock.connect_falling(IO.clock_low)

clock.connect_falling(GPR_A.clock)
clock.connect_falling(GPR_B.clock)
clock.connect_falling(GPR_C.clock)
clock.connect_falling(GPR_D.clock)

clock.connect_falling(Transfer_RHS.transfer_bus_write_clock)
clock.connect_falling(Transfer_RHS.main_bus_write_clock)
clock.connect_falling(Transfer_LHS.transfer_bus_write_clock)
clock.connect_falling(Transfer_LHS.main_bus_write_clock)

clock.connect_falling(constant.clock)

clock.connect_falling(bitwise_reg.clock)
clock.connect_falling(shift_reg.clock)

clock.connect_falling(stage_1.clock)
clock.connect_falling(stage_2.clock)

# reset connections

clock.connect_reset(pc.write_enable)
clock.connect_reset(ra.write_enable)
clock.connect_reset(sp.write_enable)
clock.connect_reset(di.write_enable)
clock.connect_reset(si.write_enable)

clock.connect_reset(GPR_A.write_enable)
clock.connect_reset(GPR_B.write_enable)
clock.connect_reset(GPR_C.write_enable)
clock.connect_reset(GPR_D.write_enable)

clock.connect_reset(Transfer_RHS.main_bus_write_enable)
clock.connect_reset(Transfer_LHS.main_bus_write_enable)

clock.connect_reset(constant.write_enable)

clock.connect_reset(bitwise_reg.write_enable)
clock.connect_reset(shift_reg.write_enable)

# control line connections
opcodes.Add_control_line("Fetch_Denied",fetch.fetch_denied)

opcodes.Add_control_line("memory_bridge_Main_Data",memory_bridge.main_data_enable)
opcodes.Add_control_line("memory_bridge_Data_Main",memory_bridge.data_main_enable)

opcodes.Add_control_line("GPR_A_Load_Main_Bus",GPR_A.write_enable)
opcodes.Add_control_line("GPR_A_Assert_Main_Bus", GPR_A.bus_output_enable)
opcodes.Add_control_line("GPR_A_Assert_LHS_Bus",  GPR_A.lhs_output_enable)
opcodes.Add_control_line("GPR_A_Assert_RHS_Bus",  GPR_A.rhs_output_enable)

opcodes.Add_control_line("GPR_B_Load_Main_Bus",GPR_B.write_enable)
opcodes.Add_control_line("GPR_B_Assert_Main_Bus", GPR_B.bus_output_enable)
opcodes.Add_control_line("GPR_B_Assert_LHS_Bus",  GPR_B.lhs_output_enable)
opcodes.Add_control_line("GPR_B_Assert_RHS_Bus",  GPR_B.rhs_output_enable)

opcodes.Add_control_line("GPR_C_Load_Main_Bus",GPR_C.write_enable)
opcodes.Add_control_line("GPR_C_Assert_Main_Bus", GPR_C.bus_output_enable)
opcodes.Add_control_line("GPR_C_Assert_LHS_Bus",  GPR_C.lhs_output_enable)
opcodes.Add_control_line("GPR_C_Assert_RHS_Bus",  GPR_C.rhs_output_enable)

opcodes.Add_control_line("GPR_D_Load_Main_Bus",GPR_D.write_enable)
opcodes.Add_control_line("GPR_D_Assert_Main_Bus", GPR_D.bus_output_enable)
opcodes.Add_control_line("GPR_D_Assert_LHS_Bus",  GPR_D.lhs_output_enable)
opcodes.Add_control_line("GPR_D_Assert_RHS_Bus",  GPR_D.rhs_output_enable)

opcodes.Add_control_line("Constant_Load_Fetch",constant.write_enable)
opcodes.Add_control_line("Constant_Assert_Main_Bus", constant.bus_output_enable)

opcodes.Add_control_line("Transfer_LHS_Load_Main_Bus", Transfer_LHS.main_bus_write_enable)
opcodes.Add_control_line("Transfer_LHS_Assert_Main_Bus", Transfer_LHS.main_bus_output_enable)
opcodes.Add_control_line("Transfer_LHS_Load_Transfer_Bus",Transfer_LHS.transfer_bus_write_enable)
opcodes.Add_control_line("Transfer_LHS_Assert_Transfer_Bus",Transfer_LHS.transfer_bus_output_enable)

opcodes.Add_control_line("Transfer_RHS_Load_Main_Bus", Transfer_RHS.main_bus_write_enable)
opcodes.Add_control_line("Transfer_RHS_Assert_Main_Bus", Transfer_RHS.main_bus_output_enable)
opcodes.Add_control_line("Transfer_RHS_Load_Transfer_Bus",Transfer_RHS.transfer_bus_write_enable)
opcodes.Add_control_line("Transfer_RHS_Assert_Transfer_Bus",Transfer_RHS.transfer_bus_output_enable)

opcodes.Add_control_line("Program_Counter_Load_Transfer_Bus", pc.write_enable)
opcodes.Add_control_line("Program_Counter_Assert_Address_Bus", pc.address_bus_output_enable)
opcodes.Add_control_line("Program_Counter_Assert_Transfer_Bus", pc.transfer_bus_output_enable)
opcodes.Add_control_line("Program_Counter_Increment", pc.increment)
opcodes.Add_control_line("Program_Counter_Decrement", pc.decrement)

opcodes.Add_control_line("Return_Address_Load_Transfer_Bus", ra.write_enable)
opcodes.Add_control_line("Return_Address_Assert_Address_Bus", ra.address_bus_output_enable)
opcodes.Add_control_line("Return_Address_Assert_Transfer_Bus", ra.transfer_bus_output_enable)
opcodes.Add_control_line("Return_Address_Increment", ra.increment)
opcodes.Add_control_line("Return_Address_Decrement", ra.decrement)

opcodes.Add_control_line("Stack_Pointer_Load_Transfer_Bus", sp.write_enable)
opcodes.Add_control_line("Stack_Pointer_Assert_Address_Bus", sp.address_bus_output_enable)
opcodes.Add_control_line("Stack_Pointer_Assert_Transfer_Bus", sp.transfer_bus_output_enable)
opcodes.Add_control_line("Stack_Pointer_Increment", sp.increment)
opcodes.Add_control_line("Stack_Pointer_Decrement", sp.decrement)

opcodes.Add_control_line("Source_Index_Load_Transfer_Bus", si.write_enable)
opcodes.Add_control_line("Source_Index_Assert_Address_Bus", si.address_bus_output_enable)
opcodes.Add_control_line("Source_Index_Assert_Transfer_Bus", si.transfer_bus_output_enable)
opcodes.Add_control_line("Source_Index_Increment", si.increment)
opcodes.Add_control_line("Source_Index_Decrement", si.decrement)

opcodes.Add_control_line("Destination_Index_Load_Transfer_Bus", di.write_enable)
opcodes.Add_control_line("Destination_Index_Assert_Address_Bus", di.address_bus_output_enable)
opcodes.Add_control_line("Destination_Index_Assert_Transfer_Bus", di.transfer_bus_output_enable)
opcodes.Add_control_line("Destination_Index_Increment", di.increment)
opcodes.Add_control_line("Destination_Index_Decrement", di.decrement)

opcodes.Add_control_line("Bitwise_Or", bitwise.or_ctrl)
opcodes.Add_control_line("Bitwise_And", bitwise.and_ctrl)
opcodes.Add_control_line("Bitwise_Xor", bitwise.xor_ctrl)
opcodes.Add_control_line("Bitwise_Nor", bitwise.nor_ctrl)
opcodes.Add_control_line("Bitwise_Pass", bitwise.pass_ctrl)
opcodes.Add_control_line("Bitwise_Fill", bitwise.fill_ctrl)
opcodes.Add_control_line("Bitwise_Carry", bitwise.carry_ctrl)

opcodes.Add_control_line("Shift_Left", shift.shl_ctrl)
opcodes.Add_control_line("Shift_Right", shift.shr_ctrl)
opcodes.Add_control_line("Shift_Pass", shift.pass_ctrl)

opcodes.Add_control_line("Bitwise_Register_Write", bitwise_reg.write_enable)
opcodes.Add_control_line("Shift_Register_Write", shift_reg.write_enable)

opcodes.Add_control_line("AlU_Assert_Main_Bus", cla.output_enable)
opcodes.Add_control_line("AlU_Loop_Carry", cla.carry_loop_or)

opcodes.Add_flags("Arithmetic_Carry_flag",cla.carry)
opcodes.Add_flags("Logic_Carry_flag",bitwise_reg.memcells[8])

opcodes.Add_flags("ALU_Zero_flag",cla.Zero_flag)
opcodes.Add_flags("ALU_Over_Flow_flag",cla.OverFlow)
opcodes.Add_flags("ALU_sign_flag",cla.out_xor[-1])

opcodes.Add_control_line("Ram_Read", ram.read)
opcodes.Add_control_line("Ram_Write", ram.write)

opcodes.Add_control_line("IO_Read", IO.read)
opcodes.Add_control_line("IO_Write", IO.write)


# Memory Bridge connections
Main_bus.connect_to_bus(memory_bridge.data_main)
Main_bus.connect_from_bus(memory_bridge.main_data)
blueprint.connect_ID(memory_bridge.main_data,fetch.fetch_input)
blueprint.connect_ID(fetch.fetch_input,memory_bridge.data_main)

# connect register outputs to main bus
Main_bus.connect_to_bus(GPR_A.bus_output)
Main_bus.connect_to_bus(GPR_B.bus_output)
Main_bus.connect_to_bus(GPR_C.bus_output)
Main_bus.connect_to_bus(GPR_D.bus_output)
Main_bus.connect_to_bus(Transfer_RHS.main_bus_output)
Main_bus.connect_to_bus(Transfer_LHS.main_bus_output)

# connect register inputs to main bus
Main_bus.connect_from_bus(GPR_A.bus_input)
Main_bus.connect_from_bus(GPR_B.bus_input)
Main_bus.connect_from_bus(GPR_C.bus_input)
Main_bus.connect_from_bus(GPR_D.bus_input)
Main_bus.connect_from_bus(Transfer_RHS.main_bus_input)
Main_bus.connect_from_bus(Transfer_LHS.main_bus_input)

# connect IO to main bus
Main_bus.connect_from_bus(IO.bus_output)
Main_bus.connect_to_bus(IO.bus_input)

# connect IO to address bus
Address_bus.connect_from_bus([None for _ in range(13)]+IO.address_ands)
Address_bus.connect_from_bus([None for _ in range(13)]+IO.address_nands)


# connect GPR outputs to ALU bus LHS
ALU_LHS_bus.connect_to_bus(GPR_A.lhs_output)
ALU_LHS_bus.connect_to_bus(GPR_B.lhs_output)
ALU_LHS_bus.connect_to_bus(GPR_C.lhs_output)
ALU_LHS_bus.connect_to_bus(GPR_D.lhs_output)

# connect GPR outputs to ALU bus RHS
ALU_RHS_bus.connect_to_bus(GPR_A.rhs_output)
ALU_RHS_bus.connect_to_bus(GPR_B.rhs_output)
ALU_RHS_bus.connect_to_bus(GPR_C.rhs_output)
ALU_RHS_bus.connect_to_bus(GPR_D.rhs_output)

# connect the 16-bit registers outputs to the Address bus
Address_bus.connect_to_bus(pc.address_bus_output)
Address_bus.connect_to_bus(ra.address_bus_output)
Address_bus.connect_to_bus(sp.address_bus_output)
Address_bus.connect_to_bus(di.address_bus_output)
Address_bus.connect_to_bus(si.address_bus_output)

# connect the 16-bit registers outputs to the Transfer bus
Transfer_bus.connect_to_bus(pc.transfer_bus_output)
Transfer_bus.connect_to_bus(ra.transfer_bus_output)
Transfer_bus.connect_to_bus(sp.transfer_bus_output)
Transfer_bus.connect_to_bus(di.transfer_bus_output)
Transfer_bus.connect_to_bus(si.transfer_bus_output)

Transfer_bus.connect_to_bus([None,None,None,None,None,None,None,None] + Transfer_RHS.transfer_bus_output)
Transfer_bus.connect_to_bus(Transfer_LHS.transfer_bus_output)


# connect the Transfer bus to 16-bit registers inputs
Transfer_bus.connect_from_bus(pc.transfer_bus_input)
Transfer_bus.connect_from_bus(ra.transfer_bus_input)
Transfer_bus.connect_from_bus(sp.transfer_bus_input)
Transfer_bus.connect_from_bus(di.transfer_bus_input)
Transfer_bus.connect_from_bus(si.transfer_bus_input)

Transfer_bus.connect_from_bus([None,None,None,None,None,None,None,None] + Transfer_RHS.transfer_bus_input)
Transfer_bus.connect_from_bus(Transfer_LHS.transfer_bus_input)

blueprint.connect_ID(fetch.fetch_input,constant.bus_input)
blueprint.connect_ID(fetch.fetch_output,stage_1.input)
blueprint.connect_ID(stage_1.memcells,stage_2.input)

Main_bus.connect_to_bus(constant.bus_output)

bitwise.connect(ALU_RHS_bus.Bus_IDS,ALU_LHS_bus.Bus_IDS)
bitwise.register(bitwise_reg)

shift.connect(ALU_LHS_bus.Bus_IDS)
shift.register(shift_reg)

cla.connect(bitwise_reg.memcells,shift_reg.memcells)

shift.carry(cla.carry_loop_and)

Main_bus.connect_to_bus(cla.output)

# fill holes
if True:
    blueprint.place_object(objects.Duct_Holder,(7,37,0),"up","up","000000")

    blueprint.place_object(objects.Duct_Holder,(16,0,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(16,36,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(16,37,0),"up","up","000000")

    blueprint.place_object(objects.Duct_Holder,(25,0,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(25,5,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(25,12,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(25,15,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(25,19,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(25,25,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(25,31,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(25,37,0),"up","up","000000")

    blueprint.place_object(objects.Duct_Holder,(28,17,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(29,17,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(29,18,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(30,18,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(30,19,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(31,19,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(31,20,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(32,20,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(32,21,0),"up","up","000000")


    blueprint.place_object(objects.Duct_Holder,(34,2,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,4,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,6,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,7,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,9,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,12,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,13,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,41,0),"up","up","000000")
    blueprint.place_object(objects.Duct_Holder,(34,42,0),"up","up","000000")

    blueprint.place_object(objects.Duct_Holder,(35,31,0),"up","up","000000")

    for x in range(9):
        blueprint.place_object(objects.Duct_Holder,(x - 9,-11,0),"up","up","000000")

    for y in range(3):
        blueprint.place_object(objects.Duct_Holder,(-1,-14 + y,0),"up","up","000000")


    for x in range(6):
        blueprint.place_object(objects.Duct_Holder,(32-x,16,0),"up","up","000000")

    for x in range(9):
        blueprint.place_object(objects.Duct_Holder,(34-x,10,0),"up","up","000000")

    for x in range(7):
        for y in range(4):
            blueprint.place_object(objects.Duct_Holder,(0+x,37+y,0),"up","up","000000")

    for y in range(42):
        blueprint.place_object(objects.Duct_Holder,(35,y-16,0),"up","up","000000")

    for y in range(8):
        blueprint.place_object(objects.Duct_Holder,(34,y-8,0),"up","up","000000")

    for y in range(9):
        blueprint.place_object(objects.Duct_Holder,(35,34+y,0),"up","up","000000")

    for y in range(7):
        blueprint.place_object(objects.Duct_Holder,(33,16+y,0),"up","up","000000")

    for y in range(4):
        blueprint.place_object(objects.Duct_Holder,(36,10 + y,0),"up","up","000000")
    for y in range(3):
        blueprint.place_object(objects.Duct_Holder,(36,40 + y,0),"up","up","000000")

    for x in range(8):
        blueprint.place_object(objects.Duct_Holder,(37+x,13,0),"up","up","000000")

    for y in range(6):
        blueprint.place_object(objects.Duct_Holder,(44,7 + y,0),"up","up","000000")
        blueprint.place_object(objects.Duct_Holder,(44,37 + y,0),"up","up","000000")

    for y in range(59):
        blueprint.place_object(objects.Small_Pipe_Tee,(-10,y - 16,0),"up","up","000000")
        blueprint.place_object(objects.Duct_End,(-10,y - 16,0),"south","right","000000")
        blueprint.place_object(objects.Duct_End,(-10,y - 16,0),"north","left","000000")
        blueprint.place_object(objects.Duct_End,(-10,y - 16,0),"south","left","000000")

        blueprint.place_object(objects.Small_Pipe_Tee,(45,y - 16,0),"up","down","000000")
        blueprint.place_object(objects.Duct_End,(45,y - 16,0),"west","down","000000")
        blueprint.place_object(objects.Duct_End,(45,y - 16,0),"south","right","000000")
        blueprint.place_object(objects.Duct_End,(45,y - 16,0),"south","left","000000")

    for x in range(54):
        blueprint.place_object(objects.Small_Pipe_Tee,(x - 9,-17,0),"up","left","000000")
        blueprint.place_object(objects.Duct_End,(x - 9,-17,0),"west","down","000000")
        blueprint.place_object(objects.Duct_End,(x - 9,-17,0),"east","left","000000")
        blueprint.place_object(objects.Duct_End,(x - 9,-17,0),"west","left","000000")

        blueprint.place_object(objects.Small_Pipe_Tee,(x - 9,43,0),"up","right","000000")
        blueprint.place_object(objects.Duct_End,(x - 9,43,0),"west","up","000000")
        blueprint.place_object(objects.Duct_End,(x - 9,43,0),"east","left","000000")
        blueprint.place_object(objects.Duct_End,(x - 9,43,0),"west","left","000000")

    blueprint.place_object(objects.Small_Pipe_Bend,(-10,-17,0),"west","left","000000")
    blueprint.place_object(objects.Duct_End,(-10,-17,0),"west","right","000000")
    blueprint.place_object(objects.Duct_End,(-10,-17,0),"south","left","000000")
    blueprint.place_object(objects.Duct_End,(-10,-17,0),"west","down","000000")
    blueprint.place_object(objects.Duct_End,(-10,-17,0),"south","up","000000")
    blueprint.place_object(objects.Small_Pipe_Bend,(-10,43,0),"west","right","000000")
    blueprint.place_object(objects.Duct_End,(-10,43,0),"west","right","000000")
    blueprint.place_object(objects.Duct_End,(-10,43,0),"north","left","000000")
    blueprint.place_object(objects.Duct_End,(-10,43,0),"west","up","000000")
    blueprint.place_object(objects.Duct_End,(-10,43,0),"north","right","000000")
    blueprint.place_object(objects.Small_Pipe_Bend,(45,-17,0),"east","left","000000")
    blueprint.place_object(objects.Duct_End,(45,-17,0),"south","left","000000")
    blueprint.place_object(objects.Duct_End,(45,-17,0),"east","left","000000")
    blueprint.place_object(objects.Duct_End,(45,-17,0),"south","down","000000")
    blueprint.place_object(objects.Duct_End,(45,-17,0),"east","up","000000")
    blueprint.place_object(objects.Small_Pipe_Bend,(45,43,0),"east","right","000000")
    blueprint.place_object(objects.Duct_End,(45,43,0),"east","down","000000")
    blueprint.place_object(objects.Duct_End,(45,43,0),"north","up","000000")
    blueprint.place_object(objects.Duct_End,(45,43,0),"east","left","000000")
    blueprint.place_object(objects.Duct_End,(45,43,0),"north","right","000000")

with open("opcodes_list.py","w") as opcodes_list_json:
    opcodes_list_json.write('class Control_Lines:\n')
    opcodes_list_json.write('    def __init__(self):\n')
    for control_line in opcodes.control_lines:
        opcodes_list_json.write(f'        self.{control_line} = {opcodes.control_lines[control_line]}\n')
    for flag in opcodes.flags:
        opcodes_list_json.write(f'        self.{flag} = {opcodes.flags[flag]}\n')


opcodes.createOpcodes()
opcodes.make_opcode_roms((36,-16,0),stage_1,stage_2)

compiler.compile()

program_rom = cc.Rom(blueprint,ID,8,"rom.txt",8,(0,-16,0),"ffffff")

memory_map.map(program_rom.enables,0)
memory_map.map(ram.enables,1)




Address_bus.connect_from_bus(memory_map.input+[None,None,None,None,None,None,None,None])
Address_bus.connect_from_bus(memory_map.input_not+[None,None,None,None,None,None,None,None])

blueprint.connect_ID(program_rom.output,fetch.fetch_input)

Address_bus.connect_from_bus([None,None,None,None,None,None,None,None] + program_rom.input)
Address_bus.connect_from_bus([None,None,None,None,None,None,None,None] + program_rom.input_not)

Address_bus.connect_from_bus([None,None,None,None,None,None,None,None,None] + ram.input_ors)
Address_bus.connect_from_bus([None,None,None,None,None,None,None,None,None] + ram.input_nors)

blueprint.connect_ID(ram.output_or,fetch.fetch_input)
blueprint.connect_ID(fetch.fetch_input,ram.input_xor)
clock.connect_falling(ram.clock)

blueprint.export_blueprint()



