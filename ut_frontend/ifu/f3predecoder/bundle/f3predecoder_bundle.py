from toffee import Bundle, Signals, SignalList, BundleList

class infoBundle(Bundle):
	_brType, _isCall, _isRet = Signals(3)

class F3PreDecoderBundle(Bundle):
	in_instrs = SignalList("in_instr_#", 16)
	out_pds = BundleList(infoBundle,"out_pd_#", 16)

