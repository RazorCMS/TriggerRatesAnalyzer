#!/bin/python

import sys
import ROOT as rt
import math
from optparse import OptionParser    
import csv

def calcRateData(options):
    
    f = open(options.pathNames)
    csvin = csv.reader(f,delimiter=' ')
    triggerDict = {}
    for row in csvin:
        triggerDict[row[-1]] = int(row[0])
        
    names = ['hltphysics']
    nLumiSec = options.nLumiSec
    prescaleNormalization = options.prescale
    instLumiRec = options.recLumi #in /picobarns/s
    instLumi = options.instLumi #in /picobarns/s
    lumiScaleFactor = instLumi/instLumiRec
    lumiSectionLength = 23.3
    print "lumi scale factor = ", lumiScaleFactor
    print "lumi section length = ", lumiSectionLength
    print "nLumiSec = ", nLumiSec
    print "prescale norm = ", prescaleNormalization
    
    #initialize all trigger rates to 0
    numTriggers = len(triggerDict)+1
    triggerRates = []
    errors = []
    triggerNameList = []
    triggerNamePadList = []
    numPassed = []
    for i in range(numTriggers): 
        triggerRates.append(0.0)
        numPassed.append(0)
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
        for name, j in triggerDict.iteritems():
            triggerNameList[int(j)] = name
        triggerNameList[-1] = 'total'
        triggerNameLengths = [len(triggerName) for triggerName in triggerNameList]
        maxLength = max(triggerNameLengths)
    
        for j, triggerName in enumerate(triggerNameList):
            while len(triggerName)<maxLength:
                triggerName+=' '
            triggerNamePadList[j] = triggerName

            
        for triggerNum in range(numTriggers):
            if triggerNameList[triggerNum]=='total':
                triggerOrBool = "||".join(["triggerPassed[%i]"%mytrigger for mytrigger in range(numTriggers-1) if 'ZeroBias' not in triggerNameList[mytrigger]])
                numPassedFile = qcdTree.Draw("", triggerOrBool)
            else:
                numPassedFile = qcdTree.Draw("", "triggerPassed[%i]"%triggerNum)
            totalEvents = qcdTree.GetEntries()
            #rate_data = (counts * lumiScaleFactor * prescaleNormalization)/(nlumiSec * lumiSectionLength)        
            print("%s: %i passed out of %i" %(triggerNamePadList[triggerNum],numPassedFile,totalEvents))            
            numPassed[triggerNum]+=numPassedFile
            
    print("Total Rates")
    
    for triggerNum in range(numTriggers):
        triggerRates[triggerNum] = lumiScaleFactor*prescaleNormalization*numPassed[triggerNum]*1.0/(nLumiSec * lumiSectionLength)
        rateError = 0.0
        if numPassed[triggerNum] > 0: 
            rateError = triggerRates[triggerNum] / math.sqrt(numPassed[triggerNum])
        else:
            rateErrror = triggerRates[triggerNum]
        errors[triggerNum] = math.sqrt(errors[triggerNum]*errors[triggerNum] + rateError*rateError)
    for triggerNum, (rate, error) in enumerate(zip(triggerRates,errors)):
        print("%s: %f +/- %f"%(triggerNamePadList[triggerNum],rate,error))
        
    
def calcRateMC(options):
    
    f = open(options.pathNames)
    csvin = csv.reader(f,delimiter=' ')
    triggerDict = {}
    for row in csvin:
        triggerDict[row[-1]] = int(row[0])
        
    names = ["list30", "list50", "list80", "list120", "list170", "list300", "list470", "list600", "list800", "list1000", "list1400", "list1800"]
    #cross sections in pb of the processes represented by the input files
    xSections = [161500000, 22110000, 3000114.3, 493200, 120300, 7475, 587.1, 167, 28.25, 8.195, 0.7346, 0.1091]
    instLumi = options.instLumi #in /picobarns/s
    
    #initialize all trigger rates to 0
    numTriggers = len(triggerDict)+1
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
        for name, j in triggerDict.iteritems():
            triggerNameList[int(j)] = name
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
            if numPassed > 0: 
                rateError = rate / math.sqrt(numPassed)
            else:
                rateError = rate
            print("%s: %i passed out of %i, for a rate contribution of %f +/- %f" %(triggerNamePadList[triggerNum],numPassed,totalEvents,rate,rateError))
            triggerRates[triggerNum] += rate
            errors[triggerNum] = math.sqrt(errors[triggerNum]*errors[triggerNum] + rateError*rateError)
        
    print("Total Rates")
    for triggerNum, (rate, error) in enumerate(zip(triggerRates,errors)):
        print("%s: %f +/- %f"%(triggerNamePadList[triggerNum],rate,error))

        
if __name__ == '__main__':

    
    parser = OptionParser()
    parser.add_option('--data',dest="isData",default=False,action='store_true',
                  help="is data")    
    parser.add_option('-l','--lumi',dest="instLumi", default=7e-3,type="float",
                  help="instantaneous luminosity to scale to in /picobarns/s")
    parser.add_option('-r','--rec-lumi',dest="recLumi", default=1.459697266e-4,type="float",
                  help="recorded instantaneous luminosity in /picobarns/s")
    parser.add_option('--prescale',dest="prescale", default=320,type="float",
                  help="prescale normalization for data sample")
    parser.add_option('--lumi-sec',dest="nLumiSec", default=320,type="float",
                  help="number of total lumi sections (summing over all files)")
    parser.add_option('--path-names',dest="pathNames",default="RazorHLTPathnames.dat",type="string",
                  help="text file containing mapping between array index and path name")
    
    (options,args) = parser.parse_args()
     
    if options.isData:
        calcRateData(options)
    else:
        calcRateMC(options)
