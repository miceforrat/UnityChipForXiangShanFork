from .f3predecoder_fixture import f3predecoder_env
from ..env import F3PreDecoderEnv
import toffee_test
import random
from ..utils import get_cfi_type

@toffee_test.testcase
async def test_smoke(f3predecoder_env : F3PreDecoderEnv):
    instrs = [483 for i in range(16)]

    await f3predecoder_env.agent.f3_predecode(instrs)

def construct_brs(rvc):
    if rvc:
        return (3 << 14 ) | (random.randint(0, 1) << 13) | (random.randint(0, (1 << 11) - 1) << 2) | 1
    else:
        return (random.randint(0, (1 << 25)-1 ) << 7) | 99

def construct_jal(rvc):
    if rvc:
        return (5 << 13) | (random.randint(0, (1 << 11) - 1 ) << 2) | 1
    
    return (random.randint(0, (1 << 25) -1 )  << 7) |  111

def construct_jalr(rvc):
    if rvc:
        rvc_jalr = (4 << 13) | (random.randint(0, 63) << 7) | 2
        return  rvc_jalr

    return (random.randint(0, (1 << 17) - 1) << 15) | (random.randint(0, 31) << 7) | 103

@toffee_test.testcase
async def test_random_for_cfis(f3predecoder_env : F3PreDecoderEnv):
    random.seed(14530529)
    for _ in range(2000):
        instrs = []
        for i in range(16):
            choice = random.randint(0, 7)
            cfi_type_choice = (choice & 6) >> 1
            rvc_choice = choice & 1
            if cfi_type_choice == 0:
                # 随机，虽然也有概率随机到其他三种类型
                while True:
                    instr = random.randint(0, (1 << 32) - 1)
                    if get_cfi_type(instr) == 0:
                        instrs.append(instr)
                        break

            elif cfi_type_choice == 1:
                instrs.append(construct_brs(rvc_choice))
            
            elif cfi_type_choice == 2:
                instrs.append(construct_jal(rvc_choice))
            else:
                instrs.append(construct_jalr(rvc_choice))
        await f3predecoder_env.agent.f3_predecode(instrs)
