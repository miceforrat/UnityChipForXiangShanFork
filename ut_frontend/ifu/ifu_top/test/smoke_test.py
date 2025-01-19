import toffee_test
from .top_test_fixture import ifu_env
from ..env import IFUTopEnv
from toffee import Executor
from ..agent import FTQQuery, ICacheResp

import random 

@toffee_test.testcase
async def test_smoke(ifu_top_env : IFUTopEnv):

    ftq_query = FTQQuery()
    ftq_query.ftqIdx.flag = False
    ftq_query.ftqIdx.value = 2

    ftq_query.ftqOffset.exists = False
    ftq_query.ftqOffset.offsetIdx = 0 
    ftq_query.startAddr = random.randint(0, (1 << 50) - 1)
    ftq_query.nextlineStart = ftq_query.startAddr + 64

    # TBD: 随机生成指令序列之后再造一个
    prepare_next = random.randint(0, (1 << 50) - 128)
    ftq_query.nextStartAddr = (random.randint(0, (1 << 50) - 128) + ftq_query.startAddr) % (ftq_query.startAddr - 64)

    icache_resp = ICacheResp()
    icache_resp.backend_exception = False
    icache_resp.double_line = (ftq_query.startAddr & 256)
    icache_resp.pmp_mmios[0] = False
    icache_resp.pmp_mmios[1] = False
    
    async with Executor() as exec:
        exec(ifu_top_env.ftq_agent.ftq_query(ftq_query))
        exec(ifu_top_env.icache_agent.fake_resp(True, )) 


