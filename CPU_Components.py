import math

import block_list
import color_list
import opcodes_list
import sm_helpers

blocks = block_list.blocks()
objects = block_list.objects()
colors = color_list.colors()
oc = opcodes_list.Control_Lines()


class Clock:
    def __init__(self,blueprint,ID,clock_high,clock_low,pos):
        self.blueprint = blueprint
        self.clock_high = clock_high
        self.clock_low = clock_low
        self.pos = pos
        self.ID_Offset = ID.claim_range(27)

        self.reset = ID.get_next()
        self.clock_rising = ID.get_next()
        self.clock_falling = ID.get_next()

        self.output_tick_gen_and = ID.get_next()
        self.output_tick_gen_nor = ID.get_next()
        self.output_tick_gen_or = ID.get_next()

        self.falling_timer = ID.get_next()

        if clock_high + clock_low > 4:
            self.clock_timer = ID.get_next()
        else:
            self.clock_nor_fast = ID.get_next()
            self.clock_and_fast = ID.get_next()

        self.clock_nor = ID.get_next()
        self.clock_and = ID.get_next()

        self.clock_enable_xor = ID.get_next()
        self.reset_enable_xor = ID.get_next()

        self.reset_timer = ID.get_next()
        self.reset_tick_gen_and = ID.get_next()
        self.reset_tick_gen_nor = ID.get_next()
        self.reset_input = ID.get_next()

        self.clock_tick_gen_and = ID.get_next()
        self.clock_tick_gen_nor = ID.get_next()
        self.clock_enable_input = ID.get_next()

        self.clock_enable_or = ID.get_next()
        self.clock_enable_nor = ID.get_next()

        self.clock_or_and = ID.get_next()
        self.clock_nor_and = ID.get_next()

        self.step_and = ID.get_next()
        self.step_input = ID.get_next()

        self.step_latch_xor = ID.get_next()
        self.step_tick_gen_and = ID.get_next()
        self.step_tick_gen_nor = ID.get_next()

        self.step_latch_nor = ID.get_next()
        self.step_latch_nor_and = ID.get_next()

        self.step_latch_or = ID.get_next()
        self.step_latch_or_and = ID.get_next()

        self.reset_button = ID.get_next()
        self.step_button = ID.get_next()
        self.run_button = ID.get_next()

        x,y,z = pos

        blueprint.button(self.reset_button,(x-1,3 + y,z + 1),"up","up","d02525")
        blueprint.button(self.step_button,(x-1,2 + y,z + 1),"up","up","0a3ee2")
        blueprint.button(self.run_button,(x-1,1 + y,z + 1),"up","up","19e753")




        blueprint.logic_gate(self.reset_input,"or",(0 + x,3 + y,z),"up","right","d02525")
        blueprint.logic_gate(self.step_latch_or,"or",(1 + x,3 + y,z),"up","right","222222")
        blueprint.addId(self.step_latch_or,self.step_latch_or_and)
        blueprint.logic_gate(self.step_latch_xor,"xor",(2 + x,3 + y,z),"up","right","222222")
        blueprint.addId(self.step_latch_xor,self.step_latch_xor)
        blueprint.addId(self.step_latch_xor,self.step_latch_or)
        blueprint.addId(self.step_latch_xor,self.step_latch_nor)
        blueprint.addId(self.step_latch_xor,self.output_tick_gen_or)
        blueprint.logic_gate(self.reset_tick_gen_nor,"nor",(3 + x,3 + y,z),"up","right","222222")
        blueprint.addId(self.reset_input,self.reset_tick_gen_nor)
        blueprint.logic_gate(self.reset_tick_gen_and,"and",(4 + x,3 + y,z),"up","right","222222")
        blueprint.addId(self.reset_input,self.reset_tick_gen_and)
        blueprint.addId(self.reset_tick_gen_nor,self.reset_tick_gen_and)
        blueprint.addId(self.reset_tick_gen_and,self.clock_nor_and)
        blueprint.logic_gate(self.reset_enable_xor,"xor",(5 + x,3 + y,z),"up","right","222222")
        blueprint.addId(self.reset_enable_xor,self.reset_enable_xor)
        blueprint.addId(self.reset_tick_gen_and,self.reset_enable_xor)
        blueprint.timer(self.reset_timer,0,clock_high + clock_low + 1,(6 + x,3 + y,z),"east","right","222222")
        blueprint.addId(self.reset_tick_gen_and,self.reset_timer)
        blueprint.addId(self.reset_timer,self.clock_or_and)
        blueprint.addId(self.reset_timer,self.reset_enable_xor)
        blueprint.logic_gate(self.reset,"and",(8 + x,3 + y,z),"up","right","d02525")
        blueprint.addId(self.reset_enable_xor,self.reset)

        blueprint.logic_gate(self.step_input,"or",(0 + x,2 + y,z),"up","right","0a3ee2")
        blueprint.addId(self.step_input,self.step_and)
        blueprint.addId(self.step_input,self.step_latch_nor_and)

        blueprint.logic_gate(self.step_latch_or_and,"and",(1 + x,2 + y,z),"up","right","222222")
        blueprint.addId(self.step_latch_or_and,self.step_latch_xor)
        blueprint.logic_gate(self.step_tick_gen_and,"and",(2 + x,2 + y,z),"up","right","222222")
        blueprint.addId(self.step_tick_gen_and,self.step_latch_xor)

        blueprint.logic_gate(self.clock_or_and,"and",(3 + x,2 + y,z),"up","right","222222")
        blueprint.addId(self.clock_or_and,self.clock_enable_xor)
        blueprint.logic_gate(self.clock_tick_gen_and,"and",(4 + x,2 + y,z),"up","right","222222")
        blueprint.addId(self.clock_tick_gen_and,self.clock_enable_xor)

        blueprint.logic_gate(self.clock_enable_xor,"xor",(5 + x,2 + y,z),"up","right","222222")
        blueprint.addId(self.clock_enable_xor,self.clock_enable_xor)
        blueprint.addId(self.clock_enable_xor,self.step_and)
        blueprint.addId(self.clock_enable_xor,self.clock_enable_nor)
        blueprint.addId(self.clock_enable_xor,self.clock_enable_or)
        blueprint.addId(self.clock_enable_xor,self.step_latch_nor)

        blueprint.timer(self.falling_timer,0,clock_low - 1,(6 + x,2 + y,z),"east","right","222222")
        blueprint.addId(self.falling_timer,self.clock_falling)

        blueprint.logic_gate(self.clock_falling,"and",(8 + x,2 + y,z),"up","right","e2db13")
        blueprint.addId(self.clock_falling,self.step_latch_or_and)

        blueprint.logic_gate(self.clock_enable_input,"or",(0 + x,1 + y,z),"up","right","19e753")

        blueprint.logic_gate(self.step_latch_nor,"nor",(1 + x,1 + y,z),"up","right","222222")
        blueprint.addId(self.step_latch_nor,self.step_latch_nor_and)

        blueprint.logic_gate(self.step_tick_gen_nor,"nor",(2 + x,1 + y,z),"up","right","222222")
        blueprint.addId(self.step_tick_gen_nor,self.step_tick_gen_and)

        blueprint.logic_gate(self.clock_nor_and,"and",(3 + x,1 + y,z),"up","right","222222")
        blueprint.addId(self.clock_nor_and,self.clock_enable_xor)

        blueprint.logic_gate(self.clock_tick_gen_nor,"nor",(4 + x,1 + y,z),"up","right","222222")
        blueprint.addId(self.clock_enable_input,self.clock_tick_gen_nor)
        blueprint.addId(self.clock_enable_input,self.clock_tick_gen_and)
        blueprint.addId(self.clock_tick_gen_nor,self.clock_tick_gen_and)

        blueprint.logic_gate(self.output_tick_gen_or,"or",(5 + x,1 + y,z),"up","right","222222")
        blueprint.logic_gate(self.output_tick_gen_nor,"nor",(6 + x,1 + y,z),"up","right","222222")
        blueprint.logic_gate(self.output_tick_gen_and,"and",(7 + x,1 + y,z),"up","right","222222")
        blueprint.logic_gate(self.clock_rising,"and",(8 + x,1 + y,z),"up","right","19e753")
        blueprint.addId(self.output_tick_gen_or,self.output_tick_gen_nor)
        blueprint.addId(self.output_tick_gen_or,self.output_tick_gen_and)
        blueprint.addId(self.output_tick_gen_nor,self.output_tick_gen_and)
        blueprint.addId(self.output_tick_gen_and,self.clock_rising)
        blueprint.addId(self.output_tick_gen_and,self.falling_timer)

        blueprint.logic_gate(self.step_latch_nor_and,"and",(1 + x,0 + y,z),"up","right","222222")
        blueprint.addId(self.step_latch_nor_and,self.step_tick_gen_nor)
        blueprint.addId(self.step_latch_nor_and,self.step_tick_gen_and)

        blueprint.logic_gate(self.step_and,"and",(2 + x,0 + y,z),"up","right","222222")
        blueprint.addId(self.step_and,self.clock_enable_input)

        blueprint.logic_gate(self.clock_enable_nor,"nor",(3 + x,0 + y,z),"up","right","222222")
        blueprint.addId(self.clock_enable_nor,self.clock_nor_and)

        blueprint.logic_gate(self.clock_enable_or,"or",(4 + x,0 + y,z),"up","right","222222")
        blueprint.addId(self.clock_enable_or,self.clock_or_and)

        blueprint.logic_gate(self.clock_and,"and",(5 + x,0 + y,z),"up","right","222222")
        blueprint.addId(self.clock_and,self.clock_nor)
        blueprint.addId(self.clock_enable_xor,self.clock_and)
        blueprint.addId(self.clock_and,self.output_tick_gen_or)
        blueprint.logic_gate(self.clock_nor,"nor",(6 + x,0 + y,z),"up","right","222222")

        if clock_high + clock_low > 4:
            blueprint.timer(self.clock_timer,0,int(clock_high / 2),(7 + x,0 + y,z),"east","right","222222")
            blueprint.addId(self.clock_nor,self.clock_timer)
            blueprint.addId(self.clock_timer,self.clock_and)
        else:
            blueprint.addId(self.clock_enable_xor,self.clock_and_fast)
            blueprint.addId(self.clock_nor,self.clock_and_fast)
            blueprint.logic_gate(self.clock_and_fast,"and",(7 + x,0 + y,z),"up","right","222222")
            blueprint.addId(self.clock_and_fast,self.clock_nor_fast)
            blueprint.logic_gate(self.clock_nor_fast,"nor",(8 + x,0 + y,z),"up","right","222222")
            blueprint.addId(self.clock_nor_fast,self.clock_and)
        # visualizer
        blueprint.logic_gate(ID.get_next(),"xor",(9 + x,1 + y,z),"up","right","222222")
        blueprint.addId(self.clock_rising,ID.current_ID)
        blueprint.addId(self.clock_falling,ID.current_ID)
        blueprint.addId(ID.current_ID,ID.current_ID)
        blueprint.addId(ID.current_ID,ID.current_ID + 1)
        blueprint.addId(ID.current_ID,ID.current_ID + 2)
        blueprint.logic_gate(ID.get_next(),"or",(9 + x,2 + y,z),"up","right","222222")
        blueprint.addId(ID.current_ID,ID.current_ID + 2)
        blueprint.logic_gate(ID.get_next(),"nor",(9 + x,3 + y,z),"up","right","222222")
        blueprint.addId(ID.current_ID,ID.current_ID + 2)
        i = 0
        for i in range(16):
            blueprint.logic_gate(ID.get_next(),"or",(9 + x - i,5 + y,z),"up","right","222222")
            blueprint.addId(ID.current_ID,ID.current_ID + 2)
            blueprint.logic_gate(ID.get_next(),"or",(9 + x - i,4 + y,z),"up","right","222222")
            blueprint.addId(ID.current_ID,ID.current_ID + 2)
        blueprint.logic_gate(ID.get_next(),"or",(8 + x - i,5 + y,z),"up","right","222222")
        blueprint.logic_gate(ID.get_next(),"or",(8 + x - i,4 + y,z),"up","right","222222")

    def connect_rising(self,clock):
        self.blueprint.addId(self.clock_rising,clock)

    def connect_falling(self,clock):
        self.blueprint.addId(self.clock_falling,clock)

    def connect_reset(self,clock):
        self.blueprint.addId(self.reset,clock)

class GPR8Bit:
    def __init__(self,blueprint,ID,pos):
        self.blueprint = blueprint
        self.ID_Offset = ID.claim_range(52)

        self.memcells = []
        self.latch = []
        self.bus_input = []
        self.bus_output = []
        self.lhs_output = []
        self.rhs_output = []
        for ID in range(8):
            self.memcells.append(ID + self.ID_Offset)
            self.latch.append(ID + 8 + self.ID_Offset)
            self.bus_input.append(ID + 16 + self.ID_Offset)
            self.bus_output.append(ID + 24 + self.ID_Offset)
            self.lhs_output.append(ID + 32 + self.ID_Offset)
            self.rhs_output.append(ID + 40 + self.ID_Offset)

        self.write_enable = 48 + self.ID_Offset
        self.clock = 49 + self.ID_Offset
        self.bus_output_enable = 50 + self.ID_Offset
        self.lhs_output_enable = 51 + self.ID_Offset
        self.rhs_output_enable = 52 + self.ID_Offset

        x,y,z = pos

        blueprint.logic_gate(self.write_enable,"or",(8 + x,2 + y,z),"up","right","19e753")
        blueprint.logic_gate(self.clock,"and",(8 + x,1 + y,z),"up","right","19e753")
        blueprint.addId(self.write_enable,self.clock)
        blueprint.logic_gate(self.bus_output_enable,"or",(8 + x,3 + y,z),"up","right","eeeeee")
        blueprint.logic_gate(self.rhs_output_enable,"or",(8 + x,5 + y,z),"up","right","cf11d2")
        blueprint.logic_gate(self.lhs_output_enable,"or",(8 + x,4 + y,z),"up","right","2ce6e6")

        for i in range(8):
            # and rhs bus out
            blueprint.logic_gate(self.rhs_output[i],"and",(i + x,5 + y,z),"up","right","cf11d2")
            blueprint.addId(self.rhs_output_enable,self.rhs_output[i])
            # and lhs bus out
            blueprint.logic_gate(self.lhs_output[i],"and",(i + x,4 + y,z),"up","right","2ce6e6")
            blueprint.addId(self.lhs_output_enable,self.lhs_output[i])
            # and main bus out
            blueprint.logic_gate(self.bus_output[i],"and",(i + x,3 + y,z),"up","right","eeeeee")
            blueprint.addId(self.bus_output_enable,self.bus_output[i])
            # xor memory cells
            blueprint.logic_gate(self.memcells[i],"xor",(x + i,2 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.memcells[i],self.memcells[i])
            blueprint.addId(self.memcells[i],self.bus_input[i])
            blueprint.addId(self.memcells[i],self.bus_output[i])
            blueprint.addId(self.memcells[i],self.lhs_output[i])
            blueprint.addId(self.memcells[i],self.rhs_output[i])
            # and gates for latch
            blueprint.logic_gate(self.latch[i],"and",(i + x,1 + y,z),"up","right","19e753")
            blueprint.addId(self.clock,self.latch[i])
            blueprint.addId(self.latch[i],self.memcells[i])
            # xor gates for input
            blueprint.logic_gate(self.bus_input[i],"xor",(i + x,y,z),"up","right","d02525")
            blueprint.addId(self.bus_input[i],self.latch[i])

class Address16Bit:
    def __init__(self,blueprint,ID,pos):
        self.blueprint = blueprint
        self.pos = pos
        self.ID_Offset = ID.claim_range(180)

        self.memcells = []
        self.transfer_bus_input = []
        self.latch = []
        self.address_bus_output = []
        self.transfer_bus_output = []
        self.not_gate = []
        self.dec_and = []
        self.inc_and = []

        for ID in range(16):
            self.memcells.append(ID + self.ID_Offset)
            self.transfer_bus_input.append(20 + ID + self.ID_Offset)
            self.latch.append(40 + ID + self.ID_Offset)
            self.address_bus_output.append(60 + ID + self.ID_Offset)
            self.transfer_bus_output.append(80 + ID + self.ID_Offset)
            self.not_gate.append(100 + ID + self.ID_Offset)
            self.inc_and.append(120 + ID + self.ID_Offset)

        self.write_enable = 160 + self.ID_Offset
        self.write_enable_clock = 161 + self.ID_Offset
        self.address_bus_output_enable = 162 + self.ID_Offset
        self.transfer_bus_output_enable = 163 + self.ID_Offset
        self.increment = 164 + self.ID_Offset
        self.increment_clock = 165 + self.ID_Offset
        self.decrement = 166 + self.ID_Offset
        self.decrement_clock = 167 + self.ID_Offset

        x,y,z = self.pos

        # logic
        blueprint.logic_gate(self.address_bus_output_enable,"or",(16 + x,6 + y,z),"up","right","0a3ee2")

        blueprint.logic_gate(self.transfer_bus_output_enable,"or",(16 + x,5 + y,z),"up","right","eeeeee")

        blueprint.logic_gate(self.decrement_clock,"nand",(16 + x,4 + y,z),"up","right","222222")
        blueprint.logic_gate(self.decrement,"or",(16 + x,3 + y,z),"up","right","222222")
        blueprint.addId(self.decrement,self.decrement_clock)

        blueprint.logic_gate(self.increment_clock,"and",(16 + x,2 + y,z),"up","right","eeeeee")
        blueprint.logic_gate(self.increment,"or",(16 + x,3 + y,z),"up","right","eeeeee")
        blueprint.addId(self.increment,self.increment_clock)

        blueprint.logic_gate(self.write_enable_clock,"and",(16 + x,1 + y,z),"up","right","19e753")
        blueprint.logic_gate(self.write_enable,"or",(16 + x,y,z),"up","right","19e753")
        blueprint.addId(self.write_enable,self.write_enable_clock)

        for i in range(16):
            # and gates address bus output
            blueprint.logic_gate(self.address_bus_output[i],"and",(i + x,6 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.address_bus_output_enable,self.address_bus_output[i])
            # and gates transfer bus output
            blueprint.logic_gate(self.transfer_bus_output[i],"and",(i + x,5 + y,z),"up","right","eeeeee")
            blueprint.addId(self.transfer_bus_output_enable,self.transfer_bus_output[i])
            # nor gates for decrement instruction
            blueprint.logic_gate(self.not_gate[i],"nor",(i + x,4 + y,z),"up","right","e2db13")
            blueprint.addId(self.not_gate[i],self.memcells[i])
            blueprint.addId(self.decrement_clock,self.not_gate[i])
            # xor gates for memory cells
            blueprint.logic_gate(self.memcells[i],"xor",(i + x,3 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.memcells[i],self.memcells[i])
            blueprint.addId(self.memcells[i],self.transfer_bus_input[i])
            blueprint.addId(self.memcells[i],self.transfer_bus_output[i])
            blueprint.addId(self.memcells[i],self.address_bus_output[i])
            blueprint.addId(self.decrement_clock,self.not_gate[i])

            # and gates for latch
            blueprint.logic_gate(self.latch[i],"and",(i + x,1 + y,z),"up","right","19e753")
            blueprint.addId(self.write_enable_clock,self.latch[i])
            blueprint.addId(self.latch[i],self.memcells[i])
            # xor for address bus input
            blueprint.logic_gate(self.transfer_bus_input[i],"xor",(i + x,y,z),"up","right","d02525")
            blueprint.addId(self.transfer_bus_input[i],self.latch[i])
        for i in range(16):
            # and gates for increment instruction
            for j in range(15 - i):
                blueprint.addId(self.memcells[15 - i],self.not_gate[j])

            blueprint.logic_gate(self.inc_and[i],"and",(i + x,2 + y,z),"up","right","eeeeee")
            blueprint.addId(self.inc_and[i],self.memcells[i])
            blueprint.addId(self.increment_clock,self.inc_and[i])
            # connections for increment instruction
            for j in range(15 - i):
                blueprint.addId(self.memcells[15 - i],self.inc_and[j])

class Bus:
    def __init__(self,blueprint,ID,bitness,pos,color):
        self.blueprint = blueprint

        self.ID_Offset = ID.claim_range(bitness)
        self.pos = pos
        self.color = color
        self.bitness = bitness

        self.Bus_IDS = []
        for id in range(self.bitness):
            self.Bus_IDS.append(id + self.ID_Offset)

        x,y,z = self.pos
        for i in range(self.bitness):
            self.blueprint.logic_gate(self.Bus_IDS[i],"or",(i + x,y,z),"up","right",color)

    def connect_to_bus(self,IDs):
        for i in range(len(IDs)):
            self.blueprint.addId(IDs[i],self.Bus_IDS[i])

    def connect_from_bus(self,IDs):
        print(IDs)
        for i in range(len(IDs)):
            if IDs[i] is not None:
                self.blueprint.addId(self.Bus_IDS[i],IDs[i])

class Transfer8Bit:
    def __init__(self,blueprint,ID,pos):
        self.blueprint = blueprint
        self.pos = pos
        self.ID_Offset = ID.claim_range(100)

        self.memcells = []
        self.transfer_bus_input = []
        self.transfer_bus_latch = []
        self.transfer_bus_output = []
        self.main_bus_input = []
        self.main_bus_latch = []
        self.main_bus_output = []
        for ID in range(8):
            self.memcells.append(ID + self.ID_Offset)
            self.transfer_bus_input.append(10 + ID + self.ID_Offset)
            self.transfer_bus_latch.append(20 + ID + self.ID_Offset)
            self.transfer_bus_output.append(30 + ID + self.ID_Offset)
            self.main_bus_input.append(40 + ID + self.ID_Offset)
            self.main_bus_latch.append(50 + ID + self.ID_Offset)
            self.main_bus_output.append(60 + ID + self.ID_Offset)

        self.main_bus_write_clock = 70 + self.ID_Offset
        self.transfer_bus_write_clock = 71 + self.ID_Offset
        self.main_bus_output_enable = 72 + self.ID_Offset
        self.transfer_bus_output_enable = 73 + self.ID_Offset

        self.main_bus_write_enable = 74 + self.ID_Offset
        self.transfer_bus_write_enable = 75 + self.ID_Offset
        x,y,z = pos

        # logic
        blueprint.logic_gate(self.main_bus_output_enable,"or",(8 + x,6 + y,z),"up","right","d02525")
        blueprint.logic_gate(self.transfer_bus_output_enable,"or",(8 + x,5 + y,z),"up","right","7f7f7f")
        blueprint.logic_gate(self.main_bus_write_enable,"or",(8 + x,3 + y,z),"up","right","d02525")
        blueprint.logic_gate(self.main_bus_write_clock,"and",(8 + x,2 + y,z),"up","right","d02525")
        blueprint.addId(self.main_bus_write_enable,self.main_bus_write_clock)
        blueprint.logic_gate(self.transfer_bus_write_enable,"or",(8 + x,1 + y,z),"up","right","7f7f7f")
        blueprint.logic_gate(self.transfer_bus_write_clock,"and",(8 + x,y,z),"up","right","7f7f7f")
        blueprint.addId(self.transfer_bus_write_enable,self.transfer_bus_write_clock)

        for i in range(8):
            # and gates for main bus output
            blueprint.logic_gate(self.main_bus_output[i],"and",(i + x,6 + y,z),"up","right","d02525")
            blueprint.addId(self.main_bus_output_enable,self.main_bus_output[i])
            # and gates for address bus output
            blueprint.logic_gate(self.transfer_bus_output[i],"and",(i + x,5 + y,z),"up","right","eeeeee")
            blueprint.addId(self.transfer_bus_output_enable,self.transfer_bus_output[i])
            # xor gates for memory cells
            blueprint.logic_gate(self.memcells[i],"xor",(i + x,4 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.memcells[i],self.memcells[i])
            blueprint.addId(self.memcells[i],self.transfer_bus_input[i])
            blueprint.addId(self.memcells[i],self.main_bus_input[i])
            blueprint.addId(self.memcells[i],self.transfer_bus_output[i])
            blueprint.addId(self.memcells[i],self.main_bus_output[i])
            # and gates for main bus latch
            blueprint.logic_gate(self.main_bus_latch[i],"and",(i + x,3 + y,z),"up","right","d02525")
            blueprint.addId(self.main_bus_latch[i],self.memcells[i])
            blueprint.addId(self.main_bus_write_clock,self.main_bus_latch[i])
            # and gates for address bus latch
            blueprint.logic_gate(self.transfer_bus_latch[i],"and",(i + x,2 + y,z),"up","right","eeeeee")
            blueprint.addId(self.transfer_bus_latch[i],self.memcells[i])
            blueprint.addId(self.transfer_bus_write_clock,self.transfer_bus_latch[i])
            # xor gates for main bus input
            blueprint.logic_gate(self.main_bus_input[i],"xor",(i + x,1 + y,z),"up","right","d02525")
            blueprint.addId(self.main_bus_input[i],self.main_bus_latch[i])
            # xor gates for address bus input
            blueprint.logic_gate(self.transfer_bus_input[i],"xor",(i + x,y,z),"up","right","eeeeee")
            blueprint.addId(self.transfer_bus_input[i],self.transfer_bus_latch[i])

class Fetch:
    def __init__(self,blueprint,ID,pos):
        self.blueprint = blueprint
        self.pos = pos
        self.ID_Offset = ID.claim_range(20)

        self.fetch_input = []
        self.fetch_output = []
        for ID in range(8):
            self.fetch_input.append(ID + self.ID_Offset)
            self.fetch_output.append(ID + 8 + self.ID_Offset)
        self.fetch_denied = 17 + self.ID_Offset

        x,y,z = pos

        # logic
        blueprint.logic_gate(self.fetch_denied,"nor",(8 + x,1 + y,z),"up","right","0a3ee2")
        for i in range(8):
            blueprint.logic_gate(self.fetch_output[i],"and",(i + x,1 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.fetch_denied,self.fetch_output[i])
            blueprint.logic_gate(self.fetch_input[i],"or",(i + x,y,z),"up","right","222222")
            blueprint.addId(self.fetch_input[i],self.fetch_output[i])

class PipeLine:
    def __init__(self,blueprint,ID,pos):
        self.blueprint = blueprint
        self.pos = pos
        self.ID_Offset = ID.claim_range(26)

        self.memcells = []
        self.latch = []
        self.input = []
        for ID in range(8):
            self.memcells.append(ID + self.ID_Offset)
            self.latch.append(ID + 8 + self.ID_Offset)
            self.input.append(ID + 16 + self.ID_Offset)

        self.clock = 25 + self.ID_Offset

        x,y,z = pos

        # logic
        blueprint.logic_gate(self.clock,"or",(8 + x,1 + y,z),"up","right","19e753")
        for i in range(8):
            blueprint.logic_gate(self.memcells[i],"xor",(i + x,2 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.memcells[i],self.memcells[i])
            blueprint.addId(self.memcells[i],self.input[i])
            blueprint.logic_gate(self.latch[i],"and",(i + x,1 + y,z),"up","right","19e753")
            blueprint.addId(self.latch[i],self.memcells[i])
            blueprint.addId(self.clock,self.latch[i])
            blueprint.logic_gate(self.input[i],"xor",(i + x,y,z),"up","right","d02525")
            blueprint.addId(self.input[i],self.latch[i])

class MemoryMap:
    def __init__(self,blueprint,ID,total_memory,chunk_size,bitness_in,pos,color):
        self.blueprint = blueprint
        self.ID = ID
        self.pos = pos
        self.color = color
        self.total_memory = total_memory
        self.chunk_size = chunk_size
        self.bitness_in = bitness_in

        self.input = []
        self.input_not = []
        for _ in range(self.bitness_in):
            self.input.append(ID.get_next())
            self.input_not.append(ID.get_next())

        posx,posy,posz = self.pos

        for x in range(bitness_in):
            blueprint.logic_gate(self.input[x],"or",(posx,x + posy,posz),"up","right","d02525")
            blueprint.logic_gate(self.input_not[x],"nor",(posx+1,x + posy,posz),"up","right","d02525")

        self.chunk_selectors = [self.ID.get_next() for _ in range(2**self.bitness_in)]


        count = 0
        for y in range(int(2 ** self.bitness_in/self.bitness_in)):
            for x in range(self.bitness_in):
                blueprint.logic_gate(self.chunk_selectors[count],"and",(y + posx+2,x + posy,posz),"up","right",color)

                mask = 1
                for i in range(self.bitness_in):
                    if count & mask == mask:
                        self.blueprint.addId(self.input[i],self.chunk_selectors[count])
                    else:
                        self.blueprint.addId(self.input_not[i],self.chunk_selectors[count])
                    mask = mask << 1
                count += 1

        self.input.reverse()
        self.input_not.reverse()

    def map(self,enables,chunk):
        for each in enables:
            self.blueprint.addId(self.chunk_selectors[chunk],each)


class Rom:
    def __init__(self,blueprint,ID,bitness_in,path,bitness_out,pos,color):
        self.blueprint = blueprint
        self.pos = pos
        self.color = color
        self.path = path
        self.bitness_in = bitness_in
        self.bitness_out = bitness_out
        self.ID = ID


        self.output = []
        for _ in range(self.bitness_out):
            self.output.append(ID.get_next())

        self.input = []
        self.input_not = []
        for _ in range(self.bitness_in):
            self.input.append(ID.get_next())
            self.input_not.append(ID.get_next())



        posx,posy,posz = self.pos

        for x in range(bitness_in):
            blueprint.logic_gate(self.input[x],"and",(posx,x + posy,posz),"up","right","d02525")
            blueprint.logic_gate(self.input_not[x],"nand",(posx+1,x + posy,posz),"up","right","d02525")

        for x in range(bitness_out):
            blueprint.logic_gate(self.output[x],"or",(2+posx + int(2 ** bitness_in / self.bitness_out),x + posy,posz),"up","right","0a3ee2")

        self.enables = (self.input+self.input_not+[ID.current_ID+1])

        with open(path,"r") as rom:
            lines = rom.read().splitlines()
            count = 0
            for y in range(int(2 ** bitness_in / self.bitness_out)):
                for x in range(len(self.output)):
                    blueprint.logic_gate(ID.get_next(),"and",(y + posx+2,x + posy,posz),"up","right",color)
                    data = 0
                    line = ""
                    if len(lines)>0:
                        line = lines.pop(0)
                    if line.isnumeric():
                        data = int(line)

                    mask = 1
                    for i in range(self.bitness_in):
                        if count & mask == mask:
                            self.blueprint.addId(self.input[i],self.ID.current_ID)
                        else:
                            self.blueprint.addId(self.input_not[i],self.ID.current_ID)
                        mask = mask << 1
                    mask = 1
                    for i in range(self.bitness_out):
                        if data & mask == mask:
                            self.blueprint.addId(self.ID.current_ID,self.output[i])
                        mask = mask << 1
                    count += 1
        self.output.reverse()
        self.input.reverse()
        self.input_not.reverse()




class LargeRom:
    def __init__(self,blueprint,ID,path,bitness_in,bitness_out,pos,color):
        self.blueprint = blueprint
        self.pos = pos
        self.color = color
        self.path = path
        self.bitness_in = bitness_in
        self.bitness_out = bitness_out
        self.ID_Offset = ID.claim_range(bitness_in * 2 + 2 ** bitness_in + bitness_out)

        self.output = []
        for ID in range(self.bitness_out):
            self.output.append(ID + 2 ** bitness_in + self.ID_Offset)

        self.input = []
        self.input_not = []
        for ID in range(self.bitness_in):
            self.input.append(ID + bitness_out + 2 ** bitness_in + self.ID_Offset)
            self.input_not.append(ID + bitness_in + bitness_out + 2 ** bitness_in + self.ID_Offset)
        posx,posy,posz = self.pos
        logic_id = self.ID_Offset
        with open(path,"r") as rom:
            for y in range(int(2 ** bitness_in / self.bitness_out)):
                for x in range(len(self.output)):
                    print(logic_id,2 ** bitness_in)
                    blueprint.logic_gate(logic_id,"and",(x + posx,y + posy + 2,posz),"up","right","ffffff")
                    line = rom.readline()
                    if line.isnumeric():
                        data = int(line)
                    else:
                        data = 0
                    mask = 1
                    for i in range(self.bitness_out):
                        if data & mask == mask:
                            print("connect")
                            blueprint.addId(logic_id,self.output[i])
                        mask = mask << 1
                    logic_id += 1

        mask = 1
        for x in range(bitness_in):
            blueprint.logic_gate(self.input[x],"or",(x + posx,posy,posz),"up","right","d02525")
            blueprint.logic_gate(self.input_not[x],"nor",(x + posx,1 + posy,+posz),"up","right","d02525")
            for ID in range(2 ** bitness_in):
                print(ID,2 ** bitness_in)
                if ID & mask == mask:
                    blueprint.addId(self.input[x],ID + self.ID_Offset)
                else:
                    blueprint.addId(self.input_not[x],ID + self.ID_Offset)
            mask = mask << 1

        for x in range(self.bitness_out):
            blueprint.logic_gate(self.output[x],"or",(x + posx,int(2 ** bitness_in / bitness_out) + posy + 2,posz),"up",
                                 "right","0a3ee2")

class Register:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.ID_Offset = ID.claim_range(4 * bitness + 3)

        self.memcells = []
        self.latch = []
        self.bus_input = []
        self.bus_output = []

        for ID in range(bitness):
            self.memcells.append(ID + self.ID_Offset)
            self.latch.append(ID + bitness + self.ID_Offset)
            self.bus_input.append(ID + bitness * 2 + self.ID_Offset)
            self.bus_output.append(ID + bitness * 3 + self.ID_Offset)

        self.write_enable = 4 * bitness + 1 + self.ID_Offset
        self.clock = 4 * bitness + 2 + self.ID_Offset
        self.bus_output_enable = 4 * bitness + 3 + self.ID_Offset

        x,y,z = pos

        blueprint.logic_gate(self.write_enable,"or",(8 + x,2 + y,z),"up","right","19e753")
        blueprint.logic_gate(self.clock,"and",(8 + x,1 + y,z),"up","right","19e753")
        blueprint.addId(self.write_enable,self.clock)
        blueprint.logic_gate(self.bus_output_enable,"or",(8 + x,3 + y,z),"up","right","eeeeee")

        for i in range(bitness):
            # and main bus out
            blueprint.logic_gate(self.bus_output[i],"and",(i + x,3 + y,z),"up","right","eeeeee")
            blueprint.addId(self.bus_output_enable,self.bus_output[i])
            # xor memory cells
            blueprint.logic_gate(self.memcells[i],"xor",(x + i,2 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.memcells[i],self.memcells[i])
            blueprint.addId(self.memcells[i],self.bus_input[i])
            blueprint.addId(self.memcells[i],self.bus_output[i])
            # and gates for latch
            blueprint.logic_gate(self.latch[i],"and",(i + x,1 + y,z),"up","right","19e753")
            blueprint.addId(self.clock,self.latch[i])
            blueprint.addId(self.latch[i],self.memcells[i])
            # xor gates for input
            blueprint.logic_gate(self.bus_input[i],"xor",(i + x,y,z),"up","right","d02525")
            blueprint.addId(self.bus_input[i],self.latch[i])

class RegisterNoOutput:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.ID_Offset = ID.claim_range(3 * bitness + 2)

        self.memcells = []
        self.latch = []
        self.bus_input = []

        for ID in range(bitness):
            self.memcells.append(ID + self.ID_Offset)
            self.latch.append(ID + bitness + self.ID_Offset)
            self.bus_input.append(ID + bitness * 2 + self.ID_Offset)

        self.write_enable = 3 * bitness + 1 + self.ID_Offset
        self.clock = 3 * bitness + 2 + self.ID_Offset

        x,y,z = pos

        blueprint.logic_gate(self.write_enable,"or",(bitness + x,2 + y,z),"up","right","19e753")
        blueprint.logic_gate(self.clock,"and",(bitness + x,1 + y,z),"up","right","19e753")
        blueprint.addId(self.write_enable,self.clock)

        for i in range(bitness):
            # xor memory cells
            blueprint.logic_gate(self.memcells[i],"xor",(x + i,2 + y,z),"up","right","0a3ee2")
            blueprint.addId(self.memcells[i],self.memcells[i])
            blueprint.addId(self.memcells[i],self.bus_input[i])
            # and gates for latch
            blueprint.logic_gate(self.latch[i],"and",(i + x,1 + y,z),"up","right","19e753")
            blueprint.addId(self.clock,self.latch[i])
            blueprint.addId(self.latch[i],self.memcells[i])
            # xor gates for input
            blueprint.logic_gate(self.bus_input[i],"xor",(i + x,y,z),"up","right","d02525")
            blueprint.addId(self.bus_input[i],self.latch[i])

class Bitwise:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.ID_Offset = ID.claim_range(7 * bitness + 7)
        self.bitness = bitness
        self.pos = pos

        self.or_ctrl = self.ID_Offset
        self.and_ctrl = self.ID_Offset + 1
        self.xor_ctrl = self.ID_Offset + 2
        self.nor_ctrl = self.ID_Offset + 3
        self.pass_ctrl = self.ID_Offset + 4
        self.fill_ctrl = self.ID_Offset + 5
        self.carry_ctrl = self.ID_Offset + 6

        self.or_gates = []
        self.or_and_gates = []
        self.and_gates = []
        self.xor_gates = []
        self.xor_and_gates = []
        self.nor_gates = []
        self.pass_gates = []
        for i in range(bitness):
            self.or_gates.append(7 + i + self.ID_Offset)
            self.or_and_gates.append(7 + i + self.ID_Offset + bitness * 1)
            self.and_gates.append(7 + i + self.ID_Offset + bitness * 2)
            self.xor_gates.append(7 + i + self.ID_Offset + bitness * 3)
            self.xor_and_gates.append(7 + i + self.ID_Offset + bitness * 4)
            self.nor_gates.append(7 + i + self.ID_Offset + bitness * 5)
            self.pass_gates.append(7 + i + self.ID_Offset + bitness * 6)

        x,y,z = pos
        blueprint.logic_gate(self.fill_ctrl,"or",(bitness + x,6 + y,z),"up","right","cf11d2")
        blueprint.logic_gate(self.or_ctrl,"or",(bitness + x,5 + y,z),"up","right","cf11d2")
        blueprint.logic_gate(self.and_ctrl,"or",(bitness + x,4 + y,z),"up","right","cf11d2")
        blueprint.logic_gate(self.carry_ctrl,"or",(bitness + x,3 + y,z),"up","right","cf11d2")
        blueprint.logic_gate(self.xor_ctrl,"or",(bitness + x,2 + y,z),"up","right","cf11d2")
        blueprint.logic_gate(self.nor_ctrl,"nor",(bitness + x,1 + y,z),"up","right","cf11d2")
        blueprint.logic_gate(self.pass_ctrl,"or",(bitness + x,y,z),"up","right","cf11d2")

        for i in range(bitness):
            blueprint.logic_gate(self.or_gates[i],"or",(i + x,6 + y,z),"up","right","cf11d2")
            blueprint.logic_gate(self.or_and_gates[i],"and",(i + x,5 + y,z),"up","right","cf11d2")

            blueprint.addId(self.or_gates[i],self.or_and_gates[i])
            blueprint.addId(self.or_ctrl,self.or_and_gates[i])
            blueprint.logic_gate(self.and_gates[i],"and",(i + x,4 + y,z),"up","right","cf11d2")
            blueprint.addId(self.and_ctrl,self.and_gates[i])
            blueprint.logic_gate(self.xor_gates[i],"xor",(i + x,3 + y,z),"up","right","cf11d2")
            blueprint.logic_gate(self.xor_and_gates[i],"and",(i + x,2 + y,z),"up","right","cf11d2")
            blueprint.addId(self.xor_gates[i],self.xor_and_gates[i])
            blueprint.addId(self.xor_ctrl,self.xor_and_gates[i])
            blueprint.logic_gate(self.nor_gates[i],"nor",(i + x,1 + y,z),"up","right","cf11d2")
            blueprint.addId(self.nor_ctrl,self.nor_gates[i])
            blueprint.logic_gate(self.pass_gates[i],"and",(i + x,y,z),"up","right","cf11d2")
            blueprint.addId(self.pass_ctrl,self.pass_gates[i])

    def connect(self,bus1,bus2):
        for i in range(self.bitness):
            self.blueprint.addId(bus1[i],self.or_gates[i])
            self.blueprint.addId(bus1[i],self.and_gates[i])
            self.blueprint.addId(bus1[i],self.xor_gates[i])
            self.blueprint.addId(bus1[i],self.nor_gates[i])
            self.blueprint.addId(bus1[i],self.pass_gates[i])

            self.blueprint.addId(bus2[i],self.or_gates[i])
            self.blueprint.addId(bus2[i],self.and_gates[i])
            self.blueprint.addId(bus2[i],self.xor_gates[i])

    def register(self,bitwise_reg):
        for i in range(self.bitness):
            self.blueprint.addId(self.or_and_gates[i],bitwise_reg.bus_input[i])
            self.blueprint.addId(self.and_gates[i],bitwise_reg.bus_input[i])
            self.blueprint.addId(self.xor_and_gates[i],bitwise_reg.bus_input[i])
            self.blueprint.addId(self.nor_gates[i],bitwise_reg.bus_input[i])
            self.blueprint.addId(self.pass_gates[i],bitwise_reg.bus_input[i])
            self.blueprint.addId(self.fill_ctrl,bitwise_reg.bus_input[i])
        self.blueprint.addId(self.carry_ctrl,bitwise_reg.bus_input[-1])

class Shift:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.bitness = bitness
        self.pos = pos

        self.shr_ctrl = ID.get_next()
        self.shl_ctrl = ID.get_next()
        self.pass_ctrl = ID.get_next()

        self.shr_gates = []
        self.shl_gates = []
        self.pass_gates = []
        for i in range(self.bitness):
            self.shr_gates.append(ID.get_next())
            self.shl_gates.append(ID.get_next())
            self.pass_gates.append(ID.get_next())

        x,y,z = pos
        blueprint.logic_gate(self.shr_ctrl,"or",(self.bitness + x,2 + y,z),"up","right","2ce6e6")
        blueprint.logic_gate(self.shl_ctrl,"or",(self.bitness + x,1 + y,z),"up","right","2ce6e6")
        blueprint.logic_gate(self.pass_ctrl,"or",(self.bitness + x,y,z),"up","right","2ce6e6")

        for i in range(self.bitness):
            blueprint.logic_gate(self.shr_gates[i],"and",(i + x,2 + y,z),"up","right","2ce6e6")
            blueprint.addId(self.shr_ctrl,self.shr_gates[i])

            blueprint.logic_gate(self.shl_gates[i],"and",(i + x,1 + y,z),"up","right","2ce6e6")
            blueprint.addId(self.shl_ctrl,self.shl_gates[i])

            blueprint.logic_gate(self.pass_gates[i],"and",(i + x,y,z),"up","right","2ce6e6")
            blueprint.addId(self.pass_ctrl,self.pass_gates[i])

    def connect(self,bus1):
        for i in range(len(bus1)):
            self.blueprint.addId(bus1[i],self.shr_gates[i])
            self.blueprint.addId(bus1[i],self.shl_gates[i])
            self.blueprint.addId(bus1[i],self.pass_gates[i])

    def register(self,shift_reg):
        shift_left = self.shl_gates[1:] + [self.shl_gates[0]]
        shift_right = [self.shr_gates[-1]]+self.shr_gates[:-1]
        shift_pass = self.pass_gates

        for i in range(self.bitness):
            self.blueprint.addId(shift_left[i],shift_reg.bus_input[i])
            self.blueprint.addId(shift_right[i],shift_reg.bus_input[i])
            self.blueprint.addId(shift_pass[i],shift_reg.bus_input[i])

    def carry(self,carry_id):
        self.blueprint.addId(carry_id,self.pass_gates[-1])
        self.blueprint.addId(carry_id,self.shr_gates[-1])
        self.blueprint.addId(carry_id,self.shl_gates[-1])

class CLA:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.ID = ID
        self.bitness = bitness
        self.pos = pos

        self.output_enable = ID.get_next()

        self.output = []
        self.in_nor = []
        self.in_nand = []
        self.out_xor = []
        self.out_and = []
        self.out_nor1 = []
        self.out_nor2 = []

        self.carry = ID.get_next()
        self.carry_or = ID.get_next()
        self.carry_nor = ID.get_next()
        self.carry_gates = []

        for i in range(bitness):
            self.output.append(ID.get_next())
            self.in_nor.append(ID.get_next())
            self.in_nand.append(ID.get_next())
            self.out_xor.append(ID.get_next())
            self.out_and.append(ID.get_next())
            self.out_nor1.append(ID.get_next())
            self.out_nor2.append(ID.get_next())
            self.carry_gates.append(ID.get_next())


        self.OverFlow = ID.get_next()
        self.OF_Xor_A = ID.get_next()
        self.OF_Xor_B = ID.get_next()

        self.Zero_flag = ID.get_next()

        x,y,z = pos

        blueprint.logic_gate(self.carry,"nor",(bitness + x,3 + y,z),"up","right","e2db13")
        blueprint.logic_gate(self.carry_or,"or",(bitness + x,5 + bitness + y,z),"up","right","e2db13")
        blueprint.addId(self.carry_or,self.carry_nor)
        blueprint.logic_gate(self.carry_nor,"nor",(bitness + x,4 + bitness + y,z),"up","right","e2db13")
        blueprint.addId(self.carry_nor,self.out_nor1[0])
        blueprint.logic_gate(self.output_enable,"or",(bitness+x,y,z),"up","right","0a3ee2")

        blueprint.logic_gate(self.Zero_flag,"nor",(bitness - 4 + x,6 + y,z),"up","right","222222")

        for i in range(bitness):
            blueprint.logic_gate(self.in_nor[i],"nor",(bitness - i + x - 1,5 + bitness + y,z),"up","right","e2db13")
            blueprint.logic_gate(self.in_nand[i],"nand",(bitness - i + x - 1,4 + bitness + y,z),"up","right","e2db13")
            blueprint.logic_gate(self.out_nor1[i],"nor",(bitness - i + x - 1,4 + y,z),"up","right","e2db13")
            blueprint.logic_gate(self.out_nor2[i],"nor",(bitness - i + x - 1,3 + y,z),"up","right","e2db13")
            blueprint.logic_gate(self.out_and[i],"and",(bitness - i + x - 1,2 + y,z),"up","right","e2db13")
            blueprint.logic_gate(self.out_xor[i],"xor",(bitness - i + x - 1,1 + y,z),"up","right","e2db13")
            blueprint.logic_gate(self.output[i],"and",(i + x,y,z),"up","right","0a3ee2")
            blueprint.logic_gate(self.carry_gates[i],"and",(bitness + x,3 + bitness + y - i,z),"up","right","e2db13")

            for j in range(i):
                j += 1
                blueprint.logic_gate(ID.get_next(),"and",(bitness - i + x - 1,4 + bitness - j + y,z),"up","right","e2db13")
                blueprint.addId(ID.current_ID,self.out_nor1[i])
                blueprint.addId(self.in_nand[i],self.carry_gates[j])
                if j == 1:
                    blueprint.addId(self.carry_nor,ID.current_ID)

                for k in range(bitness):
                    if k + 1 >= j:
                        if k != i:
                            blueprint.addId(self.in_nand[k],ID.current_ID)

                for l in range(bitness):
                    l += 1
                    if j == l + 1:
                        if l >= 1:
                            pass
                            blueprint.addId(self.in_nor[l - 1],ID.current_ID)

            if i < bitness - 1:
                blueprint.addId(self.in_nor[i],self.out_nor1[i + 1])
                blueprint.addId(self.in_nor[i],self.carry_gates[i + 1])

            blueprint.addId(self.output_enable,self.output[i])
            blueprint.addId(self.out_xor[i],self.output[-i-1])
            blueprint.addId(self.in_nand[i],self.out_and[i])
            blueprint.addId(self.in_nor[i],self.out_nor2[i])
            blueprint.addId(self.out_nor1[i],self.out_xor[i])
            blueprint.addId(self.out_nor2[i],self.out_and[i])
            blueprint.addId(self.out_and[i],self.out_xor[i])
            blueprint.addId(self.carry_gates[i],self.carry)
            blueprint.addId(self.in_nand[i],self.carry_gates[0])
            blueprint.addId(self.out_xor[i],self.Zero_flag)

        blueprint.addId(self.in_nor[-1],self.carry)

        self.carry_loop_and = ID.get_next()
        self.carry_loop_or = ID.get_next()

        blueprint.logic_gate(self.OF_Xor_A,"xor",(bitness - 2 + x,6 + y,z),"up","right","222222")
        blueprint.logic_gate(self.OF_Xor_B,"xor",(bitness - 2 + x, 7 + y,z),"up","right","222222")
        blueprint.logic_gate(self.OverFlow,"and",(bitness - 2 + x, 8 + y,z),"up","right","222222")
        blueprint.addId(self.out_xor[-1],self.OF_Xor_A)
        blueprint.addId(self.OF_Xor_A,self.OverFlow)
        blueprint.addId(self.out_xor[-1],self.OF_Xor_B)
        blueprint.addId(self.OF_Xor_B,self.OverFlow)

        blueprint.logic_gate(self.carry_loop_or,"or",(bitness - 3 + x, 6+ y,z),"up","right","222222")
        blueprint.logic_gate(self.carry_loop_and,"and",(bitness - 3 + x, 7+ y,z),"up","right","222222")
        blueprint.addId(self.carry,self.carry_loop_and)
        blueprint.addId(self.carry_loop_or,self.carry_loop_and)



    def connect(self,lhs,rhs):
        for i in range(self.bitness):
            self.blueprint.addId(lhs[i],self.in_nand[-i - 1])
            self.blueprint.addId(lhs[i],self.in_nor[-i - 1])
            self.blueprint.addId(rhs[i],self.in_nand[-i - 1])
            self.blueprint.addId(rhs[i],self.in_nor[-i - 1])
        self.blueprint.addId(lhs[-1],self.carry_or)
        self.blueprint.addId(rhs[-1],self.carry_or)
        self.blueprint.addId(lhs[-2],self.OF_Xor_A)
        self.blueprint.addId(rhs[-2],self.OF_Xor_B)

class MemoryBridge:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.ID = ID
        self.bitness = bitness
        self.pos = pos

        self.main_data_enable = ID.get_next()
        self.data_main_enable = ID.get_next()

        self.main_data = []
        self.data_main = []

        for i in range(bitness):
            self.main_data.append(ID.get_next())
            self.data_main.append(ID.get_next())

        x,y,z = pos
        blueprint.logic_gate(self.main_data_enable,"or",(bitness + x,y,z),"up","right","0a3ee2")
        blueprint.logic_gate(self.data_main_enable,"or",(bitness + x,y+1,z),"up","right","0a3ee2")
        for i in range(bitness):
            blueprint.logic_gate(self.main_data[i],"and",(i + x,y,z),"up","right","0a3ee2")
            blueprint.logic_gate(self.data_main[i],"and",(i + x,y+1,z),"up","right","0a3ee2")
            blueprint.addId(self.main_data_enable,self.main_data[i])
            blueprint.addId(self.data_main_enable,self.data_main[i])

class OpCodes:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.ID = ID
        self.bitness = bitness
        self.flags = {}
        self.pos = pos
        self.control_lines = {}
        self.Opcodes = {}

    def Add_control_line(self,name,ID):
        self.control_lines[name] = ID

    def Add_flags(self,name,ID):
        self.flags[name] = ID

    def createOpcodes(self):
        self.Opcodes["No_operation"] = [[0],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[]]

        self.Opcodes["Move_A_Constant"] = [[1],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load_Fetch,oc.Fetch_Denied],[oc.Constant_Assert_Main_Bus,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["Move_B_Constant"] = [[2],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load_Fetch,oc.Fetch_Denied],[oc.Constant_Assert_Main_Bus,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["Move_C_Constant"] = [[3],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load_Fetch,oc.Fetch_Denied],[oc.Constant_Assert_Main_Bus,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["Move_D_Constant"] = [[4],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load_Fetch,oc.Fetch_Denied],[oc.Constant_Assert_Main_Bus,oc.GPR_D_Load_Main_Bus]]
        self.Opcodes["Move_TL_Constant"] = [[5],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load_Fetch,oc.Fetch_Denied],[oc.Constant_Assert_Main_Bus,oc.Transfer_RHS_Load_Main_Bus]]
        self.Opcodes["Move_TH_Constant"] = [[6],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load_Fetch,oc.Fetch_Denied],[oc.Constant_Assert_Main_Bus,oc.Transfer_LHS_Load_Main_Bus]]

        self.Opcodes["Move_B_into_A"] = [[7],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_B_Assert_Main_Bus,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["Move_C_into_A"] = [[8],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["Move_D_into_A"] = [[9],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_D_Assert_Main_Bus,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_A"] = [[10],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_RHS_Assert_Main_Bus,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_A"] = [[11],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Main_Bus,oc.GPR_A_Load_Main_Bus]]

        self.Opcodes["Move_A_into_B"] = [[12],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_A_Assert_Main_Bus,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["Move_C_into_B"] = [[13],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["Move_D_into_B"] = [[14],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_D_Assert_Main_Bus,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_B"] = [[15],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_RHS_Assert_Main_Bus,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_B"] = [[16],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Main_Bus,oc.GPR_B_Load_Main_Bus]]

        self.Opcodes["Move_A_into_C"] = [[17],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_B_Assert_Main_Bus,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["Move_B_into_C"] = [[18],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["Move_D_into_C"] = [[19],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_D_Assert_Main_Bus,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_C"] = [[20],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_RHS_Assert_Main_Bus,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_C"] = [[21],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Main_Bus,oc.GPR_C_Load_Main_Bus]]

        self.Opcodes["Move_A_into_D"] = [[22],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_A_Assert_Main_Bus,oc.GPR_D_Load_Main_Bus]]
        self.Opcodes["Move_B_into_D"] = [[23],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_B_Assert_Main_Bus,oc.GPR_D_Load_Main_Bus]]
        self.Opcodes["Move_C_into_D"] = [[24],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.GPR_D_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_D"] = [[25],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_RHS_Assert_Main_Bus,oc.GPR_D_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_D"] = [[26],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Main_Bus,oc.GPR_D_Load_Main_Bus]]

        self.Opcodes["Move_A_into_TL"] = [[27],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_A_Assert_Main_Bus,oc.Transfer_RHS_Load_Main_Bus]]
        self.Opcodes["Move_B_into_TL"] = [[28],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_B_Assert_Main_Bus,oc.Transfer_RHS_Load_Main_Bus]]
        self.Opcodes["Move_C_into_TL"] = [[29],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.Transfer_RHS_Load_Main_Bus]]
        self.Opcodes["Move_D_into_TL"] = [[30],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_D_Assert_Main_Bus,oc.Transfer_RHS_Load_Main_Bus]]

        self.Opcodes["Move_A_into_TH"] = [[31],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_A_Assert_Main_Bus,oc.Transfer_LHS_Load_Main_Bus]]
        self.Opcodes["Move_B_into_TH"] = [[32],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_B_Assert_Main_Bus,oc.Transfer_LHS_Load_Main_Bus]]
        self.Opcodes["Move_C_into_TH"] = [[33],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.Transfer_LHS_Load_Main_Bus]]
        self.Opcodes["Move_D_into_TH"] = [[34],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_D_Assert_Main_Bus,oc.Transfer_LHS_Load_Main_Bus]]

        self.Opcodes["Move_A_into_si"] = [[35],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_A_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]
        self.Opcodes["Move_B_into_si"] = [[36],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_B_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]
        self.Opcodes["Move_C_into_si"] = [[37],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]
        self.Opcodes["Move_D_into_si"] = [[38],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_D_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]

        self.Opcodes["Move_A_into_di"] = [[39],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_A_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]
        self.Opcodes["Move_B_into_di"] = [[40],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_B_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]
        self.Opcodes["Move_C_into_di"] = [[41],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_C_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]
        self.Opcodes["Move_D_into_di"] = [[42],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.GPR_D_Assert_Main_Bus,oc.Fetch_Denied,oc.memory_bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]

        self.Opcodes["Move_tx_into_ra"] = [[51],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Transfer_Bus,oc.Transfer_RHS_Assert_Transfer_Bus,oc.Return_Address_Load_Transfer_Bus]]
        self.Opcodes["Move_ra_into_tx"] = [[52],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Return_Address_Assert_Transfer_Bus,oc.Transfer_LHS_Load_Transfer_Bus,oc.Transfer_RHS_Load_Transfer_Bus]]
        self.Opcodes["Move_tx_into_sp"] = [[53],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Transfer_Bus,oc.Transfer_RHS_Assert_Transfer_Bus,oc.Stack_Pointer_Load_Transfer_Bus]]
        self.Opcodes["Move_sp_into_tx"] = [[54],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Stack_Pointer_Assert_Transfer_Bus,oc.Transfer_LHS_Load_Transfer_Bus,oc.Transfer_RHS_Load_Main_Bus]]
        self.Opcodes["Move_tx_into_si"] = [[55],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Transfer_Bus,oc.Transfer_RHS_Assert_Transfer_Bus,oc.Source_Index_Load_Transfer_Bus]]
        self.Opcodes["Move_si_into_tx"] = [[56],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Source_Index_Assert_Transfer_Bus,oc.Transfer_LHS_Load_Transfer_Bus,oc.Transfer_RHS_Load_Transfer_Bus]]
        self.Opcodes["Move_tx_into_di"] = [[57],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Transfer_LHS_Assert_Transfer_Bus,oc.Transfer_RHS_Assert_Transfer_Bus,oc.Destination_Index_Load_Transfer_Bus]]
        self.Opcodes["Move_di_into_tx"] = [[58],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Destination_Index_Assert_Transfer_Bus,oc.Transfer_LHS_Load_Transfer_Bus,oc.Transfer_RHS_Load_Transfer_Bus]]
        self.Opcodes["Move_si_into_di"] = [[59],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Source_Index_Assert_Transfer_Bus,oc.Destination_Index_Load_Transfer_Bus]]
        self.Opcodes["Move_di_into_si"] = [[60],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Destination_Index_Assert_Transfer_Bus,oc.Source_Index_Load_Transfer_Bus]]
        self.Opcodes["Move_sp_into_si"] = [[61],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Stack_Pointer_Assert_Transfer_Bus,oc.Source_Index_Load_Transfer_Bus]]
        self.Opcodes["Move_sp_into_di"] = [[62],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Stack_Pointer_Assert_Transfer_Bus,oc.Destination_Index_Load_Transfer_Bus]]

        self.Opcodes["Increment_sp"] = [[63],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Stack_Pointer_Increment]]
        self.Opcodes["Increment_si"] = [[64],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Source_Index_Increment]]
        self.Opcodes["Increment_di"] = [[65],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Destination_Index_Increment]]

        self.Opcodes["Decrement_ra"] = [[66],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Return_Address_Decrement],[]]
        self.Opcodes["Decrement_sp"] = [[67],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Stack_Pointer_Decrement],[]]
        self.Opcodes["Decrement_si"] = [[68],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Source_Index_Decrement],[]]
        self.Opcodes["Decrement_di"] = [[69],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Destination_Index_Decrement],[]]

        self.Opcodes["call_tx"] = [[70],[],[]]
        self.Opcodes["call_di"] = [[71],[],[]]
        self.Opcodes["return"] = [[72],[],[]]

        jump = [oc.Transfer_LHS_Assert_Transfer_Bus,oc.Transfer_RHS_Assert_Transfer_Bus,oc.Program_Counter_Load_Transfer_Bus,oc.Fetch_Denied]

        self.Opcodes["Jump_tx"] = [[73],[oc.Transfer_LHS_Assert_Transfer_Bus,oc.Transfer_RHS_Assert_Transfer_Bus,oc.Program_Counter_Load_Transfer_Bus],[]]
        self.Opcodes["Jump_di"] = [[74],[oc.Destination_Index_Assert_Transfer_Bus,oc.Program_Counter_Load_Transfer_Bus],[]]

        self.Opcodes["jo_tx"] = [[75,(oc.ALU_Over_Flow_flag,True)],jump,[]]
        self.Opcodes["jno_di"] = [[76,(oc.ALU_Over_Flow_flag,False)],jump,[]]
        self.Opcodes["js_tx"] = [[77,(oc.ALU_sign_flag,True)],jump,[]]
        self.Opcodes["jns_tx"] = [[78,(oc.ALU_sign_flag,False)],jump,[]]
        self.Opcodes["jz_tx"] = [[79,(oc.ALU_Zero_flag,True)],jump,[]]
        self.Opcodes["jnz_tx"] = [[80,(oc.ALU_Zero_flag,False)],jump,[]]
        #self.Opcodes["je_tx"] = [[79,(oc.ALU_Zero_flag,True)],jump,[]]
        #self.Opcodes["jne_tx"] = [[80,(oc.ALU_Zero_flag,False)],jump,[]]

        self.Opcodes["jump_Arithmetic_Carry"] = [[81,(oc.Arithmetic_Carry_flag,True)],jump,[]]
        self.Opcodes["jump_not_Arithmetic_Carry"] = [[82,(oc.Arithmetic_Carry_flag,False)],jump,[]]
        self.Opcodes["jump_Carry_Or_Zero"] = [[83,(oc.Arithmetic_Carry_flag,True)],jump,[]]
        #self.Opcodes["jump_Carry_Or_Zero"] = [[83,(oc.ALU_Zero_flag,True)],jump,[]]
        self.Opcodes["jump_Not_Carry_And_Not_Zero"] = [[84,(oc.Arithmetic_Carry_flag,False),(oc.ALU_Zero_flag,False)],jump,[]]

        self.Opcodes["jump_Sign_Not_Equal_Overflow"] = [[85,(oc.ALU_sign_flag,False),(oc.ALU_sign_flag,True)],jump,[]]
        #self.Opcodes["jump_Sign_Not_Equal_Overflow"] = [[85,(oc.ALU_sign_flag,True),(oc.ALU_sign_flag,False)],jump,[]]
        self.Opcodes["jump_Sign_Equal_Overflow"] = [[86,(oc.ALU_sign_flag,True),(oc.ALU_sign_flag,True)],jump,[]]
        #self.Opcodes["jump_Sign_Equal_Overflow"] = [[86,(oc.ALU_sign_flag,False),(oc.ALU_sign_flag,False)],jump,[]]
        self.Opcodes["jump_Zero_Or_Sign_Equal_Overflow"] = [[87,(oc.ALU_Zero_flag,True),(oc.ALU_sign_flag,True),(oc.ALU_sign_flag,True)],jump,[]]
        #self.Opcodes["jump_Zero_Or_Sign_Equal_Overflow"] = [[87,(oc.ALU_Zero_flag,True),(oc.ALU_sign_flag,False),(oc.ALU_sign_flag,False)],jump,[]]
        self.Opcodes["jump_Not_Zero_Or_Sign_Equal_Overflow"] = [[88,(oc.ALU_Zero_flag,False),(oc.ALU_sign_flag,True),(oc.ALU_sign_flag,True)],jump,[]]
        #self.Opcodes["jump_Not_Zero_Or_Sign_Equal_Overflow"] = [[88,(oc.ALU_Zero_flag,False),(oc.ALU_sign_flag,False),(oc.ALU_sign_flag,False)],jump,[]]

        self.Opcodes["jlc_tx"] = [[89,(oc.Logic_Carry_flag,True)],jump,[]]
        self.Opcodes["jnlc_tx"] = [[90,(oc.Logic_Carry_flag,False)],jump,[]]



        self.Opcodes["push_a"] = [[91],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Main_Data,oc.GPR_A_Assert_Main_Bus,oc.Ram_Write],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_b"] = [[92],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Main_Data,oc.GPR_B_Assert_Main_Bus,oc.Ram_Write],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_c"] = [[93],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Main_Data,oc.GPR_C_Assert_Main_Bus,oc.Ram_Write],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_d"] = [[94],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Main_Data,oc.GPR_D_Assert_Main_Bus,oc.Ram_Write],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_tl"] = [[95],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Main_Data,oc.Transfer_RHS_Assert_Main_Bus,oc.Ram_Write],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_th"] = [[96],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Main_Data,oc.Transfer_LHS_Assert_Main_Bus,oc.Ram_Write],[oc.Stack_Pointer_Increment]]

        self.Opcodes["pop_a"] = [[97],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Data_Main,oc.Ram_Read,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["pop_b"] = [[98],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Data_Main,oc.Ram_Read,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["pop_c"] = [[99],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Data_Main,oc.Ram_Read,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["pop_d"] = [[100],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Data_Main,oc.Ram_Read,oc.GPR_D_Load_Main_Bus]]
        self.Opcodes["pop_tl"] = [[101],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Data_Main,oc.Ram_Read,oc.Transfer_RHS_Load_Main_Bus]]
        self.Opcodes["pop_th"] = [[102],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.memory_bridge_Data_Main,oc.Ram_Read,oc.Transfer_LHS_Load_Main_Bus]]

        self.Opcodes["break"] = [[103],[],[]]

        self.Opcodes["Move_Di_IO_A"] = [[104],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_A_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_B"] = [[105],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_B_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_C"] = [[106],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_C_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_D"] = [[107],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_D_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_Constant"] = [[108],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Write,oc.Constant_Assert_Main_Bus]]

        self.Opcodes["Move_Di_A_IO"] = [[109],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["Move_Di_B_IO"] = [[110],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["Move_Di_C_IO"] = [[111],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["Move_Di_D_IO"] = [[112],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_D_Load_Main_Bus]]

        self.Opcodes["Move_Si_IO_A"] = [[113],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_A_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_B"] = [[114],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_B_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_C"] = [[115],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_C_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_D"] = [[116],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Write,oc.GPR_D_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_Constant"] = [[117],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Write,oc.Constant_Assert_Main_Bus]]

        self.Opcodes["Move_Si_A_IO"] = [[118],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_A_Load_Main_Bus]]
        self.Opcodes["Move_Si_B_IO"] = [[119],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_B_Load_Main_Bus]]
        self.Opcodes["Move_Si_C_IO"] = [[120],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_C_Load_Main_Bus]]
        self.Opcodes["Move_Si_D_IO"] = [[121],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Read,oc.GPR_D_Load_Main_Bus]]






        # ALU operations

        # ADD
        self.Opcodes["add_B_to_A"] = [[128],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_C_to_A"] = [[129],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_D_to_A"] = [[130],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["add_A_to_B"] = [[131],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_C_to_B"] = [[132],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_D_to_B"] = [[133],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["add_A_to_C"] = [[134],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_B_to_C"] = [[135],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_D_to_C"] = [[136],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["add_A_to_D"] = [[137],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_B_to_D"] = [[138],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_C_to_D"] = [[139],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Add with carry
        self.Opcodes["add_B_to_A_Carry"] = [[140],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_C_to_A_Carry"] = [[141],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_D_to_A_Carry"] = [[142],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["add_A_to_B_Carry"] = [[143],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_C_to_B_Carry"] = [[144],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_D_to_B_Carry"] = [[145],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["add_A_to_C_Carry"] = [[146],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_B_to_C_Carry"] = [[147],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_D_to_C_Carry"] = [[148],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["add_A_to_D_Carry"] = [[149],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_B_to_D_Carry"] = [[150],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["add_C_to_D_Carry"] = [[151],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Subtract
        self.Opcodes["sub_B_from_A"] = [[152],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_C_from_A"] = [[153],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_D_from_A"] = [[154],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["sub_A_from_B"] = [[155],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_C_from_B"] = [[156],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_D_from_B"] = [[157],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["sub_A_from_C"] = [[158],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_B_from_C"] = [[159],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_D_from_C"] = [[160],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["sub_A_from_D"] = [[161],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_B_from_D"] = [[162],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_C_from_D"] = [[163],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Subtract with borrow
        self.Opcodes["sub_B_from_A_Borrow"] = [[164],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_C_from_A_Borrow"] = [[165],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_D_from_A_Borrow"] = [[166],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["sub_A_from_B_Borrow"] = [[167],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_C_from_B_Borrow"] = [[168],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_D_from_B_Borrow"] = [[169],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["sub_A_from_C_Borrow"] = [[170],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_B_from_C_Borrow"] = [[171],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_D_from_C_Borrow"] = [[172],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["sub_A_from_D_Borrow"] = [[173],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_B_from_D_Borrow"] = [[174],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["sub_C_from_D_Borrow"] = [[175],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Shift left
        self.Opcodes["Shift_Left_A"] = [[176],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Shift_Left_B"] = [[177],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Shift_Left_C"] = [[178],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Shift_Left_D"] = [[179],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Shift Right
        self.Opcodes["Shift_Right_A"] = [[180],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Shift_Right_B"] = [[181],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Shift_Right_C"] = [[182],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Shift_Right_D"] = [[183],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Increments
        self.Opcodes["Increment_A"] = [[184],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Increment_B"] = [[185],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Increment_C"] = [[186],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Increment_D"] = [[187],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Increments with carry
        self.Opcodes["Increment_A_Carry"] = [[188],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Increment_B_Carry"] = [[189],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Increment_C_Carry"] = [[190],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Increment_D_Carry"] = [[191],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.Shift_Pass,oc.AlU_Loop_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Decrements
        self.Opcodes["Decrement_A"] = [[192],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Decrement_B"] = [[193],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Decrement_C"] = [[194],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Decrement_D"] = [[195],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # And
        self.Opcodes["and_B_with_A"] = [[196],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_C_with_A"] = [[197],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_D_with_A"] = [[198],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["and_A_with_B"] = [[199],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_C_with_B"] = [[200],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_D_with_B"] = [[201],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["and_A_with_C"] = [[202],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_B_with_C"] = [[203],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_D_with_C"] = [[204],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["and_A_with_D"] = [[205],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_B_with_D"] = [[206],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["and_C_with_D"] = [[207],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # OR
        self.Opcodes["Or_B_with_A"] = [[208],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_C_with_A"] = [[209],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_D_with_A"] = [[210],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["Or_A_with_B"] = [[211],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_C_with_B"] = [[212],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_D_with_B"] = [[213],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["Or_A_with_C"] = [[214],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_B_with_C"] = [[215],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_D_with_C"] = [[216],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["Or_A_with_D"] = [[217],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_B_with_D"] = [[218],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Or_C_with_D"] = [[219],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Xor
        self.Opcodes["Xor_A_with_A"] = [[220],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_B_with_A"] = [[221],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_C_with_A"] = [[222],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_D_with_A"] = [[223],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["Xor_A_with_B"] = [[224],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_B_with_B"] = [[225],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_C_with_B"] = [[226],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_D_with_B"] = [[227],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["Xor_A_with_C"] = [[228],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_B_with_C"] = [[229],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_C_with_C"] = [[230],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_D_with_C"] = [[231],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        self.Opcodes["Xor_A_with_D"] = [[232],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_B_with_D"] = [[233],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_C_with_D"] = [[234],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Xor_D_with_D"] = [[235],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Not
        self.Opcodes["Not_A"] = [[236],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_A_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Not_B"] = [[237],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_B_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Not_C"] = [[238],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_C_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]
        self.Opcodes["Not_D"] = [[239],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[oc.GPR_D_Load_Main_Bus,oc.AlU_Assert_Main_Bus]]

        # Compare
        self.Opcodes["Compare_B_with_A"] = [[240],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_C_with_A"] = [[241],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_D_with_A"] = [[242],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]

        self.Opcodes["Compare_A_with_B"] = [[243],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_C_with_B"] = [[244],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_D_with_B"] = [[245],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]

        self.Opcodes["Compare_A_with_C"] = [[246],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_B_with_C"] = [[247],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_D_with_C"] = [[248],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.GPR_D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]

        self.Opcodes["Compare_A_with_D"] = [[249],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_B_with_D"] = [[250],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Compare_C_with_D"] = [[251],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.GPR_C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]

        # Test
        self.Opcodes["Test_A"] = [[252],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_A_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Test_B"] = [[253],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_B_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Test_C"] = [[254],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_C_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]
        self.Opcodes["Test_D"] = [[255],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.GPR_D_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Register_Write,oc.Shift_Register_Write],[]]

    def make_opcode_roms(self,pos,stage_1,stage_2):
        x,y,z = pos

        self.input_stage_1 = []
        self.input_not_stage_1 = []

        self.input_stage_2 = []
        self.input_not_stage_2 = []

        for flag in self.flags:
            self.flags[flag] = [self.flags[flag]]
            self.flags[flag].append(self.ID.get_next())
            self.flags[flag].append(self.ID.get_next())
            self.flags[flag].append(self.ID.get_next())
            self.flags[flag].append(self.ID.get_next())

        for _ in range(self.bitness):
            self.input_stage_1.append(self.ID.get_next())
            self.input_not_stage_1.append(self.ID.get_next())

            self.input_stage_2.append(self.ID.get_next())
            self.input_not_stage_2.append(self.ID.get_next())


        for i in range(self.bitness):
            self.blueprint.logic_gate(self.input_stage_1[i],"or",(x,i+y,z),"up","right","d02525")
            self.blueprint.logic_gate(self.input_not_stage_1[i],"nor",(x,i+self.bitness+len(self.flags) + y,z),"up","right","d02525")

        pos = 0
        for flag in self.flags:
            self.blueprint.logic_gate(self.flags[flag][1],"or",(x,self.bitness+pos+y,z),"up","right","e2db13")
            self.blueprint.logic_gate(self.flags[flag][2],"nor",(x,self.bitness*2+len(self.flags) + pos + y,z),"up","right","e2db13")
            self.blueprint.addId(self.flags[flag][0],self.flags[flag][1])
            self.blueprint.addId(self.flags[flag][0],self.flags[flag][2])
            pos+=1


        for i in range(self.bitness):
            self.blueprint.logic_gate(self.input_stage_2[i],"or",(x,i+y+30,z),"up","right","0a3ee2")
            self.blueprint.logic_gate(self.input_not_stage_2[i],"nor",(x,i+self.bitness+len(self.flags) + y+30,z),"up","right","0a3ee2")

        pos = 0
        for flag in self.flags:
            self.blueprint.logic_gate(self.flags[flag][3],"or",(x,self.bitness+pos+y+30,z),"up","right","e2db13")
            self.blueprint.logic_gate(self.flags[flag][4],"nor",(x,self.bitness*2+len(self.flags) + pos + y+30,z),"up","right","e2db13")
            self.blueprint.addId(self.flags[flag][0],self.flags[flag][3])
            self.blueprint.addId(self.flags[flag][0],self.flags[flag][4])
            pos+=1

        for i in range(self.bitness):
            self.blueprint.addId(stage_1.memcells[-1-i],self.input_stage_1[i])
            self.blueprint.addId(stage_1.memcells[-1-i],self.input_not_stage_1[i])
            self.blueprint.addId(stage_2.memcells[-1-i],self.input_stage_2[i])
            self.blueprint.addId(stage_2.memcells[-1-i],self.input_not_stage_2[i])

        rx = 0
        ry = 0

        for opcode in self.Opcodes:
            fetch_flags,stage1,stage2 = self.Opcodes[opcode]
            code = fetch_flags[0]
            flags = fetch_flags[1:]

            self.blueprint.logic_gate(self.ID.get_next(),"and",(rx + x+1,ry + y,z),"up","right","d02525")

            mask = 1
            for i in range(self.bitness):
                if code & mask == mask:
                    self.blueprint.addId(self.input_stage_1[i],self.ID.current_ID)
                else:
                    self.blueprint.addId(self.input_not_stage_1[i],self.ID.current_ID)
                mask = mask << 1
            for line in stage1:
                self.blueprint.addId(self.ID.current_ID,line)



            self.blueprint.logic_gate(self.ID.get_next(),"and",(rx + x+1,ry + y+30,z),"up","right","0a3ee2")

            mask = 1
            for i in range(self.bitness):
                if code & mask == mask:
                    self.blueprint.addId(self.input_stage_2[i],self.ID.current_ID)
                else:
                    self.blueprint.addId(self.input_not_stage_2[i],self.ID.current_ID)
                mask = mask << 1
            for line in stage2:
                self.blueprint.addId(self.ID.current_ID,line)


            for each_flags in self.flags:
                each_flags = self.flags[each_flags]
                for each_flag in flags:
                    print(f"flags = {flags} : each_flag = {each_flag} : each_flags = {each_flags}")
                    if each_flags[0] == each_flag[0]:
                        print(opcode)

                        if each_flag[1]:
                            self.blueprint.addId(each_flags[1],self.ID.current_ID-1)
                            self.blueprint.addId(each_flags[3],self.ID.current_ID)
                        else:
                            self.blueprint.addId(each_flags[2],self.ID.current_ID-1)
                            self.blueprint.addId(each_flags[4],self.ID.current_ID)

            ry += 1
            if ry > 28:
                ry = 0
                rx += 1


class Ram:
    def __init__(self,blueprint,ID,bitness_in,bitness_out,pos,rotation = "x,y,z"):
        self.blueprint = blueprint
        self.ID = ID
        self.bitness_in = bitness_in
        self.bitness_out = bitness_out
        self.pos = pos
        self.rotation = rotation


        self.input_ors = [ID.get_next() for _ in range(self.bitness_in)]
        self.input_nors = [ID.get_next() for _ in range(self.bitness_in)]
        self.output_or = [ID.get_next() for _ in range(self.bitness_out)]
        self.input_and = [ID.get_next() for _ in range(self.bitness_out)]
        self.write = ID.get_next()
        self.read = ID.get_next()
        self.write_driver = ID.get_next()
        self.read_driver = ID.get_next()

        x,y,z = pos

        self.blueprint.logic_gate(self.read,"or",(x,y - 1,z),"up","down","eeeeee",rotation)
        self.blueprint.logic_gate(self.write,"or",(x + 1,y - 1,z),"up","down","19e753",rotation)
        self.blueprint.logic_gate(self.write_driver,"or",(x + 2,y - 1,z),"up","down","19e753",rotation)
        self.blueprint.logic_gate(self.read_driver,"or",(x + 3,y - 1,z),"up","down","19e753",rotation)

        self.blueprint.addId(self.read,self.read_driver)
        self.blueprint.addId(self.write,self.write_driver)




        self.blueprint.logic_gate(ID.get_next(),"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        self.blueprint.addId(self.read,ID.current_ID)
        self.blueprint.addId(ID.current_ID,self.read_driver)

        self.blueprint.logic_gate(ID.get_next(),"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        self.blueprint.addId(self.write,ID.current_ID)
        self.blueprint.addId(ID.current_ID,self.read_driver)

        self.blueprint.logic_gate(ID.get_next(),"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        self.blueprint.addId(ID.current_ID-1,ID.current_ID)

        self.blueprint.logic_gate(ID.get_next(),"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        self.blueprint.addId(ID.current_ID - 1,ID.current_ID)
        self.blueprint.addId(ID.current_ID,self.write_driver)
        self.blueprint.addId(ID.current_ID,self.read_driver)




        for i in range(bitness_out):
            self.blueprint.logic_gate(self.input_and[i],"and",(x+1,i + y,z),"up","down","19e753",rotation)
            blueprint.addId(self.write_driver,self.input_and[i])
            self.blueprint.logic_gate(self.output_or[i],"or",(x,i + y,z),"up","down","eeeeee",rotation)
        for i in range(bitness_in):
            self.blueprint.logic_gate(self.input_ors[i],"and",(2 + x,i + y,z),"up","down","d02525",rotation)
            self.blueprint.logic_gate(self.input_nors[i],"nand",(3 + x,i + y,z),"up","down","d02525",rotation)
        for i in range(bitness_out-bitness_in):
            blueprint.place_object(objects.Duct_Holder,(2 + x,i + y+bitness_in,z),"up","up","000000",rotation)
            blueprint.place_object(objects.Duct_Holder,(3 + x,i + y+bitness_in,z),"up","up","000000",rotation)

        self.enables = self.input_ors+self.input_nors+[ID.current_ID+self.bitness_out*3+1,ID.current_ID+self.bitness_out*3+2]

        for i in range(2**bitness_in):
            Xor_self_wire,connection,write_read = self.cell((4+i+x,y,z))

            blueprint.addId(self.read_driver,write_read)
            for j in range(bitness_out):
                blueprint.addId(connection[j],self.output_or[j])
                blueprint.addId(self.input_and[j],Xor_self_wire[j])

            mask = 1
            for k in range(self.bitness_in):
                if i & mask == mask:
                    self.blueprint.addId(self.input_ors[k],write_read)
                else:
                    self.blueprint.addId(self.input_nors[k],write_read)
                mask = mask << 1

        self.input_ors.reverse()
        self.input_nors.reverse()
        self.input_and.reverse()
        self.output_or.reverse()







    def cell(self,pos):
        x,y,z = pos
        Xor_self_wire = [self.ID.get_next() for _ in range(self.bitness_out)]
        connection = [self.ID.get_next() for _ in range(self.bitness_out)]

        write_read = self.ID.get_next()


        self.blueprint.logic_gate(write_read,"and",(x,y-1,z),"up","down","19e753",self.rotation)
        for i in range(self.bitness_out):
            self.blueprint.logic_gate(connection[i],"and",(x,i + y,z),"up","down","eeeeee",self.rotation)
            self.blueprint.logic_gate(Xor_self_wire[i],"xor",(x,i + y,z+1),"up","down","0a3ee2",self.rotation)
            self.blueprint.addId(Xor_self_wire[i],Xor_self_wire[i])
            self.blueprint.addId(Xor_self_wire[i],connection[i])
            self.blueprint.addId(write_read,connection[i])

        for i in range(len(connection)):
            if i % 2:
                self.blueprint.addId(connection[i],Xor_self_wire[i - 1])
            else:
                self.blueprint.addId(connection[i],Xor_self_wire[i+1])
        return Xor_self_wire,connection,write_read


class IO:
    def __init__(self,blueprint,ID,bitness,pos,rotation="x,y,z"):
        self.blueprint = blueprint
        self.ID = ID
        self.number_devices = 8
        self.pos = pos
        self.rotation = rotation

        address_bitness = int(math.ceil(math.sqrt(self.number_devices)))

        self.address_ands = [ID.get_next() for _ in range(address_bitness)]
        self.address_nands = [ID.get_next() for _ in range(address_bitness)]

        self.input_ors = [ID.get_next() for _ in range(bitness)]

        self.write = ID.get_next()
        self.read = ID.get_next()
        self.clock_high = ID.get_next()
        self.clock_low = ID.get_next()

        self.bus_output = [ID.get_next() for _ in range(bitness)]
        self.bus_input = [ID.get_next() for _ in range(bitness)]

        x,y,z = self.pos

        pos_x = 0
        pos_y = -1
        size = math.ceil(self.number_devices/bitness)

        for i in range(address_bitness):
            self.blueprint.logic_gate(self.address_ands[i],"and",(bitness+x-i-1,y+size+3,z),"up","right","d02525",rotation)
            self.blueprint.logic_gate(self.address_nands[i],"nand",(bitness+x-i-1, y+size+2,z),"up","right","d02525",rotation)

        for i in range(bitness - address_bitness-1):
            blueprint.place_object(objects.Duct_Holder,(1 + x+i,y+size+3,z),"up","up","000000",rotation)
            blueprint.place_object(objects.Duct_Holder,(1 + x+i,y+size+2,z),"up","up","000000",rotation)

        self.blueprint.logic_gate(self.clock_high,"or",(x,y+size+3,z),"up","right","19e753",rotation)
        self.blueprint.logic_gate(self.clock_low,"or",(x, y+size+2,z),"up","right","e2db13",rotation)


        for device in range(self.number_devices):
            blueprint.logic_gate(ID.get_next(),"and",(x + pos_x,y + pos_y+size+2, z),"up","right","29842e")
            mask = 1
            for i in range(address_bitness):
                if device & mask == mask:
                    self.blueprint.addId(self.address_ands[i],self.ID.current_ID)
                else:
                    self.blueprint.addId(self.address_nands[i],self.ID.current_ID)
                mask = mask << 1

            pos_x += 1
            if pos_x >= 8:
                pos_x = 0
                pos_y -= 1

        remainder = (bitness % 2 ** address_bitness) - (2**address_bitness-self.number_devices)

        for i in range(2**address_bitness-self.number_devices):
            blueprint.place_object(objects.Duct_Holder,(x+remainder+i,y,z),"up","up","000000",rotation)

        for i in range(bitness):
            self.blueprint.logic_gate(self.bus_input[i],"or",(bitness+x-i-1,y+size,z),"up","right","eeeeee",rotation)
            self.blueprint.logic_gate(self.bus_output[i],"or",(bitness+x-i-1, y,z),"up","right","19e753",rotation)

        self.blueprint.logic_gate(self.read,"or",(bitness + x,y+1,z),"up","right","eeeeee",rotation)
        self.blueprint.logic_gate(self.write,"or",(bitness + x,y,z),"up","right","19e753",rotation)





class equality_checker:
    def __init__(self,blueprint,ID,A,B,pos,rotation="x,y,z"):
        self.blueprint = blueprint
        self.ID = ID
        self.A = A
        self.B = B
        if len(A) != len(B):
            print("error in equality_checker")
            print("A and B must be the same length")
            exit(1)
        self.bitness = len(A)
        self.pos = pos
        self.rotation = rotation

        self.xnors = [ID.get_next() for _ in range(self.bitness)]


        self.output = ID.get_next()

        x,y,z = self.pos
        self.blueprint.logic_gate(self.output,"and",(x + self.bitness,y,z),"up","right","eeeeee",rotation)

        for i in range(self.bitness):
            self.blueprint.logic_gate(self.xnors[i],"xnor",(x + i,y,z),"up","right","eeeeee",rotation)
            self.blueprint.addId(self.xnors[i],self.output)
            self.blueprint.addId(self.A[i],self.xnors[i])
            self.blueprint.addId(self.B[i],self.xnors[i])


class disk:
    def __init__(self,blueprint,ID,bitness_in,bitness_out,disk_size,pos,rotation="x,y,z"):
        self.blueprint = blueprint
        self.ID = ID
        self.bitness_in = bitness_in
        self.bitness_out = bitness_out
        self.pos = pos
        self.rotation = rotation
        self.disk_size = disk_size
        self.address_size =  math.floor(math.log2(int(2 ** self.bitness_in / self.disk_size - 1))) + 1
        self.counter_size = bitness_in - self.address_size

        print(self.address_size,self.counter_size)


        self.timer_cell_controller()
        self.timer_cells()
        blueprint, ram_address_ands, ram_address_nors, ram_input_ors, ram_output_or, write, read = self.disk_ram()
        self.blueprint.merge(blueprint)




    def timer_cell_controller(self):

        x, y, z = self.pos

        self.xnors = [self.ID.get_next() for _ in range(self.counter_size)]
        self.trigger = self.ID.get_next()
        self.trigger_2 = self.ID.get_next()

        self.counter_gates = [self.ID.get_next() for _ in range(self.counter_size)]
        self.address_gates = [self.ID.get_next() for _ in range(self.counter_size)]

        self.address_ands = [self.ID.get_next() for _ in range(self.address_size)]
        self.address_nors = [self.ID.get_next() for _ in range(self.address_size)]

        self.enable = self.ID.get_next()

        self.read = self.ID.get_next()
        self.write = self.ID.get_next()

        self.input_gates = [self.ID.get_next() for _ in range(self.bitness_out)]
        self.output_gates = [self.ID.get_next() for _ in range(self.bitness_out)]


        # input and trigger gates
        self.blueprint.logic_gate(self.read, "or", (self.bitness_out*2+1 + x, y, z), "up", "right", colors.White)
        self.blueprint.logic_gate(self.write, "or", (self.bitness_out*2+1 + x, y + 1, z), "up", "right", colors.Green)
        self.blueprint.logic_gate(self.enable, "and", (self.bitness_out*2+1 + x, y + 2, z), "up", "right", colors.Black)

        self.blueprint.logic_gate(self.trigger,"and",(x + self.bitness_out*2+1,y+3,z),"up","right",colors.Black, self.rotation)
        self.blueprint.logic_gate(self.trigger_2, "and", (x + self.bitness_out*2+1, y+4, z), "up", "right", colors.Black, self.rotation)


        self.blueprint.addId(self.enable,self.address_gates[-1])

        # address and counting gates and connections
        for i in range(self.counter_size):
            self.blueprint.logic_gate(self.xnors[i],"xnor",(x + i+self.address_size,y,z),"up","right","eeeeee",self.rotation)
            self.blueprint.addId(self.xnors[i],self.trigger)
            self.blueprint.addId(self.xnors[i], self.trigger_2)
            self.blueprint.logic_gate(self.address_gates[i],"xor",(x + i+self.address_size,y+1,z),"up","right","eeeeee",self.rotation)
            self.blueprint.addId(self.address_gates[i],self.address_gates[i])

            self.blueprint.logic_gate(self.counter_gates[i],"and",(i + x+self.address_size,y+2,z),"up","right","eeeeee",self.rotation)
            self.blueprint.addId(self.enable,self.counter_gates[i])

            self.blueprint.addId(self.address_gates[i], self.xnors[i])


        for i in range(self.address_size):
            self.blueprint.logic_gate(self.address_ands[i], "and", (i + x, y + 1, z), "up", "right", "eeeeee",self.rotation)
            self.blueprint.logic_gate(self.address_nors[i], "nor", (i + x, y + 2, z), "up", "right", "eeeeee",self.rotation)


        # more connections for counting
        for i in range(self.counter_size):
            for j in range(self.counter_size - i):
                self.blueprint.addId(self.address_gates[self.counter_size-1-i],self.counter_gates[j])


        for i in range(self.counter_size-1):
            self.blueprint.addId(self.counter_gates[i+1],self.address_gates[i])


        # inputs and outputs
        for i in range(self.bitness_out):
            self.blueprint.logic_gate(self.input_gates[self.bitness_out-1-i],"or",(i + x,y + 3,z),"up","right",colors.Red,self.rotation)
            self.blueprint.logic_gate(self.output_gates[self.bitness_out-1-i],"or",(i + x,y + 4,z),"up","right",colors.Blue_Diamond,self.rotation)


        self.address_ands.reverse()
        self.address_nors.reverse()


    def timer_cells(self):
        x, y, z = self.pos
        for i in range(int(2**self.bitness_in/self.disk_size)):
            bp, read, write, output, input = self.disk_sector((x,y+i+3,z))
            self.blueprint.merge(bp)

            self.blueprint.connect_ID(output,self.output_gates)
            self.blueprint.connect_ID(self.input_gates, input)

            self.blueprint.addId(self.trigger, read)
            self.blueprint.addId(self.trigger_2, write)

            self.blueprint.addId(self.read, read)
            self.blueprint.addId(self.write, write)

            mask = 1
            for j in range(math.floor(math.log2(int(2**self.bitness_in/self.disk_size-1)))+1):
                if i & mask == mask:
                    self.blueprint.addId(self.address_ands[j], write)
                    self.blueprint.addId(self.address_ands[j], read)
                else:
                    self.blueprint.addId(self.address_nors[j], write)
                    self.blueprint.addId(self.address_nors[j], read)
                mask = mask << 1

    def disk_ram(self):
        blueprint = sm_helpers.Blueprint(self.ID)

        x, y, z = self.pos
        ram_bitness_in = math.floor(math.log2(int(2**self.bitness_in/self.disk_size-1)))+1

        ram_address_ands = [self.ID.get_next() for _ in range(ram_bitness_in)]
        ram_address_nors = [self.ID.get_next() for _ in range(ram_bitness_in)]
        ram_output_or = [self.ID.get_next() for _ in range(self.bitness_out)]
        ram_input_ors  = [self.ID.get_next() for _ in range(self.bitness_out)]
        ram_write = self.ID.get_next()
        ram_read = self.ID.get_next()

        x, y, z = self.pos

        x += 9
        y += 5

        blueprint.logic_gate(ram_read, "or", (x + self.bitness_out, y, z), "up", "right", "eeeeee", self.rotation)
        blueprint.logic_gate(ram_write, "or", (x + self.bitness_out, y + 1, z), "up", "right", "19e753", self.rotation)

        for i in range(self.bitness_out):
            blueprint.logic_gate(ram_input_ors[i], "or", (x + i, y + 1, z), "up", "right", "19e753", self.rotation)
            blueprint.logic_gate(ram_output_or[i], "or", (x + i, y, z), "up", "right", "eeeeee", self.rotation)
        for i in range(ram_bitness_in):
            blueprint.logic_gate(ram_address_ands[i], "and", (x + ram_bitness_in - i + 1, y + 2, z), "up", "right", "d02525", self.rotation)
            blueprint.logic_gate(ram_address_nors[i], "nand", (x + ram_bitness_in - i + 1, y + 3, z), "up", "right", "d02525", self.rotation)
        for i in range(self.bitness_out - ram_bitness_in):
            blueprint.place_object(objects.Duct_Holder, (x + i, y + 2, z), "up", "up", "000000", self.rotation)
            blueprint.place_object(objects.Duct_Holder, (x + i, y + 3, z), "up", "up", "000000", self.rotation)

        self.enables = ram_address_ands + ram_address_nors

        for i in range(2 ** ram_bitness_in):
            write,read,xors,read_ands = self.cell((x, y + i + 4 , z))

            blueprint.addId(ram_write, write)
            blueprint.addId(ram_read, read)

            blueprint.connect_ID(ram_input_ors, xors)
            blueprint.connect_ID(read_ands, ram_output_or)

            mask = 1
            for k in range(ram_bitness_in):
                if i & mask == mask:
                    blueprint.addId(ram_address_ands[k], write)
                    blueprint.addId(ram_address_ands[k], read)
                else:
                    blueprint.addId(ram_address_nors[k], write)
                    blueprint.addId(ram_address_nors[k], read)
                mask = mask << 1

        ram_address_ands.reverse()
        ram_address_nors.reverse()
        ram_input_ors.reverse()
        ram_output_or.reverse()

        return blueprint, ram_address_ands, ram_address_nors, ram_input_ors, ram_output_or, write, read




    def cell(self, pos):
        x, y, z = pos
        Xor_self_wire = [self.ID.get_next() for _ in range(self.bitness_out)]
        xors = [self.ID.get_next() for _ in range(self.bitness_out)]
        write_ands = [self.ID.get_next() for _ in range(self.bitness_out)]
        read_ands = [self.ID.get_next() for _ in range(self.bitness_out)]

        write = self.ID.get_next()
        read = self.ID.get_next()

        self.blueprint.logic_gate(write, "and", (x + self.bitness_out, y, z+1), "up", "right", colors.Green, self.rotation)
        self.blueprint.logic_gate(read, "and", (x + self.bitness_out, y, z), "up", "right", colors.White, self.rotation)
        for i in range(self.bitness_out):
            self.blueprint.logic_gate(xors[i], "xor", (x + i, y, z), "up", "right", colors.Red, self.rotation)
            self.blueprint.logic_gate(write_ands[i], "and", (x + i, y, z+1), "up", "right", colors.Green, self.rotation)
            self.blueprint.logic_gate(read_ands[i], "and", (x + i, y, z+2), "up", "right", colors.White, self.rotation)
            self.blueprint.logic_gate(Xor_self_wire[i], "xor", (x + i, y, z + 3), "up", "right", "0a3ee2", self.rotation)

        self.blueprint.connect_ID(Xor_self_wire,Xor_self_wire)
        self.blueprint.connect_ID(Xor_self_wire, read_ands)
        self.blueprint.connect_ID(Xor_self_wire, xors)
        self.blueprint.connect_ID(xors, write_ands)
        self.blueprint.connect_ID(write_ands, Xor_self_wire)

        self.blueprint.connect_IDS(write,write_ands)
        self.blueprint.connect_IDS(read,read_ands)

        return write,read,xors,read_ands



    def connect_address(self,IDs):


        for i in range(len(IDs)):
            if i < self.address_size:
                self.blueprint.addId(IDs[i],self.address_nors[-1-i])
                self.blueprint.addId(IDs[i], self.address_ands[-1-i])
            else:
                self.blueprint.addId(IDs[i], self.xnors[i-self.address_size])


    def disk_sector(self,pos):
        blueprint = sm_helpers.Blueprint(self.ID,"","")

        time = self.disk_size
        num_timers = 1

        while time > 2400:
            num_timers+=1
            time-=2400



        last_timer = time - (2+num_timers)

        timer_seconds = math.floor(last_timer/40)
        timer_ticks = last_timer%40

        print(self.disk_size,num_timers,last_timer,timer_seconds,timer_ticks)


        read = self.ID.get_next()
        write = self.ID.get_next()

        erase_driver = self.ID.get_next()
        read_driver = self.ID.get_next()
        write_driver = self.ID.get_next()

        ors = [self.ID.get_next() for _ in range(self.bitness_out)]
        timers = [self.ID.get_next() for _ in range(self.bitness_out)]
        erase = [self.ID.get_next() for _ in range(self.bitness_out)]
        output = [self.ID.get_next() for _ in range(self.bitness_out)]
        input = [self.ID.get_next() for _ in range(self.bitness_out)]


        x, y, z = pos

        y+=2

        blueprint.logic_gate(read,"and",(x+self.bitness_out, y, z + 4),"east","left",colors.White)
        blueprint.logic_gate(write, "and", (x+self.bitness_out, y, z + 3), "east", "left", colors.Green)

        blueprint.logic_gate(erase_driver, "nor", (x+self.bitness_out, y, z + 2), "east", "left", colors.Black)
        blueprint.logic_gate(read_driver, "and", (x+self.bitness_out, y, z + 1), "east", "left", colors.Black)
        blueprint.logic_gate(write_driver, "and", (x+self.bitness_out, y, z), "east", "left", colors.Black)

        for i in range(self.bitness_out):
            blueprint.logic_gate(ors[i], "or", (x + i, y, z + 3+num_timers*2), "up", "right", colors.Black)
            if num_timers > 1:
                timer_id = self.ID.get_next()
                blueprint.addId(ors[i], timer_id)
                for j in range(num_timers-1):
                    blueprint.timer(timer_id, 59,40, (x + i, y, z + 3+(j+1)*2), "up", "up", colors.Black)
                    if j == num_timers-2:
                        blueprint.addId(timer_id, timers[i])
                    else:
                        timer_id = self.ID.get_next()

            blueprint.timer(timers[i], timer_seconds,timer_ticks, (x + i, y, z + 3), "up", "up", colors.Black)

            blueprint.logic_gate(erase[i], "and", (x + i, y, z + 2), "up", "right", colors.Black)
            blueprint.logic_gate(output[i], "and", (x + i, y, z + 1), "up", "right", colors.Black)
            blueprint.logic_gate(input[i], "and", (x + i, y, z), "up", "right", colors.Black)

            blueprint.addId(timers[i], erase[i])
            blueprint.addId(erase[i], ors[i])
            blueprint.addId(ors[i], output[i])
            blueprint.addId(input[i], ors[i])

            blueprint.addId(erase_driver, erase[i])
            blueprint.addId(read_driver, output[i])
            blueprint.addId(write_driver, input[i])

        blueprint.addId(read, read_driver)
        blueprint.addId(write, erase_driver)
        blueprint.addId(write, write_driver)

        input.reverse()
        output.reverse()

        return blueprint, read, write, output, input





class buttons:
    def __init__(self,blueprint,ID,number,pos,rotation="x,y,z"):
        self.blueprint = blueprint
        self.ID = ID
        self.number = number
        self.pos = pos
        self.rotation = rotation
        x,y,z = self.pos
        self.buttons = [ID.get_next() for _ in range(self.number)]
        for i in range(self.number):
            self.blueprint.button(self.buttons[i],(x + i,y,z),"up","up",rotation=rotation)

class switches:
    def __init__(self,blueprint,ID,number,pos,rotation="x,y,z"):
        self.blueprint = blueprint
        self.ID = ID
        self.number = number
        self.pos = pos
        self.rotation = rotation
        x,y,z = self.pos
        self.switches = [ID.get_next() for _ in range(self.number)]
        for i in range(self.number):
            self.blueprint.switch(self.switches[i],(x + i,y,z),"up","up",rotation=rotation)

class display:
    def __init__(self,blueprint,ID,res,pos,rotation="x,y,z"):
        self.blueprint = blueprint
        self.ID = ID
        self.x,self.y = res
        self.pos = pos
        self.rotation = rotation
        x,y,z = self.pos

        for i in range(self.x):
            for j in range(self.y):
                b,id = self.pixel((i,j))
                blueprint.merge(b)


    def pixel(self,pos):
        pos = (self.pos[0]+pos[0],self.pos[1]+pos[1],self.pos[2])
        logic_pos = (pos[0],pos[1],pos[2]-2)
        blueprint = sm_helpers.Blueprint(self.ID,"","")

        blueprint.place_object(objects.Duct_Holder,(pos[0],pos[1],pos[2]-1),"up","up","000000")
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="FFFFFF")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="FFFF00")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="FF00FF")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="FF0000")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="00FFFF")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="00FF00")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="0000FF")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)
        blueprint.place_light_object(objects.Shack_Light,self.ID.get_next(),pos,"down","up",color="000000")
        blueprint.logic_gate(self.ID.get_next(),"nand",logic_pos,"up","right",colors.Black)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-1)

        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Black)
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Black)
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Black)
        blueprint.logic_gate(self.ID.get_next(),"nor",logic_pos,"up","right",colors.Black)
        blueprint.logic_gate(self.ID.get_next(),"nor",logic_pos,"up","right",colors.Black)
        blueprint.logic_gate(self.ID.get_next(),"nor",logic_pos,"up","right",colors.Black)

        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Red)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID - 3)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID - 6)
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Green)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID - 3)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID - 6)
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Blue)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID - 3)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID - 6)


        mask = 1
        for I in range(8):
            mask = 1
            for i in range(3):
                if I & mask == mask:
                    self.blueprint.addId(self.ID.current_ID-i-6,self.ID.current_ID-I*2-9)
                else:
                    self.blueprint.addId(self.ID.current_ID-i-3,self.ID.current_ID-I*2-9)
                mask = mask << 1
        """
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Blue)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-3)
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Blue)
        blueprint.addId(self.ID.current_ID-3,self.ID.current_ID)

        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Blue)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-3)
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Blue)
        blueprint.addId(self.ID.current_ID-3,self.ID.current_ID)

        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Blue)
        blueprint.addId(self.ID.current_ID,self.ID.current_ID-3)
        blueprint.logic_gate(self.ID.get_next(),"and",logic_pos,"up","right",colors.Blue)
        blueprint.addId(self.ID.current_ID-3,self.ID.current_ID)
        """
        return (blueprint,self.ID.current_ID)

