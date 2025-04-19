from ut_frontend.ifu.instr_utils import fetch
from dut.PreDecode import DUTPreDecode
from toffee import CovGroup

RVC_LABEL = "rvc"
RVI_FIRST_HALF_LABEL = "rvi_first_half"
RVI_SECOND_HALF_LABEL = "rvi_second_half"

def ckpt_rvci(isRVC, i):

    def rvci_covered(dut: DUTPreDecode):

        instr = getattr(dut, f"io_out_instr_{i}").value
        rvc = fetch(instr, 0, 1) != 3

        if isRVC:
            return rvc
        return not rvc
    return rvci_covered

appeared_poses = [{RVC_LABEL: False, RVI_FIRST_HALF_LABEL: False, RVI_SECOND_HALF_LABEL: False} for i in range(16)]



def ckpt_jmp_offs(isBr, isRVC, i):

    def check_jmp(dut:DUTPreDecode):
        instr = getattr(dut, f"io_out_instr_{i}").value
        # print(f"{instr} in check jmp")
        op = fetch(instr, 0, 1)
        # print(f"fetched {op}")

        if isRVC:
            if op != 1:
                return False
            funct = fetch(instr, 13, 15)
            if isBr:
                # print("br true detected")
                return (funct == 6 or funct == 7)
            else:
                # print(f"j true detected")

                return funct == 5
            
        else:

            if op != 3:
                return False
            
            rvi_funct = fetch(instr, 0, 6)

            if isBr:
                return rvi_funct == 99
            else:
                return rvi_funct == 111
    return check_jmp
            
from comm import UT_FCOV

def get_coverage_group_of_predecode(dut: DUTPreDecode) -> CovGroup:
    g = CovGroup(UT_FCOV("../../PreDecode"))

    for i in range(16):
        instr_pin = getattr(dut, f"io_out_instr_{i}")
        g.add_watch_point(instr_pin,
        {
            f"{i}_concat_out":  lambda x: instr_pin.W() == 32
        },
        name=f"concat_hits_{i}"
        )

        g.add_watch_point(dut, 
            {
                f"{i}_rvc": ckpt_rvci(True, i),
                f"{i}_rvi": ckpt_rvci(False, i)
            },
            name=f"rvc_judge_hits_{i}"
        )

        g.add_watch_point(appeared_poses,
            {
                f"{i}_{RVC_LABEL}": lambda d: appeared_poses[i][RVC_LABEL],
                f"{i}_{RVI_FIRST_HALF_LABEL}": lambda d: appeared_poses[i][RVI_FIRST_HALF_LABEL],
                f"{i}_{RVI_SECOND_HALF_LABEL}": lambda d: appeared_poses[i][RVI_SECOND_HALF_LABEL]
            },
            name=f"valids_hits_{i}"       
        )

        # g.add_watch_point(appeared_poses,
        #     {
        #         f"{i}_{RVC_LABEL}": lambda: True,
        #         f"{i}_{RVI_FIRST_HALF_LABEL}": lambda: True,
        #         f"{i}_{RVI_SECOND_HALF_LABEL}": lambda: True
        #     },
        #     name=f"valids_hits_{i}"       
        # )

        g.add_watch_point(dut, 
            {
                f"{i}_rvc_br": ckpt_jmp_offs(True, True, i),
                f"{i}_rvc_j": ckpt_jmp_offs(False, True, i),
                f"{i}_rvi_br": ckpt_jmp_offs(True, False, i),
                f"{i}_rvi_j": ckpt_jmp_offs(False, False, i)                
            },
            name=f"off_cal_hits_{i}"   
        )
    return g



    