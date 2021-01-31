import json


class characterBuilder():
    def __init__(self,characterlist,skinslist,maxstatus):
        self.characters = characterlist # type:dict
        self.skins = skinslist # type: dict
        self.maxStatus = maxstatus
        self.starttime = 1559453208

    @classmethod
    def init(cls,filepath="./data/arkhack_data.json"):
        try:
            with open(filepath,"r",encoding="utf-8") as f:
                data = json.loads(f.read().strip())
                return cls(data["character"],data["shopskins"],data["maxstatus"])
        except:
            return None

    def getCharacter(self,instId,charId):
        if (charId not in self.characters.keys()):
            return None
        self.starttime +=1
        return {"instId":int(instId),
                "charId":charId,
                "favorPoint":0,
                "potentialRank":0,
                "mainSkillLvl":1,
                "skin":self.characters[charId]["skins"][0],
                "level":1,
                "exp":0,
                "evolvePhase":0,
                "defaultSkillIndex":-1 if self.characters[charId]["rarity"] <=1 else 0,
                "gainTime":self.starttime,
                "skills":[{"skillId":skillId,
                           "unlock":1 if index == 0 else 0,
                           "state":0,
                           "specializeLevel":0,
                           "completeUpgradeTime":-1} for index,skillId in enumerate(self.characters[charId]["skills"])]}

    def graduate(self,cdata):
        rarity = self.characters[cdata["charId"]]["rarity"]
        for r,v in self.maxStatus.items():
            if rarity>=int(r):
                for key,val in v.items():
                    cdata[key] = val
        # 4星及其以上干员设置衣服, 专精
        if rarity >= 3:
            if (len(self.characters[cdata["charId"]]["skins"])>=3):
                cdata["skin"] = self.characters[cdata["charId"]]["skins"][2]
            elif (len(self.characters[cdata["charId"]]["skins"]) < 2):
                    cdata["skin"] = self.characters[cdata["charId"]]["skins"][0]
            else:
                 cdata["skin"] = self.characters[cdata["charId"]]["skins"][1]
            for skill in cdata["skills"]:
                skill["unlock"] = 1
                skill["specializeLevel"] = 3
        return cdata


class troopBuilder():
    def __init__(self,curCharInstId,curSquadCount,squads,chars,cBuilder: characterBuilder=None):
        self.curCharInstId = curCharInstId
        self.curSquadCount = curSquadCount
        # dict string key "0","1","2","3"
        self.squads = squads # type:dict
        # dict string key start from 1
        self.chars = chars # type:dict
        self.cBuilder = cBuilder # type

    @classmethod
    def init(cls,filepath="./data/arkhack_troop.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.loads(f.read().strip())
                return cls(data["curCharInstId"],data["curSquadCount"],data["squads"],data["chars"])
        except:
            return None

    def setCharacterBuilder(self,cb: characterBuilder):
        self.cBuilder =cb

    def getCharData(self,charId):
        for char in self.chars.values():
            if char["charId"] == charId:
                return char
        return None

    def addCharacter(self,charId,force=False):
        if not force:
            for c in self.chars.values():
                if c["charId"] == charId:
                    return False
        cdata = self.cBuilder.getCharacter(self.curCharInstId,charId)
        if cdata == None:
            return False
        self.chars[str(self.curCharInstId)] = cdata
        self.curCharInstId +=1
        return True

    def dump(self):
        return {"curCharInstId": self.curCharInstId, "curSquadCount": self.curSquadCount,
                    "squads": self.squads, "chars": self.chars}

    def save(self,filepath="./data/arkhack_troop.json",indent=2):
        with open(filepath, "w", encoding="utf8") as f:
            f.write(json.dumps({"curCharInstId": self.curCharInstId, "curSquadCount": self.curSquadCount,
                                "squads":self.squads,"chars":self.chars}, indent=indent))

