#!/bin/python

import sys
import ROOT as rt
import math

#names of the input files, without '.root'
names = ["list30", "list50", "list80", "list120", "list170", "list300", "list470", "list600", "list800", "list1000", "list1400", "list1800"]
#cross sections in pb of the processes represented by the input files
xSections = [161500000, 22110000, 3000114.3, 493200, 120300, 7475, 587.1, 167, 28.25, 8.195, 0.7346, 0.1091]

#initialize all trigger rates to 0
numTriggers = 37
triggerRates = []
errors = []
for i in range(numTriggers): 
    triggerRates.append(0.0)
    errors.append(0.0)

#loop over the files and measure the trigger rates
for i, name in enumerate(names):
    qcdfile = rt.TFile(name+".root")
    print("File: "+name+".root")
    directory = qcdfile.GetDirectory("triggerRatesAnalysis", True)
    qcdTree = directory.Get('TriggerInfo')
    if not qcdTree:
        print("Error: didn't find the trigger info tree!")
        exit()
    for triggerNum in range(numTriggers):
        numPassed = qcdTree.Draw("", "triggerPassed["+str(triggerNum)+"]")
        totalEvents = qcdTree.GetEntries()
        #rate = luminosity*cross section*fraction of events passing
        #here 0.005 is obtained as 5e33 (inst. luminosity) divided by 10^36 (conversion from picobarns to cm^2)
        #for 1.4e34 luminosity, use 0.014
        instLumi = 0.014 #in /picobarns/s
        rate = instLumi*xSections[i]*numPassed*1.0/totalEvents
        error = 0.0
        if numPassed > 0: error = rate / math.sqrt(numPassed)
        print("Trigger "+str(triggerNum)+": "+str(numPassed)+" passed out of "+str(totalEvents)+", for a rate contribution of "+str(rate)+" +/- "+str(error))
        triggerRates[triggerNum] += rate
        errors[triggerNum] = math.sqrt(errors[triggerNum]*errors[triggerNum] + error*error)
for i, rate in enumerate(triggerRates): print(str(i)+": "+str(rate)+" +/- "+str(errors[i]))
