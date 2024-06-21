import json


def hex_rgb(color):
    r = int(color[:2],16)
    g = int(color[2:4],16)
    b = int(color[4:],16)
    return r,g,b


def rgb_hex(color):
    if color[0] > 255:
        red = 255
    elif color[0] < 0:
        red = 0
    else:
        red = color[0]

    if color[1] > 255:
        green = 255
    elif color[1] < 0:
        green = 0
    else:
        green = color[1]

    if color[2] > 255:
        blue = 255
    elif color[2] < 0:
        blue = 0
    else:
        blue = color[2]

    hex_red = hex(red).replace("0x","")
    if len(hex_red) == 1:
        hex_red = "0" + hex_red
    hex_green = hex(green).replace("0x","")
    if len(hex_green) == 1:
        hex_green = "0" + hex_green
    hex_blue = hex(blue).replace("0x","")
    if len(hex_blue) == 1:
        hex_blue = "0" + hex_blue
    return hex_red + hex_green + hex_blue

def face(direction,facing,rotated):
    if direction == "up":
        if facing == "up":
            if rotated == "up":
                return "west","left"
            if rotated == "right":
                return "west","up"
            if rotated == "down":
                return "west","left"
            if rotated == "left":
                return "west","down"

        if facing == "down":
            if rotated == "up":
                return "east","right"
            if rotated == "right":
                return "east","up"
            if rotated == "down":
                return "east","left"
            if rotated == "left":
                return "east","down"

        if facing == "north":
            if rotated == "up":
                return "north","right"
            if rotated == "right":
                return "north","down"
            if rotated == "down":
                return "north","left"
            if rotated == "left":
                return "noth","up"

        if facing == "east":
            if rotated == "up":
                return "up","left"
            if rotated == "right":
                return "up","up"
            if rotated == "down":
                return "up","right"
            if rotated == "left":
                return "up","down"

        if facing == "south":
            if rotated == "up":
                return "south","left"
            if rotated == "right":
                return "south","up"
            if rotated == "down":
                return "south","right"
            if rotated == "left":
                return "south","down"

        if facing == "west":
            if rotated == "up":
                return "down","left"
            if rotated == "right":
                return "down","up"
            if rotated == "down":
                return "down","right"
            if rotated == "left":
                return "down","down"

    if direction == "right":
        if facing == "up":
            if rotated == "up":
                return "up","left"
            if rotated == "right":
                return "up","down"
            if rotated == "down":
                return "up","right"
            if rotated == "left":
                return "up","up"

        if facing == "down":
            if rotated == "up":
                return "down","right"
            if rotated == "right":
                return "down","down"
            if rotated == "down":
                return "down","left"
            if rotated == "left":
                return "down","up"

        if facing == "north":
            if rotated == "up":
                return "east","up"
            if rotated == "right":
                return "east","right"
            if rotated == "down":
                return "east","down"
            if rotated == "left":
                return "east","left"

        if facing == "east":
            if rotated == "up":
                return "south","up"
            if rotated == "right":
                return "south","right"
            if rotated == "down":
                return "south","down"
            if rotated == "left":
                return "south","left"

        if facing == "south":
            if rotated == "up":
                return "west","up"
            if rotated == "right":
                return "west","right"
            if rotated == "down":
                return "west","down"
            if rotated == "left":
                return "west","left"

        if facing == "west":
            if rotated == "up":
                return "north","up"
            if rotated == "right":
                return "north","right"
            if rotated == "down":
                return "north","down"
            if rotated == "left":
                return "north","left"

    if direction == "down":
        if facing == "up":
            if rotated == "up":
                return "east","left"
            if rotated == "right":
                return "east","up"
            if rotated == "down":
                return "east","left"
            if rotated == "left":
                return "east","down"

        if facing == "down":
            if rotated == "up":
                return "west","right"
            if rotated == "right":
                return "west","up"
            if rotated == "down":
                return "west","left"
            if rotated == "left":
                return "west","down"

        if facing == "north":
            if rotated == "up":
                return "north","left"
            if rotated == "right":
                return "north","up"
            if rotated == "down":
                return "north","right"
            if rotated == "left":
                return "noth","down"

        if facing == "east":
            if rotated == "up":
                return "down","left"
            if rotated == "right":
                return "down","up"
            if rotated == "down":
                return "down","right"
            if rotated == "left":
                return "down","down"

        if facing == "south":
            if rotated == "up":
                return "south","right"
            if rotated == "right":
                return "south","dwon"
            if rotated == "down":
                return "south","left"
            if rotated == "left":
                return "south","up"

        if facing == "west":
            if rotated == "up":
                return "up","left"
            if rotated == "right":
                return "up","up"
            if rotated == "down":
                return "up","right"
            if rotated == "left":
                return "up","down"

    if direction == "left":
        if facing == "up":
            if rotated == "up":
                return "up","right"
            if rotated == "right":
                return "up","up"
            if rotated == "down":
                return "up","left"
            if rotated == "left":
                return "up","down"

        if facing == "down":
            if rotated == "up":
                return "down","left"
            if rotated == "right":
                return "down","up"
            if rotated == "down":
                return "down","right"
            if rotated == "left":
                return "down","down"

        if facing == "north":
            if rotated == "up":
                return "west","up"
            if rotated == "right":
                return "west","right"
            if rotated == "down":
                return "west","down"
            if rotated == "left":
                return "west","left"

        if facing == "east":
            if rotated == "up":
                return "north","up"
            if rotated == "right":
                return "north","right"
            if rotated == "down":
                return "north","down"
            if rotated == "left":
                return "north","left"

        if facing == "south":
            if rotated == "up":
                return "east","up"
            if rotated == "right":
                return "east","right"
            if rotated == "down":
                return "east","down"
            if rotated == "left":
                return "east","left"

        if facing == "west":
            if rotated == "up":
                return "south","up"
            if rotated == "right":
                return "south","right"
            if rotated == "down":
                return "south","down"
            if rotated == "left":
                return "south","left"

    return facing,rotated
    
def rotate(rotation,pos,facing,rotated):
    facing = facing
    rotated = rotated
    rx,ry,rz = pos


    if rotation == "x,y,z":
        facing = facing
        rotated = rotated

    elif rotation == "y,x,z":
        facing,rotated = face("left",facing,rotated)
    elif rotation == "-y,x,z":
        facing,rotated = face("right",facing,rotated)



    if rotation.split(",")[0] == "x":
        rx = pos[0]
    elif rotation.split(",")[0] == "y":
        rx = pos[1]
    elif rotation.split(",")[0] == "z":
        rx = pos[2]
    elif rotation.split(",")[0] == "-x":
        rx = -pos[0]
    elif rotation.split(",")[0] == "-y":
        rx = -pos[1]
    elif rotation.split(",")[0] == "-z":
        rx = -pos[2]

    if rotation.split(",")[1] == "x":
        ry = pos[0]
    elif rotation.split(",")[1] == "y":
        ry = pos[1]
    elif rotation.split(",")[1] == "z":
        ry = pos[2]
    elif rotation.split(",")[1] == "-x":
        ry = -pos[0]
    elif rotation.split(",")[1] == "-y":
        ry = -pos[1]
    elif rotation.split(",")[1] == "-z":
        ry = -pos[2]

    if rotation.split(",")[2] == "x":
        rz = pos[0]
    elif rotation.split(",")[2] == "y":
        rz = pos[1]
    elif rotation.split(",")[2] == "z":
        rz = pos[2]
    elif rotation.split(",")[2] == "-x":
        rz = -pos[0]
    elif rotation.split(",")[2] == "-y":
        rz = -pos[1]
    elif rotation.split(",")[2] == "-z":
        rz = -pos[2]

    return (rx,ry,rz),facing,rotated


def location(pos,facing,rotated):
    x,y,z = pos

    if facing == "west":
        if rotated == "down":
            return (x + 1,y,z + 1),(-3,2)
        elif rotated == "right":
            return (x + 1,y + 1,z + 1),(-2,-3)
        elif rotated == "left":
            return (x + 1,y,z),(2,3)
        elif rotated == "up":
            return (x + 1,y + 1,z),(3,-2)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "up":
        if rotated == "down":
            return (x + 1,y + 1,z),(-2,-1)
        elif rotated == "right":
            return (x,y + 1,z),(1,-2)
        elif rotated == "left":
            return (x + 1,y,z),(-1,2)
        elif rotated == "up":
            return (x,y,z),(2,1)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "down":
        if rotated == "down":
            return (x + 1,y + 1,z + 1),(-1,-2)
        elif rotated == "right":
            return (x + 1,y,z + 1),(2,-1)
        elif rotated == "left":
            return (x,y + 1,z + 1),(-2,1)
        elif rotated == "up":
            return (x,y,z + 1),(1,2)
        else:
            print("not a valid rotation")
            exit(1)

    elif facing == "south":
        if rotated == "down":
            return (x + 1,y + 1,z + 1),(-3,-1)
        elif rotated == "right":
            return (x,y + 1,z + 1),(1,-3)
        elif rotated == "left":
            return (x + 1,y + 1,z),(-1,3)
        elif rotated == "up":
            return (x,y + 1,z),(3,1)
        else:
            print("not a valid rotation")
            exit(1)

    elif facing == "north":
        if rotated == "down":
            return (x + 1,y,z + 1),(-1,-3)
        elif rotated == "right":
            return (x,y,z),(1,3)
        elif rotated == "left":
            return (x,y,z + 1),(-3,1)
        elif rotated == "up":
            return (x + 1,y,z),(3,-1)
        else:
            print("not a valid rotation")
            exit(1)

    elif facing == "east":
        if rotated == "down":
            return (x,y + 1,z + 1),(-3,-2)
        elif rotated == "right":
            return (x,y + 1,z),(-2,3)
        elif rotated == "left":
            return (x,y,z + 1),(2,-3)
        elif rotated == "up":
            return (x,y,z),(3,2)
        else:
            print("not a valid rotation")
            exit(1)
    else:
        print("not a valid rotation")
        exit(1)


def object_rotations(pos,facing,rotated):
    x,y,z = pos

    if facing == "west":
        if rotated == "down":
            return (x + 1,y,z),(2,3)
        elif rotated == "right":
            return (x + 1,y + 1,z),(3,-2)
        elif rotated == "left":
            return (x + 1,y,z + 1),(-3,2)
        elif rotated == "up":
            return (x + 1,y + 1,z + 1),(-2,-3)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "up":
        if rotated == "down":
            return (1 + x,1 + y,z),(-2,-1)
        elif rotated == "right":
            return (x,y + 1,z),(1,-2)
        elif rotated == "left":
            return (x + 1,y,z),(-1,2)
        elif rotated == "up":
            return (x,y,z),(2,1)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "down":
        if rotated == "down":
            return (x + 1,y + 1,z + 1),(-1,-2)
        elif rotated == "right":
            return (x + 1,y,z + 1),(2,-1)
        elif rotated == "left":
            return (x,y + 1,z + 1),(-2,1)
        elif rotated == "up":
            return (x,y,z + 1),(1,2)
        else:
            print("not a valid rotation")
            exit(1)

    elif facing == "south":
        if rotated == "down":
            return (x + 1,y + 1,z),(-1,3)
        elif rotated == "right":
            return (x,y + 1,z),(3,1)
        elif rotated == "left":
            return (x + 1,y + 1,z + 1),(-3,-1)
        elif rotated == "up":
            return (x,y + 1,z + 1),(1,-3)
        else:
            print("not a valid rotation")
            exit(1)

    elif facing == "north":
        if rotated == "down":
            return (x,y,z),(1,3)
        elif rotated == "right":
            return (x + 1,y,z),(3,-1)
        elif rotated == "left":
            return (x,y,z + 1),(-3,1)
        elif rotated == "up":
            return (x + 1,y,z + 1),(-1,-3)
        else:
            print("not a valid rotation")
            exit(1)

    elif facing == "east":
        if rotated == "down":
            return (x,y + 1,z),(-2,3)
        elif rotated == "right":
            return (x,y,z),(3,2)
        elif rotated == "left":
            return (x,y + 1,z + 1),(-3,-2)
        elif rotated == "up":
            return (x,y,z + 1),(2,-3)
        else:
            print("not a valid rotation")
            exit(1)
    else:
        print("not a valid rotation")
        exit(1)


def wedge_color_match(color):
    red,green,blue = hex_rgb(color)
    red -= 25
    green -= 32
    blue -= 32
    return rgb_hex((red,green,blue))


class ID:
    def __init__(self):
        self.used_IDs = []
        self.current_ID = 0

    def cheak_ID(self,ID):
        for ID_range in self.used_IDs:
            if ID_range[0] <= ID <= ID_range[1]:
                return True
        return False

    def add_ID(self,ID):
        if self.cheak_ID(ID):
            return False
        self.used_IDs.append((ID,ID))
        self.clean()
        return True

    def get_next(self):
        while not self.add_ID(self.current_ID):
            self.current_ID += 1
        self.clean()
        return self.current_ID

    def set_ID(self,ID):
        if self.add_ID(ID):
            return ID
        else:
            return None

    def set_range(self,range):
        self.used_IDs.append(range)

    def clean(self):
        length = len(self.used_IDs)
        new_range = [self.used_IDs[0][0],self.used_IDs[0][1]]
        new_used_IDs = []
        for index in range(length):
            if index + 1 < length:
                if self.used_IDs[index + 1][0] == new_range[1] + 1:
                    new_range[1] = self.used_IDs[index + 1][1]
                else:
                    new_used_IDs.append(tuple(new_range))
                    new_range = [self.used_IDs[index + 1][0],self.used_IDs[index + 1][1]]
            else:
                new_used_IDs.append(tuple(new_range))
        self.used_IDs = new_used_IDs

    def claim_range(self,amount):
        next = 0
        for range in self.used_IDs:
            s,e = range
            if next <= s <= next + amount or next <= e <= next + amount:
                next = e + 1

        self.used_IDs.append((next,next + amount))
        print(next)
        return (next)



class Blueprint:
    def __init__(self,Logic_ID,path="",blueprint=""):
        self.version = 4
        self.bodies = []
        self.childs = []
        self.Logic_ID = Logic_ID
        self.path = path.replace("\\","/")
        self.blueprint = blueprint

    def export_blueprint(self):
        blueprint = {}
        blueprint["bodies"] = self.bodies
        blueprint["bodies"].append({
            "childs":self.childs})
        blueprint["version"] = self.version
        with open(f"{self.path+self.blueprint}/blueprint.json","w") as bp:
            bp.write(json.dumps(blueprint))
        print(self.path+self.blueprint)
        print("export complete")

    def connect_ID(blueprint,IDs1,IDs2):
        for i in range(len(IDs1)):
            blueprint.addId(IDs1[i],IDs2[i])

    def connect_IDS(blueprint,ID,IDs):
        for i in range(len(IDs)):
            blueprint.addId(ID,IDs[i])


    def timer(self,ID,seconds,ticks,positon,facing,rotated,color=None,rotation="x,y,z"):
        if 0 <= seconds <= 59:
            if 0 <= ticks <= 40:
                pos,facing,rotated = rotate(rotation,positon,facing,rotated)
                pos,rot = location(pos,facing,rotated)

                self.childs.append({
                    "color":color,
                    "controller":{
                        "active":False,
                        "controllers":None,
                        "id":ID,
                        "joints":None,
                        "seconds":seconds,
                        "ticks":ticks},

                    "pos":{
                        "x":pos[0],
                        "y":pos[1],
                        "z":pos[2]},
                    "shapeId":"8f7fd0e7-c46e-4944-a414-7ce2437bb30f",
                    "xaxis":rot[0],
                    "zaxis":rot[1]})
                return
        print("timer error")


    def button(self,ID,positon,facing,rotated,color=None,rotation="x,y,z"):
        pos,facing,rotated = rotate(rotation,positon,facing,rotated)
        pos,rot = location(pos,facing,rotated)
        if color == None:
            color = "df7f01"
        self.childs.append({
            "color":color,
            "controller":{
                "controllers":None,
                "id":ID,
                "joints":None},
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":"1e8d93a4-506b-470d-9ada-9c0a321e2db5",
            "xaxis":rot[0],
            "zaxis":rot[1]})


    def switch(self,ID,positon,facing,rotated,color=None,rotation="x,y,z"):
        pos,facing,rotated = rotate(rotation,positon,facing,rotated)
        pos,rot = location(pos,facing,rotated)
        if color == None:
            color = "df7f01"

        self.childs.append({
            "color":color,
            "controller":{
                "active":False,
                "controllers":None,
                "id":ID,
                "joints":None},
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":"7cf717d7-d167-4f2d-a6e7-6b2c70aa3986",
            "xaxis":rot[0],
            "zaxis":rot[1]})


    def logic_gate(self,ID,Mode,positon,facing,rotated,color=None,rotation="x,y,z"):
        pos,facing,rotated = rotate(rotation,positon,facing,rotated)
        pos,rot = location(pos,facing,rotated)

        if Mode == "and":
            mode = 0
        elif Mode == "or":
            mode = 1
        elif Mode == "xor":
            mode = 2
        elif Mode == "nand":
            mode = 3
        elif Mode == "nor":
            mode = 4
        elif Mode == "xnor":
            mode = 5
        else:
            mode = 0
        if color == None:
            color = "df7f01"

        self.childs.append({
            "color":color,
            "controller":{
                "active":False,
                "controllers":None,
                "id":ID,
                "mode":mode},
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":"9f0f56e8-2c31-4d83-996c-d00a9b296c3f",
            "xaxis":rot[0],
            "zaxis":rot[1]})

    def place_light_object(self,block,ID,positon,facing,rotated,color=None,lightColor=None,coneAngle=0,activity=False,rotation="x,y,z"):
        pos,facing,rotated = rotate(rotation,positon,facing,rotated)
        pos,rot = location(pos,facing,rotated)
        if color == None:
            color = block["color"]

        if lightColor == None:
            lightColor = block["color"]

        if coneAngle == 0:
            coneAngle = 0
        if activity == False:
            activity = False

        self.childs.append({
            "color":color,
            "controller":{
                "color":lightColor,
                "coneAngle":coneAngle,
                "active":activity,
                "controllers":None,
                "id":ID,
                "joints":None,
                "luminance":0},
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":block["uuid"],
            "xaxis":rot[0],
            "zaxis":rot[1]})

    def addId(self,ID1,ID2):
        for index in range(len(self.childs)):
            each = self.childs[index]
            if "controller" in each.keys():
                if "id" in each["controller"].keys():
                    if each["controller"]["id"] == ID1:
                        if each["controller"]["controllers"] == None:
                            self.childs[index]["controller"]["controllers"] = []
                        control = {}
                        control["id"] = ID2
                        self.childs[index]["controller"]["controllers"].append(control)

    def addIds(self,ID1,IDs):
        for index in range(len(self.childs)):
            each = self.childs[index]
            if "controller" in each.keys():
                if "id" in each["controller"].keys():
                    if each["controller"]["id"] == ID1:
                        if each["controller"]["controllers"] == None:
                            self.childs[index]["controller"]["controllers"] = []
                        for ID2 in IDs:
                            control = {}
                            control["id"] = ID2
                            self.childs[index]["controller"]["controllers"].append(control)

    def linkIDs(self,ID1,IDs):
        for index in range(len(self.childs)):
            each = self.childs[index]
            if "controller" in each.keys():
                if "id" in each["controller"].keys():
                    for ID2 in IDs:
                        if each["controller"]["id"] == ID2:
                            if each["controller"]["controllers"] == None:
                                self.childs[index]["controller"]["controllers"] = []
                                control = {}
                                control["id"] = ID1
                                self.childs[index]["controller"]["controllers"].append(control)

    def place_object(self,block,positon,facing,rotated,color=None,rotation="x,y,z"):
        pos,facing,rotated = rotate(rotation,positon,facing,rotated)
        pos,rot = location(pos,facing,rotated)
        if color == None:
            color = block["color"]
        self.childs.append({
            "color":color,
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":block["uuid"],
            "xaxis":rot[0],
            "zaxis":rot[1]})

    def fill_block(self,block,pos,size,color=None,rotation="x,y,z"):
        pos,facing,rotated = rotate(rotation,pos,"up","right")
        print(pos,facing,rotated )
        pos,rot = location(pos,facing,rotated)
        if color == None:
            color = block["color"]
        self.childs.append({
            "bounds":{
                "x":size[0],
                "y":size[1],
                "z":size[2]},
            "color":color,
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":block["uuid"],
            "xaxis":1,
            "zaxis":3})

    def fast_logic_gate(self,ID,Mode,positon,facing,rotated,color=None,rotation="x,y,z"):
        pos,facing,rotated = rotate(rotation,positon,facing,rotated)
        pos,rot = location(pos,facing,rotated)
        if Mode == "and":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggA"
        elif Mode == "or":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggB"
        elif Mode == "xor":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggC"
        elif Mode == "nand":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggD"
        elif Mode == "nor":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggE"
        elif Mode == "xnor":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggF"
        else:
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggA"

        if color == None:
            color = "df7f01"
        self.childs.append({
            "color":color,
            "controller":{
                "containers":None,
                "controllers":None,
                "data":mode,
                "id":ID,
                "joints":None},
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":"8f98db04-72eb-4a3a-88a1-f4f3e8d818ee",
            "xaxis":rot[0],
            "zaxis":rot[1]})

    def merge(self,blueprint):
        self.childs = self.childs + blueprint.childs

    def load(self):
        with open(f"{self.path+self.blueprint}/blueprint.json","r") as bp:
            blueprint = json.loads(bp.read())

        self.bodies = []
        self.childs = blueprint["bodies"][0]["childs"]
        self.version = blueprint["version"]

        print("load complete")
