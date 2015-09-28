import FWCore.ParameterSet.Config as cms
import os
import sys

process = cms.Process('TESTING')

process.load('FWCore.MessageService.MessageLogger_cfi')


if len(sys.argv) < 4:
    print "usage:"
    print "cmsRun TriggerRatesAnalyzer.py listTextFileName maxEvents"
    
#define input
maxEvents = int(sys.argv[3])
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(maxEvents) )

#listFile = 'listQCD_Pt_120to170.txt'
#listFile = 'hltphysicspart0.txt'
listFile = sys.argv[2]

print "using list file: %s with maxEvents = %i" % (listFile, maxEvents)

inputFiles = []
with open(listFile) as inFileList:
    for i, line in enumerate(inFileList):
        inputFiles.append(line)

process.source = cms.Source("PoolSource", 
        fileNames = cms.untracked.vstring(inputFiles)
)

#TFileService for output
process.TFileService = cms.Service("TFileService",
    #fileName = cms.string("test.root"),
    fileName = cms.string(listFile.replace('txt', 'root')),
    closeFileFast = cms.untracked.bool(True)
)

#declare analyzer module
process.triggerRatesAnalysis = cms.EDAnalyzer("TriggerRatesAnalyzer",
  TriggerResults = cms.InputTag('TriggerResults','','TEST'),
)

#define messagelogger (controls verbosity of the module)
process.MessageLogger = cms.Service("MessageLogger",
       #destinations   = cms.untracked.vstring('detailedInfo','critical','cerr'),
       destinations   = cms.untracked.vstring('critical','cerr'),
       critical       = cms.untracked.PSet(threshold = cms.untracked.string('ERROR')),
       #detailedInfo   = cms.untracked.PSet(threshold  = cms.untracked.string('INFO') ),
       cerr           = cms.untracked.PSet(threshold  = cms.untracked.string('WARNING') )
)

process.run_module = cms.Path(process.triggerRatesAnalysis)
