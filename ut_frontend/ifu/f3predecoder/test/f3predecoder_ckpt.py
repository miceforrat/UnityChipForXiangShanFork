from dut.F3Predecoder import DUTF3Predecoder
from toffee import CovGroup
from ..utils import get_cfi_type, if_ret, if_call

def cfi_type_ckpt(tgt_type):
    def check_cfi_type(instr_pin):
        instr = instr_pin.value
        return get_cfi_type(instr) == tgt_type
    return check_cfi_type

def check_call_ret_instrs(tgt_type, ifcallret, which_sp, rvc=False, rvc_checked=False):
    def check_cfi_call(instr_pin):
        instr = instr_pin.value
        instr_type = get_cfi_type(instr)
        if instr_type != tgt_type:
            return False
        if rvc_checked and ((instr & 3) < 3) != rvc:
            return False
        if which_sp > 0:
            return ifcallret == if_ret(instr, instr_type)
        return ifcallret == if_call(instr, instr_type)
    return check_cfi_call
    

def get_coverage_group_of_predecode(dut: DUTF3Predecoder) -> CovGroup:
    g = CovGroup("F3Predecoder")

    sp_types = ["call", "ret"]
    for i in range(16):
        instr = getattr(dut, f"io_in_instr_{i}")
        g.add_watch_point(instr,
            {
                f"instr_{i}_nocfi": cfi_type_ckpt(0),
                f"instr_{i}_br": cfi_type_ckpt(1),
                f"instr_{i}_jal": cfi_type_ckpt(2),
                f"instr_{i}_jalr": cfi_type_ckpt(3),
            }, name=f"instr_{i}_cfi_type_watcher"
        )

        for j in range(2):
            sp_type = sp_types[j]
            next_gs = {
                f"instr_{i}_nocfi_{sp_type}_always_false": check_call_ret_instrs(0, False, j), 
                f"instr_{i}_br_{sp_type}_always_false": check_call_ret_instrs(1, False, j), 
                f"instr_{i}_c_jal_{sp_type}_false": check_call_ret_instrs(2, False, j, True, True), 
                f"instr_{i}_c_jal_{sp_type}_false": check_call_ret_instrs(2, False, j, False, True), 
                f"instr_{i}_c_jalr_{sp_type}_false": check_call_ret_instrs(3, False, j, True, True), 
                f"instr_{i}_c_jalr_{sp_type}_true": check_call_ret_instrs(3, True, j, True, True), 
                f"instr_{i}_i_jalr_{sp_type}_false": check_call_ret_instrs(3, False, j, False, True), 
                f"instr_{i}_i_jalr_{sp_type}_true": check_call_ret_instrs(3, True, j, False, True), 
            }        
            if sp_type == "call":
                next_gs[ f"instr_{i}_i_jal_{sp_type}_true"] = check_call_ret_instrs(2, True, j, False, True)
            g.add_watch_point(
                instr, next_gs, name=f"{sp_type}_{i}_watcher"
            )
    return g