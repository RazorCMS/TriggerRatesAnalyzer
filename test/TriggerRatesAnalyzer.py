import FWCore.ParameterSet.Config as cms
import os
import sys

process = cms.Process('TESTING')

process.load('FWCore.MessageService.MessageLogger_cfi')

#define input
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#listFile = 'list30V2.txt'
#listFile = 'list50V2.txt'
#listFile = 'list80V2.txt'
#listFile = 'list120V2.txt'
#listFile = 'list170V2.txt'
#listFile = 'list300V2.txt'
#listFile = 'list470V2.txt'
#listFile = 'list600V2.txt'
#listFile = 'list800V2.txt'
#listFile = 'list1000V2.txt'
#listFile = 'list1400V2.txt'
listFile = 'list1800V2.txt'
inputFiles = []
with open(listFile) as inFileList:
    for line in inFileList:
        inputFiles.append(line)

process.source = cms.Source("PoolSource", 
        fileNames = cms.untracked.vstring(inputFiles)
)

#TFileService for output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("test.root"),
    #fileName = cms.string(listFile.replace('txt', 'root')),
    closeFileFast = cms.untracked.bool(True)
)

#declare analyzer module
process.triggerRatesAnalysis = cms.EDAnalyzer("TriggerRatesAnalyzer",
  TriggerResults = cms.InputTag('TriggerResults','','reHLT'),
)

#define messagelogger (controls verbosity of the module)
process.MessageLogger = cms.Service("MessageLogger",
       destinations   = cms.untracked.vstring('detailedInfo','critical','cerr'),
       critical       = cms.untracked.PSet(threshold = cms.untracked.string('ERROR')),
       detailedInfo   = cms.untracked.PSet(threshold  = cms.untracked.string('INFO') ),
       cerr           = cms.untracked.PSet(threshold  = cms.untracked.string('WARNING') )
)

process.run_module = cms.Path(process.triggerRatesAnalysis)
