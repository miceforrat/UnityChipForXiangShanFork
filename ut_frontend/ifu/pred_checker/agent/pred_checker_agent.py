from toffee.agent import *
from ..bundle import PredCheckerBundle
from ... import PREDICT_WIDTH, RVC_LABEL, RET_LABEL, BRTYPE_LABEL

class PredCheckerAgent(Agent):
    def __init__(self, bundle: PredCheckerBundle):
        super().__init__(bundle)
        self.bundle = bundle

    @driver_method()
    async def agent_pred_check(self, ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
        self.bundle.io._in.ftqOffset.valid.value = ftqValid
        self.bundle.io._in.ftqOffset.bits.value = ftqOffBits
        self.bundle.io._in.target.value = tgt
        self.bundle.io._in.fire_in.value = fire
        print("binds_single_finished")
        for i in range(PREDICT_WIDTH):
            self.bundle.io._in.pcs[i].value = pc[i]
            self.bundle.io._in.instrRanges[i].value = instrRange[i]
            self.bundle.io._in.instrValids[i].value = instrValid[i]
            self.bundle.io._in.jumpOffsets[i].value = jumpOffset[i]
            
            self.bundle.io._in.pds[i]._isRVC.value = pds[i][RVC_LABEL]
            self.bundle.io._in.pds[i]._brType.value = pds[i][BRTYPE_LABEL]
            self.bundle.io._in.pds[i]._isRet.value = pds[i][RET_LABEL]

        await self.bundle.step()
        stg1_fixedRange = [self.bundle.io._out.stage1Out.fixedRanges[i].value for i in range(PREDICT_WIDTH)]
        stg1_fixedTaken = [self.bundle.io._out.stage1Out.fixedTakens[i].value for i in range(PREDICT_WIDTH)]
        # yield stg1_fixedRange, stg1_fixedTaken
        await self.bundle.step()
        stg2_fixedTarget = [self.bundle.io._out.stage2Out.fixedTargets[i].value for i in range(PREDICT_WIDTH)]
        stg2_fixedMissPred = [self.bundle.io._out.stage2Out.fixedMissPreds[i].value for i in range(PREDICT_WIDTH)]
        stg2_jalTarget = [self.bundle.io._out.stage2Out.jalTargets[i].value for i in range(PREDICT_WIDTH)]
        stg2_faultTypes = [self.bundle.io._out.stage2Out.faultTypes[i].value for i in range(PREDICT_WIDTH)]
        return [ [stg1_fixedRange, stg1_fixedTaken], [stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred, stg2_faultTypes]]