import FWCore.ParameterSet.Config as cms

def userMETs(process, isData, era,subtractMu):

    ### MET recalculation
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD

    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription#Puppi_MET
    #if subtractMu:
    process.noMuCands = cms.EDFilter("CandPtrSelector",
                                 src=cms.InputTag("packedPFCandidates"),
                                 cut=cms.string("abs(pdgId)!=13")
                                 )
    updatedMET_tag="";

    if subtractMu: 
      updatedMET_tag="noMu";
      if era == '2016':
  
         runMetCorAndUncFromMiniAOD(process, isData = isData,
           fixEE2017 = False,pfCandColl=cms.InputTag("noMuCands"),postfix="noMu",recoMetFromPFCs=True,
         )
      elif era == '2017':
         runMetCorAndUncFromMiniAOD(process, isData = isData,
           fixEE2017 = True,
           fixEE2017Params = {'userawPt': True, 'ptThreshold': 50.0, 'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
           pfCandColl=cms.InputTag("noMuCands"),postfix="noMu",
         )

      elif era == '2018':
         runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
           fixEE2017 = False,pfCandColl=cms.InputTag("noMuCands"),postfix="noMu",
         )

      else:
         raise RuntimeError('userMETs_cff.py -- invalid value for "era"OA: '+str(era))

    else:
      if era == '2016':

         runMetCorAndUncFromMiniAOD(process, isData = isData,
           fixEE2017 = False,recoMetFromPFCs=True,
         )
      elif era == '2017':
         runMetCorAndUncFromMiniAOD(process, isData = isData,
           fixEE2017 = True,
           fixEE2017Params = {'userawPt': True, 'ptThreshold': 50.0, 'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
         )

      elif era == '2018':
         runMetCorAndUncFromMiniAOD(process, isData = isData,
           fixEE2017 = False,
         )

    process.METSeq = cms.Sequence(
      process.noMuCands*
      getattr(process, 'fullPatMetSequence'+updatedMET_tag)#process.fullPatMetSequencePuppinoMu,
    )
    return process
