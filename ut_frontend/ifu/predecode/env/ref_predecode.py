from toffee import Model, driver_hook
from ..agent import PreDecodeDataDef
from ut_frontend.ifu.instr_utils import fetch, concat

class PredecodeRef(Model):

    @driver_hook(agent_name="predecode_agent")
    def predecode(self, instrs: list[int]) -> PreDecodeDataDef:
        ret = PreDecodeDataDef()

        for i in range(16):
            ret.new_instrs.append(instrs[i] | (instrs[i+1] << 16))
            ret.rvcs.append((ret.new_instrs[i] & 3) != 3)
            ret.jmp_offsets.append(self.calc_imm(ret.new_instrs[i]))
            ret.valid_starts.append(False)
            ret.half_valid_starts.append(False)

            if i == 0:
                ret.valid_starts[i] = True
                ret.half_valid_starts[i] = False
            elif i == 1:
                ret.half_valid_starts[i] = True
                ret.valid_starts[i] = ret.rvcs[0]
            else:
                if ret.half_valid_starts[i-1] == True:
                    ret.half_valid_starts[i] = ret.rvcs[i-1]
                else:
                    ret.half_valid_starts[i] = True
                
                if ret.valid_starts[i-1] == True:
                    ret.valid_starts[i] = ret.rvcs[i-1]
                else:
                    ret.valid_starts[i] = True
        return ret

    def calc_imm(self, instr):

        op = fetch(instr, 0, 1)
        funct = fetch(instr, 13, 15)

        if op == 1: # C.J or beq

            if funct == 6 or funct == 7: # beq 
                return concat(instr, [[12], [5, 6], [2], [10, 11], [3, 4]]) << 1
            
                # if funct == 5: # C.J
            return concat(instr, [[12], [8], [9, 10], [6],[7], [2], [3, 5]]) << 1
            
        rvi_funct = fetch(instr, 0, 6)
        
        if rvi_funct == 99: # 1100011 b
            return concat(instr, [[31], [7], [25, 30], [8, 11]]) << 1

        # if rvi_funct == 111: # "1101111 JAL"：
        return concat(instr, [[31], [12, 19], [20], [21, 30]]) << 1
        
        
