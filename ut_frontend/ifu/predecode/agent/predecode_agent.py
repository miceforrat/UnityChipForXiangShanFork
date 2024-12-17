from toffee import Agent
from ..bundle import PreDecodeBundle

class PreDecodeAgent(Agent):
    def __init__(self, bundle:PreDecodeBundle):
        super().__init__(bundle)
        self.bundle = bundle
    
    # input: 17 x 2B raw instrs
    # return: (16 x 4B instrs, 16 x jumpoffsets, 16 x RVC, 16 x (valid, half_valid) )
    def predecode(instrs: list[int]) -> tuple[list[int], list[int]]: