import math
import block_list
import color_list
import sm_helpers as sm

blocks = block_list.blocks()
objects = block_list.objects()
colors = color_list.colors()

class Clock:
    def __init__(self,bp,id,clock_high,clock_low,pos):
        self.blueprint = bp
        self.id = id
        self.clock_high = clock_high
        self.clock_low = clock_low
        self.pos = pos
        x, y, z = pos

        self.cpu_enable = sm.LogicGate(bp, id, "nor", (9 + x, y, z), "up", "right", colors.Green)

        self.reset = sm.LogicGate(bp,id,"and",(8 + x,3 + y,z),"up","right","d02525")
        self.clock_rising = sm.LogicGate(bp,id,"and",(8 + x,1 + y,z),"up","right","19e753")
        self.clock_falling = sm.LogicGate(bp,id,"and",(8 + x,2 + y,z),"up","right","e2db13")

        self.output_tick_gen_and = sm.LogicGate(bp,id,"and",(7 + x,1 + y,z),"up","right","222222")
        self.output_tick_gen_nor = sm.LogicGate(bp,id,"nor",(6 + x,1 + y,z),"up","right","222222")
        self.output_tick_gen_or = sm.LogicGate(bp,id,"or",(5 + x,1 + y,z),"up","right","222222")

        self.falling_timer = sm.Timer(bp,id,0,clock_low - 1,(6 + x,2 + y,z),"east","right","222222")

        if clock_high + clock_low > 4:
            self.clock_timer = sm.Timer(bp,id,0,int(clock_high / 2),(7 + x,0 + y,z),"east","right","222222")
        else:
            self.clock_nor_fast = sm.LogicGate(bp,id,"nor",(8 + x,0 + y,z),"up","right","222222")
            self.clock_and_fast = sm.LogicGate(bp,id,"and",(7 + x,0 + y,z),"up","right","222222")

        self.clock_nor = sm.LogicGate(bp,id,"nor",(6 + x,0 + y,z),"up","right","222222")
        self.clock_and = sm.LogicGate(bp,id,"and",(5 + x,0 + y,z),"up","right","222222")

        self.clock_enable_xor = sm.LogicGate(bp,id,"xor",(5 + x,2 + y,z),"up","right","222222")
        self.reset_enable_xor = sm.LogicGate(bp,id,"xor",(5 + x,3 + y,z),"up","right","222222")

        self.enable_timer = sm.Timer(bp,id,0, 2,(x-1, y ,z),"east","right","222222")
        self.reset_timer = sm.Timer(bp,id,0, clock_high + clock_low + 1,(6 + x,3 + y,z),"east","right","222222")
        self.reset_tick_gen_and = sm.LogicGate(bp,id,"and",(4 + x,3 + y,z),"up","right","222222")
        self.reset_tick_gen_nor = sm.LogicGate(bp,id,"nor",(3 + x,3 + y,z),"up","right","222222")
        self.reset_input = sm.LogicGate(bp,id,"or",(0 + x,3 + y,z),"up","right","d02525")

        self.clock_tick_gen_and = sm.LogicGate(bp,id,"and",(4 + x,2 + y,z),"up","right","222222")
        self.clock_tick_gen_nor = sm.LogicGate(bp,id,"nor",(4 + x,1 + y,z),"up","right","222222")
        self.clock_enable_input = sm.LogicGate(bp,id,"or",(0 + x,1 + y,z),"up","right","19e753")

        self.clock_enable_or = sm.LogicGate(bp,id,"or",(4 + x,0 + y,z),"up","right","222222")
        self.clock_enable_nor = sm.LogicGate(bp,id,"nor",(3 + x,0 + y,z),"up","right","222222")

        self.clock_or_and = sm.LogicGate(bp,id,"and",(3 + x,2 + y,z),"up","right","222222")
        self.clock_nor_and = sm.LogicGate(bp,id,"and",(3 + x,1 + y,z),"up","right","222222")

        self.step_and = sm.LogicGate(bp,id,"and",(2 + x,0 + y,z),"up","right","222222")
        self.step_input = sm.LogicGate(bp,id,"or",(0 + x,2 + y,z),"up","right","0a3ee2")

        self.step_latch_xor = sm.LogicGate(bp,id,"xor",(2 + x,3 + y,z),"up","right","222222")
        self.step_tick_gen_and = sm.LogicGate(bp,id,"and",(2 + x,2 + y,z),"up","right","222222")
        self.step_tick_gen_nor = sm.LogicGate(bp,id,"nor",(2 + x,1 + y,z),"up","right","222222")

        self.step_latch_nor = sm.LogicGate(bp,id,"nor",(1 + x,1 + y,z),"up","right","222222")
        self.step_latch_nor_and = sm.LogicGate(bp,id,"and",(1 + x,0 + y,z),"up","right","222222")

        self.step_latch_or = sm.LogicGate(bp,id,"or",(1 + x,3 + y,z),"up","right","222222")
        self.step_latch_or_and = sm.LogicGate(bp,id,"and",(1 + x,2 + y,z),"up","right","222222")


        self.reset_button = sm.button(bp,id,(x-1,3 + y,z + 1),"up","up","d02525")
        self.step_button = sm.button(bp,id,(x-1,2 + y,z + 1),"up","up","0a3ee2")
        self.run_button = sm.button(bp,id,(x-1,1 + y,z + 1),"up","up","19e753")

        self.connections()


    def connections(self):
        x, y, z = self.pos
        self.blueprint.place_object(objects.Duct_Holder, (x-1,3 + y,z), "up", "up", "000000")
        self.blueprint.place_object(objects.Duct_Holder, (x - 1, 2 + y, z), "up", "up", "000000")
        self.blueprint.place_object(objects.Duct_Holder, (x - 1, 1 + y, z), "up", "up", "000000")

        self.reset_button.connect(self.reset_input)
        self.step_button.connect(self.step_input)
        self.run_button.connect(self.clock_enable_input)

        self.step_latch_or.connect(self.step_latch_or_and)
        self.step_latch_xor.connect(self.step_latch_xor)
        self.step_latch_xor.connect(self.step_latch_or)
        self.step_latch_xor.connect(self.step_latch_nor)
        self.step_latch_xor.connect(self.output_tick_gen_or)
        self.reset_input.connect(self.reset_tick_gen_nor)
        self.reset_input.connect(self.reset_tick_gen_and)
        self.reset_tick_gen_nor.connect(self.reset_tick_gen_and)
        self.reset_tick_gen_and.connect(self.clock_nor_and)
        self.reset_enable_xor.connect(self.reset_enable_xor)
        self.reset_enable_xor.connect(self.cpu_enable)
        self.reset_enable_xor.connect(self.enable_timer)
        self.enable_timer.connect(self.cpu_enable)
        self.reset_tick_gen_and.connect(self.reset_enable_xor)
        self.reset_tick_gen_and.connect(self.reset_timer)
        self.reset_timer.connect(self.clock_or_and)
        self.reset_timer.connect(self.reset_enable_xor)
        self.reset_enable_xor.connect(self.reset)


        self.step_input.connect(self.step_and)
        self.step_input.connect(self.step_latch_nor_and)

        self.step_latch_or_and.connect(self.step_latch_xor)
        self.step_tick_gen_and.connect(self.step_latch_xor)

        self.clock_or_and.connect(self.clock_enable_xor)
        self.clock_tick_gen_and.connect(self.clock_enable_xor)

        self.clock_enable_xor.connect(self.clock_enable_xor)
        self.clock_enable_xor.connect(self.step_and)
        self.clock_enable_xor.connect(self.clock_enable_nor)
        self.clock_enable_xor.connect(self.clock_enable_or)
        self.clock_enable_xor.connect(self.step_latch_nor)

        self.falling_timer.connect(self.clock_falling)
        self.clock_falling.connect(self.step_latch_or_and)

        self.step_latch_nor.connect(self.step_latch_nor_and)

        self.step_tick_gen_nor.connect(self.step_tick_gen_and)

        self.clock_nor_and.connect(self.clock_enable_xor)

        self.clock_enable_input.connect(self.clock_tick_gen_nor)
        self.clock_enable_input.connect(self.clock_tick_gen_and)
        self.clock_tick_gen_nor.connect(self.clock_tick_gen_and)

        self.output_tick_gen_or.connect(self.output_tick_gen_nor)
        self.output_tick_gen_or.connect(self.output_tick_gen_and)
        self.output_tick_gen_nor.connect(self.output_tick_gen_and)
        self.output_tick_gen_and.connect(self.clock_rising)
        self.output_tick_gen_and.connect(self.falling_timer)

        self.step_latch_nor_and.connect(self.step_tick_gen_nor)
        self.step_latch_nor_and.connect(self.step_tick_gen_and)

        self.step_and.connect(self.clock_enable_input)

        self.clock_enable_nor.connect(self.clock_nor_and)

        self.clock_enable_or.connect(self.clock_or_and)

        self.clock_and.connect(self.clock_nor)
        self.clock_enable_xor.connect(self.clock_and)
        self.clock_and.connect(self.output_tick_gen_or)

        if self.clock_high + self.clock_low > 4:
            self.clock_nor.connect(self.clock_timer)
            self.clock_timer.connect(self.clock_and)
        else:
            self.clock_enable_xor.connect(self.clock_and_fast)
            self.clock_nor.connect(self.clock_and_fast)
            self.clock_and_fast.connect(self.clock_nor_fast)
            self.clock_nor_fast.connect(self.clock_and)

        # visualizer
        visualizer_xor = sm.LogicGate(self.blueprint,self.id,"xor",(9 + x,1 + y,z),"up","right","222222")
        self.clock_rising.connect(visualizer_xor)
        self.clock_falling.connect(visualizer_xor)
        visualizer_xor.connect(visualizer_xor)
        visualizer_xor.connect(visualizer_xor.ID + 1)
        visualizer_xor.connect(visualizer_xor.ID + 2)
        visualizer_or = sm.LogicGate(self.blueprint,self.id,"or",(9 + x,2 + y,z),"up","right","222222")
        visualizer_or.connect(visualizer_or.ID + 2)
        visualizer_nor = sm.LogicGate(self.blueprint,self.id,"nor",(9 + x,3 + y,z),"up","right","222222")
        visualizer_nor.connect(visualizer_nor.ID + 2)
        i = 0
        for i in range(16):
            visualizer_top = sm.LogicGate(self.blueprint,self.id,"or",(9 + x - i,5 + y,z),"up","right","222222")
            visualizer_top.connect(self.id.current_ID + 2)
            visualizer_bottom = sm.LogicGate(self.blueprint,self.id,"or",(9 + x - i,4 + y,z),"up","right","222222")
            visualizer_bottom.connect(self.id.current_ID + 2)
        sm.LogicGate(self.blueprint,self.id,"or",(8 + x - i,5 + y,z),"up","right","222222")
        sm.LogicGate(self.blueprint,self.id,"or",(8 + x - i,4 + y,z),"up","right","222222")

    def connect_rising(self,clock):
        self.clock_rising.connect(clock)

    def connect_falling(self,clock):
        self.clock_falling.connect(clock)

    def connect_reset(self,clock):
        self.reset.connect(clock)

    def connect_enable(self,clock):
        self.cpu_enable.connect(clock)


    def connect(self,components):
        for each_component in components:
            component = components[each_component]
            if self != component:
                if hasattr(component, "rising"):
                    for each in component.rising:
                        each.connect(self.clock_rising)
                        print(f"connected {each.__class__.__name__} in {each_component} to clock_rising ")
                if hasattr(component, "falling"):
                    for each in component.falling:
                        each.connect(self.clock_falling)
                        print(f"connected {each.__class__.__name__} in {each_component} to clock_falling")
                if hasattr(component, "reset"):
                    for each in component.reset:
                        each.connect(self.reset)
                        print(f"connected {each.__class__.__name__} in {each_component} to reset ")
                if hasattr(component, "enable"):
                    for each in component.enable:
                        each.connect(self.cpu_enable)
                        print(f"connected {each.__class__.__name__} in {each_component} to cpu_enable ")

class GPR:
    def __init__(self,bp,id,bitness,label,pos):
        x, y, z = pos
        self.label = label
        self.memcells = [sm.LogicGate(bp,id,"xor",(x + i,2 + y,z),"up","right","0a3ee2")for i in range(bitness)]
        self.latch = [sm.LogicGate(bp,id,"and",(i + x,1 + y,z),"up","right","19e753") for i in range(bitness)]
        self.bus_input = [sm.LogicGate(bp,id,"xor",(i + x,y,z),"up","right","d02525") for i in range(bitness)]
        self.bus_output = [sm.LogicGate(bp,id,"and",(i + x,3 + y,z),"up","right","eeeeee") for i in range(bitness)]
        self.lhs_output = [sm.LogicGate(bp,id,"and",(i + x,4 + y,z),"up","right","2ce6e6") for i in range(bitness)]
        self.rhs_output = [sm.LogicGate(bp,id,"and",(i + x,5 + y,z),"up","right","cf11d2") for i in range(bitness)]

        self.write_enable = sm.LogicGate(bp,id,"or",(8 + x,2 + y,z),"up","right","19e753")
        self.clock = sm.LogicGate(bp,id,"and",(8 + x,1 + y,z),"up","right","19e753")
        self.bus_output_enable = sm.LogicGate(bp,id,"or",(8 + x,3 + y,z),"up","right","eeeeee")
        self.lhs_output_enable = sm.LogicGate(bp,id,"or",(8 + x,4 + y,z),"up","right","2ce6e6")
        self.rhs_output_enable = sm.LogicGate(bp,id,"or",(8 + x,5 + y,z),"up","right","cf11d2")

        # control
        self.control_lines = {f"{label}_Load_Main_Bus":self.write_enable,
                              f"{label}_Assert_Main_Bus":self.bus_output_enable,
                              f"{label}_Assert_LHS_Bus":self.lhs_output_enable,
                              f"{label}_Assert_RHS_Bus":self.rhs_output_enable}

        self.falling = [self.clock]

        for i in range(bitness):
            # and rhs bus out
            self.rhs_output_enable.connect(self.rhs_output[i])
            # and lhs bus out
            self.lhs_output_enable.connect(self.lhs_output[i])
            # and main bus out
            self.bus_output_enable.connect(self.bus_output[i])
            # xor memory cells
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.bus_input[i])
            self.memcells[i].connect(self.bus_output[i])
            self.memcells[i].connect(self.lhs_output[i])
            self.memcells[i].connect(self.rhs_output[i])
            # and gates for latch
            self.write_enable.connect(self.clock)
            self.clock.connect(self.latch[i])
            self.latch[i].connect(self.memcells[i])
            # xor gates for input
            self.bus_input[i].connect(self.latch[i])

class AddressRegister:
    def __init__(self,bp,id,bitness,label,pos):
        self.blueprint = bp
        self.pos = pos
        x,y,z = self.pos
        self.label = label
        self.memcells = [sm.LogicGate(bp,id,"xor",(i + x,3 + y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.transfer_bus_input = [sm.LogicGate(bp,id,"xor",(i + x,y,z),"up","right","d02525") for i in range(bitness)]
        self.latch = [sm.LogicGate(bp,id,"and",(i + x,1 + y,z),"up","right","19e753") for i in range(bitness)]
        self.address_bus_output = [sm.LogicGate(bp,id,"and",(i + x,6 + y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.transfer_bus_output = [sm.LogicGate(bp,id,"and",(i + x,5 + y,z),"up","right","eeeeee") for i in range(bitness)]
        self.not_gate = [sm.LogicGate(bp,id,"nor",(i + x,4 + y,z),"up","right","e2db13") for i in range(bitness)]
        self.inc_and = [sm.LogicGate(bp,id,"and",(i + x,2 + y,z),"up","right","eeeeee") for i in range(bitness)]

        self.write_enable = sm.LogicGate(bp,id,"or",(16 + x,y,z),"up","right","19e753")
        self.write_enable_clock = sm.LogicGate(bp,id,"and",(16 + x,1 + y,z),"up","right","19e753")
        self.address_bus_output_enable = sm.LogicGate(bp,id,"or",(16 + x,6 + y,z),"up","right","0a3ee2")
        self.transfer_bus_output_enable = sm.LogicGate(bp,id,"or",(16 + x,5 + y,z),"up","right","eeeeee")
        self.increment = sm.LogicGate(bp,id,"or",(16 + x,3 + y,z),"up","right","eeeeee")
        self.increment_clock = sm.LogicGate(bp,id,"and",(16 + x,2 + y,z),"up","right","eeeeee")
        self.decrement = sm.LogicGate(bp,id,"or",(16 + x,3 + y,z),"up","right","222222")
        self.decrement_clock = sm.LogicGate(bp,id,"nand",(16 + x,4 + y,z),"up","right","222222")

        # control
        self.control_lines = {f"{label}_Load_Transfer_Bus":self.write_enable,
                              f"{label}_Assert_Address_Bus":self.address_bus_output_enable,
                              f"{label}_Assert_Transfer_Bus":self.transfer_bus_output_enable,
                              f"{label}_Increment":self.increment,
                              f"{label}_Decrement":self.decrement}

        self.rising = [self.increment_clock,self.decrement_clock]
        self.falling = [self.write_enable_clock]
        self.enable = [self.increment_clock,self.decrement_clock]

        # logic
        self.decrement.connect(self.decrement_clock)
        self.increment.connect(self.increment_clock)
        self.write_enable.connect(self.write_enable_clock)

        for i in range(bitness):
            # and gates address bus output
            self.address_bus_output_enable.connect(self.address_bus_output[i])
            # and gates transfer bus output
            self.transfer_bus_output_enable.connect(self.transfer_bus_output[i])
            # nor gates for decrement instruction
            self.not_gate[i].connect(self.memcells[i])
            self.decrement_clock.connect(self.not_gate[i])
            # xor gates for memory cells
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.transfer_bus_input[i])
            self.memcells[i].connect(self.transfer_bus_output[i])
            self.memcells[i].connect(self.address_bus_output[i])
            self.decrement_clock.connect(self.not_gate[i])

            # and gates for latch
            self.write_enable_clock.connect(self.latch[i])
            self.latch[i].connect(self.memcells[i])
            # xor for address bus input
            self.transfer_bus_input[i].connect(self.latch[i])
        for i in range(bitness):
            # and gates for increment instruction
            for j in range((bitness-1) - i):
                self.memcells[(bitness-1) - i].connect(self.not_gate[j])

            self.inc_and[i].connect(self.memcells[i])
            self.increment_clock.connect(self.inc_and[i])
            # connections for increment instruction
            for j in range((bitness-1) - i):
                self.memcells[(bitness-1) - i].connect(self.inc_and[j])

class Bus:
    def __init__(self,bp,id,bitness,name,pos,color):
        self.name = name
        self.pos = pos
        self.color = color
        self.bitness = bitness
        x, y, z = self.pos
        self.Bus = [sm.LogicGate(bp,id,"or",(i + x,y,z),"up","right",color) for i in range(bitness)]

    def connect(self,device):
        if device.__getattribute__(self.name+"_bus_output"):
            outputs = device.__getattribute__(self.name+"_bus_output")
            for i in range(len(outputs)):
                outputs[i].connect(self.Bus[i])
        else:
            print("device has no output gates for this bus")

        if device.__getattribute__(self.name+"_bus_input"):
            inputs = device.__getattribute__(self.name+"_bus_input")
            for i in range(len(inputs)):
                self.Bus[i].connect(inputs[i])
        else:
            print("device has no input gates for this bus")


    def connect_to_bus(self,IDs):
        for i in range(len(IDs)):
            if IDs[i] is not None:
                IDs[i].connect(self.Bus[i])

    def connect_from_bus(self,IDs):
        for i in range(len(IDs)):
            if IDs[i] is not None:
                self.Bus[i].connect(IDs[i])

class TransferRegister:
    def __init__(self,bp,id,bitness,label,pos):
        x,y,z = pos
        self.label = label
        self.memcells = [sm.LogicGate(bp,id,"xor",(i + x,4 + y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.transfer_bus_input = [sm.LogicGate(bp,id,"xor",(i + x,y,z),"up","right","eeeeee") for i in range(bitness)]
        self.transfer_bus_latch = [sm.LogicGate(bp,id,"and",(i + x,2 + y,z),"up","right","eeeeee") for i in range(bitness)]
        self.transfer_bus_output = [sm.LogicGate(bp,id,"and",(i + x,5 + y,z),"up","right","eeeeee") for i in range(bitness)]
        self.main_bus_input = [sm.LogicGate(bp,id,"xor",(i + x,1 + y,z),"up","right","d02525") for i in range(bitness)]
        self.main_bus_latch = [sm.LogicGate(bp,id,"and",(i + x,3 + y,z),"up","right","d02525") for i in range(bitness)]
        self.main_bus_output = [sm.LogicGate(bp,id,"and",(i + x,6 + y,z),"up","right","d02525") for i in range(bitness)]


        self.main_bus_write_clock = sm.LogicGate(bp,id,"and",(8 + x,2 + y,z),"up","right","d02525")
        self.transfer_bus_write_clock = sm.LogicGate(bp,id,"and",(8 + x,y,z),"up","right","7f7f7f")
        self.main_bus_output_enable = sm.LogicGate(bp,id,"or",(8 + x,6 + y,z),"up","right","d02525")
        self.transfer_bus_output_enable = sm.LogicGate(bp,id,"or",(8 + x,5 + y,z),"up","right","7f7f7f")

        self.main_bus_write_enable = sm.LogicGate(bp,id,"or",(8 + x,3 + y,z),"up","right","d02525")
        self.transfer_bus_write_enable = sm.LogicGate(bp,id,"or",(8 + x,1 + y,z),"up","right","7f7f7f")

        # control
        self.control_lines = {f"{label}_Load_Main_Bus": self.main_bus_write_enable,
                              f"{label}_Assert_Main_Bus": self.main_bus_output_enable,
                              f"{label}_Load_Transfer_Bus": self.transfer_bus_write_enable,
                              f"{label}_Assert_Transfer_Bus": self.transfer_bus_output_enable}

        self.falling = [self.transfer_bus_write_clock,self.main_bus_write_clock]

        # logic
        self.transfer_bus_write_enable.connect(self.transfer_bus_write_clock)

        for i in range(bitness):
            # and gates for main bus output
            self.main_bus_output_enable.connect(self.main_bus_output[i])
            # and gates for address bus output

            self.transfer_bus_output_enable.connect(self.transfer_bus_output[i])
            # xor gates for memory cells
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.transfer_bus_input[i])
            self.memcells[i].connect(self.main_bus_input[i])
            self.memcells[i].connect(self.transfer_bus_output[i])
            self.memcells[i].connect(self.main_bus_output[i])
            # and gates for main bus latch
            self.main_bus_latch[i].connect(self.memcells[i])
            self.main_bus_write_clock.connect(self.main_bus_latch[i])
            # and gates for address bus latch
            self.transfer_bus_latch[i].connect(self.memcells[i])
            self.transfer_bus_write_clock.connect(self.transfer_bus_latch[i])
            # xor gates for main bus input
            self.main_bus_input[i].connect(self.main_bus_latch[i])
            # xor gates for address bus input
            self.transfer_bus_input[i].connect(self.transfer_bus_latch[i])

class Fetch:
    def __init__(self,bp,id,bitness,pos):
        x,y,z = pos
        self.fetch_input = [sm.LogicGate(bp,id,"or",(i + x,y,z),"up","right","222222") for i in range(bitness)]
        self.fetch_output = [sm.LogicGate(bp,id,"and",(i + x,1 + y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.fetch_denied = sm.LogicGate(bp,id,"nor",(8 + x,1 + y,z),"up","right","0a3ee2")

        # control
        self.control_lines = {"Fetch_Denied":self.fetch_denied}

        # logic
        for i in range(8):
            self.fetch_denied.connect(self.fetch_output[i])
            self.fetch_input[i].connect(self.fetch_output[i])

class PipeLine:
    def __init__(self,bp,id,bitness,pos):
        x,y,z = pos
        self.memcells = [sm.LogicGate(bp,id,"xor",(i + x,2 + y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.latch = [sm.LogicGate(bp,id,"and",(i + x,1 + y,z),"up","right","19e753") for i in range(bitness)]
        self.input = [sm.LogicGate(bp,id,"xor",(i + x,y,z),"up","right","d02525") for i in range(bitness)]
        self.clock = sm.LogicGate(bp,id,"or",(8 + x,1 + y,z),"up","right","19e753")

        # control
        self.falling = [self.clock]

        # logic
        for i in range(8):
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.input[i])
            self.latch[i].connect(self.memcells[i])
            self.clock.connect(self.latch[i])
            self.input[i].connect(self.latch[i])

class MemoryMap:
    def __init__(self,bp,id,total_memory,chunk_size,bitness,pos,color):
        self.pos = pos
        self.color = color
        self.total_memory = total_memory
        self.chunk_size = chunk_size
        self.bitness = bitness
        x,y,z = self.pos

        self.chunk_selectors = []

        self.input = [sm.LogicGate(bp,id,"or",(x,i+y,z),"up","right","d02525") for i in range(bitness)]
        self.input_not = [sm.LogicGate(bp,id,"nor",(x+1,i+y,z),"up","right","d02525") for i in range(bitness)]
        for i in range(int(2 ** self.bitness/self.bitness)):
            for j in range(self.bitness):
                self.chunk_selectors.append(sm.LogicGate(bp, id, "and", (i + x + 2, j + y, z), "up", "right", color))

        count = 0
        for i in range(int(2 ** self.bitness/self.bitness)):
            for j in range(self.bitness):
                mask = 1
                for k in range(self.bitness):
                    if count & mask == mask:
                        self.input[k].connect(self.chunk_selectors[count])
                    else:
                        self.input_not[k].connect(self.chunk_selectors[count])
                    mask = mask << 1
                count += 1

        self.input.reverse()
        self.input_not.reverse()

    def map(self,enables,chunk):
        for each in enables:
            self.chunk_selectors[chunk].connect(each)

class Rom:
    def __init__(self,bp,id,bitness_in,path,bitness_out,pos,color):

        px,py,pz = pos

        self.output = [sm.LogicGate(bp,id,"or",(2+px + int(2 ** bitness_in / bitness_out),x + py,pz),"up","right","0a3ee2") for x in range(bitness_out)]

        self.input = [sm.LogicGate(bp,id,"and",(px,x + py,pz),"up","right","d02525") for x in range(bitness_in)]
        self.input_not = [sm.LogicGate(bp,id,"nand",(px+1,x + py,pz),"up","right","d02525") for x in range(bitness_in)]

        self.memory_map = (self.input+self.input_not+[id.current_ID+1])

        with open(path,"r") as rom:
            lines = rom.read().splitlines()
            count = 0
            for y in range(int(2 ** bitness_in / bitness_out)):
                for x in range(len(self.output)):
                    gate = sm.LogicGate(bp,id,"and",(y + px+2,x + py,pz),"up","right",color)
                    data = 0
                    line = ""
                    if len(lines)>0:
                        line = lines.pop(0)
                    if line.isnumeric():
                        data = int(line)

                    mask = 1
                    for i in range(bitness_in):
                        if count & mask == mask:
                            self.input[i].connect(gate)
                        else:
                            self.input_not[i].connect(gate)
                        mask = mask << 1
                    mask = 1
                    for i in range(bitness_out):
                        if data & mask == mask:
                            gate.connect(self.output[i])
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
    def __init__(self,bp,id,bitness,label,pos):
        x,y,z = pos
        self.label = label
        self.memcells = [sm.LogicGate(bp,id,"xor",(x + i,2 + y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.latch = [sm.LogicGate(bp,id,"and",(i + x,1 + y,z),"up","right","19e753") for i in range(bitness)]
        self.bus_input = [sm.LogicGate(bp,id,"xor",(i + x,y,z),"up","right","d02525") for i in range(bitness)]
        self.bus_output = [sm.LogicGate(bp,id,"and",(i + x,3 + y,z),"up","right","eeeeee") for i in range(bitness)]

        self.write_enable = sm.LogicGate(bp,id,"or",(8 + x,2 + y,z),"up","right","19e753")
        self.clock = sm.LogicGate(bp,id,"and",(8 + x,1 + y,z),"up","right","19e753")
        self.bus_output_enable = sm.LogicGate(bp,id,"or",(8 + x,3 + y,z),"up","right","eeeeee")

        # control
        self.control_lines = {f"{label}_Load":self.write_enable,
                              f"{label}_Assert":self.bus_output_enable}

        self.falling = [self.clock]

        self.write_enable.connect(self.clock)
        for i in range(bitness):
            # and main bus out
            self.bus_output_enable.connect(self.bus_output[i])
            # xor memory cells
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.bus_input[i])
            self.memcells[i].connect(self.bus_output[i])
            # and gates for latch
            self.clock.connect(self.latch[i])
            self.latch[i].connect(self.memcells[i])
            # xor gates for input
            self.bus_input[i].connect(self.latch[i])

class RegisterNoOutput:
    def __init__(self,bp,id,bitness,label,pos):
        x,y,z = pos
        self.label = label
        self.memcells = [sm.LogicGate(bp,id,"xor",(x + i,2 + y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.latch = [sm.LogicGate(bp,id,"and",(i + x,1 + y,z),"up","right","19e753") for i in range(bitness)]
        self.bus_input = [sm.LogicGate(bp,id,"xor",(i + x,y,z),"up","right","d02525") for i in range(bitness)]

        self.write_enable = sm.LogicGate(bp,id,"or",(bitness + x,2 + y,z),"up","right","19e753")
        self.clock = sm.LogicGate(bp,id,"and",(bitness + x,1 + y,z),"up","right","19e753")

        # control
        self.control_lines = {f"{label}_Load": self.write_enable}

        self.falling = [self.clock]

        # logic
        self.write_enable.connect(self.clock)

        for i in range(bitness):
            # xor memory cells
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.bus_input[i])
            # and gates for latch
            self.clock.connect(self.latch[i])
            self.latch[i].connect(self.memcells[i])
            # xor gates for input
            self.bus_input[i].connect(self.latch[i])

class Bitwise:
    def __init__(self,bp,id,bitness,pos):
        self.blueprint = bp
        self.ID = id
        self.bitness = bitness
        self.pos = pos
        x,y,z = pos

        self.or_ctrl = sm.LogicGate(bp,id,"or",(bitness + x,8 + y,z),"up","right","cf11d2")
        self.and_ctrl = sm.LogicGate(bp,id,"or",(bitness + x,7 + y,z),"up","right","cf11d2")
        self.xor_ctrl = sm.LogicGate(bp,id,"or",(bitness + x,5 + y,z),"up","right","cf11d2")
        self.nor_ctrl = sm.LogicGate(bp,id,"nor",(bitness + x,4 + y,z),"up","right","cf11d2")
        self.pass_ctrl = sm.LogicGate(bp,id,"or",(bitness + x,y+3,z),"up","right","cf11d2")
        self.fill_ctrl = sm.LogicGate(bp,id,"or",(bitness + x,9 + y,z),"up","right","cf11d2")
        self.carry_ctrl = sm.LogicGate(bp,id,"or",(bitness + x,6 + y,z),"up","right","cf11d2")

        self.or_gates = [sm.LogicGate(bp,id,"or",(i + x,9 + y,z),"up","right","cf11d2") for i in range(bitness)]
        self.or_and_gates = [sm.LogicGate(bp,id,"and",(i + x,8 + y,z),"up","right","cf11d2") for i in range(bitness)]
        self.and_gates = [sm.LogicGate(bp,id,"and",(i + x,7 + y,z),"up","right","cf11d2") for i in range(bitness)]
        self.xor_gates = [sm.LogicGate(bp,id,"xor",(i + x,6 + y,z),"up","right","cf11d2") for i in range(bitness)]
        self.xor_and_gates = [sm.LogicGate(bp,id,"and",(i + x,5 + y,z),"up","right","cf11d2") for i in range(bitness)]
        self.nor_gates = [sm.LogicGate(bp,id,"nor",(i + x,4 + y,z),"up","right","cf11d2") for i in range(bitness)]
        self.pass_gates = [sm.LogicGate(bp,id,"and",(i + x,y+3,z),"up","right","cf11d2") for i in range(bitness)]

        self.memcells = [sm.LogicGate(bp, id, "xor", (x + i, 2 + y, z), "up", "right", "0a3ee2") for i in range(bitness)]
        self.latch = [sm.LogicGate(bp, id, "and", (i + x, 1 + y, z), "up", "right", "19e753") for i in range(bitness)]
        self.bus_input = [sm.LogicGate(bp, id, "xor", (i + x, y, z), "up", "right", "d02525") for i in range(bitness)]

        self.write_enable = sm.LogicGate(bp, id, "or", (bitness + x, 2 + y, z), "up", "right", "19e753")
        self.clock = sm.LogicGate(bp, id, "and", (bitness + x, 1 + y, z), "up", "right", "19e753")

        self.write_enable.connect(self.clock)

        for i in range(bitness):
            # xor memory cells
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.bus_input[i])
            # and gates for latch
            self.clock.connect(self.latch[i])
            self.latch[i].connect(self.memcells[i])
            # xor gates for input
            self.bus_input[i].connect(self.latch[i])
            self.or_and_gates[i].connect(self.bus_input[i])
            self.and_gates[i].connect(self.bus_input[i])
            self.xor_and_gates[i].connect(self.bus_input[i])
            self.nor_gates[i].connect(self.bus_input[i])
            self.pass_gates[i].connect(self.bus_input[i])
            self.fill_ctrl.connect(self.bus_input[i])

        self.carry_ctrl.connect(self.bus_input[-1])

        # control
        self.control_lines = {"Bitwise_Or": self.or_ctrl,
                              "Bitwise_And": self.and_ctrl,
                              "Bitwise_Xor": self.xor_ctrl,
                              "Bitwise_Nor": self.nor_ctrl,
                              "Bitwise_Pass": self.pass_ctrl,
                              "Bitwise_Fill": self.fill_ctrl,
                              "Bitwise_Carry": self.carry_ctrl,
                              "Bitwise_Load": self.write_enable}

        for i in range(bitness):
            self.or_gates[i].connect(self.or_and_gates[i])
            self.or_ctrl.connect(self.or_and_gates[i])
            self.and_ctrl.connect(self.and_gates[i])
            self.xor_gates[i].connect(self.xor_and_gates[i])
            self.xor_ctrl.connect(self.xor_and_gates[i])
            self.nor_ctrl.connect(self.nor_gates[i])
            self.pass_ctrl.connect(self.pass_gates[i])

    def connect(self,bus1,bus2):
        for i in range(self.bitness):
            bus1[i].connect(self.or_gates[i])
            bus1[i].connect(self.and_gates[i])
            bus1[i].connect(self.xor_gates[i])
            bus1[i].connect(self.nor_gates[i])
            bus1[i].connect(self.pass_gates[i])

            bus2[i].connect(self.or_gates[i])
            bus2[i].connect(self.and_gates[i])
            bus2[i].connect(self.xor_gates[i])

class Shift:
    def __init__(self,bp,id,bitness,pos):
        self.blueprint = bp
        self.bitness = bitness
        self.pos = pos
        x, y, z = pos

        self.shr_ctrl = sm.LogicGate(bp,id,"or",(self.bitness + x,y+5,z),"up","right","2ce6e6")
        self.shl_ctrl = sm.LogicGate(bp,id,"or",(self.bitness + x,y+4,z),"up","right","2ce6e6")
        self.pass_ctrl = sm.LogicGate(bp,id,"or",(self.bitness + x,y+3,z),"up","right","2ce6e6")

        self.shr_gates = [sm.LogicGate(bp,id,"and",(i + x,y+5,z),"up","right","2ce6e6") for i in range(self.bitness)]
        self.shl_gates = [sm.LogicGate(bp,id,"and",(i + x,y+4,z),"up","right","2ce6e6") for i in range(self.bitness)]
        self.pass_gates = [sm.LogicGate(bp,id,"and",(i + x,y+3,z),"up","right","2ce6e6") for i in range(self.bitness)]


        self.memcells = [sm.LogicGate(bp, id, "xor", (x + i,y+2, z), "up", "right", "0a3ee2") for i in range(bitness)]
        self.latch = [sm.LogicGate(bp, id, "and", (i + x, y+1, z), "up", "right", "19e753") for i in range(bitness)]
        self.bus_input = [sm.LogicGate(bp, id, "xor", (i + x, y, z), "up", "right", "d02525") for i in range(bitness)]

        self.write_enable = sm.LogicGate(bp, id, "or", (bitness + x, 2 + y, z), "up", "right", "19e753")
        self.clock = sm.LogicGate(bp, id, "and", (bitness + x, 1 + y, z), "up", "right", "19e753")

        self.write_enable.connect(self.clock)

        for i in range(bitness):
            # xor memory cells
            self.memcells[i].connect(self.memcells[i])
            self.memcells[i].connect(self.bus_input[i])
            # and gates for latch
            self.clock.connect(self.latch[i])
            self.latch[i].connect(self.memcells[i])
            # xor gates for input
            self.bus_input[i].connect(self.latch[i])

        shift_left = self.shl_gates[1:] + [self.shl_gates[0]]
        shift_right = [self.shr_gates[-1]]+self.shr_gates[:-1]
        shift_pass = self.pass_gates

        for i in range(self.bitness):
            shift_left[i].connect(self.bus_input[i])
            shift_right[i].connect(self.bus_input[i])
            shift_pass[i].connect(self.bus_input[i])

        # control
        self.control_lines = {"Shift_Right": self.shr_ctrl,
                              "Shift_Left": self.shl_ctrl,
                              "Shift_Pass": self.pass_ctrl,
                              "Shift_Load": self.write_enable}

        self.control_flags = {"Logic_Carry_Flag": self.memcells[0]}

        for i in range(self.bitness):
            self.shr_ctrl.connect(self.shr_gates[i])
            self.shl_ctrl.connect(self.shl_gates[i])
            self.pass_ctrl.connect(self.pass_gates[i])

    def connect(self,bus1):
        for i in range(len(bus1)):
            bus1[i].connect(self.shr_gates[i])
            bus1[i].connect(self.shl_gates[i])
            bus1[i].connect(self.pass_gates[i])


    def carry(self,carry_id):
        carry_id.connect(self.pass_gates[-1])
        carry_id.connect(self.shr_gates[-1])
        carry_id.connect(self.shl_gates[-1])

class CLA:
    def __init__(self,bp,id,bitness,pos):
        self.blueprint = bp
        self.ID = id
        self.bitness = bitness
        self.pos = pos
        x,y,z = pos

        self.output_enable = sm.LogicGate(bp,id,"or",(bitness+x,y,z),"up","right","0a3ee2")

        self.output = [sm.LogicGate(bp,id,"and",(i + x,y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.in_nor = [sm.LogicGate(bp,id,"nor",(bitness - i + x - 1,5 + bitness + y,z),"up","right","e2db13") for i in range(bitness)]
        self.in_nand = [sm.LogicGate(bp,id,"nand",(bitness - i + x - 1,4 + bitness + y,z),"up","right","e2db13") for i in range(bitness)]
        self.out_xor = [sm.LogicGate(bp,id,"xor",(bitness - i + x - 1,1 + y,z),"up","right","e2db13") for i in range(bitness)]
        self.out_and = [sm.LogicGate(bp,id,"and",(bitness - i + x - 1,2 + y,z),"up","right","e2db13") for i in range(bitness)]
        self.out_nor1 = [sm.LogicGate(bp,id,"nor",(bitness - i + x - 1,4 + y,z),"up","right","e2db13") for i in range(bitness)]
        self.out_nor2 = [sm.LogicGate(bp,id,"nor",(bitness - i + x - 1,3 + y,z),"up","right","e2db13") for i in range(bitness)]

        self.carry = sm.LogicGate(bp,id,"nor",(bitness + x,3 + y,z),"up","right","e2db13")
        self.carry_or = sm.LogicGate(bp,id,"or",(bitness + x,5 + bitness + y,z),"up","right","e2db13")
        self.carry_nor = sm.LogicGate(bp,id,"nor",(bitness + x,4 + bitness + y,z),"up","right","e2db13")
        self.carry_gates = [sm.LogicGate(bp,id,"and",(bitness + x,3 + bitness + y - i,z),"up","right","e2db13") for i in range(bitness)]


        self.OverFlow = sm.LogicGate(bp,id,"xor",(bitness - 2 + x,6 + y,z),"up","right","222222")
        self.OF_Xor_A = sm.LogicGate(bp,id,"xor",(bitness - 2 + x, 7 + y,z),"up","right","222222")
        self.OF_Xor_B = sm.LogicGate(bp,id,"and",(bitness - 2 + x, 8 + y,z),"up","right","222222")

        self.Zero_flag = sm.LogicGate(bp,id,"nor",(bitness - 4 + x,6 + y,z),"up","right","222222")

        self.carry_loop_and = sm.LogicGate(bp,id,"and",(bitness - 3 + x, 7+ y,z),"up","right","222222")
        self.carry_loop_or = sm.LogicGate(bp,id,"or",(bitness - 3 + x, 6+ y,z),"up","right","222222")


        # control
        self.control_lines = {"ALU_Assert": self.output_enable,
                              "ALU_Loop_Carry": self.carry_loop_or}

        self.control_flags = {"ALU_Zero_Flag": self.Zero_flag,
                              "ALU_Over_Flow_Flag": self.OverFlow,
                              "ALU_Carry_Flag": self.carry,
                              "ALU_Sign_Flag":self.out_xor[0]}

        self.out_xor[0].color = colors.Blue_Diamond

        self.carry_or.connect(self.carry_nor)
        self.carry_nor.connect(self.out_nor1[0])
        for i in range(bitness):
            for j in range(i):
                j += 1
                temp = sm.LogicGate(bp,id,"and",(bitness - i + x - 1,4 + bitness - j + y,z),"up","right","e2db13")
                temp.connect(self.out_nor1[i])
                self.in_nand[i].connect(self.carry_gates[j])
                if j == 1:
                    self.carry_nor.connect(temp)

                for k in range(bitness):
                    if k + 1 >= j:
                        if k != i:
                            self.in_nand[k].connect(temp)

                for l in range(bitness):
                    l += 1
                    if j == l + 1:
                        if l >= 1:
                            pass
                            self.in_nor[l - 1].connect(temp)

            if i < bitness - 1:
                self.in_nor[i].connect(self.out_nor1[i + 1])
                self.in_nor[i].connect(self.carry_gates[i + 1])

            self.output_enable.connect(self.output[i])
            self.out_xor[i].connect(self.output[-i-1])
            self.in_nand[i].connect(self.out_and[i])
            self.in_nor[i].connect(self.out_nor2[i])
            self.out_nor1[i].connect(self.out_xor[i])
            self.out_nor2[i].connect(self.out_and[i])
            self.out_and[i].connect(self.out_xor[i])
            self.carry_gates[i].connect(self.carry)
            self.in_nand[i].connect(self.carry_gates[0])
            self.out_xor[i].connect(self.Zero_flag)

        self.in_nor[-1].connect(self.carry)

        self.out_xor[-1].connect(self.OF_Xor_A)
        self.OF_Xor_A.connect(self.OverFlow)
        self.out_xor[-1].connect(self.OF_Xor_B)
        self.OF_Xor_B.connect(self.OverFlow)

        self.carry.connect(self.carry_loop_and)
        self.carry_loop_or.connect(self.carry_loop_and)

    def connect(self,lhs,rhs):
        for i in range(self.bitness):
            lhs[i].connect(self.in_nand[-i - 1])
            lhs[i].connect(self.in_nor[-i - 1])
            rhs[i].connect(self.in_nand[-i - 1])
            rhs[i].connect(self.in_nor[-i - 1])
        lhs[-1].connect(self.carry_or)
        rhs[-1].connect(self.carry_or)
        lhs[-2].connect(self.OF_Xor_A)
        rhs[-2].connect(self.OF_Xor_B)

class MemoryBridge:
    def __init__(self,bp,id,bitness,pos):
        x, y, z = pos
        self.main_data_enable = sm.LogicGate(bp,id,"or",(bitness + x,y,z),"up","right","0a3ee2")
        self.data_main_enable = sm.LogicGate(bp,id,"or",(bitness + x,y+1,z),"up","right","0a3ee2")

        self.main_data = [sm.LogicGate(bp,id,"and",(i + x,y,z),"up","right","0a3ee2") for i in range(bitness)]
        self.data_main = [sm.LogicGate(bp,id,"and",(i + x,y+1,z),"up","right","0a3ee2") for i in range(bitness)]


        # control
        self.control_lines = {"Memory_Bridge_Main_Data": self.main_data_enable,
                              "Memory_Bridge_Data_Main": self.data_main_enable}

        for i in range(bitness):
            self.main_data_enable.connect(self.main_data[i])
            self.data_main_enable.connect(self.data_main[i])

class OpCodes:
    def __init__(self,blueprint,ID,bitness,pos):
        self.blueprint = blueprint
        self.ID = ID
        self.bitness = bitness
        self.flags = {}
        self.pos = pos
        self.lines = {}
        self.Opcodes = {}
        self.control_lines = {}
        self.flags = {}

    def createOpcodes(self):
        try:
            import opcodes_list
            oc = opcodes_list.Control_Lines()
            cf = opcodes_list.Control_Flags()
        except:
            print("could not import opcodes")
            exit(1)
            
        self.Opcodes["No_operation"] = [[0],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[]]

        self.Opcodes["Move_A_Constant"] = [[1],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load,oc.Fetch_Denied],[oc.Constant_Assert,oc.A_Load_Main_Bus]]
        self.Opcodes["Move_B_Constant"] = [[2],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load,oc.Fetch_Denied],[oc.Constant_Assert,oc.B_Load_Main_Bus]]
        self.Opcodes["Move_C_Constant"] = [[3],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load,oc.Fetch_Denied],[oc.Constant_Assert,oc.C_Load_Main_Bus]]
        self.Opcodes["Move_D_Constant"] = [[4],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load,oc.Fetch_Denied],[oc.Constant_Assert,oc.D_Load_Main_Bus]]
        self.Opcodes["Move_TL_Constant"] = [[5],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load,oc.Fetch_Denied],[oc.Constant_Assert,oc.RHS_Load_Main_Bus]]
        self.Opcodes["Move_TH_Constant"] = [[6],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.Constant_Load,oc.Fetch_Denied],[oc.Constant_Assert,oc.LHS_Load_Main_Bus]]

        self.Opcodes["Move_B_into_A"] = [[7],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.B_Assert_Main_Bus,oc.A_Load_Main_Bus]]
        self.Opcodes["Move_C_into_A"] = [[8],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.A_Load_Main_Bus]]
        self.Opcodes["Move_D_into_A"] = [[9],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.D_Assert_Main_Bus,oc.A_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_A"] = [[10],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.RHS_Assert_Main_Bus,oc.A_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_A"] = [[11],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Main_Bus,oc.A_Load_Main_Bus]]

        self.Opcodes["Move_A_into_B"] = [[12],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.A_Assert_Main_Bus,oc.B_Load_Main_Bus]]
        self.Opcodes["Move_C_into_B"] = [[13],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.B_Load_Main_Bus]]
        self.Opcodes["Move_D_into_B"] = [[14],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.D_Assert_Main_Bus,oc.B_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_B"] = [[15],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.RHS_Assert_Main_Bus,oc.B_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_B"] = [[16],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Main_Bus,oc.B_Load_Main_Bus]]

        self.Opcodes["Move_A_into_C"] = [[17],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.B_Assert_Main_Bus,oc.C_Load_Main_Bus]]
        self.Opcodes["Move_B_into_C"] = [[18],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.C_Load_Main_Bus]]
        self.Opcodes["Move_D_into_C"] = [[19],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.D_Assert_Main_Bus,oc.C_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_C"] = [[20],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.RHS_Assert_Main_Bus,oc.C_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_C"] = [[21],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Main_Bus,oc.C_Load_Main_Bus]]

        self.Opcodes["Move_A_into_D"] = [[22],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.A_Assert_Main_Bus,oc.D_Load_Main_Bus]]
        self.Opcodes["Move_B_into_D"] = [[23],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.B_Assert_Main_Bus,oc.D_Load_Main_Bus]]
        self.Opcodes["Move_C_into_D"] = [[24],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.D_Load_Main_Bus]]
        self.Opcodes["Move_TL_into_D"] = [[25],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.RHS_Assert_Main_Bus,oc.D_Load_Main_Bus]]
        self.Opcodes["Move_TH_into_D"] = [[26],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Main_Bus,oc.D_Load_Main_Bus]]

        self.Opcodes["Move_A_into_TL"] = [[27],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.A_Assert_Main_Bus,oc.RHS_Load_Main_Bus]]
        self.Opcodes["Move_B_into_TL"] = [[28],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.B_Assert_Main_Bus,oc.RHS_Load_Main_Bus]]
        self.Opcodes["Move_C_into_TL"] = [[29],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.RHS_Load_Main_Bus]]
        self.Opcodes["Move_D_into_TL"] = [[30],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.D_Assert_Main_Bus,oc.RHS_Load_Main_Bus]]

        self.Opcodes["Move_A_into_TH"] = [[31],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.A_Assert_Main_Bus,oc.LHS_Load_Main_Bus]]
        self.Opcodes["Move_B_into_TH"] = [[32],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.B_Assert_Main_Bus,oc.LHS_Load_Main_Bus]]
        self.Opcodes["Move_C_into_TH"] = [[33],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.LHS_Load_Main_Bus]]
        self.Opcodes["Move_D_into_TH"] = [[34],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.D_Assert_Main_Bus,oc.LHS_Load_Main_Bus]]

        self.Opcodes["Move_A_into_si"] = [[35],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.A_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]
        self.Opcodes["Move_B_into_si"] = [[36],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.B_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]
        self.Opcodes["Move_C_into_si"] = [[37],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]
        self.Opcodes["Move_D_into_si"] = [[38],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.D_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Source_Index_Assert_Address_Bus]]

        self.Opcodes["Move_A_into_di"] = [[39],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.A_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]
        self.Opcodes["Move_B_into_di"] = [[40],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.B_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]
        self.Opcodes["Move_C_into_di"] = [[41],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.C_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]
        self.Opcodes["Move_D_into_di"] = [[42],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.D_Assert_Main_Bus,oc.Fetch_Denied,oc.Memory_Bridge_Main_Data,oc.Destination_Index_Assert_Address_Bus]]

        self.Opcodes["Move_tx_into_ra"] = [[51],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Transfer_Bus,oc.RHS_Assert_Transfer_Bus,oc.Return_Address_Load_Transfer_Bus]]
        self.Opcodes["Move_ra_into_tx"] = [[52],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Return_Address_Assert_Transfer_Bus,oc.LHS_Load_Transfer_Bus,oc.RHS_Load_Transfer_Bus]]
        self.Opcodes["Move_tx_into_sp"] = [[53],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Transfer_Bus,oc.RHS_Assert_Transfer_Bus,oc.Stack_Pointer_Load_Transfer_Bus]]
        self.Opcodes["Move_sp_into_tx"] = [[54],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Stack_Pointer_Assert_Transfer_Bus,oc.LHS_Load_Transfer_Bus,oc.RHS_Load_Main_Bus]]
        self.Opcodes["Move_tx_into_si"] = [[55],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Transfer_Bus,oc.RHS_Assert_Transfer_Bus,oc.Source_Index_Load_Transfer_Bus]]
        self.Opcodes["Move_si_into_tx"] = [[56],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Source_Index_Assert_Transfer_Bus,oc.LHS_Load_Transfer_Bus,oc.RHS_Load_Transfer_Bus]]
        self.Opcodes["Move_tx_into_di"] = [[57],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.LHS_Assert_Transfer_Bus,oc.RHS_Assert_Transfer_Bus,oc.Destination_Index_Load_Transfer_Bus]]
        self.Opcodes["Move_di_into_tx"] = [[58],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus],[oc.Destination_Index_Assert_Transfer_Bus,oc.LHS_Load_Transfer_Bus,oc.RHS_Load_Transfer_Bus]]
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

        jump = [oc.LHS_Assert_Transfer_Bus,oc.RHS_Assert_Transfer_Bus,oc.Program_Counter_Load_Transfer_Bus,oc.Fetch_Denied]

        self.Opcodes["Jump_tx"] = [[73],[oc.LHS_Assert_Transfer_Bus,oc.RHS_Assert_Transfer_Bus,oc.Program_Counter_Load_Transfer_Bus],[]]
        self.Opcodes["Jump_di"] = [[74],[oc.Destination_Index_Assert_Transfer_Bus,oc.Program_Counter_Load_Transfer_Bus],[]]

        self.Opcodes["jo_tx"] = [[75,(cf.ALU_Over_Flow_Flag,True)],jump,[]]
        self.Opcodes["jno_di"] = [[76,(cf.ALU_Over_Flow_Flag,False)],jump,[]]
        self.Opcodes["js_tx"] = [[77,(cf.ALU_Sign_Flag,True)],jump,[]]
        self.Opcodes["jns_tx"] = [[78,(cf.ALU_Sign_Flag,False)],jump,[]]
        self.Opcodes["jz_tx"] = [[79,(cf.ALU_Zero_Flag,True)],jump,[]]
        self.Opcodes["jnz_tx"] = [[80,(cf.ALU_Zero_Flag,False)],jump,[]]
        #self.Opcodes["je_tx"] = [[79,(cf.ALU_Zero_Flag,True)],jump,[]]
        #self.Opcodes["jne_tx"] = [[80,(cf.ALU_Zero_Flag,False)],jump,[]]

        self.Opcodes["jump_Arithmetic_Carry"] = [[81,(cf.ALU_Carry_Flag,True)],jump,[]]
        self.Opcodes["jump_not_Arithmetic_Carry"] = [[82,(cf.ALU_Carry_Flag,False)],jump,[]]
        self.Opcodes["jump_Carry_Or_Zero"] = [[83,(cf.ALU_Carry_Flag,True)],jump,[]]
        #self.Opcodes["jump_Carry_Or_Zero"] = [[83,(cf.ALU_Zero_Flag,True)],jump,[]]
        self.Opcodes["jump_Not_Carry_And_Not_Zero"] = [[84,(cf.ALU_Carry_Flag,False),(cf.ALU_Zero_Flag,False)],jump,[]]

        self.Opcodes["jump_Sign_Not_Equal_Overflow"] = [[85,(cf.ALU_Sign_Flag,False),(cf.ALU_Sign_Flag,True)],jump,[]]
        #self.Opcodes["jump_Sign_Not_Equal_Overflow"] = [[85,(cf.ALU_Sign_Flag,True),(cf.ALU_Sign_Flag,False)],jump,[]]
        self.Opcodes["jump_Sign_Equal_Overflow"] = [[86,(cf.ALU_Sign_Flag,True),(cf.ALU_Sign_Flag,True)],jump,[]]
        #self.Opcodes["jump_Sign_Equal_Overflow"] = [[86,(cf.ALU_Sign_Flag,False),(cf.ALU_Sign_Flag,False)],jump,[]]
        self.Opcodes["jump_Zero_Or_Sign_Equal_Overflow"] = [[87,(cf.ALU_Zero_Flag,True),(cf.ALU_Sign_Flag,True),(cf.ALU_Sign_Flag,True)],jump,[]]
        #self.Opcodes["jump_Zero_Or_Sign_Equal_Overflow"] = [[87,(cf.ALU_Zero_Flag,True),(cf.ALU_Sign_Flag,False),(cf.ALU_Sign_Flag,False)],jump,[]]
        self.Opcodes["jump_Not_Zero_Or_Sign_Equal_Overflow"] = [[88,(cf.ALU_Zero_Flag,False),(cf.ALU_Sign_Flag,True),(cf.ALU_Sign_Flag,True)],jump,[]]
        #self.Opcodes["jump_Not_Zero_Or_Sign_Equal_Overflow"] = [[88,(cf.ALU_Zero_Flag,False),(cf.ALU_Sign_Flag,False),(cf.ALU_Sign_Flag,False)],jump,[]]

        self.Opcodes["jlc_tx"] = [[89,(cf.Logic_Carry_Flag,True)],jump,[]]
        self.Opcodes["jnlc_tx"] = [[90,(cf.Logic_Carry_Flag,False)],jump,[]]



        self.Opcodes["push_a"] = [[91],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Main_Data,oc.A_Assert_Main_Bus,oc.Ram_Load],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_b"] = [[92],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Main_Data,oc.B_Assert_Main_Bus,oc.Ram_Load],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_c"] = [[93],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Main_Data,oc.C_Assert_Main_Bus,oc.Ram_Load],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_d"] = [[94],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Main_Data,oc.D_Assert_Main_Bus,oc.Ram_Load],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_tl"] = [[95],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Main_Data,oc.RHS_Assert_Main_Bus,oc.Ram_Load],[oc.Stack_Pointer_Increment]]
        self.Opcodes["push_th"] = [[96],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Main_Data,oc.LHS_Assert_Main_Bus,oc.Ram_Load],[oc.Stack_Pointer_Increment]]

        self.Opcodes["pop_a"] = [[97],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Data_Main,oc.Ram_Assert,oc.A_Load_Main_Bus]]
        self.Opcodes["pop_b"] = [[98],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Data_Main,oc.Ram_Assert,oc.B_Load_Main_Bus]]
        self.Opcodes["pop_c"] = [[99],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Data_Main,oc.Ram_Assert,oc.C_Load_Main_Bus]]
        self.Opcodes["pop_d"] = [[100],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Data_Main,oc.Ram_Assert,oc.D_Load_Main_Bus]]
        self.Opcodes["pop_tl"] = [[101],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Data_Main,oc.Ram_Assert,oc.RHS_Load_Main_Bus]]
        self.Opcodes["pop_th"] = [[102],[oc.Stack_Pointer_Decrement],[oc.Fetch_Denied,oc.Stack_Pointer_Assert_Address_Bus,oc.Memory_Bridge_Data_Main,oc.Ram_Assert,oc.LHS_Load_Main_Bus]]

        self.Opcodes["break"] = [[103],[],[]]

        self.Opcodes["Move_Di_IO_A"] = [[104],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Load,oc.A_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_B"] = [[105],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Load,oc.B_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_C"] = [[106],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Load,oc.C_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_D"] = [[107],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Load,oc.D_Assert_Main_Bus]]
        self.Opcodes["Move_Di_IO_Constant"] = [[108],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Load,oc.Constant_Assert]]

        self.Opcodes["Move_Di_A_IO"] = [[109],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Assert,oc.A_Load_Main_Bus]]
        self.Opcodes["Move_Di_B_IO"] = [[110],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Assert,oc.B_Load_Main_Bus]]
        self.Opcodes["Move_Di_C_IO"] = [[111],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Assert,oc.C_Load_Main_Bus]]
        self.Opcodes["Move_Di_D_IO"] = [[112],[],[oc.Destination_Index_Assert_Address_Bus,oc.IO_Assert,oc.D_Load_Main_Bus]]

        self.Opcodes["Move_Si_IO_A"] = [[113],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Load,oc.A_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_B"] = [[114],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Load,oc.B_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_C"] = [[115],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Load,oc.C_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_D"] = [[116],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Load,oc.D_Assert_Main_Bus]]
        self.Opcodes["Move_Si_IO_Constant"] = [[117],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Load,oc.Constant_Assert]]

        self.Opcodes["Move_Si_A_IO"] = [[118],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Assert,oc.A_Load_Main_Bus]]
        self.Opcodes["Move_Si_B_IO"] = [[119],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Assert,oc.B_Load_Main_Bus]]
        self.Opcodes["Move_Si_C_IO"] = [[120],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Assert,oc.C_Load_Main_Bus]]
        self.Opcodes["Move_Si_D_IO"] = [[121],[],[oc.Source_Index_Assert_Address_Bus,oc.IO_Assert,oc.D_Load_Main_Bus]]






        # ALU operations

        # ADD
        self.Opcodes["add_B_to_A"] = [[128],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_C_to_A"] = [[129],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_D_to_A"] = [[130],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["add_A_to_B"] = [[131],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_C_to_B"] = [[132],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_D_to_B"] = [[133],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["add_A_to_C"] = [[134],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_B_to_C"] = [[135],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_D_to_C"] = [[136],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["add_A_to_D"] = [[137],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_B_to_D"] = [[138],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_C_to_D"] = [[139],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Add with carry
        self.Opcodes["add_B_to_A_Carry"] = [[140],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_C_to_A_Carry"] = [[141],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_D_to_A_Carry"] = [[142],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["add_A_to_B_Carry"] = [[143],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_C_to_B_Carry"] = [[144],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_D_to_B_Carry"] = [[145],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["add_A_to_C_Carry"] = [[146],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_B_to_C_Carry"] = [[147],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_D_to_C_Carry"] = [[148],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["add_A_to_D_Carry"] = [[149],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_B_to_D_Carry"] = [[150],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["add_C_to_D_Carry"] = [[151],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Pass,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Subtract
        self.Opcodes["sub_B_from_A"] = [[152],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_C_from_A"] = [[153],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_D_from_A"] = [[154],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["sub_A_from_B"] = [[155],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_C_from_B"] = [[156],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_D_from_B"] = [[157],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["sub_A_from_C"] = [[158],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_B_from_C"] = [[159],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_D_from_C"] = [[160],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["sub_A_from_D"] = [[161],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_B_from_D"] = [[162],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_C_from_D"] = [[163],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Subtract with borrow
        self.Opcodes["sub_B_from_A_Borrow"] = [[164],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_C_from_A_Borrow"] = [[165],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_D_from_A_Borrow"] = [[166],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["sub_A_from_B_Borrow"] = [[167],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_C_from_B_Borrow"] = [[168],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_D_from_B_Borrow"] = [[169],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["sub_A_from_C_Borrow"] = [[170],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_B_from_C_Borrow"] = [[171],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_D_from_C_Borrow"] = [[172],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["sub_A_from_D_Borrow"] = [[173],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_B_from_D_Borrow"] = [[174],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["sub_C_from_D_Borrow"] = [[175],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Shift left
        self.Opcodes["Shift_Left_A"] = [[176],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Shift_Left_B"] = [[177],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Shift_Left_C"] = [[178],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Shift_Left_D"] = [[179],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.Shift_Left,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Shift Right
        self.Opcodes["Shift_Right_A"] = [[180],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Shift_Right_B"] = [[181],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Shift_Right_C"] = [[182],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Shift_Right_D"] = [[183],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.Shift_Right,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Increments
        self.Opcodes["Increment_A"] = [[184],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Increment_B"] = [[185],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Increment_C"] = [[186],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Increment_D"] = [[187],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Increments with carry
        self.Opcodes["Increment_A_Carry"] = [[188],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Increment_B_Carry"] = [[189],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Increment_C_Carry"] = [[190],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Increment_D_Carry"] = [[191],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.Shift_Pass,oc.ALU_Loop_Carry,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Decrements
        self.Opcodes["Decrement_A"] = [[192],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Decrement_B"] = [[193],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Decrement_C"] = [[194],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Decrement_D"] = [[195],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Fill,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # And
        self.Opcodes["and_B_with_A"] = [[196],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_C_with_A"] = [[197],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_D_with_A"] = [[198],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["and_A_with_B"] = [[199],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_C_with_B"] = [[200],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_D_with_B"] = [[201],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["and_A_with_C"] = [[202],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_B_with_C"] = [[203],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_D_with_C"] = [[204],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["and_A_with_D"] = [[205],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_B_with_D"] = [[206],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["and_C_with_D"] = [[207],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_And,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # OR
        self.Opcodes["Or_B_with_A"] = [[208],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_C_with_A"] = [[209],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_D_with_A"] = [[210],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["Or_A_with_B"] = [[211],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_C_with_B"] = [[212],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_D_with_B"] = [[213],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["Or_A_with_C"] = [[214],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_B_with_C"] = [[215],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_D_with_C"] = [[216],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["Or_A_with_D"] = [[217],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_B_with_D"] = [[218],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Or_C_with_D"] = [[219],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Or,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Xor
        self.Opcodes["Xor_A_with_A"] = [[220],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_B_with_A"] = [[221],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_C_with_A"] = [[222],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_D_with_A"] = [[223],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["Xor_A_with_B"] = [[224],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_B_with_B"] = [[225],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_C_with_B"] = [[226],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_D_with_B"] = [[227],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["Xor_A_with_C"] = [[228],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_B_with_C"] = [[229],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_C_with_C"] = [[230],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_D_with_C"] = [[231],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]

        self.Opcodes["Xor_A_with_D"] = [[232],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_B_with_D"] = [[233],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_C_with_D"] = [[234],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Xor_D_with_D"] = [[235],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Xor,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Not
        self.Opcodes["Not_A"] = [[236],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Load,oc.Shift_Load],[oc.A_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Not_B"] = [[237],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Load,oc.Shift_Load],[oc.B_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Not_C"] = [[238],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Load,oc.Shift_Load],[oc.C_Load_Main_Bus,oc.ALU_Assert]]
        self.Opcodes["Not_D"] = [[239],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Bitwise_Load,oc.Shift_Load],[oc.D_Load_Main_Bus,oc.ALU_Assert]]

        # Compare
        self.Opcodes["Compare_B_with_A"] = [[240],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_C_with_A"] = [[241],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_D_with_A"] = [[242],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]

        self.Opcodes["Compare_A_with_B"] = [[243],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_C_with_B"] = [[244],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_D_with_B"] = [[245],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]

        self.Opcodes["Compare_A_with_C"] = [[246],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_B_with_C"] = [[247],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_D_with_C"] = [[248],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.D_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]

        self.Opcodes["Compare_A_with_D"] = [[249],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.A_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_B_with_D"] = [[250],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.B_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Compare_C_with_D"] = [[251],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.C_Assert_RHS_Bus,oc.Bitwise_Nor,oc.Shift_Pass,oc.Bitwise_Carry,oc.Bitwise_Load,oc.Shift_Load],[]]

        # Test
        self.Opcodes["Test_A"] = [[252],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.A_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Test_B"] = [[253],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.B_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Test_C"] = [[254],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.C_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[]]
        self.Opcodes["Test_D"] = [[255],[oc.Program_Counter_Increment,oc.Program_Counter_Assert_Address_Bus,oc.D_Assert_LHS_Bus,oc.Shift_Pass,oc.Bitwise_Load,oc.Shift_Load],[]]

    def make_opcode_roms(self,pos,stage_1,stage_2):
        x,y,z = pos

        self.input_stage_1 = [sm.LogicGate(self.blueprint,self.ID,"or",(x,i+y,z),"up","right","d02525") for i in range(self.bitness)]
        self.input_not_stage_1 = [sm.LogicGate(self.blueprint,self.ID,"nor",(x,i+self.bitness+len(self.flags) + y,z),"up","right","d02525")  for i in range(self.bitness)]

        self.input_stage_2 = [sm.LogicGate(self.blueprint,self.ID,"or",(x,i+y+30,z),"up","right","0a3ee2")  for i in range(self.bitness)]
        self.input_not_stage_2 = [sm.LogicGate(self.blueprint,self.ID,"nor",(x,i+self.bitness+len(self.flags) + y+30,z),"up","right","0a3ee2")  for i in range(self.bitness)]
        pos = 0
        for flag in self.flags:
            self.flags[flag] = [self.flags[flag]]
            self.flags[flag].append(sm.LogicGate(self.blueprint,self.ID,"or",(x,self.bitness+pos+y,z),"up","right","e2db13"))
            self.flags[flag].append(sm.LogicGate(self.blueprint,self.ID,"nor",(x,self.bitness*2+len(self.flags) + pos + y,z),"up","right","e2db13"))
            self.flags[flag].append(sm.LogicGate(self.blueprint,self.ID,"or",(x,self.bitness+pos+y+30,z),"up","right","e2db13"))
            self.flags[flag].append(sm.LogicGate(self.blueprint,self.ID,"nor",(x,self.bitness*2+len(self.flags) + pos + y+30,z),"up","right","e2db13"))
            pos += 1



        for flag in self.flags:
            self.flags[flag][0].connect(self.flags[flag][1])
            self.flags[flag][0].connect(self.flags[flag][2])

        for flag in self.flags:
            self.flags[flag][0].connect(self.flags[flag][3])
            self.flags[flag][0].connect(self.flags[flag][4])


        for i in range(self.bitness):
            stage_1.memcells[-1-i].connect(self.input_stage_1[i])
            stage_1.memcells[-1-i].connect(self.input_not_stage_1[i])
            stage_2.memcells[-1-i].connect(self.input_stage_2[i])
            stage_2.memcells[-1-i].connect(self.input_not_stage_2[i])

        rx = 0
        ry = 0

        for opcode in self.Opcodes:
            fetch_flags,stage1,stage2 = self.Opcodes[opcode]
            code = fetch_flags[0]
            flags = fetch_flags[1:]

            flage_gate_s1 = sm.LogicGate(self.blueprint,self.ID,"and",(rx + x+1,ry + y,z),"up","right","d02525")

            mask = 1
            for i in range(self.bitness):
                if code & mask == mask:
                    self.input_stage_1[i].connect(flage_gate_s1)
                else:
                    self.input_not_stage_1[i].connect(flage_gate_s1)
                mask = mask << 1
            for line in stage1:
                flage_gate_s1.connect(line)



            flage_gate_s2 = sm.LogicGate(self.blueprint,self.ID,"and",(rx + x+1,ry + y+30,z),"up","right","0a3ee2")

            mask = 1
            for i in range(self.bitness):
                if code & mask == mask:
                    self.input_stage_2[i].connect(flage_gate_s2)
                else:
                    self.input_not_stage_2[i].connect(flage_gate_s2)
                mask = mask << 1
            for line in stage2:
                flage_gate_s2.connect(line)


            for each_flags in self.flags:
                each_flags = self.flags[each_flags]
                for each_flag in flags:
                    print(f"flags = {flags} : each_flag = {each_flag} : each_flags = {each_flags}")
                    if each_flags[0] == each_flag[0]:
                        print(opcode)

                        if each_flag[1]:
                            each_flags[1].connect(self.ID.current_ID-1)
                            each_flags[3].connect(self.ID.current_ID)
                        else:
                            each_flags[2].connect(self.ID.current_ID-1)
                            each_flags[4].connect(self.ID.current_ID)

            ry += 1
            if ry > 28:
                ry = 0
                rx += 1

class Ram:
    def __init__(self,bp,id,bitness_in,bitness_out,pos,rotation = "x,y,z", Maxsize = None):
        self.bp = bp
        self.id = id
        self.bitness_in = bitness_in
        self.bitness_out = bitness_out
        self.pos = pos
        self.rotation = rotation
        x, y, z = pos

        self.address_ands = [sm.LogicGate(bp,id,"and",(2 + x,i + y,z),"up","down","d02525",rotation) for i in range(self.bitness_in)]
        self.address_nands = [sm.LogicGate(bp,id,"nand",(3 + x,i + y,z),"up","down","d02525",rotation) for i in range(self.bitness_in)]
        self.output_or = [sm.LogicGate(bp,id,"or",(x,i + y,z),"up","down","eeeeee",rotation) for i in range(self.bitness_out)]
        self.input_and = [sm.LogicGate(bp,id,"and",(x+1,i + y,z),"up","down","19e753",rotation) for i in range(self.bitness_out)]
        self.write = sm.LogicGate(bp,id,"or",(x + 1,y - 1,z),"up","down","19e753",rotation)
        self.read = sm.LogicGate(bp,id,"or",(x,y - 1,z),"up","down","eeeeee",rotation)
        self.write_driver = sm.LogicGate(bp,id,"or",(x + 2,y - 1,z),"up","down","19e753",rotation)
        self.read_driver = sm.LogicGate(bp,id,"or",(x + 3,y - 1,z),"up","down","19e753",rotation)

        self.enables = self.address_nands+self.address_nands

        # control
        self.control_lines = {"Ram_Assert": self.write,
                              "Ram_Load": self.read}

        # logic
        self.read.connect(self.read_driver)
        self.write.connect(self.write_driver)

        or_1 = sm.LogicGate(bp,id,"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        self.read.connect(or_1)
        or_1.connect(self.read_driver)

        or_2 = sm.LogicGate(bp,id,"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        self.write.connect(or_2)
        or_2.connect(self.read_driver)

        or_3 = sm.LogicGate(bp,id,"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        or_2.connect(or_3)

        or_4 = sm.LogicGate(bp,id,"or",(x+2,y - 1,z),"up","down","19e753",rotation)
        or_3.connect(or_4)
        or_4.connect(self.write_driver)
        or_4.connect(self.read_driver)

        for i in range(bitness_out):
            self.write_driver.connect(self.input_and[i])

        if Maxsize == None:
            size = 2**bitness_in
        else:
            size = Maxsize

        for i in range(size):
            Xor_self_wire,connection,write_read = self.cell((4+i+x,y,z))

            self.read_driver.connect(write_read)
            for j in range(bitness_out):
                connection[j].connect(self.output_or[j])
                self.input_and[j].connect(Xor_self_wire[j])

            mask = 1
            for k in range(self.bitness_in):
                if i & mask == mask:
                    self.address_ands[k].connect(write_read)
                else:
                    self.address_nands[k].connect(write_read)
                mask = mask << 1

        self.address_ands.reverse()
        self.address_nands.reverse()
        self.input_and.reverse()
        self.output_or.reverse()







    def cell(self,pos):
        x,y,z = pos
        Xor_self_wire = [sm.LogicGate(self.bp,self.id,"xor",(x,i + y,z+1),"up","down","0a3ee2",self.rotation) for i in range(self.bitness_out)]
        connection = [sm.LogicGate(self.bp,self.id,"and",(x,i + y,z),"up","down","eeeeee",self.rotation) for i in range(self.bitness_out)]

        write_read = sm.LogicGate(self.bp,self.id,"and",(x,y-1,z),"up","down","19e753",self.rotation)


        for i in range(self.bitness_out):
            Xor_self_wire[i].connect(Xor_self_wire[i])
            Xor_self_wire[i].connect(connection[i])
            write_read.connect(connection[i])

        for i in range(len(connection)):
            if i % 2:
                connection[i].connect(Xor_self_wire[i - 1])
            else:
                connection[i].connect(Xor_self_wire[i+1])
        return Xor_self_wire,connection,write_read

class IO:
    def __init__(self,bp,id,bitness,pos,rotation="x,y,z"):
        self.number_devices = 8
        self.pos = pos
        self.rotation = rotation
        x, y, z = self.pos

        pos_x = 0
        pos_y = -1
        size = math.ceil(self.number_devices/bitness)

        address_bitness = int(math.ceil(math.sqrt(self.number_devices)))

        self.address_ands = [sm.LogicGate(bp,id,"and",(bitness+x-i-1,y+size+3,z),"up","right","d02525",rotation) for i in range(address_bitness)]
        self.address_nands = [sm.LogicGate(bp,id,"nand",(bitness+x-i-1, y+size+2,z),"up","right","d02525",rotation) for i in range(address_bitness)]

        self.write = sm.LogicGate(bp,id,"or",(bitness + x,y,z),"up","right","19e753",rotation)
        self.read = sm.LogicGate(bp,id,"or",(bitness + x,y+1,z),"up","right","eeeeee",rotation)
        self.clock_high = sm.LogicGate(bp,id,"or",(x,y+size+3,z),"up","right","19e753",rotation)
        self.clock_low = sm.LogicGate(bp,id,"or",(x, y+size+2,z),"up","right","e2db13",rotation)

        self.bus_output = [sm.LogicGate(bp,id,"or",(bitness+x-i-1, y,z),"up","right","19e753",rotation) for i in range(bitness)]
        self.bus_input = [sm.LogicGate(bp,id,"or",(bitness+x-i-1,y+size,z),"up","right","eeeeee",rotation) for i in range(bitness)]

        # control
        self.control_lines = {"IO_Load": self.write,
                              "IO_Assert": self.read}




        for device in range(self.number_devices):
            dvice_selector = sm.LogicGate(bp,id,"and",(x + pos_x,y + pos_y+size+2, z),"up","right","29842e")
            mask = 1
            for i in range(address_bitness):
                if device & mask == mask:
                    self.address_ands[i].connect(dvice_selector)
                else:
                    self.address_nands[i].connect(dvice_selector)
                mask = mask << 1

            pos_x += 1
            if pos_x >= 8:
                pos_x = 0
                pos_y -= 1

        remainder = (bitness % 2 ** address_bitness) - (2**address_bitness-self.number_devices)

        for i in range(2**address_bitness-self.number_devices):
            bp.place_object(objects.Duct_Holder,(x+remainder+i,y,z),"up","up","000000",rotation)

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
        self.address_size = math.floor(math.log2(int(2 ** self.bitness_in / self.disk_size - 1))) + 1
        self.counter_size = bitness_in - self.address_size

        print(self.address_size,self.counter_size)


        self.timer_cell_controller()
        self.timer_cells()
        self.disk_ram()


    def timer_cell_controller(self):

        x, y, z = self.pos

        self.xnors = [sm.LogicGate(self.blueprint,self.ID.get_next(),"xnor",(x + pos,y+2,z),"up","right","eeeeee",self.rotation) for pos in range(self.counter_size)]
        self.counter_gates = [sm.LogicGate(self.blueprint,self.ID.get_next(),"and",(x + pos,y+4,z),"up","right","eeeeee",self.rotation) for pos in range(self.counter_size)]
        self.address_gates = [sm.LogicGate(self.blueprint,self.ID.get_next(),"xor",(x + pos,y+3,z),"up","right","eeeeee",self.rotation) for pos in range(self.counter_size)]

        self.address_ands = [sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (self.bitness_out - self.address_size + pos + x, y + 5, z), "up", "right", "eeeeee",self.rotation) for pos in range(self.address_size)]
        self.address_nors = [sm.LogicGate(self.blueprint,self.ID.get_next(), "nor", (self.bitness_out - self.address_size + pos + x, y + 6, z), "up", "right", "eeeeee",self.rotation) for pos in range(self.address_size)]

        self.enable = sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (self.bitness_out + x, y + 5, z), "up", "right", colors.Black)

        self.trigger = sm.LogicGate(self.blueprint,self.ID.get_next(),"and",(x + self.bitness_out,y+6,z),"up","right",colors.Black, self.rotation)
        self.trigger_2 = sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + self.bitness_out, y+6, z), "up", "right", colors.Black, self.rotation)
        self.write = sm.LogicGate(self.blueprint,self.ID.get_next(), "or", (self.bitness_out + x, y + 8, z), "up", "right", colors.Blue_Diamond)
        self.read = sm.LogicGate(self.blueprint,self.ID.get_next(), "or", (self.bitness_out + x, y+7, z), "up", "right", colors.Red)


        self.input_gates = [sm.LogicGate(self.blueprint,self.ID.get_next(), "or",(pos + x,y + 7,z),"up","right", colors.Red, self.rotation) for pos in range(self.bitness_out)]
        self.output_gates = [sm.LogicGate(self.blueprint,self.ID.get_next(), "or",(pos + x,y + 8,z),"up","right", colors.Blue_Diamond, self.rotation) for pos in range(self.bitness_out)]

        self.enable.connect(self.address_gates[-1])

        # address and counting gates and connections
        for i in range(self.counter_size):
            self.xnors[i].connect(self.trigger)
            self.xnors[i].connect(self.trigger_2)
            self.address_gates[i].connect(self.address_gates[i])
            self.enable.connect(self.counter_gates[i])
            self.address_gates[i].connect(self.xnors[i])

        # more connections for counting
        for i in range(self.counter_size):
            for j in range(self.counter_size - i):
                self.address_gates[self.counter_size-1-i].connect(self.counter_gates[j])


        for i in range(self.bitness_out - self.address_size):
            self.blueprint.place_object(objects.Duct_Holder, (x + i, y + 5, z), "up", "up", "000000", self.rotation)
            self.blueprint.place_object(objects.Duct_Holder, (x + i, y + 6, z), "up", "up", "000000", self.rotation)


        for i in range(self.counter_size-1):
            self.counter_gates[i+1].connect(self.address_gates[i])

        self.address_ands.reverse()
        self.address_nors.reverse()

    def timer_cells(self):
        x, y, z = self.pos
        y+=4
        count = 0
        for i in range(int(2**self.bitness_in/self.disk_size)):
            count += 1
            read, write, output, input = self.disk_sector((x,y+i+3,z))

            for i in range(len(output)):
                output[i].connect(self.output_gates[i])
                self.input_gates[i].connect(input[i])

            self.trigger.connect(read)
            self.trigger_2.connect(write)

            self.read.connect(read)
            self.write.connect(write)

            mask = 1
            for j in range(math.floor(math.log2(int(2**self.bitness_in/self.disk_size-1)))+1):
                if i & mask == mask:
                    self.address_ands[j].connect(write)
                    self.address_ands[j].connect(read)
                else:
                    self.address_nors[j].connect(write)
                    self.address_nors[j].connect(read)
                mask = mask << 1




    def disk_ram(self):
        x, y, z = self.pos
        x += 9
        y += 5

        ram_bitness_in = math.floor(math.log2(int(2**self.bitness_in/self.disk_size-1)))+1
        print(ram_bitness_in)

        ram_address_ands = [sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (7 + x - pos, y, z), "up", "right", "d02525", self.rotation) for pos in range(ram_bitness_in)]
        ram_address_nors = [sm.LogicGate(self.blueprint,self.ID.get_next(), "nand", (7 + x - pos, y + 1, z), "up", "right", "d02525", self.rotation) for pos in range(ram_bitness_in)]
        ram_output_or = [sm.LogicGate(self.blueprint,self.ID.get_next(), "or", (x + pos, y+2, z), "up", "right", "eeeeee", self.rotation) for pos in range(self.bitness_out)]
        ram_input_ors  = [sm.LogicGate(self.blueprint,self.ID.get_next(), "or", (x + pos, y + 3, z), "up", "right", "19e753", self.rotation) for pos in range(self.bitness_out)]
        Ram_Load = sm.LogicGate(self.blueprint,self.ID.get_next(), "or", (x + self.bitness_out, y + 3, z), "up", "right", "19e753", self.rotation)
        Ram_Assert = sm.LogicGate(self.blueprint,self.ID.get_next(), "or", (x + self.bitness_out, y+2, z), "up", "right", "eeeeee", self.rotation)

        for i in range(self.bitness_out - ram_bitness_in):
            self.blueprint.place_object(objects.Duct_Holder, (x + i, y, z), "up", "up", "000000", self.rotation)
            self.blueprint.place_object(objects.Duct_Holder, (x + i, y + 1, z), "up", "up", "000000", self.rotation)

        self.enables = ram_address_ands + ram_address_nors

        for i in range(2 ** ram_bitness_in):
            write,read,xors,read_ands = self.cell((x, y + i + 4 , z))

            Ram_Load.connect(write)
            Ram_Assert.connect(read)

            for i in range(len(ram_input_ors)):
                ram_input_ors[i].connect(xors[i])
                read_ands[i].connect(ram_output_or[i])

            mask = 1
            for k in range(ram_bitness_in):
                if i & mask == mask:
                    ram_address_ands[k].connect(write)
                    ram_address_ands[k].connect(read)
                else:
                    ram_address_nors[k].connect(write)
                    ram_address_nors[k].connect(read)
                mask = mask << 1

        ram_address_ands.reverse()
        ram_address_nors.reverse()
        ram_input_ors.reverse()
        ram_output_or.reverse()

        return ram_address_ands, ram_address_nors, ram_input_ors, ram_output_or, write, read




    def cell(self, pos):
        x, y, z = pos

        Xor_self_wire = []
        xors = []
        write_ands = []
        read_ands = []

        for i in range(self.bitness_out):
            Xor_self_wire.append(sm.LogicGate(self.blueprint,self.ID.get_next(), "xor", (x + i, y, z + 3), "up", "right", "0a3ee2", self.rotation))
            xors.append(sm.LogicGate(self.blueprint,self.ID.get_next(), "xor", (x + i, y, z), "up", "right", colors.Red, self.rotation))
            write_ands.append(sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + i, y, z+1), "up", "right", colors.Green, self.rotation))
            read_ands.append(sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + i, y, z+2), "up", "right", colors.White, self.rotation))

        write = sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + self.bitness_out, y, z+1), "up", "right", colors.Green, self.rotation)
        read = sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + self.bitness_out, y, z), "up", "right", colors.White, self.rotation)

        sm.connect_logic(Xor_self_wire,Xor_self_wire)
        sm.connect_logic(Xor_self_wire, read_ands)
        sm.connect_logic(Xor_self_wire, xors)
        sm.connect_logic(xors, write_ands)
        sm.connect_logic(write_ands, Xor_self_wire)

        write.connect(write_ands)
        read.connect(read_ands)



        return write,read,xors,read_ands



    def connect_address(self,IDs):
        for i in range(len(IDs)):
            if i < self.address_size:
                IDs[i].connect(self.address_nors[-1-i])
                IDs[i].connect(self.address_ands[-1-i])
            else:
                IDs[i].connect(self.xnors[i-self.address_size])


    def disk_sector(self,pos):
        time = self.disk_size
        num_timers = 1

        while time > 2400:
            num_timers+=1
            time-=2400

        last_timer = time - (2+num_timers)

        timer_seconds = math.floor(last_timer/40)
        timer_ticks = last_timer%40

        #print(self.disk_size,num_timers,last_timer,timer_seconds,timer_ticks)

        x, y, z = pos
        y+=2

        read = sm.LogicGate(self.blueprint,self.ID.get_next(),"and",(x+self.bitness_out, y, z + 4),"east","left",colors.White)
        write = sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x+self.bitness_out, y, z + 3), "east", "left", colors.Green)

        erase_driver = sm.LogicGate(self.blueprint,self.ID.get_next(), "nor", (x+self.bitness_out, y, z + 2), "east", "left", colors.Black)
        read_driver = sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x+self.bitness_out, y, z + 1), "east", "left", colors.Black)
        write_driver = sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x+self.bitness_out, y, z), "east", "left", colors.Black)

        ors = [sm.LogicGate(self.blueprint,self.ID.get_next(), "or", (x + pos, y, z + 3+num_timers*2), "up", "right", colors.Black) for pos in range(self.bitness_out)]
        timers = [sm.Timer(self.blueprint,self.ID.get_next(), timer_seconds,timer_ticks, (x + pos, y, z + 3), "up", "up", colors.Black) for pos in range(self.bitness_out)]
        erase = [sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + pos, y, z + 2), "up", "right", colors.Black) for pos in range(self.bitness_out)]
        output = [sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + pos, y, z + 1), "up", "right", colors.Black)for pos in range(self.bitness_out)]
        input = [sm.LogicGate(self.blueprint,self.ID.get_next(), "and", (x + pos, y, z), "up", "right", colors.Black) for pos in range(self.bitness_out)]


        for i in range(self.bitness_out):
            if num_timers > 1:
                timer = sm.Timer(self.blueprint,self.ID.get_next(), 59,40, (x + i, y, z + 3+(j+1)*2), "up", "up", colors.Black)
                ors[i].connect(timer)
                for j in range(num_timers-1):
                    if j == num_timers-2:
                        timer.connect(timers[i])
                    else:
                        timer = sm.Timer(self.blueprint,self.ID.get_next(), 59,40, (x + i, y, z + 3+(j+1)*2), "up", "up", colors.Black)

            timers[i].connect(erase[i])
            erase[i].connect(ors[i])
            ors[i].connect(output[i])
            input[i].connect(ors[i])

            erase_driver.connect(erase[i])
            read_driver.connect(output[i])
            write_driver.connect(input[i])

        read.connect(read_driver)
        write.connect(erase_driver)
        write.connect(write_driver)

        input.reverse()
        output.reverse()

        return read, write, output, input

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
        self.switches = [sm.Switch(ID.get_next(),(x + i,y,z),"up","up",rotation=rotation) for i in range(self.number)]

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
        blueprint = sm.Blueprint(self.ID,"","")

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

