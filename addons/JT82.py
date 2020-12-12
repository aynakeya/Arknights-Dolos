from mitmproxy.http import HTTPFlow, HTTPResponse
from addons import ArkInterceptor
from model.troopBuilder import troopBuilder
import json, copy


class JT82(ArkInterceptor):
    '''
        Require: BattleEssential
    '''

    def __init__(self):
        self.info("Loading success")

    def response(self, flow: HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/account/syncData"):
            data = json.loads(flow.response.get_text())
            data["user"]["dungeon"]["stages"]["main_08-17"] = {"stageId": "main_08-17", "completeTimes": 0, "startTimes": 0, "practiceTimes": 0, "state": 0,
                 "hasBattleReplay": 0, "noCostCnt": 1}
            flow.response.set_text(json.dumps(data))
            self.info("Complete")

    def request(self, flow: HTTPFlow):
        if flow.request.host in self.ServersList and flow.request.path.startswith("/quest/battleStart"):
            req = json.loads(flow.request.get_text())
            if (req["stageId"] != "main_08-16"):
                return
            self.info("Receive JT8-2 battle start request")
            fakeData = {
                "apFailReturn": 20,
                "battleId": "6c86c7c0-3373-11eb-9784-0d36b8275660",
                "isApProtect": 0,
                "notifyPowerScoreNotEnoughIfFailed": False,
                "playerDataDelta": {
                    "deleted": {},
                    "modified": {
                        # "dungeon": {
                        #     "stages": {
                        #         "main_07-01": {
                        #             "completeTimes": 1,
                        #             "hasBattleReplay": 1,
                        #             "noCostCnt": 0,
                        #             "practiceTimes": 0,
                        #             "stageId": "main_07-01",
                        #             "startTimes": 2,
                        #             "state": 3
                        #         }
                        #     }
                        # }
                    }
                },
                "result": 0
            }
            flow.response = HTTPResponse.make(200, json.dumps(fakeData),
                                              {"Content-Type": "application/json; charset=utf-8"})
            self.info("complete")
