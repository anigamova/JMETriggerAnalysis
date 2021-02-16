###
### VarParsing (command-line arguments)
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('logs', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create log files configured via MessageLogger')

opts.register('reportEvery', 100,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'report Run/Lumi/Event information every N events')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('isData', True,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'apply customizations for real collisions Data')

opts.register('era', "2018",
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword for data-taking period')

opts.register('globalTag', "102X_dataRun2_v13",
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')
opts.register('subtractMu', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'path to output ROOT file')

opts.parseArguments()

###
### Process
###
import FWCore.ParameterSet.Config as cms

process = cms.Process('ANALYSIS')

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')

###
### PoolSource (EDM input)
###
process.source = cms.Source('PoolSource',
  #fileNames = cms.untracked.vstring("/store/data/Run2016B/SingleMuon/MINIAOD/17Jul2018_ver2-v1/20000/E44FFA08-629A-E811-BDAE-1CB72C1B65D4.root"),
  fileNames = cms.untracked.vstring("/store/data/Run2018B/EGamma/MINIAOD/17Sep2018-v1/00000/090C4819-004F-9C4D-A113-1BCDD65DDF99.root"),
  #fileNames = cms.untracked.vstring(opts.inputFiles),
  secondaryFileNames = cms.untracked.vstring(opts.secondaryInputFiles),
  # number of events to be skipped
  skipEvents = cms.untracked.uint32(opts.skipEvents)
)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

###
### EDM Options
###
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(opts.maxEvents))

process.options = cms.untracked.PSet(
  # show cmsRun summary at job completion
  wantSummary = cms.untracked.bool(opts.wantSummary),
  # multi-threading settings
  numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1),
  numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1),
)

###
### Global Tag
###
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
if opts.globalTag is not None:
   from Configuration.AlCa.GlobalTag import GlobalTag
   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')
else:
   raise RuntimeError('failed to specify name of the GlobalTag (use "globalTag=XYZ")')

###
### TFileService
###
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

###
### MessageLogger
###
if opts.logs:
   process.MessageLogger = cms.Service('MessageLogger',
     destinations = cms.untracked.vstring(
       'cerr',
       'logError',
       'logInfo',
       'logDebug',
     ),
     # scram b USER_CXXFLAGS="-DEDM_ML_DEBUG"
     debugModules = cms.untracked.vstring(
       'JMETriggerNTuple',
     ),
     categories = cms.untracked.vstring(
       'FwkReport',
     ),
     cerr = cms.untracked.PSet(
       threshold = cms.untracked.string('WARNING'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
     logError = cms.untracked.PSet(
       threshold = cms.untracked.string('ERROR'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
     logInfo = cms.untracked.PSet(
       threshold = cms.untracked.string('INFO'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
     logDebug = cms.untracked.PSet(
       threshold = cms.untracked.string('DEBUG'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
   )
else:
   process.load('FWCore.MessageLogger.MessageLogger_cfi')
   process.MessageLogger.cerr.threshold = 'INFO'
   process.MessageLogger.cerr.FwkReport.reportEvery = opts.reportEvery

###
### Analysis Modules
###

## METFilters
from JMETriggerAnalysis.NTuplizers.METFilters_cff import METFilters
process = METFilters(process, era=opts.era, isData=opts.isData)

## Muons
from JMETriggerAnalysis.NTuplizers.userMuons_cff import userMuons
process, userMuonsCollection = userMuons(process)

## Electrons
from JMETriggerAnalysis.NTuplizers.userElectrons_cff import userElectrons
process, userElectronsCollection = userElectrons(process, era=opts.era)

###METs
from JMETriggerAnalysis.NTuplizers.userMETs_cff import userMETs,updatedMET_tag
process = userMETs(process, isData=opts.isData, era=opts.era, subtractMu=opts.subtractMu) 
## Electrons
from JMETriggerAnalysis.NTuplizers.userJets_AK04PFCHS_cff import userJets_AK04PFCHS
process, userJetsAK04PFCHSCollection = userJets_AK04PFCHS(process, era=opts.era, isData=opts.isData)

from JMETriggerAnalysis.NTuplizers.ele32DoubleL1ToSingleL1FlagProducer_cfi import ele32DoubleL1ToSingleL1FlagProducer
process.ele32DoubleL1ToSingleL1Flag = ele32DoubleL1ToSingleL1FlagProducer.clone(
  electrons = cms.InputTag('slimmedElectrons'),
  triggerResults = cms.InputTag('TriggerResults::HLT'),
  triggerObjects = cms.InputTag('slimmedPatTrigger'),
)

## Event Selection

from PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi import selectedPatMuons
process.evtselMuons = selectedPatMuons.clone(
  src = cms.InputTag(userMuonsCollection),
  cut = cms.string('(pt > 24.) && (userInt("IDMedium") > 0) && (userFloat("pfIsoR04") < 0.25)'),
)

from PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi import selectedPatElectrons
process.evtselElectrons = selectedPatElectrons.clone(
  src = cms.InputTag(userElectronsCollection),
  cut = cms.string('(pt > 27.) && (userInt("IDCutBasedMedium") > 0)'),
)

process.evtselLeptons = cms.EDProducer('CandViewMerger',
  src = cms.VInputTag('evtselMuons', 'evtselElectrons')
)

process.evtselTask = cms.Task(process.evtselMuons, process.evtselElectrons, process.evtselLeptons)

process.evtselLeptonsMultiplicityFilter = cms.EDFilter('CandViewCountFilter',
  src = cms.InputTag('evtselLeptons'),
  minNumber = cms.uint32(1),
)

## JMETrigger NTuple
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults::HLT'),

  TriggerResultsFilterOR = cms.vstring(
    # IsoMu
    'HLT_IsoMu24',
    'HLT_IsoMu24_eta2p1',
    'HLT_IsoMu27',

    # Ele
    'HLT_Ele27_WPTight_Gsf',
    'HLT_Ele32_WPTight_Gsf',
    'HLT_Ele32_WPTight_Gsf_L1DoubleEG',
    'HLT_Ele35_WPTight_Gsf',
  ),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(
    # IsoMu
    'HLT_IsoMu24',
    'HLT_IsoMu24_eta2p1',
    'HLT_IsoMu27',

    # Ele
    'HLT_Ele27_WPTight_Gsf',
    'HLT_Ele32_WPTight_Gsf',
    'HLT_Ele32_WPTight_Gsf_L1DoubleEG',
    'HLT_Ele35_WPTight_Gsf',

    # PFJet, PFHT, Others
    'HLT_AK4PFJet100',
    'HLT_AK4PFJet120',
    'HLT_AK4PFJet30',
    'HLT_AK4PFJet50',
    'HLT_AK4PFJet80',
    'HLT_AK8PFHT750_TrimMass50',
    'HLT_AK8PFHT800_TrimMass50',
    'HLT_AK8PFHT850_TrimMass50',
    'HLT_AK8PFHT900_TrimMass50',
    'HLT_AK8PFJet140',
    'HLT_AK8PFJet15',
    'HLT_AK8PFJet200',
    'HLT_AK8PFJet25',
    'HLT_AK8PFJet260',
    'HLT_AK8PFJet320',
    'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1',
    'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17',
    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2',
    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4',
    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02',
    'HLT_AK8PFJet360_TrimMass30',
    'HLT_AK8PFJet380_TrimMass30',
    'HLT_AK8PFJet40',
    'HLT_AK8PFJet400',
    'HLT_AK8PFJet400_TrimMass30',
    'HLT_AK8PFJet420_TrimMass30',
    'HLT_AK8PFJet450',
    'HLT_AK8PFJet500',
    'HLT_AK8PFJet550',
    'HLT_AK8PFJet60',
    'HLT_AK8PFJet80',
    'HLT_AK8PFJetFwd140',
    'HLT_AK8PFJetFwd15',
    'HLT_AK8PFJetFwd200',
    'HLT_AK8PFJetFwd25',
    'HLT_AK8PFJetFwd260',
    'HLT_AK8PFJetFwd320',
    'HLT_AK8PFJetFwd40',
    'HLT_AK8PFJetFwd400',
    'HLT_AK8PFJetFwd450',
    'HLT_AK8PFJetFwd500',
    'HLT_AK8PFJetFwd60',
    'HLT_AK8PFJetFwd80',
    'HLT_DiJet110_35_Mjj650_PFMET110',
    'HLT_DiJet110_35_Mjj650_PFMET120',
    'HLT_DiJet110_35_Mjj650_PFMET130',
    'HLT_DiPFJetAve140',
    'HLT_DiPFJetAve200',
    'HLT_DiPFJetAve260',
    'HLT_DiPFJetAve320',
    'HLT_DiPFJetAve40',
    'HLT_DiPFJetAve400',
    'HLT_DiPFJetAve500',
    'HLT_DiPFJetAve60',
    'HLT_DiPFJetAve80',
    'HLT_DoublePFJets100_CaloBTagDeepCSV_p71',
    'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71',
    'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71',
    'HLT_DoublePFJets200_CaloBTagDeepCSV_p71',
    'HLT_DoublePFJets350_CaloBTagDeepCSV_p71',
    'HLT_DoublePFJets40_CaloBTagDeepCSV_p71',
    'HLT_PFHT1050',
    'HLT_PFHT180',
    'HLT_PFHT250',
    'HLT_PFHT330PT30_QuadPFJet_75_60_45_40',
    'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5',
    'HLT_PFHT350',
    'HLT_PFHT350MinPFJet15',
    'HLT_PFHT370',
    'HLT_PFHT400_FivePFJet_100_100_60_30_30',
    'HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5',
    'HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5',
    'HLT_PFHT400_SixPFJet32',
    'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94',
    'HLT_PFHT430',
    'HLT_PFHT450_SixPFJet36',
    'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59',
    'HLT_PFHT500_PFMET100_PFMHT100_IDTight',
    'HLT_PFHT500_PFMET110_PFMHT110_IDTight',
    'HLT_PFHT510',
    'HLT_PFHT590',
    'HLT_PFHT680',
    'HLT_PFHT700_PFMET85_PFMHT85_IDTight',
    'HLT_PFHT700_PFMET95_PFMHT95_IDTight',
    'HLT_PFHT780',
    'HLT_PFHT800',
    'HLT_PFHT800_PFMET75_PFMHT75_IDTight',
    'HLT_PFHT800_PFMET85_PFMHT85_IDTight',
    'HLT_PFHT890',
    'HLT_PFHT900',
    'HLT_PFJet140',
    'HLT_PFJet15',
    'HLT_PFJet200',
    'HLT_PFJet25',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet40',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500',
    'HLT_PFJet550',
    'HLT_PFJet60',
    'HLT_PFJet80',
    'HLT_PFJetFwd140',
    'HLT_PFJetFwd15',
    'HLT_PFJetFwd200',
    'HLT_PFJetFwd25',
    'HLT_PFJetFwd260',
    'HLT_PFJetFwd320',
    'HLT_PFJetFwd40',
    'HLT_PFJetFwd400',
    'HLT_PFJetFwd450',
    'HLT_PFJetFwd500',
    'HLT_PFJetFwd60',
    'HLT_PFJetFwd80',
    'HLT_QuadPFJet103_88_75_15',
    'HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
    'HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2',
    'HLT_QuadPFJet105_88_76_15',
    'HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
    'HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2',
    'HLT_QuadPFJet111_90_80_15',
    'HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
    'HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2',
    'HLT_QuadPFJet98_83_71_15',
    'HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
    'HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2',
    'HLT_TripleJet110_35_35_Mjj650_PFMET110',
    'HLT_TripleJet110_35_35_Mjj650_PFMET120',
    'HLT_TripleJet110_35_35_Mjj650_PFMET130',

    # PFMET
    'HLT_PFHT300_PFMET100',
    'HLT_PFHT300_PFMET110',
    'HLT_PFMET100_PFMHT100_IDTight',
    'HLT_PFMET100_PFMHT100_IDTight_BeamHaloCleaned',
    'HLT_PFMET100_PFMHT100_IDTight_PFHT60',
    'HLT_PFMET110_PFMHT110_IDTight',
    'HLT_PFMET120_PFMHT120_IDTight',
    'HLT_PFMET120_PFMHT120_IDTight_HFCleaned',
    'HLT_PFMET120_PFMHT120_IDTight_PFHT60',
    'HLT_PFMET120_PFMHT120_IDTight_PFHT60_HFCleaned',
    'HLT_PFMET130_PFMHT130_IDTight',
    'HLT_PFMET140_PFMHT140_IDTight',
    'HLT_PFMET170_BeamHaloCleaned',
    'HLT_PFMET170_HBHECleaned',
    'HLT_PFMET170_HBHE_BeamHaloCleaned',
    'HLT_PFMET170_JetIdCleaned',
    'HLT_PFMET170_NoiseCleaned',
    'HLT_PFMET170_NotCleaned',
    'HLT_PFMET200_HBHECleaned',
    'HLT_PFMET200_HBHE_BeamHaloCleaned',
    'HLT_PFMET200_NotCleaned',
    'HLT_PFMET250_HBHECleaned',
    'HLT_PFMET300',
    'HLT_PFMET300_HBHECleaned',
    'HLT_PFMET400',
    'HLT_PFMET500',
    'HLT_PFMET600',
    'HLT_PFMET90_PFMHT90_IDTight',
    'HLT_PFMETNoMu100_PFMHTNoMu100_IDTight',
    'HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60',
    'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_HFCleaned',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60',
    'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight',
    'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight',
    'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight',
    'HLT_PFMETTypeOne100_PFMHT100_IDTight_PFHT60',
    'HLT_PFMETTypeOne110_PFMHT110_IDTight',
    'HLT_PFMETTypeOne120_PFMHT120_IDTight',
    'HLT_PFMETTypeOne120_PFMHT120_IDTight_HFCleaned',
    'HLT_PFMETTypeOne120_PFMHT120_IDTight_PFHT60',
    'HLT_PFMETTypeOne130_PFMHT130_IDTight',
    'HLT_PFMETTypeOne140_PFMHT140_IDTight',
    'HLT_PFMETTypeOne190_HBHE_BeamHaloCleaned',
    'HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned',
  ),

  fillCollectionConditions = cms.PSet(),

  bools = cms.PSet(
    Flag_ele32DoubleL1ToSingleL1 = cms.InputTag('ele32DoubleL1ToSingleL1Flag'),
  ),

  recoVertexCollections = cms.PSet(
#    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
#    hltVerticesPF = cms.InputTag('hltVerticesPF'),
  ),

  recoPFCandidateCollections = cms.PSet(
#    hltParticleFlow = cms.InputTag('hltParticleFlow'),
  ),

  patPackedCandidateCollections = cms.PSet(
#    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(
#    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
#    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(
#    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
#    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

#    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
#    hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(
  ),

  recoPFJetCollections = cms.PSet(
#    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
#    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

#    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
#    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
  ),

  patJetCollections = cms.PSet(
    offlineJetsAK04PFCHS = cms.InputTag(userJetsAK04PFCHSCollection),
  ),

  recoGenMETCollections = cms.PSet(
#    genMETCalo = cms.InputTag('genMetCalo::HLT'),
#    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(
#    hltCaloMET = cms.InputTag('hltMet'),
  ),

  recoPFClusterMETCollections = cms.PSet(
  ),

  recoPFMETCollections = cms.PSet(
#    hltPFMET = cms.InputTag('hltPFMETProducer'),
#    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
  ),

  patMETCollections = cms.PSet(
    offlineMETs = cms.InputTag('slimmedMETs'+updatedMET_tag),
    #offlineMETsPuppi = cms.InputTag('slimmedMETsPuppinoMu'),
    #offlineMETsPuppi_EGCor = cms.InputTag('puppiMETEGCor'),
    #offlineMETsPuppi_MuCor = cms.InputTag('puppiMETMuCor'),
    #offlineMETs_MuEGClean = cms.InputTag('slimmedMETsMuEGClean'),
    #offlineMETs_EGClean = cms.InputTag('slimmedMETsEGClean'),
  ),

  patMuonCollections = cms.PSet(
    offlineMuons = cms.InputTag(userMuonsCollection),
  ),

  patElectronCollections = cms.PSet(
    offlineElectrons = cms.InputTag(userElectronsCollection),
  ),

  stringCutObjectSelectors = cms.PSet(
#    ak4GenJetsNoNu = cms.string('pt > 12'),
#    ak8GenJetsNoNu = cms.string('pt > 50'),

#    hltAK4CaloJets = cms.string('pt > 12'),
#    hltAK4CaloJetsCorrected = cms.string('pt > 12'),

#    hltAK8CaloJets = cms.string('pt > 80'),
#    hltAK8CaloJetsCorrected = cms.string('pt > 80'),

#    hltAK4PFJets = cms.string('pt > 12'),
#    hltAK4PFJetsCorrected = cms.string('pt > 12'),

#    hltAK8PFJets = cms.string('pt > 80'),
#    hltAK8PFJetsCorrected = cms.string('pt > 80'),
  ),

  boolValueMaps = cms.PSet(
  ),

  outputBranchesToBeDropped = cms.vstring(
#    'offlinePrimaryVertices_tracksSize',
#
##    'hltPFMet_ChargedEMEtFraction',
##    'hltPFMetTypeOne_ChargedEMEtFraction',
#
#    'genMetCalo_MuonEtFraction',
#    'genMetCalo_InvisibleEtFraction',
  ),
)

## Trigger Flags
process.triggerFlagsTask = cms.Task()

hltPathsWithTriggerFlags = [
  'HLT_PFJet40',
  'HLT_PFJet60',
  'HLT_PFJet80',
  'HLT_PFJet140',
  'HLT_PFJet200',
  'HLT_PFJet260',
  'HLT_PFJet320',
  'HLT_PFJet400',
  'HLT_PFJet500',

  'HLT_PFHT250',
  'HLT_PFHT350',
  'HLT_PFHT510',
  'HLT_PFHT780',
  'HLT_PFHT800',
  'HLT_PFHT890',
  'HLT_PFHT900',
  'HLT_PFHT1050',

  'HLT_PFMET170_NotCleaned',
  'HLT_PFMET170_HBHECleaned',
  'HLT_PFMET170_HBHE_BeamHaloCleaned',
  'HLT_PFMET200_NotCleaned',
  'HLT_PFMET200_HBHECleaned',
  'HLT_PFMET200_HBHE_BeamHaloCleaned',
  'HLT_PFMET250_HBHECleaned',
  'HLT_PFMETTypeOne190_HBHE_BeamHaloCleaned',
  'HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned',
]

from JMETriggerAnalysis.NTuplizers.triggerFlagsProducer_cfi import triggerFlagsProducer

for _hltPathUnv in hltPathsWithTriggerFlags:
    _triggerFlagsModName = 'triggerFlags'+_hltPathUnv.replace('_','')
    setattr(process, _triggerFlagsModName, triggerFlagsProducer.clone(
      triggerResults = 'TriggerResults::HLT',
      ignorePathVersion = True,
      pathName = _hltPathUnv,
    ))
    process.triggerFlagsTask.add(getattr(process, _triggerFlagsModName))

    setattr(process.JMETriggerNTuple.bools, 'Flag_'+_hltPathUnv+'_L1TSeedAccept', cms.InputTag(_triggerFlagsModName+':L1TSeedAccept'))
    setattr(process.JMETriggerNTuple.bools, 'Flag_'+_hltPathUnv+'_L1TSeedPrescaledOrMasked', cms.InputTag(_triggerFlagsModName+':L1TSeedPrescaledOrMasked'))
    setattr(process.JMETriggerNTuple.bools, 'Flag_'+_hltPathUnv+'_HLTPathPrescaled', cms.InputTag(_triggerFlagsModName+':HLTPathPrescaled'))
    setattr(process.JMETriggerNTuple.bools, 'Flag_'+_hltPathUnv+'_HLTPathAccept', cms.InputTag(_triggerFlagsModName+':HLTPathAccept'))

process.triggerFlagsSeq = cms.Sequence(process.triggerFlagsTask)

## TriggerObjMatch ValueMaps
process.triggerObjMatchValueMapsTask = cms.Task()

hltPathsWithTriggerObjMatchFlags = [
  'HLT_PFJet40',
  'HLT_PFJet60',
  'HLT_PFJet80',
  'HLT_PFJet140',
  'HLT_PFJet200',
  'HLT_PFJet260',
  'HLT_PFJet320',
  'HLT_PFJet400',
  'HLT_PFJet500',
]

from JMETriggerAnalysis.NTuplizers.triggerObjMatchValueMapsProducer_cfi import triggerObjMatchValueMapsProducer

for _jetColl in process.JMETriggerNTuple.patJetCollections.parameterNames_():
    _jetCollInputTag = process.JMETriggerNTuple.patJetCollections.getParameter(_jetColl)

    for _hltPathUnv in hltPathsWithTriggerObjMatchFlags:
        _triggerObjMatchValueMapsModName = 'triggerObjMatchValueMaps'+_hltPathUnv.replace('_','')
        setattr(process, _triggerObjMatchValueMapsModName, triggerObjMatchValueMapsProducer.clone(
          triggerResults = 'TriggerResults::HLT',
          ignorePathVersion = True,
          src = _jetCollInputTag,
          pathName = _hltPathUnv,
          deltaR = 0.2,
        ))
        process.triggerObjMatchValueMapsTask.add(getattr(process, _triggerObjMatchValueMapsModName))

        if not hasattr(process.JMETriggerNTuple.boolValueMaps, _jetColl):
           setattr(process.JMETriggerNTuple.boolValueMaps, _jetColl, cms.PSet())
        _vmapPSet = getattr(process.JMETriggerNTuple.boolValueMaps, _jetColl)

        for _trigObjMatchTag in ['trigObjMatchL1TSeed', 'trigObjMatchHLTLastFilter', 'trigObjMatchHLTAllFilters']:
            setattr(_vmapPSet, _trigObjMatchTag+'_'+_hltPathUnv, cms.InputTag(_triggerObjMatchValueMapsModName+':'+_trigObjMatchTag))

process.triggerObjMatchValueMapsSeq = cms.Sequence(process.triggerObjMatchValueMapsTask)

process.analysisCollectionsPath = cms.Path(
    process.METFiltersSeq
  + process.METSeq
  + process.userMuonsSeq
  + process.userElectronsSeq
  + process.evtselMuons
  + process.evtselElectrons
  + process.evtselLeptons
  + process.evtselLeptonsMultiplicityFilter
  + process.userJetsAK04PFCHSSeq
  + process.ele32DoubleL1ToSingleL1Flag
  + process.triggerFlagsSeq
  + process.triggerObjMatchValueMapsSeq
  + process.JMETriggerNTuple
)

#process.JMETriggerNTupleEndPath = cms.EndPath(process.analysisCollectionsPath)

### dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

### print-outs
print '--- jmeTriggerNTuple_cfg.py ---'
print ''
print 'option: output =', opts.output
print 'option: dumpPython =', opts.dumpPython
print ''
print 'process.GlobalTag =', process.GlobalTag.dumpPython()
print 'process.source =', process.source.dumpPython()
print 'process.maxEvents =', process.maxEvents.dumpPython()
print 'process.options =', process.options.dumpPython()
print 'process.MessageLogger.cerr.FwkReport.reportEvery =', process.MessageLogger.cerr.FwkReport.reportEvery
print '-------------------------------'
