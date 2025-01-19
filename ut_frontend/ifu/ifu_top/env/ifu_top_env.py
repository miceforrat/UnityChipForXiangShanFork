from ..agent import FTQAgent, ICacheAgent
from ..bundle import IFUTopBundle
from toffee import Env
from dut.NewIFU import DUTNewIFU

class IFUTopEnv(Env):
    def __init__(self, dut: DUTNewIFU):
        super().__init__()
        top_bundle = IFUTopBundle.from_prefix("").bind(dut)
        self.ftq_agent = FTQAgent(top_bundle.io_ftqInter, top_bundle.internal_flushes)
        self.icache_agent = ICacheAgent(top_bundle._icacheInterCtrl)
    