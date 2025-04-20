from toffee import Agent
from ..bundle import PreDecodeBundle
from toffee import *

class PreDecodeDataDef():
    new_instrs = []
    jmp_offsets = []
    rvcs = []
    valid_starts = []
    half_valid_starts = []

    def __str__(self):
        res = f"new instrs: {self.new_instrs}\njump offsets: {self.jmp_offsets}\nrvcs: {self.rvcs}\nvalid_starts: {self.valid_starts}\nhalf_valid_starts: {self.half_valid_starts}\n"
        return res
    
    def __eq__(self, value):
        if type(self) is not type(value):
            return False
        return self.__str__() == value.__str__()

class PreDecodeAgent(Agent):
    def __init__(self, bundle:PreDecodeBundle):
        super().__init__(bundle)
        self.bundle = bundle
    
    # input: 17 x 2B raw instrs
    # return: (16 x 4B instrs, 16 x jumpoffsets, 16 x RVC, 16 x (valid), 16 x half_valid )
    @driver_method()
    async def predecode(self, instrs: list[int]) -> PreDecodeDataDef:
        for i in range(17):
            self.bundle.in_datas[i].value = instrs[i]
        await self.bundle.step()
        ret = PreDecodeDataDef()

        for i in range(16):
            ret.new_instrs.append(self.bundle.out.instrs[i].value)
            ret.jmp_offsets.append(self.bundle.out.jumpOffsets[i].value)
            ret.rvcs.append(self.bundle.out.pds[i]._isRVC.value)

            if i == 0: 
                ret.half_valid_starts.append(0)
                ret.valid_starts.append(1)

            elif i == 1:
                ret.half_valid_starts.append(1)
                ret.valid_starts.append(self.bundle.out.pds[i]._valid.value)

            else:
                ret.half_valid_starts.append(self.bundle.out.hasHalfValids[i].value)
                ret.valid_starts.append(self.bundle.out.pds[i]._valid.value)

        return ret