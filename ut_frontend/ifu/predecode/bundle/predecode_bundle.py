from toffee import Bundle, Signals, SignalList, BundleList

class _9Bundle(Bundle):
	_isRVC, _valid, _brType, _isCall, _isRet = Signals(5)

class _11Bundle(Bundle):
	instrs = SignalList("instr_#", 16)
	jumpOffsets = SignalList("jumpOffset_#", 16)
	hasHalfValids = SignalList("hasHalfValid_#", 16)
	pds = BundleList(_9Bundle, "pd_#", 16)

class PreDecodeBundle(Bundle):
	in_datas = SignalList("in_bits_data_#", 17)
	out = _11Bundle.from_prefix("out_")

