import toffee_test
from .predecode_fixture import predecode_env
from ..env import PreDecodeEnv
import random
import datetime
from .predecode_ckpt import appeared_poses, RVC_LABEL, RVI_FIRST_HALF_LABEL, RVI_SECOND_HALF_LABEL

@toffee_test.testcase
async def test_smoke(predecode_env : PreDecodeEnv):
    fake_instrs = [19212 for i in range(17)]

    res = await predecode_env.predecode_agent.predecode(fake_instrs)

def gen_rvc():
    return (random.randint(0, (1 << 14) -1) << 2) | random.randint(0, 2)

def gen_rvi():
    return (random.randint(0, (1 << 30) -1 )  << 2) | 3

def gen_jmp(br, rvc):
    if rvc:
        if br: 
            return (random.randint(6, 7) << 13) | (random.randint(0, (1 << 11) - 1) << 2) | 1
        
        return (5 << 13) | (random.randint(0, (1 << 11) - 1) << 2) | 1

    if br:
        return (random.randint(0, (1 << 25) - 1) << 7) | 99
    return (random.randint(0, (1 << 25) - 1) << 7) | 111

@toffee_test.testcase
async def test_last_start_rvi(predecode_env: PreDecodeEnv):
    random.seed(int(round(datetime.datetime.now().timestamp())))
    for i in range(200):
        instrs = []
        instrs.append(gen_rvi() >> 16)
        appeared_poses[0][RVI_SECOND_HALF_LABEL] = True

        for j in range(16):
            instrs.append(random.randint(0, (1 << 16) - 1))
        # print(instrs)
        await predecode_env.predecode_agent.predecode(instrs)

@toffee_test.testcase
async def test_jmps(predecode_env: PreDecodeEnv):
    for i in range(17):
        for x in range(16):
            instrs = [0 for j in range(17)]
            pos = 0
            br = x < 8
            while pos < i:
                if pos < i - 2:
                    choice =random.randint(0, 6)
                    if choice < 2:
                        next = gen_rvc()
                        isRVI = False
                    else:
                        next = gen_rvi()
                        isRVI = True
                elif pos == i - 2:
                    choice =random.randint(0, 6)
                    if choice < 2:
                        next = gen_rvc()
                        isRVI = False
                    else:
                        next = gen_jmp(br, False)
                        isRVI = True
                else:
                    next = gen_jmp(br, True)
                    isRVI = False

                instrs[pos] = next & ((1 << 16) - 1)
                if pos < 16:
                    if isRVI:
                        appeared_poses[pos][RVI_FIRST_HALF_LABEL] = True
                    else:
                        appeared_poses[pos][RVC_LABEL] = True
                pos += 1

                if isRVI and pos < 17:
                    instrs[pos] = next >> 16
                    if pos < 16:
                        appeared_poses[pos][RVI_SECOND_HALF_LABEL] = True
                    pos += 1

@toffee_test.testcase
async def test_special_randoms(predecode_env: PreDecodeEnv):
    for i in range(500):
        pos = 0
        instrs = [0 for j in range(17)]
        while pos < 17:
            next_choice = random.randint(0, 23)
            if next_choice < 10: # choose random rvc
                next = gen_rvc()
                isRVI=False
            elif next_choice < 20: # choose random rvi
                next = gen_rvi()
                isRVI = True
            elif next_choice == 20: # choose rvc br
                next= gen_jmp(True, True)
                isRVI = False
            elif next_choice == 21: # choose rvc j
                next = gen_jmp(False, True)
                isRVI = False
            elif next_choice == 22: # choose rvi br
                next = gen_jmp(True, False)
                isRVI = True
            else:
                next = gen_jmp(False, False)
                isRVI=True
            
            instrs[pos] = next & ((1 << 16) - 1)
            if pos < 16:
                if isRVI:
                    appeared_poses[pos][RVI_FIRST_HALF_LABEL] = True
                else:
                    appeared_poses[pos][RVC_LABEL] = True
            pos += 1

            if isRVI and pos < 17:
                instrs[pos] = next >> 16
                if pos < 16:
                    appeared_poses[pos][RVI_SECOND_HALF_LABEL] = True
                pos += 1
        await predecode_env.predecode_agent.predecode(instrs)


# @toffee_test.testcase
# async def test_totally_random(predecode_env: PreDecodeEnv):
#     random.seed(int(round(datetime.datetime.now().timestamp())))
#     for i in range(2000):
#         instrs = []
#         for j in range(17):
#             next = random.randint(0, 1 << 16 - 1)
#             instrs.append(next)
        
#         await predecode_env.predecode_agent.predecode(instrs)

