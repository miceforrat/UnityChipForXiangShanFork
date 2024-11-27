from toffee.agent import *
from ..bundle import PredCheckerIOBundle
from ... import PREDICT_WIDTH, RVC_LABEL, RET_LABEL, BRTYPE_LABEL

class PredCheckerAgent(Agent):
    def __init__(self, bundle: PredCheckerIOBundle):
        super().__init__(bundle)
        self.bundle = bundle

    @driver_method()
    async def agent_pred_check(self, ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
        self.bundle.sig_in.ftqOffset_valid.value = ftqValid
        self.bundle.sig_in.ftqOffset_bits.value = ftqOffBits
        self.bundle.sig_in.target.value = tgt
        self.bundle.sig_in.fire_in.value = fire
        print(self.bundle.sig_in.ftqOffset_valid.value)
        print("binds_single_finished")
        
        for i in range(PREDICT_WIDTH):
            getattr(self.bundle.sig_in, f'pc_{i}').value = pc[i]
            getattr(self.bundle.sig_in, f'instrRange_{i}').value = instrRange[i]
            getattr(self.bundle.sig_in, f'instrValid_{i}').value = instrValid[i]
            getattr(self.bundle.sig_in, f'jumpOffset_{i}').value = jumpOffset[i]
            
            # pd = getattr(self.bundle.sig_in, f'pds_{i}_')
            # pd = self.bundle.sig_in.pds[i]
            getattr(self.bundle.sig_in, f'pds_{i}_').isRVC.value = pds[i][RVC_LABEL]
            getattr(self.bundle.sig_in, f'pds_{i}_').brType.value = pds[i][BRTYPE_LABEL]
            getattr(self.bundle.sig_in, f'pds_{i}_').isRet.value = pds[i][RET_LABEL]
            # print(pd.brType.value)
        await self.bundle.step(2)
        # await self.bundle.step()
        stg1_fixedRange = [getattr(self.bundle.sig_out.stage1Out, f'fixedRange_{i}').value for i in range(PREDICT_WIDTH)]
        stg1_fixedTaken = [getattr(self.bundle.sig_out.stage1Out, f'fixedTaken_{i}').value for i in range(PREDICT_WIDTH)]

        stg2_fixedTarget = [getattr(self.bundle.sig_out.stage2Out, f'fixedTarget_{i}').value for i in range(PREDICT_WIDTH)]
        stg2_fixedMissPred = [getattr(self.bundle.sig_out.stage2Out, f'fixedMissPred_{i}').value for i in range(PREDICT_WIDTH)]
        stg2_jalTarget = [getattr(self.bundle.sig_out.stage2Out, f'jalTarget_{i}').value for i in range(PREDICT_WIDTH)]

        return stg1_fixedRange, stg1_fixedTaken, \
                stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred