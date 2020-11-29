from mitmproxy.http import HTTPFlow, HTTPResponse
from addons import ArkInterceptor
from model.troopBuilder import troopBuilder
import json,copy


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

#master.addons.add(CharsEssential())