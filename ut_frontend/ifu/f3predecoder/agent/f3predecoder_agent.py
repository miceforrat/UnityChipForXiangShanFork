from toffee import Agent, driver_method
from ..bundle import F3PreDecoderBundle

class F3PreDecodeData():
    brTypes = [] 
    isCalls = [] 
    isRets = []

    def __str__(self):
        return f"brTypes: {self.brTypes}\nisCalls: {self.isCalls}\nisRets: {self.isRets}"
    
    def __eq__(self, value):
        if type(value) != F3PreDecodeData:
            return False
        return str(self) == str(value)

class F3PreDecoderAgent(Agent):
    
    def __init__(self, bundle:F3PreDecoderBundle):
        super().__init__(bundle)
        self.bundle = bundle
    
    @driver_method()
    async def f3_predecode(self, instrs: list[int]) -> F3PreDecodeData:
        for i in range(16):
            self.bundle.in_instrs[i].value = instrs[i]
            # getattr(self.bundle.io._in_instr, f"_{i}").value= instrs[i]

        await self.bundle.step()

        ret = F3PreDecodeData()
        for i in range(16):
            ret.brTypes.append(self.bundle.out_pds[i]._brType.value)
            ret.isCalls.append(self.bundle.out_pds[i]._isCall.value)
            ret.isRets.append(self.bundle.out_pds[i]._isRet.value)

            # ret.brTypes.append(getattr(self.bundle.io._out_pd, f"_{i}")._brType.value)
            # ret.isCalls.append(getattr(self.bundle.io._out_pd, f"_{i}")._isCall.value)
            # ret.isRets.append(getattr(self.bundle.io._out_pd, f"_{i}")._isRet.value)
        return ret