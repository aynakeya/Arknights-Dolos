from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import master
from addons import ArkEssential,ArkInterceptor
from addons.userStatus import userInfo,userData
from addons.graduateChars import graduateChars
from addons.unlockSkins import unlockSkins
from addons.CharsEssential import CharsEssential
from addons.BattleEssential import BattleEssential
from model.troopBuilder import troopBuilder

class ProxyMaster(DumpMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        print("run")
        try:
            DumpMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

def run_web_debug(options):
    '''

    :param options:
    :return:
    '''
    from mitmproxy.tools import web
    webserver = web.master.WebMaster(options)
    webserver.server = ProxyServer(ProxyConfig(options))
    return webserver  # type: master.Master


def run_proxy(options, **kwargs):
    server = ProxyMaster(options, with_termlog=False, with_dumper=False, **kwargs)
    server.server = ProxyServer(ProxyConfig(options))
    return server  # type: master.Master


if __name__ == "__main__":
    ops = Options(listen_host='0.0.0.0', listen_port=8080, http2=True, ssl_insecure=True)
    master = run_web_debug(ops)
    #ArkInterceptor.tBuilder = troopBuilder.init()
    master.addons.add(ArkEssential())
    master.addons.add(CharsEssential())
    master.addons.add(BattleEssential())
    # master.addons.add(fakeGacha())
    #master.addons.add(userInfo.init("Rua牛","0000",120,0))
    #master.addons.add(userData.init(999,999,1919810,114514,6666666))
    #master.addons.add(graduateChars())
    #master.addons.add(unlockSkins())
    master.run()
