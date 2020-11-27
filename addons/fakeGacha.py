from mitmproxy.http import HTTPFlow
from addons import ArkInterceptor
import json

class fakeGacha(ArkInterceptor):
    def response(self, flow: HTTPFlow):
        # do something in response
        if flow.request.host in self.ServersList and flow.request.path.startswith("/gacha/tenAdvancedGacha"):
            print("开始制作虚假的10连")
            data = json.loads(flow.response.get_text())
            for index, gacha in enumerate(data["gachaResultList"]):
                if (index == 0):
                    gacha["isNew"] = 1
                    gacha["charInstId"] = 42
                    gacha["itemGet"] = [
                        {
                            "count": 1,
                            "id": "4004",
                            "type": "HGG_SHD"
                        }
                    ]
                else:
                    gacha["isNew"] = 0
                    gacha["charInstId"] = 42
                    gacha["itemGet"] = [
                        {
                            "count": 10,
                            "id": "4004",
                            "type": "HGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_char_2013_cerber",
                            "type": "MATERIAL"
                        }
                    ]
                gacha["charId"] = "char_2013_cerber"
            flow.response.set_text(json.dumps(data))
            print("修改完成")