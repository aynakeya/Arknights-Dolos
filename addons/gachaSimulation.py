from mitmproxy.http import HTTPFlow,HTTPResponse
from addons import ArkInterceptor
import json,random


class gachaSimulation(ArkInterceptor):
    '''
        Require: CharsEssential,allChars
    '''
    dataPath = "./data/arkhack_pool.json"

    def __init__(self, dp=dataPath,baodi = True):
        self.poolData = {
            "poolInfo": [
                {"rarityRank": 5,"charIdList": ["char_103_angel"],"totalPercent": 0.02,"upPercent":0.5},
                {"rarityRank": 4,"charIdList": ["char_103_angel"],"totalPercent": 0.08,"upPercent":0.5},
                {"rarityRank": 3,"charIdList": ["char_103_angel"],"totalPercent": 0.5,"upPercent":0.2},
                {"rarityRank": 2, "charIdList": ["char_103_angel"], "totalPercent": 0.4,"upPercent":0}
            ]}
        try:
            with open(dp,"r",encoding="utf-8") as f:
                self.poolData = json.loads(f.read().strip())
        except Exception as e:
            pass
        self.rarityList = []
        self.gachaList = {}
        self.upChar = {"char_103_angel"}
        self.updateInfo()
        self.count = 0
        self.baodi = baodi
        self.info("Loading success")

    def setUp(self,*args):
        self.upChar = set(args)
        self.updateInfo()

    def addUp(self,*args):
        for arg in args:
            self.upChar.add(arg)
        self.updateInfo()

    def updateInfo(self):
        self.rarityList = [str(x["rarityRank"]) for x in self.poolData["poolInfo"] for i in range(int(x["totalPercent"]*100))]
        random.shuffle(self.rarityList)
        self.upnormalList = {}
        for x in self.poolData["poolInfo"]:
            rarity = str(x["rarityRank"])
            self.upnormalList[rarity] = ["up" for i in range(int(x["upPercent"]*100))]+["normal" for i in range(100-int(x["upPercent"]*100))]
            self.gachaList[rarity] = {}
            self.gachaList[rarity]["normal"] = list(set(x["charIdList"]).difference(self.upChar))
            self.gachaList[rarity]["up"] = list(set(x["charIdList"]).intersection(self.upChar))
            if len(self.gachaList[rarity]["normal"]) == 0:
                self.gachaList[rarity]["normal"] = x["charIdList"]
            if len(self.gachaList[rarity]["up"]) == 0:
                self.gachaList[rarity]["up"] = x["charIdList"]

    def updateRarityList(self):
        for i in range(len(self.rarityList)):
            if self.rarityList[i] != "5":
                self.rarityList[i] = "5"
                return
    def getOne(self):
        self.count +=1
        if self.baodi and self.count >50:
            for i in range(2):
                self.updateRarityList()
        rarity = random.choice(self.rarityList)
        if rarity == "5":
            self.count =0
            self.updateInfo()
        pl = random.choice(self.upnormalList[rarity])
        return (random.choice(self.gachaList[rarity][pl]),rarity)

    def getTen(self):
        return [self.getOne() for x in range(10)]

    def request(self, flow:HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/gacha/tenAdvancedGacha"):
            respData= {"gachaResultList":[],"playerDataDelta":{"deleted":{},"modified":{}}, "result": 0}
            self.info("十连中...")
            charlist = self.getTen()
            for charId,rarity in charlist:
                gacha = {}
                gacha["isNew"] = 0
                gacha["charId"] = charId
                cdata = self.tBuilder.getCharData(charId)
                if cdata == None:
                    continue
                gacha["charInstId"] = cdata["instId"]
                if rarity == "5":
                    gacha["itemGet"] = [
                        {
                            "count": 15,
                            "id": "4004",
                            "type": "HGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_"+charId,
                            "type": "MATERIAL"
                        }
                    ]
                if rarity == "4":
                    gacha["itemGet"] = [
                        {
                            "count": 8,
                            "id": "4004",
                            "type": "HGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_"+charId,
                            "type": "MATERIAL"
                        }
                    ]
                if rarity == "3":
                    gacha["itemGet"] = [
                        {
                            "count": 30,
                            "id": "4005",
                            "type": "LGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_"+charId,
                            "type": "MATERIAL"
                        }
                    ]
                if rarity == "2":
                    gacha["itemGet"] = [
                        {
                            "count": 5,
                            "id": "4005",
                            "type": "LGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_"+charId,
                            "type": "MATERIAL"
                        }
                    ]
                respData["gachaResultList"].append(gacha)
            flow.response = HTTPResponse.make(200, json.dumps(respData),
                                              {"Content-Type": "application/json; charset=utf-8"})
            self.info("完成")
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/gacha/advancedGacha"):
            respData= {"charGet":{},"playerDataDelta":{"deleted":{},"modified":{}}, "result": 0}
            self.info("单抽中...")
            charId,rarity = self.getOne()
            gacha = {}
            gacha["isNew"] = 0
            gacha["charId"] = charId
            cdata = self.tBuilder.getCharData(charId)
            gacha["charInstId"] = cdata["instId"]
            if rarity == "5":
                gacha["itemGet"] = [
                    {
                        "count": 15,
                        "id": "4004",
                        "type": "HGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]
            if rarity == "4":
                gacha["itemGet"] = [
                    {
                        "count": 8,
                        "id": "4004",
                        "type": "HGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]
            if rarity == "3":
                gacha["itemGet"] = [
                    {
                        "count": 30,
                        "id": "4005",
                        "type": "LGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]
            if rarity == "2":
                gacha["itemGet"] = [
                    {
                        "count": 5,
                        "id": "4005",
                        "type": "LGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]

            respData["charGet"] = gacha
            flow.response = HTTPResponse.make(200, json.dumps(respData),
                                              {"Content-Type": "application/json; charset=utf-8"})
            self.info("完成")

