from .f3predecoder_fixture import f3predecoder_env
from ..env import F3PreDecoderEnv
import toffee_test
import random
from ...instr_utils import construct_instrs

@toffee_test.testcase
async def test_smoke(f3predecoder_env : F3PreDecoderEnv):
    instrs = [0 for i in range(16)]
    instrs[1] = 32770
    res = await f3predecoder_env.agent.f3_predecode(instrs)
    print(res)
    # await f3predecoder_env.agent.bundle.step()

@toffee_test.testcase
async def test_random_for_cfis(f3predecoder_env : F3PreDecoderEnv):
    random.seed(14530529)
    for _ in range(20000):
        instrs = []
        for i in range(16):
            choice = random.randint(0, 7)
            cfi_type_choice = (choice & 6) >> 1
            rvc_choice = choice & 1
            instrs.append(construct_instrs(cfi_type_choice, rvc_choice))
        await f3predecoder_env.agent.f3_predecode(instrs)
