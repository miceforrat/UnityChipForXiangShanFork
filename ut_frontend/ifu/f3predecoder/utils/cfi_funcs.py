from ut_frontend.ifu.instr_utils import fetch


def get_cfi_type(instr):
    op = fetch(instr, 0, 1)
    if op == 3: # RVI
        funct = fetch(instr, 0, 6)
        if funct == 99: # branch
            return 1

        if funct == 111: # jal
            return 2

        if funct == 103: # maybe jalr
            mids = fetch(instr, 12, 14)
            if mids == 0:
                return 3
        return 0
    else: # RVC
        funct = fetch(instr, 13, 15)
        if (funct == 6 or funct == 7) and op == 1:# c.beqz c.bnez
            return 1
        
        if funct == 5 and op == 1: # c.j
            return 2
        
        if funct == 4 and op == 2:
            rs2 = fetch(instr, 2, 6)
            rs1 = fetch(instr, 7, 11)
            if fetch(instr, 12, 12) == 1 and rs2 == 0 and rs1 != 0: # c.jalr
                return 3
            
            if fetch(instr, 12, 12) == 0 and rs2 == 0: # c.jr and hint
                return 3
        return 0
    

def if_call(instr, cfi):
    if cfi < 2 or cfi > 3:
        return False
    
    op = fetch(instr, 0, 1)
    if cfi == 2:
        if op == 3:
            rd = fetch(instr, 7, 11)
            if rd == 1 or rd == 5:
                return True
        return False
    
    # cfi == 3
    if op == 2:
        return fetch(instr, 12, 12) == 1
    elif op < 2 or op > 3:
        return False 
    
    rd = fetch(instr, 7, 11)
    return rd == 1 or rd == 5
    
def if_ret(instr, cfi):
    if cfi != 3:
        return False
    
    op = fetch(instr, 0, 1)
    if op == 3: # rvi
        rd = fetch(instr, 7, 11)
        rs = fetch(instr, 15, 19)
        return rd != 1 and rd !=5 and (rs == 1 or rs ==5)
    
    if op != 2:
        return False
    
    if fetch(instr, 12, 12) == 1:
        return False
    
    rs = fetch(instr, 7, 11)

    return rs == 1 or rs == 5