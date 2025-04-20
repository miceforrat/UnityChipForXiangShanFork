from toffee import Bundle, Signals, SignalList, Signal, BundleList

# class _0Bundle(Bundle):
# 	_13, _6, _9, _2, _4, _10, _14, _3, _7, _12, _11, _15, _1, _8, _5, _0 = Signals(16)

class _5Bundle(Bundle):
	valid, bits = Signals(2)

class _6Bundle(Bundle):
	_isRet, _brType, _isRVC = Signals(3)

# class _7Bundle(Bundle):
# 	_0 = _6Bundle.from_prefix("_0")
# 	_1 = _6Bundle.from_prefix("_1")
# 	_4 = _6Bundle.from_prefix("_4")
# 	_7 = _6Bundle.from_prefix("_7")
# 	_10 = _6Bundle.from_prefix("_10")
# 	_9 = _6Bundle.from_prefix("_9")
# 	_11 = _6Bundle.from_prefix("_11")
# 	_13 = _6Bundle.from_prefix("_13")
# 	_3 = _6Bundle.from_prefix("_3")
# 	_2 = _6Bundle.from_prefix("_2")
# 	_8 = _6Bundle.from_prefix("_8")
# 	_12 = _6Bundle.from_prefix("_12")
# 	_5 = _6Bundle.from_prefix("_5")
# 	_15 = _6Bundle.from_prefix("_15")
# 	_14 = _6Bundle.from_prefix("_14")
# 	_6 = _6Bundle.from_prefix("_6")

class _8Bundle(Bundle):
	fire_in, target = Signals(2)
	instrValids = SignalList("instrValid_#", 16)
	# _0Bundle.from_prefix("_instrValid")
	instrRanges = SignalList("instrRange_#", 16)
	pcs = SignalList("pc_#", 16)
	jumpOffsets = SignalList("jumpOffset_#", 16)
	ftqOffset = _5Bundle.from_prefix("ftqOffset_")
	pds = BundleList(_6Bundle, "pds_#", 16)

class _9Bundle(Bundle):
	fixedRanges = SignalList("fixedRange_#", 16)
	fixedTakens = SignalList("fixedTaken_#", 16)

class singleFaultTypeBundle(Bundle):
	_value = Signal()

# class faultTypesBundle(Bundle):
# 	_12 = singleFaultTypeBundle.from_prefix("_12")
# 	_1 = singleFaultTypeBundle.from_prefix("_1")
# 	_9 = singleFaultTypeBundle.from_prefix("_9")
# 	_15 = singleFaultTypeBundle.from_prefix("_15")
# 	_6 = singleFaultTypeBundle.from_prefix("_6")
# 	_5 = singleFaultTypeBundle.from_prefix("_5")
# 	_7 = singleFaultTypeBundle.from_prefix("_7")
# 	_3 = singleFaultTypeBundle.from_prefix("_3")
# 	_4 = singleFaultTypeBundle.from_prefix("_4")
# 	_2 = singleFaultTypeBundle.from_prefix("_2")
# 	_11 = singleFaultTypeBundle.from_prefix("_11")
# 	_8 = singleFaultTypeBundle.from_prefix("_8")
# 	_14 = singleFaultTypeBundle.from_prefix("_14")
# 	_13 = singleFaultTypeBundle.from_prefix("_13")
# 	_10 = singleFaultTypeBundle.from_prefix("_10")
# 	_0 = singleFaultTypeBundle.from_prefix("_0")

class _10Bundle(Bundle):
	fixedTargets = SignalList("fixedTarget_#", 16)
	fixedMissPreds = SignalList("fixedMissPred_#", 16)
	jalTargets = SignalList("jalTarget_#", 16)
	faultTypes = SignalList("faultType_#_value", 16)

class _11Bundle(Bundle):
	stage2Out = _10Bundle.from_prefix("stage2Out_")
	stage1Out = _9Bundle.from_prefix("stage1Out_")

class _12Bundle(Bundle):
	_in = _8Bundle.from_prefix("_in_")
	_out = _11Bundle.from_prefix("_out_")

class PredCheckerBundle(Bundle):
	clock = Signal()
	# PredChecker = _4Bundle.from_prefix("PredChecker")
	io = _12Bundle.from_prefix("io")

