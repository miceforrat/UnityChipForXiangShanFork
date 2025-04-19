from toffee import Bundle, Signals, SignalList, BundleList

class _9Bundle(Bundle):
	_isRVC, _valid, _brType, _isCall, _isRet = Signals(5)

class _11Bundle(Bundle):
	instrs = SignalList("_instr_#", 16)
	jumpOffsets = SignalList("_jumpOffset_#", 16)
	_hasHalfValid = SignalList("_hasHalfValid_#", 16)
	pds = BundleList(_9Bundle, "_pd_#", 16)

class PreDecodeBundle(Bundle):
	in_datas = SignalList("_in_bits_data_#", 17)
	_out = _11Bundle.from_prefix("_out")

