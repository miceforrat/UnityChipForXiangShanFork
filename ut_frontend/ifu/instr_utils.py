## fetch [start, end] bits from num
def fetch(num, start, end):
    shift_left = (1 << (end - start + 1)) - 1
    return (num >> start) & shift_left

## pass in offs like [[], [], []], works similar to cat() in chisel
def concat(num, offs):
    ret = 0
    for off in offs:
        start = off[0]
        if len(off) == 1:
            end = off[0]
        elif len(off) == 2:
            end = off[1]
        move = end -start + 1
        ret <<= move
        mid = fetch(num, start, end)
        ret += mid
    return ret