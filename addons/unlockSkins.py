from mitmproxy.http import HTTPFlow,HTTPResponse
from addons import ArkInterceptor
import json


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
            self.tBuilder.chars[str(req["charInstId"])]["skin"] = req["skinId"]
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
