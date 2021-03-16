from ROOT import *; import glob, numpy as n; from array import array
import CMS_tdrStyle_lumi
isMC = 0;

CMS_tdrStyle_lumi.extraText       = "Work in progress"
gStyle.SetOptStat(0);
gStyle.SetPalette(56)
CMS_tdrStyle_lumi.setTDRStyle()


MyFileNamesMC = []#
era="D"
FileNamesMINI = glob.glob("/pnfs/desy.de/cms/tier2/store/user/anigamov/jme_trigger/Run2EffStudies/SingleMuon/Run2018D-PromptReco-v2/210224_154904/0000/out_1*.root")

MyFileNames = FileNamesMINI 
ch = TChain('JMETriggerNTuple/Events');
for fName in  MyFileNames:
    ii = ch.Add(fName);

dencut = "(HLT_IsoMu27 || HLT_IsoMu24) && Sum$(offlineElectrons_id==1)==0 &&Sum$(offlineMuons_pt>30 && offlineMuons_eta<2.5 && offlineMuons_pfIso<0.15 && offlineMuons_id>=7)==1 && (Sum$(offlineJetsAK04PFCHS_pt*(offlineJetsAK04PFCHS_pt>30 && abs(offlineJetsAK04PFCHS_eta)<2.4)))>100"

nEvt = ch.GetEntries(); print "entries: from", 0, 'to', nEvt-1; 

METFilterNames = [
'hltPrePFMET120PFMHT120IDTight',#HLT_PFMET120_PFMHT120_IDTight filters
'hltMET90',
'hltMht',
'hltMHT90',
'hltPFMHTTightID',
'hltPFMHTTightID120',
'hltPFMET120',
'hltL1sAllETMHFSeeds',
'hltPFMET200',
'hltPFMETTypeOne200',
'hltSingleCaloJet50',
'hltSinglePFJet80',
]

TriggerResultsCollections_low = [
    'HLT_PFMET120_PFMHT120_IDTight',
    'HLT_PFMET120_PFMHT120_IDTight_PFHT60',
    'HLT_PFMET130_PFMHT130_IDTight',
    'HLT_PFMET140_PFMHT140_IDTight',
]
TriggerResultsCollections_NoMu =[
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60',
    'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight',
    'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight',
]
TriggerResultsCollections_TypeOne=[ 
    'HLT_PFMETTypeOne140_PFMHT140_IDTight',
    'HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned',
]
TriggerResultsCollections_med =[
  'HLT_PFMET200_HBHE_BeamHaloCleaned',
  'HLT_PFMET250_HBHECleaned',
  'HLT_PFMET300_HBHECleaned',
]
TriggerResultsCollections_high =[
    'HLT_PFHT300_PFMET100',
    'HLT_PFHT300_PFMET110',
    'HLT_PFMET300',
    'HLT_PFMET300_HBHECleaned',
    'HLT_PFMET400',
    'HLT_PFMET500',
    'HLT_PFMET600',
]

object_pt = ["offlineMETs_noMu_Raw_pt","offlineMETs_noMu_Type1_pt","offlineMETs_Puppi_Raw_pt","offlineMETsPuppi_Raw_pt","offlineMETs_Type1_pt"]
titles_object_pt = ["PF NoMu [GeV]","Type1 NoMu [GeV]","Puppi NoMu [GeV]","offlineMETs_noMu_Type1_pt","offlineMETs_Puppi_Raw_pt","offlineMETsPuppi_Raw_pt","offlineMETs_Type1_pt"]
ptMins= []
for i in range(21):
  ptMins.insert(i,20*i)
ptMins.insert(22,450)
ptMins.insert(23,600)
ptMins.insert(24,775)
MET_binsarr = array("f", ptMins + [1000]);
print MET_binsarr

myhs=[]
myhsHLT=[]
myhsHLT_den=[]

denHist = TH1F('denHist','denHist',len(MET_binsarr)-1,MET_binsarr)
denHist.Sumw2()
ch.Draw(object_pt[1]+">>denHist",dencut,"goff")

myhsHLT=[]
myEff = []
for i in range(0,len(TriggerResultsCollections_NoMu)):
    myhsHLT.insert(i, TH1F(TriggerResultsCollections_NoMu[i].strip(" ||"), TriggerResultsCollections_NoMu[i]+";PFMET (no #mu) [GeV]; Efficiency", len(MET_binsarr)-1,MET_binsarr))
    myhsHLT[i].Sumw2()
    ch.Draw(object_pt[1]+">>"+TriggerResultsCollections_NoMu[i].strip(" ||"),dencut + "&&" +TriggerResultsCollections_NoMu[i],"goff")
    myEff.insert(i,TEfficiency(myhsHLT[i],denHist))

_MYW = 800; _MYH = 600
_MYT = 0.10*_MYH; _MYB = 0.14*_MYH;
_MYL = 0.14*_MYW; _MYR = 0.02*_MYW

cc=TCanvas("cc","cc",_MYW,_MYH);
cc.SetLeftMargin( _MYL/_MYW );  cc.SetRightMargin( _MYR/_MYW );
cc.SetTopMargin( _MYT/_MYH );   cc.SetBottomMargin( _MYB/_MYH );
cc.SetGrid()
leg = TLegend(0.35, 0.4, 0.9, 0.70);
leg.SetTextFont(42)
leg.SetBorderSize(0)
colors = [30,1,2,9,28,12]
for i in range(0,len(myEff)):
    myEff[i].SetTitle(";"+titles_object_pt[1]+";Efficiency")
    myEff[i].SetMarkerStyle(20)
    myEff[i].SetMarkerColor(colors[i])
    myEff[i].SetLineColor(colors[i])
    if i==0:myEff[i].Draw()
    else: myEff[i].Draw("same")
    leg.AddEntry(myEff[i], TriggerResultsCollections_NoMu[i], "ep");
leg.Draw()
cc.SetTickx(0); cc.SetTicky(0);
CMS_tdrStyle_lumi.CMS_lumi( cc, 0 if isMC==1 else 0, 0 ); ## 2nd argument = 0 for MC
cc.SaveAs('CombinedEffHLT'+object_pt[1]+'_'+era+'1603.pdf')
