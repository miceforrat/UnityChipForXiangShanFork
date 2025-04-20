from toffee import Model, driver_hook
from ..agent import F3PreDecodeData
from ...instr_utils import get_cfi_type, if_ret, if_call


class F3PredecoderRef(Model):

    @driver_hook(agent_name="agent")
    def f3_predecode(self, instrs: list[int]) -> F3PreDecodeData: 
        ret = F3PreDecodeData()
        for i in range(16):
            instr = instrs[i]
            ret.brTypes.append(get_cfi_type(instr))
            ret.isCalls.append(1 if if_call(instr, ret.brTypes[i]) else 0)
            ret.isRets.append(1 if if_ret(instr, ret.brTypes[i]) else 0)
        return ret
        
            
        
