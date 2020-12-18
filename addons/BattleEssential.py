from mitmproxy.http import HTTPFlow, HTTPResponse
from addons import ArkInterceptor
from model.troopBuilder import troopBuilder
import json,copy

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
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/quest/squadFormation"):
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

        if self.inServersList(flow.request.host) and (flow.request.path.startswith("/quest/battleStart") or
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
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/quest/squadFormation"):
            data = json.loads(flow.response.get_text())
            self.info('setting squad data for local modification')
            for sid in data['playerDataDelta']['modified']['troop']['squads'].keys():
                data['playerDataDelta']['modified']['troop']['squads'][sid] = self.tBuilder.squads[sid]
            flow.response.set_text(json.dumps(data))
            self.info("complete")

#master.addons.add(BattleEssential())

 # Deprecated
    # def _weak_request(self,flow: HTTPFlow):
    #     if self.inServersList(flow.request.host) and flow.request.path.startswith("/quest/squadFormation"):
    #         self.info("setting squad for remote server sync")
    #         req = json.loads(flow.request.get_text())
    #         self.tBuilder.squads[req["squadId"]]["slots"] = req["slots"]
    #         req = copy.deepcopy(req)
    #         for s in req['slots']:
    #             if s is not None and s["skillIndex"] != -1:
    #                 s["skillIndex"] = 0
    #         flow.request.set_text(json.dumps(req))
    #         self.info("complete")
    #     if self.inServersList(flow.request.host) and flow.request.path.startswith("/charBuild/setDefaultSkill"):
    #         self.info("Receive default skill change change request")
    #         req = json.loads(flow.request.get_text())
    #         self.tBuilder.chars[str(req["charInstId"])]["defaultSkillIndex"] = req["defaultSkillIndex"]
    #         resp = {"playerDataDelta": {"deleted": {},
    #                                     "modified": {
    #                                         "troop": {"chars": {str(req["charInstId"]): {"defaultSkillIndex": req["defaultSkillIndex"]}}}}}}
    #         self.info("make response")
    #         flow.response = HTTPResponse.make(200,
    #                                           json.dumps(resp),
    #                                           {"Content-Type": "application/json; charset=utf-8"})
    #         self.info("Reply Complete")
    #     if self.inServersList(flow.request.host) and flow.request.path.startswith("/quest/battleStart"):
    #         self.info("battle start: setting squad for remote server")
    #         req = json.loads(flow.request.get_text())
    #         for s in req['squad']['slots']:
    #             if s is not None and s["skillIndex"] != -1:
    #                 s["skillIndex"] = 0
    #         flow.request.set_text(json.dumps(req))
    #         self.info("complete")
    #
    #
    # def _weak_response(self,flow: HTTPFlow):
    #     if self.inServersList(flow.request.host) and flow.request.path.startswith("/quest/squadFormation"):
    #         data = json.loads(flow.response.get_text())
    #         self.info('setting squad data for local modification')
    #         for sid in data['playerDataDelta']['modified']['troop']['squads'].keys():
    #             data['playerDataDelta']['modified']['troop']['squads'][sid] = self.tBuilder.squads[sid]
    #         flow.response.set_text(json.dumps(data))
    #         self.info("complete")