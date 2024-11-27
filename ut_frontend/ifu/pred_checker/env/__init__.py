from toffee import Env
from ..agent import PredCheckerAgent
from ..bundle import PredCheckerIOBundle


class PredCheckerEnv(Env):

    def __init__(self, predCheckerBundle: PredCheckerIOBundle):
        super().__init__()
        self.predCheckerAgent = PredCheckerAgent(predCheckerBundle)