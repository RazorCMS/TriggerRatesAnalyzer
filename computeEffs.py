#!/bin/python

import sys
import ROOT as rt
import math

#names of the input files, without '.root'
names = ["listT1bbbb","listT2tt"]
#cross sections in pb of the processes represented by the input files
xSections = [0.0141903, 0.0189612]
intLumi = 3000 #in /picobarns

#loop over the files and measure the trigger rates
for i, name in enumerate(names):
    smsfile = rt.TFile(name+".root")
    print("File: "+name+".root")
    directory = smsfile.GetDirectory("triggerRatesAnalysis", True)
    smsTree = directory.Get('TriggerInfo')
            
    if not smsTree:
        print("Error: didn't find the trigger info tree!")
        exit()
        
    # get the trigger names form the vector of strings
    triggerNameList = []
    triggerNamePadList = []
    smsTree.GetEntry(0)
    for name in smsTree.triggerNames:
        triggerNameList.append(name)
    triggerNameLengths = [len(triggerName) for triggerName in triggerNameList]
    maxLength = max(triggerNameLengths)
    
    for triggerName in triggerNameList:
        while len(triggerName)<maxLength:
            triggerName+=' '
        triggerNamePadList.append(triggerName)
    
    for triggerNum in range(numTriggers):
        numPassed = smsTree.Draw("", "triggerPassed[%i]"%triggerNum)
        totalEvents = smsTree.GetEntries()
        eff = numPassed*1.0/totalEvents
        expEvents = intLumi*xSections[i]*eff
        effError = 0.0
        if numPassed > 0:
            effError = eff / math.sqrt(numPassed)
            
        print("%s: %i passed out of %i, for an efficiency of %f +/- %f" %(triggerNamePadList[triggerNum],numPassed,totalEvents,eff,effError))
