import toffee_test
from dut.PreDecode import DUTPreDecode
from ..env import PreDecodeEnv
from toffee import start_clock
from .predecode_ckpt import get_coverage_group_of_predecode


@toffee_test.fixture
async def predecode_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    # version_check()
    dut = toffee_request.create_dut(DUTPreDecode)
    toffee_request.add_cov_groups([
        get_coverage_group_of_predecode(dut)
    ])
    start_clock(dut)
    predecode_env = PreDecodeEnv(dut)
    yield predecode_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break