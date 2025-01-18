from toffee import Env
from dut.F3Predecoder import DUTF3Predecoder
from ..agent import F3PreDecoderAgent
from ..bundle import F3PreDecoderBundle
from .ref_f3predecoder import F3PredecoderRef

class F3PreDecoderEnv(Env):

    def __init__(self, dut:DUTF3Predecoder):
        super().__init__()
        
        bundle = F3PreDecoderBundle.from_prefix("").bind(dut)
        bundle.io._in_instr.set_write_mode_as_imme()

        self.agent = F3PreDecoderAgent(bundle)
        self.attach(F3PredecoderRef())
