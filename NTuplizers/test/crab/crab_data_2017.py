import sys
from CRABClient.UserUtilities import config
config = config()

store_dir = 'jme_trigger/Run2EffStudies/'

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'jmeTriggerNTuple_cfg.py'
config.JobType.inputFiles = []
config.JobType.pyCfgParams = ['globalTag=102X_dataRun2_v13',"isData=True","era=2017"]
#config.JobType.pyCfgParams = ['globalTag=102X_dataRun2_Prompt_v16',"isData=True","era=2018"]
config.JobType.maxJobRuntimeMin = 2880
config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.splitting = 'FileBased'
config.Data.outLFNDirBase = '/store/user/anigamov/'+store_dir+'/'
config.Data.unitsPerJob = 5
config.Data.allowNonValidInputDataset = True
config.Data.lumiMask ='https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

runs = ['B','C','D','E','F']

if __name__ == '__main__':
    f=open(sys.argv[1])
    content = f.readlines()
    content = [x.strip() for x in content]
    from CRABAPI.RawCommand import crabCommand
    n=79
    for dataset in content :
        for run in runs:
            if 'Run2017%s'%run in dataset:
                if 'SingleMuon' in dataset: config.JobType.pyCfgParams = ['globalTag=102X_dataRun2_v13',"isData=True","era=2017","subtractMu=True"]
                config.Data.inputDataset = dataset
                config.General.requestName = "EffStudiesRun2_"+dataset.split('/')[1][:30]+dataset.split('/')[2][:30]
                config.Data.outputDatasetTag = dataset.split('/')[2][:30]
                crabCommand('submit', config = config)


