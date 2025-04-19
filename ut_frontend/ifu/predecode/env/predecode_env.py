from toffee import Env
from ..bundle import PreDecodeBundle
from dut.PreDecode import DUTPreDecode
from ..agent import PreDecodeAgent
from .ref_predecode import PredecodeRef

class PreDecodeEnv(Env):

    def __init__(self, dut: DUTPreDecode):
        super().__init__()
        bundle = PreDecodeBundle.from_prefix("io").bind(dut)
        self.predecode_agent = PreDecodeAgent(bundle)
        self.attach(PredecodeRef())
