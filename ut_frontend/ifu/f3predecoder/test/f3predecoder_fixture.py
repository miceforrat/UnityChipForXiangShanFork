import toffee_test
from dut.F3Predecoder import DUTF3Predecoder
from toffee import start_clock
from ..env import F3PreDecoderEnv
from .f3predecoder_ckpt import get_coverage_group_of_predecode

@toffee_test.fixture
async def f3predecoder_env(toffee_request: toffee_test.ToffeeRequest):
    dut = toffee_request.create_dut(DUTF3Predecoder)
    toffee_request.add_cov_groups(get_coverage_group_of_predecode(dut))
    start_clock(dut)
    predecode_env = F3PreDecoderEnv(dut)
    yield predecode_env
    import asyncio
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
