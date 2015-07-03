#!/bin/python

import sys
import ROOT as rt
import math

#names of the input files, without '.root'
names = ["list30", "list50", "list80", "list120", "list170", "list300", "list470", "list600", "list800", "list1000", "list1400", "list1800"]
#cross sections in pb of the processes represented by the input files
xSections = [161500000, 22110000, 3000114.3, 493200, 120300, 7475, 587.1, 167, 28.25, 8.195, 0.7346, 0.1091]
instLumi = 0.014 #in /picobarns/s

#initialize all trigger rates to 0
numTriggers = 20
triggerRates = []
errors = []
triggerNameList = []
triggerNamePadList = []
for i in range(numTriggers): 
    triggerRates.append(0.0)
    errors.append(0.0)
    triggerNameList.append('')
    triggerNamePadList.append('')

#loop over the files and measure the trigger rates
for i, name in enumerate(names):
    qcdfile = rt.TFile(name+".root")
    print("File: "+name+".root")
    directory = qcdfile.GetDirectory("triggerRatesAnalysis", True)
    qcdTree = directory.Get('TriggerInfo')
    if not qcdTree:
        print("Error: didn't find the trigger info tree!")
        exit()
        
    # get the trigger names form the vector of strings
    qcdTree.GetEntry(0)
    for j, name in enumerate(qcdTree.triggerNames):
        triggerNameList[j] = name
    triggerNameLengths = [len(triggerName) for triggerName in triggerNameList]
    maxLength = max(triggerNameLengths)
    
    for j, triggerName in enumerate(triggerNameList):
        while len(triggerName)<maxLength:
            triggerName+=' '
        triggerNamePadList[j] = triggerName
    

    for triggerNum in range(numTriggers):
        numPassed = qcdTree.Draw("", "triggerPassed[%i]"%triggerNum)
        totalEvents = qcdTree.GetEntries()
        #rate = luminosity*cross section*fraction of events passing
        #here 0.005 is obtained as 5e33 (inst. luminosity) divided by 10^36 (conversion from picobarns to cm^2)
        #for 1.4e34 luminosity, use 0.014
        rate = instLumi*xSections[i]*numPassed*1.0/totalEvents
        rateError = 0.0
        if numPassed > 0: rateError = rate / math.sqrt(numPassed)
        print("%s: %i passed out of %i, for a rate contribution of %f +/- %f" %(triggerNamePadList[triggerNum],numPassed,totalEvents,rate,rateError))
        triggerRates[triggerNum] += rate
        errors[triggerNum] = math.sqrt(errors[triggerNum]*errors[triggerNum] + rateError*rateError)
        
print("Total Rates")
for triggerNum, (rate, error) in enumerate(zip(triggerRates,errors)):
    print("%s: %f +/- %f"%(triggerNamePadList[triggerNum],rate,error))
