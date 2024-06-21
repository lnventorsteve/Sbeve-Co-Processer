#instrution
def compile():
    with open("code.txt", "r") as file:
        code = file.read()
        #instrution
        #dec
        #nop
        code = code.replace('nop',str(0))
        #load constants
        code = code.replace('mov a,#',str(1))
        code = code.replace('mov b,#',str(2))
        code = code.replace('mov c,#',str(3))
        code = code.replace('mov d,#',str(4))
        code = code.replace('mov tl,#',str(5))
        code = code.replace('mov th,#',str(6))
        #8 bit moves
        code = code.replace('mov a,b',str(7))
        code = code.replace('mov a,c',str(8))
        code = code.replace('mov a,d',str(9))
        code = code.replace('mov a,tl',str(10))
        code = code.replace('mov a,th',str(11))

        code = code.replace('mov b,a',str(12))
        code = code.replace('mov b,c',str(13))
        code = code.replace('mov b,d',str(14))
        code = code.replace('mov b,tl',str(15))
        code = code.replace('mov b,th',str(16))

        code = code.replace('mov c,a',str(17))
        code = code.replace('mov c,b',str(18))
        code = code.replace('mov c,d',str(19))
        code = code.replace('mov c,tl',str(20))
        code = code.replace('mov c,th',str(21))

        code = code.replace('mov d,a',str(22))
        code = code.replace('mov d,b',str(23))
        code = code.replace('mov d,c',str(24))
        code = code.replace('mov d,tl',str(25))
        code = code.replace('mov d,th',str(26))

        code = code.replace('mov tl,a',str(27))
        code = code.replace('mov tl,b',str(28))
        code = code.replace('mov tl,c',str(29))
        code = code.replace('mov tl,d',str(30))

        code = code.replace('mov th,a',str(31))
        code = code.replace('mov th,b',str(32))
        code = code.replace('mov th,c',str(33))
        code = code.replace('mov th,d',str(34))

        #memory read
        code = code.replace('mov a,[si]',str(35))
        code = code.replace('mov b,[si]',str(36))
        code = code.replace('mov c,[si]',str(37))
        code = code.replace('mov d,[si]',str(38))

        code = code.replace('mov a,[di]',str(39))
        code = code.replace('mov b,[di]',str(40))
        code = code.replace('mov c,[di]',str(41))
        code = code.replace('mov d,[di]',str(42))

        #memory write
        code = code.replace('mov [si],a',str(43))
        code = code.replace('mov [si],b',str(44))
        code = code.replace('mov [si],c',str(45))
        code = code.replace('mov [si],d',str(46))

        code = code.replace('mov [di],a',str(47))
        code = code.replace('mov [di],b',str(48))
        code = code.replace('mov [di],c',str(49))
        code = code.replace('mov [di],d',str(50))

        #16 bit moves
        code = code.replace('mov ra,tx',str(51))
        code = code.replace('mov tx,ra',str(52))
        code = code.replace('mov sp,tx',str(53))
        code = code.replace('mov tx,sp',str(54))
        code = code.replace('mov si,tx',str(55))
        code = code.replace('mov tx,si',str(56))
        code = code.replace('mov di,tx',str(57))
        code = code.replace('mov tx,di',str(58))
        code = code.replace('mov di,si',str(59))
        code = code.replace('mov si,di',str(60))
        code = code.replace('mov si,sp',str(61))
        code = code.replace('mov di,sp',str(62))

        #16 bit inc / dec
        code = code.replace('dec ra',str(63))
        code = code.replace('dec  sp',str(64))
        code = code.replace('dec si',str(65))
        code = code.replace('dec di',str(66))
        code = code.replace(' inc sp',str(67))
        code = code.replace('inc si',str(68))
        code = code.replace('inc di',str(69))

        #flow control
        #call and return
        code = code.replace('call tx',str(70)+"\n0")
        code = code.replace('call di',str(71)+"\n0")
        code = code.replace('ret',str(72)+"\n0")

        code = code.replace('callBD tx',str(70))
        code = code.replace('callBD di',str(71))
        code = code.replace('retBD',str(72))
        #jumps
        code = code.replace('jmp tx',str(73))
        code = code.replace('jmp di',str(74))

        code = code.replace('jo tx',str(75))
        code = code.replace('jno tx',str(76))
        code = code.replace('js tx',str(77))
        code = code.replace('jns tx',str(78))
        code = code.replace('jz tx',str(79))
        code = code.replace('jnz tx',str(80))
        code = code.replace('je tx',str(79))
        code = code.replace('jne tx',str(80))
        #unsigned operations
        code = code.replace('jc tx',str(81))
        code = code.replace('jnae tx',str(81))
        code = code.replace('jb tx',str(81))
        code = code.replace('jnc tx',str(82))
        code = code.replace('jae tx',str(82))
        code = code.replace('jnb tx',str(82))
        code = code.replace('jbe tx',str(83))
        code = code.replace('jna tx',str(83))
        code = code.replace('ja tx',str(84))
        code = code.replace('jnbe tx',str(84))
        #signed operations
        code = code.replace('jl tx',str(85))
        code = code.replace('jnge tx',str(85))
        code = code.replace('jge tx',str(86))
        code = code.replace('jnl tx',str(86))
        code = code.replace('jle tx',str(87))
        code = code.replace('jng tx',str(87))
        code = code.replace('jg tx',str(88))
        code = code.replace('jnle tx',str(88))
        #logical carry operations
        code = code.replace('jlc tx',str(89))
        code = code.replace('jnlc tx',str(90))
        #push and pop
        code = code.replace('push a',str(91))
        code = code.replace('push b',str(92))
        code = code.replace('push c',str(93))
        code = code.replace('push d',str(94))
        code = code.replace('push tl',str(95))
        code = code.replace('push th',str(96))

        code = code.replace('pop a',str(97))
        code = code.replace('pop b',str(98))
        code = code.replace('pop c',str(99))
        code = code.replace('pop d',str(100))
        code = code.replace('pop tl',str(101))
        code = code.replace('pop th',str(102))
        #break
        code = code.replace('break',str(103))

        code = code.replace('IO Di,a',str(104))
        code = code.replace('IO Di,b',str(105))
        code = code.replace('IO Di,c',str(106))
        code = code.replace('IO Di,d',str(107))
        code = code.replace('IO Di,constant',str(108))

        code = code.replace('IO a,Di',str(109))
        code = code.replace('IO b,Di',str(110))
        code = code.replace('IO c,Di',str(111))
        code = code.replace('IO d,Di',str(112))

        code = code.replace('IO Si,a',str(113))
        code = code.replace('IO Si,b',str(114))
        code = code.replace('IO Si,c',str(115))
        code = code.replace('IO Si,d',str(116))
        code = code.replace('IO Si,constant',str(117))

        code = code.replace('IO a,Si',str(118))
        code = code.replace('IO b,Si',str(119))
        code = code.replace('IO c,Si',str(120))
        code = code.replace('IO d,Si',str(121))


        #127 instructions left

        #clear flags
        code = code.replace('clc',str(127))
        #ALU
        #add
        code = code.replace('add a,b',str(128))
        code = code.replace('add a,c',str(129))
        code = code.replace('add a,d',str(130))

        code = code.replace('add b,a',str(131))
        code = code.replace('add b,c',str(132))
        code = code.replace('add b,d',str(133))

        code = code.replace('add c,a',str(134))
        code = code.replace('add c,b',str(135))
        code = code.replace('add c,d',str(136))

        code = code.replace('add d,a',str(137))
        code = code.replace('add d,b',str(138))
        code = code.replace('add d,c',str(139))
        #add with carry
        code = code.replace('addc a,b',str(140))
        code = code.replace('addc a,c',str(141))
        code = code.replace('addc a,d',str(142))

        code = code.replace('addc b,a',str(143))
        code = code.replace('addc b,c',str(144))
        code = code.replace('addc b,d',str(145))

        code = code.replace('addc c,a',str(146))
        code = code.replace('addc c,b',str(147))
        code = code.replace('addc c,d',str(148))

        code = code.replace('addc d,a',str(149))
        code = code.replace('addc d,b',str(150))
        code = code.replace('addc d,c',str(151))
        #subtract
        code = code.replace('sub a,b',str(152))
        code = code.replace('sub a,c',str(153))
        code = code.replace('sub a,d',str(154))

        code = code.replace('sub b,a',str(155))
        code = code.replace('sub b,c',str(156))
        code = code.replace('sub b,d',str(157))

        code = code.replace('sub c,a',str(158))
        code = code.replace('sub c,b',str(159))
        code = code.replace('sub c,d',str(160))

        code = code.replace('sub d,a',str(161))
        code = code.replace('sub d,b',str(162))
        code = code.replace('sub d,c',str(163))
        #subtract carry
        code = code.replace('subb a,b',str(164))
        code = code.replace('subb a,c',str(165))
        code = code.replace('subb a,d',str(166))

        code = code.replace('subb b,a',str(167))
        code = code.replace('subb b,c',str(168))
        code = code.replace('subb b,d',str(169))

        code = code.replace('subb c,a',str(170))
        code = code.replace('subb c,b',str(171))
        code = code.replace('subb c,d',str(172))

        code = code.replace('subb d,a',str(173))
        code = code.replace('subb d,b',str(174))
        code = code.replace('subb d,c',str(175))
        #shift left
        code = code.replace('shl a',str(176))
        code = code.replace('shl b',str(177))
        code = code.replace('shl c',str(178))
        code = code.replace('shl d',str(179))
        #shift right
        code = code.replace('shr a',str(180))
        code = code.replace('shr b',str(181))
        code = code.replace('shr c',str(182))
        code = code.replace('shr d',str(183))
        #inc
        code = code.replace('inc a',str(184))
        code = code.replace('inc b',str(185))
        code = code.replace('inc c',str(186))
        code = code.replace('inc d',str(187))
        #inc with carry
        code = code.replace('incc a',str(188))
        code = code.replace('incc b',str(189))
        code = code.replace('incc c',str(190))
        code = code.replace('incc d',str(191))
        #dec
        code = code.replace('dec a',str(192))
        code = code.replace('dec b',str(193))
        code = code.replace('dec c',str(194))
        code = code.replace('dec d',str(195))
        #and
        code = code.replace('and a,b',str(196))
        code = code.replace('and a,c',str(197))
        code = code.replace('and a,d',str(198))

        code = code.replace('and b,a',str(199))
        code = code.replace('and b,c',str(200))
        code = code.replace('and b,d',str(201))

        code = code.replace('and c,a',str(202))
        code = code.replace('and c,b',str(203))
        code = code.replace('and c,d',str(204))

        code = code.replace('and d,a',str(205))
        code = code.replace('and d,b',str(206))
        code = code.replace('and d,c',str(207))
        #or
        code = code.replace('or a,b',str(208))
        code = code.replace('or a,c',str(209))
        code = code.replace('or a,d',str(210))

        code = code.replace('or b,a',str(211))
        code = code.replace('or b,c',str(212))
        code = code.replace('or b,d',str(213))

        code = code.replace('or c,a',str(214))
        code = code.replace('or c,b',str(215))
        code = code.replace('or c,d',str(216))

        code = code.replace('or d,a',str(217))
        code = code.replace('or d,b',str(218))
        code = code.replace('or d,c',str(219))
        #xor
        code = code.replace('xor a,a',str(220))
        code = code.replace('xor a,b',str(221))
        code = code.replace('xor a,c',str(222))
        code = code.replace('xor a,d',str(223))

        code = code.replace('xor b,a',str(224))
        code = code.replace('xor b,b',str(225))
        code = code.replace('xor b,c',str(226))
        code = code.replace('xor b,d',str(227))

        code = code.replace('xor c,a',str(228))
        code = code.replace('xor c,b',str(229))
        code = code.replace('xor c,c',str(230))
        code = code.replace('xor c,d',str(231))

        code = code.replace('xor d,a',str(232))
        code = code.replace('xor d,b',str(233))
        code = code.replace('xor d,c',str(234))
        code = code.replace('xor d,d',str(235))
        #not
        code = code.replace('not a',str(236))
        code = code.replace('not b',str(237))
        code = code.replace('not c',str(238))
        code = code.replace('not d',str(239))
        #compare
        code = code.replace('cmp a,b',str(240))
        code = code.replace('cmp a,c',str(241))
        code = code.replace('cmp a,d',str(242))

        code = code.replace('cmp b,a',str(243))
        code = code.replace('cmp b,c',str(244))
        code = code.replace('cmp b,d',str(245))

        code = code.replace('cmp c,a',str(246))
        code = code.replace('cmp c,b',str(247))
        code = code.replace('cmp c,d',str(248))

        code = code.replace('cmp d,a',str(249))
        code = code.replace('cmp d,b',str(250))
        code = code.replace('cmp d,c',str(251))
        #test
        code = code.replace('test a',str(252))
        code = code.replace('test b',str(253))
        code = code.replace('test c',str(254))
        code = code.replace('test d',str(255))

    with open("rom.txt","w") as rom:
        rom.write(code)

if __name__ == "__main__":
    compile()
    print("done")