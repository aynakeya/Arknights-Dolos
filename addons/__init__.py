from mitmproxy.http import HTTPFlow
from model.troopBuilder import troopBuilder,characterBuilder
import re

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

    def inServersList(self,url):
        return re.match(r"ak-.*\.hypergryph.com",url) != None

    def info(self,msg):
        print("Arkhack - %s > %s" %(self.__class__.__name__,msg))


class ArkEssential(ArkInterceptor):
    def __init__(self):
        self.info("Load success")
    def http_connect(self, flow: HTTPFlow):
        # replace all localhost server to correct server
        if (flow.request.host in self.Servers.keys()):
            flow.request.host, flow.request.port = self.Servers.get(flow.request.host)