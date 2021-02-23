from mitmproxy.http import HTTPFlow
from addons import ArkInterceptor
import json

class moreChars(ArkInterceptor):
    '''
        Require: CharsEssential,BattleEssential
    '''
    def __init__(self):
        self.execute = True
        self.extraChars = []
        self.info("Loading success")

    def addChar(self,char):
        self.extraChars.append(char)

    def addChars(self,chars):
        self.extraChars.extend(chars)

    def executable(self):
        return self.execute

    @ArkInterceptor.checkExecutable
    def response(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            for c in self.extraChars:
                self.info("Adding extra character - %s" %c)
                self.tBuilder.addCharacter(c,force=True)
            data["user"]["troop"] = self.tBuilder.dump()
            flow.response.set_text(json.dumps(data))
            self.info("Complete")
            self.execute = False

# mc = moreChars()
# mc.addChar("char_350_surtr")
# mc.addChars(["char_350_surtr"]*10+["char_172_svrash"]*10+["char_180_amgoat"]*10+["char_151_myrtle"]*5+["char_222_bpipe"]*5+["char_400_weedy"]*12)
# master.addons.add(mc)