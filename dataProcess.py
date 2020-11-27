import json

character_table = "./data/character_table.json"
skin_table = "./data/skin_table.json"
maxStatus = {0:{"level":30,"potentialRank":5,"mainSkillLvl":1,"favorPoint":240000},
             1:{},
             2:{"level":55,"mainSkillLvl":7,"evolvePhase":1},
             3:{"level":70,"evolvePhase":2},
             4:{"level":80},
             5:{"level":90}}

def processCharacter(ct,st):
    newdata = {}
    skinlist = []
    with open(ct,"r",encoding="utf8") as f:
        data = json.loads(f.read().strip())
        for key,value in data.items():
            newdata[key] = {"rarity":value["rarity"],"obtainable":not value["isNotObtainable"],"skills":[skill["skillId"] for skill in value["skills"]],"skins":[]}
    with open(st,"r",encoding="utf8") as f:
        data = json.loads(f.read().strip())
        for key,value in data["charSkins"].items():
            newdata[value["charId"]]["skins"].append(value["skinId"])
            if ("@" in value["skinId"]):
                skinlist.append(value["skinId"])

    with open("./data/arkhack_data.json","w",encoding="utf8") as f:
        f.write(json.dumps({"character":newdata,"shopskins":skinlist,"maxstatus":maxStatus},indent=2))

processCharacter(character_table,skin_table)