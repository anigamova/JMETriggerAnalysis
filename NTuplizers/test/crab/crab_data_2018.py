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
#config.JobType.pyCfgParams = ['globalTag=102X_dataRun2_v13',"isData=True","era=2018"]
#config.JobType.pyCfgParams = ['globalTag=102X_dataRun2_Prompt_v16',"isData=True","era=2018"]
config.JobType.maxJobRuntimeMin = 2880
config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = True
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.splitting = 'FileBased'
config.Data.outLFNDirBase = '/store/user/anigamov/'+store_dir+'/'
#config.Data.unitsPerJob = 1
config.Data.allowNonValidInputDataset = True
config.Data.lumiMask ='https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

runs = ['A','B','C','D']

if __name__ == '__main__':
    f=open(sys.argv[1])
    content = f.readlines()
    content = [x.strip() for x in content]
    from CRABAPI.RawCommand import crabCommand
    n=79
    for dataset in content :
        for run in runs:
            if 'Run2018%s'%run in dataset:
                if run=="D":
                    config.JobType.pyCfgParams = ['globalTag=102X_dataRun2_Prompt_v16',"isData=True","era=2018"]
                    config.Data.unitsPerJob = 8
                else: 
                    config.JobType.pyCfgParams = ['globalTag=102X_dataRun2_v13',"isData=True","era=2018"]
                    if run=="A":
                      config.Data.unitsPerJob = 5
                    else:
                      config.Data.unitsPerJob = 2
                config.Data.inputDataset = dataset
                config.General.requestName = "EffStudiesRun2_"+dataset.split('/')[1][:30]+dataset.split('/')[2][:30]
                config.Data.outputDatasetTag = dataset.split('/')[2][:30]
                crabCommand('submit', config = config)


