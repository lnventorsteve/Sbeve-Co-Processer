class Control_Lines:
    def __init__(self):
        self.Fetch_Denied = 117
        self.memory_bridge_Main_Data = 175
        self.memory_bridge_Data_Main = 176
        self.GPR_A_Load_Main_Bus = 302
        self.GPR_A_Assert_Main_Bus = 304
        self.GPR_A_Assert_LHS_Bus = 305
        self.GPR_A_Assert_RHS_Bus = 306
        self.GPR_B_Load_Main_Bus = 355
        self.GPR_B_Assert_Main_Bus = 357
        self.GPR_B_Assert_LHS_Bus = 358
        self.GPR_B_Assert_RHS_Bus = 359
        self.GPR_C_Load_Main_Bus = 408
        self.GPR_C_Assert_Main_Bus = 410
        self.GPR_C_Assert_LHS_Bus = 411
        self.GPR_C_Assert_RHS_Bus = 412
        self.GPR_D_Load_Main_Bus = 461
        self.GPR_D_Assert_Main_Bus = 463
        self.GPR_D_Assert_LHS_Bus = 464
        self.GPR_D_Assert_RHS_Bus = 465
        self.Constant_Load_Fetch = 499
        self.Constant_Assert_Main_Bus = 501
        self.Transfer_LHS_Load_Main_Bus = 677
        self.Transfer_LHS_Assert_Main_Bus = 675
        self.Transfer_LHS_Load_Transfer_Bus = 678
        self.Transfer_LHS_Assert_Transfer_Bus = 676
        self.Transfer_RHS_Load_Main_Bus = 576
        self.Transfer_RHS_Assert_Main_Bus = 574
        self.Transfer_RHS_Load_Transfer_Bus = 577
        self.Transfer_RHS_Assert_Transfer_Bus = 575
        self.Program_Counter_Load_Transfer_Bus = 864
        self.Program_Counter_Assert_Address_Bus = 866
        self.Program_Counter_Assert_Transfer_Bus = 867
        self.Program_Counter_Increment = 868
        self.Program_Counter_Decrement = 870
        self.Return_Address_Load_Transfer_Bus = 1045
        self.Return_Address_Assert_Address_Bus = 1047
        self.Return_Address_Assert_Transfer_Bus = 1048
        self.Return_Address_Increment = 1049
        self.Return_Address_Decrement = 1051
        self.Stack_Pointer_Load_Transfer_Bus = 1226
        self.Stack_Pointer_Assert_Address_Bus = 1228
        self.Stack_Pointer_Assert_Transfer_Bus = 1229
        self.Stack_Pointer_Increment = 1230
        self.Stack_Pointer_Decrement = 1232
        self.Source_Index_Load_Transfer_Bus = 1588
        self.Source_Index_Assert_Address_Bus = 1590
        self.Source_Index_Assert_Transfer_Bus = 1591
        self.Source_Index_Increment = 1592
        self.Source_Index_Decrement = 1594
        self.Destination_Index_Load_Transfer_Bus = 1407
        self.Destination_Index_Assert_Address_Bus = 1409
        self.Destination_Index_Assert_Transfer_Bus = 1410
        self.Destination_Index_Increment = 1411
        self.Destination_Index_Decrement = 1413
        self.Bitwise_Or = 1609
        self.Bitwise_And = 1610
        self.Bitwise_Xor = 1611
        self.Bitwise_Nor = 1612
        self.Bitwise_Pass = 1613
        self.Bitwise_Fill = 1614
        self.Bitwise_Carry = 1615
        self.Shift_Left = 1704
        self.Shift_Right = 1703
        self.Shift_Pass = 1705
        self.Bitwise_Register_Write = 1701
        self.Shift_Register_Write = 1761
        self.AlU_Assert_Main_Bus = 1763
        self.AlU_Loop_Carry = 1864
        self.Ram_Read = 1896
        self.Ram_Write = 1895
        self.IO_Read = 3461
        self.IO_Write = 3460
        self.Arithmetic_Carry_flag = 1764
        self.Logic_Carry_flag = 1681
        self.ALU_Zero_flag = 1834
        self.ALU_Over_Flow_flag = 1831
        self.ALU_sign_flag = 1826
