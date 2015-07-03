import FWCore.ParameterSet.Config as cms
import os
import sys

process = cms.Process('TESTING')

process.load('FWCore.MessageService.MessageLogger_cfi')

#define input
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#listFile = 'list30.txt'
#listFile = 'list50.txt'
#listFile = 'list80.txt'
#listFile = 'list120.txt'
#listFile = 'list170.txt'
#listFile = 'list300.txt'
#listFile = 'list470.txt'
#listFile = 'list600.txt'
#listFile = 'list800.txt'
#listFile = 'list1000.txt'
#listFile = 'list1400.txt'
#listFile = 'list1800.txt'
listFile = 'listT2tt.txt'
inputFiles = []
with open(listFile) as inFileList:
    for i, line in enumerate(inFileList):
        if i<1: inputFiles.append(line)

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
       destinations   = cms.untracked.vstring('detailedInfo','critical','cerr'),
       critical       = cms.untracked.PSet(threshold = cms.untracked.string('ERROR')),
       detailedInfo   = cms.untracked.PSet(threshold  = cms.untracked.string('INFO') ),
       cerr           = cms.untracked.PSet(threshold  = cms.untracked.string('WARNING') )
)

process.run_module = cms.Path(process.triggerRatesAnalysis)
