from mitmproxy.http import HTTPFlow, HTTPResponse
import json,copy

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
            if (len(self.characters[cdata["charId"]]["skins"])>=2):
                cdata["skin"] = self.characters[cdata["charId"]]["skins"][1]
            else:
                cdata["skin"] = self.characters[cdata["charId"]]["skins"][0]
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

class ArkInterceptor():
    # from https://github.com/GhostStar/Arknights-Armada/
    Servers = {"ak-gs-localhost.hypergryph.com": ("ak-gs.hypergryph.com", 8443),
               "ak-gs-b-localhost.hypergryph.com": ("ak-gs.hypergryph.com", 8443),
               "ak-as-localhost.hypergryph.com": ("ak-as.hypergryph.com", 9443)}

    ServersList = [key for key in Servers.keys()] + [val[0] for val in Servers.values()]
    tBuilder = None # type:troopBuilder
    cBuilder = characterBuilder.init()

    @staticmethod
    def setTroopBuilder(tb):
        ArkInterceptor.tBuilder = tb

    def http_connect(self, flow: HTTPFlow):
        pass

    def request(self, flow:HTTPFlow):
        pass

    def response(self, flow: HTTPFlow):
        pass

    def info(self,msg):
        print("Arkhack - %s > %s" %(self.__class__.__name__,msg))

class ArkEssential(ArkInterceptor):
    def http_connect(self, flow: HTTPFlow):
        # replace all localhost server to correct server
        if (flow.request.host in self.Servers.keys()):
            flow.request.host, flow.request.port = self.Servers.get(flow.request.host)

class BattleEssential(ArkInterceptor):
    '''
        Require: CharsEssential
    '''

    def __init__(self):
        self.info("Loading success")

    def request(self, flow:HTTPFlow):
        """
            {
                "changeSkill": 0,
                "slots": [{
                    "charInstId": 1,
                    "skillIndex": 0
                    },null,null,null,null,null,null
                    ],
                "squadId": "0"
            }
        """
        if flow.request.host in self.ServersList and flow.request.path.startswith("/quest/squadFormation"):
            self.info("Receive squad change request")
            req = json.loads(flow.request.get_text())
            self.tBuilder.squads[req["squadId"]]["slots"] = req["slots"]
            req = copy.deepcopy(req)
            req["slots"] = [{
                "charInstId": 1,
                "skillIndex": 0
            }, None, None, None, None, None, None, None, None, None, None, None]
            flow.request.set_text(json.dumps(req))
            self.info("complete")

        if flow.request.host in self.ServersList and (flow.request.path.startswith("/quest/battleStart") or
                                                      flow.request.path.startswith("/campaignV2/battleStart")):
            self.info("battle %s start: setting squad for remote server" % flow.request.path.split("/")[1])
            req = json.loads(flow.request.get_text())
            req['squad']['slots'] = [{
                "charInstId": 1,
                "skillIndex": 0
            }, None, None, None, None, None, None, None, None, None, None, None]
            flow.request.set_text(json.dumps(req))
            self.info("complete")

    def response(self, flow: HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/quest/squadFormation"):
            data = json.loads(flow.response.get_text())
            self.info('setting squad data for local modification')
            for sid in data['playerDataDelta']['modified']['troop']['squads'].keys():
                data['playerDataDelta']['modified']['troop']['squads'][sid] = self.tBuilder.squads[sid]
            flow.response.set_text(json.dumps(data))
            self.info("complete")

class CharsEssential(ArkInterceptor):
    def __init__(self,mode="weak"):
        self.mode = mode
        self.info("Loading success, mode %s" %self.mode)

    def request(self, flow:HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/charBuild/setDefaultSkill"):
            self.info("Receive default skill change change request")
            req = json.loads(flow.request.get_text())
            self.tBuilder.chars[str(req["charInstId"])]["defaultSkillIndex"] = req["defaultSkillIndex"]
            resp = {"playerDataDelta": {"deleted": {},
                                        "modified": {
                                            "troop": {"chars": {str(req["charInstId"]): {
                                                "defaultSkillIndex": req["defaultSkillIndex"]}}}}}}
            self.info("make response")
            flow.response = HTTPResponse.make(200,
                                              json.dumps(resp),
                                              {"Content-Type": "application/json; charset=utf-8"})
            self.info("Reply Complete")

    def response(self, flow: HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/account/syncData"):
            data = json.loads(flow.response.get_text())
            if self.tBuilder is None:
                self.info("Troop builder not found, create from response data")
                ArkInterceptor.tBuilder = troopBuilder(data["user"]["troop"]["curCharInstId"],
                                             data["user"]["troop"]["curSquadCount"],
                                             data["user"]["troop"]["squads"],
                                             data["user"]["troop"]["chars"])
            else:
                self.info("Find exist troop builder, write config to response")
                data["user"]["troop"] = self.tBuilder.dump()
                flow.response.set_text(json.dumps(data))
            ArkInterceptor.tBuilder.setCharacterBuilder(ArkInterceptor.cBuilder)
            self.info("Complete")

class graduateChars(ArkInterceptor):
    '''
        Require: CharsEssential,BattleEssential
    '''
    def __init__(self):
        self.info("Loading success")

    def response(self, flow: HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            for key,char in self.tBuilder.chars.items():
                self.info("Upgrade: %s-%s" %(key,char["charId"]))
                self.tBuilder.chars[key] = self.cBuilder.graduate(self.tBuilder.chars[key])
            data["user"]["troop"] = self.tBuilder.dump()
            flow.response.set_text(json.dumps(data))
            self.info("Complete")
class unlockSkins(ArkInterceptor):
    '''
        Require: CharsEssential
    '''
    def __init__(self):
        self.info("Loading success")

    def request(self, flow: HTTPFlow):
        """
            {
                "charInstId": 9,
                "skinId": "char_123_fang#1"
            }
        """
        if flow.request.host in self.ServersList and flow.request.path.startswith("/charBuild/changeCharSkin"):
            self.info("Receive skin change request")
            req = json.loads(flow.request.get_text())
            resp = {"playerDataDelta": {"deleted": {},
                    "modified": { "troop": {"chars": {str(req["charInstId"]): {"skin": req["skinId"]}}}}}}
            self.info("make response")
            self.tBuilder.chars[req["charInstId"]]["skin"] = req["skinId"]
            flow.response = HTTPResponse.make(200,
                                              json.dumps(resp),
                                              {"Content-Type":"application/json; charset=utf-8"})
            self.info("Reply Complete")

    def response(self, flow: HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            self.info("Unlocking....")
            data["user"]["skin"]["characterSkins"] = dict((key, 1) for key in self.cBuilder.skins)
            flow.response.set_text(json.dumps(data))
            self.info("Complete")

class allChars(ArkInterceptor):
    '''
        Require: CharsEssential,BattleEssential
    '''
    def __init__(self):
        self.info("Loading success")

    def response(self, flow: HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            char = []
            self.info("Get character list")
            for c in self.tBuilder.cBuilder.characters.keys():
                if "char" in c:
                    char.append(c)
            self.info("add characters.....")
            for c in char:
                self.tBuilder.addCharacter(c)
            data["user"]["troop"] = self.tBuilder.dump()
            flow.response.set_text(json.dumps(data))
            self.info("Complete")


ArkInterceptor.cBuilder = characterBuilder.init("arkhack_data.json")

addons = [
    ArkEssential(),
    CharsEssential(),
    BattleEssential(),
    allChars(),
    graduateChars(),
    unlockSkins()
]
