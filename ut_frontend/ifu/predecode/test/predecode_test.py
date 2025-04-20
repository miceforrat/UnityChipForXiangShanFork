import toffee_test
from .predecode_fixture import predecode_env
from ..env import PreDecodeEnv
import random
import datetime
from .predecode_ckpt import appeared_poses, RVC_LABEL, RVI_FIRST_HALF_LABEL, RVI_SECOND_HALF_LABEL
from ...instr_utils import construct_non_cfis, construct_instrs

@toffee_test.testcase
async def test_smoke(predecode_env : PreDecodeEnv):
    fake_instrs = [19212 for i in range(17)]

    res = await predecode_env.predecode_agent.predecode(fake_instrs)

@toffee_test.testcase
async def test_last_start_rvi(predecode_env: PreDecodeEnv):
    random.seed(int(round(datetime.datetime.now().timestamp())))
    for i in range(200):
        instrs = []
        instrs.append(construct_non_cfis(False, True) >> 16)
        appeared_poses[0][RVI_SECOND_HALF_LABEL] = True

        for j in range(16):
            instrs.append(random.randint(0, (1 << 16) - 1))
        # print(instrs)
        await predecode_env.predecode_agent.predecode(instrs)

@toffee_test.testcase
async def test_jmps(predecode_env: PreDecodeEnv):
    base_num = 12
    for i in range(19):
        for x in range(base_num * 3):
            instrs = [0 for j in range(17)]
            pos = 0
            cfi_type = (x / base_num) + 1
            min = i if i < 16 else 16
            choose_to_stop_earlier = (x % base_num) < 2
            while pos <= min:
                if pos < i - 1:
                    choice =random.randint(0, 6)
                    if choice < 2 or (choose_to_stop_earlier and pos == i-2):
                        next = construct_non_cfis(True, True)
                        isRVI = False
                    else:
                        next = construct_non_cfis(False, True)
                        isRVI = True
                elif pos == i - 1:
                    if choose_to_stop_earlier:
                        next = construct_instrs(cfi_type, False)
                        isRVI = True
                    else:
                        next = construct_non_cfis(True, True)
                        isRVI = False
                        
                else:
                    next = construct_instrs(cfi_type, True)
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
            await predecode_env.predecode_agent.predecode(instrs)

# @toffee_test.testcase
# async def test_special_randoms(predecode_env: PreDecodeEnv):
#     for i in range(500):
#         pos = 0
#         instrs = [0 for j in range(17)]
#         while pos < 17:
#             next_choice = random.randint(0, 23)
#             if next_choice < 10: # choose random rvc
#                 next = gen_rvc()
#                 isRVI=False
#             elif next_choice < 20: # choose random rvi
#                 next = gen_rvi()
#                 isRVI = True
#             elif next_choice == 20: # choose rvc br
#                 next= gen_jmp(True, True)
#                 isRVI = False
#             elif next_choice == 21: # choose rvc j
#                 next = gen_jmp(False, True)
#                 isRVI = False
#             elif next_choice == 22: # choose rvi br
#                 next = gen_jmp(True, False)
#                 isRVI = True
#             else:
#                 next = gen_jmp(False, False)
#                 isRVI=True
            
#             instrs[pos] = next & ((1 << 16) - 1)
#             if pos < 16:
#                 if isRVI:
#                     appeared_poses[pos][RVI_FIRST_HALF_LABEL] = True
#                 else:
#                     appeared_poses[pos][RVC_LABEL] = True
#             pos += 1

#             if isRVI and pos < 17:
#                 instrs[pos] = next >> 16
#                 if pos < 16:
#                     appeared_poses[pos][RVI_SECOND_HALF_LABEL] = True
#                 pos += 1
#         await predecode_env.predecode_agent.predecode(instrs)


# @toffee_test.testcase
# async def test_totally_random(predecode_env: PreDecodeEnv):
#     random.seed(int(round(datetime.datetime.now().timestamp())))
#     for i in range(2000):
#         instrs = []
#         for j in range(17):
#             next = random.randint(0, 1 << 16 - 1)
#             instrs.append(next)
        
#         await predecode_env.predecode_agent.predecode(instrs)

