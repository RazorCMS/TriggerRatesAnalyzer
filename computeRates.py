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

    triggerDict['total'] = -1
    
    names = ['hltphysics3_grun']
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
    numTriggers = len(triggerDict)
    triggerRatesDict = {}
    errorsDict = {}
    triggerNameList = []
    triggerNumList = []
    triggerNamePadDict = {}
    numPassedDict = {}
    for key, val in triggerDict.iteritems():
        triggerRatesDict[key] = 0.0
        numPassedDict[key] = 0
        errorsDict[key] = 0.0
        triggerNamePadDict[key] = ''
    # get the trigger names form the vector of strings
    for name, j in triggerDict.iteritems():
        triggerNameList.append(name)
        exclude = False
        #for exclName in ['HLT_ZeroBias_v2','total','DST_','AlCa_','MC_','HLT_Mu','HLT_Ele','HLT_Photon','DiPFJetAve','HLT_PFJet','NoBPTX','HLT_BTagMu','HLT_HcalNZS_v2']:
        for exclName in ['HLT_ZeroBias_v2','total']:
            if exclName in name:
                exclude = True
        if not exclude:
            triggerNumList.append(j)
        triggerNameLengths = [len(triggerName) for triggerName in triggerNameList]
        maxLength = max(triggerNameLengths)
    for triggerName, j in triggerDict.iteritems():
        paddedTriggerName = triggerName
        while len(paddedTriggerName)<maxLength:
            paddedTriggerName+=' '
        triggerNamePadDict[triggerName] = paddedTriggerName
                                                                                        


    
    #loop over the files and measure the trigger rates
    for i, name in enumerate(names):
        qcdfile = rt.TFile(name+".root")
        print("File: "+name+".root")
        directory = qcdfile.GetDirectory("triggerRatesAnalysis", True)
        qcdTree = directory.Get('TriggerInfo')

        if not qcdTree:
            print("Error: didn't find the trigger info tree!")
            exit()
                    
        for triggerName, triggerNum in triggerDict.iteritems():
            if triggerName == 'total':
                numPassedFile = 0                
                qcdTree.Draw('>>elist','','entrylist')
                elist = rt.gDirectory.Get('elist')
                entry = -1
                while True:
                    entry = elist.Next()
                    if entry == -1: break
                    qcdTree.GetEntry(entry)
                    for mytrigger in triggerNumList:
                        if qcdTree.triggerPassed[mytrigger]:
                            numPassedFile+=1
                            break
                #numPassedFile = qcdTree.Draw("", "||".join(["triggerPassed[%i]"%mytrigger for mytrigger in triggerNumList]))
            else:
                numPassedFile = qcdTree.Draw("", "triggerPassed[%i]"%triggerNum)
            totalEvents = qcdTree.GetEntries()
            print("%s: %i passed out of %i" %(triggerNamePadDict[triggerName],numPassedFile,totalEvents))            
            numPassedDict[triggerName]+=numPassedFile
            
    print("\nTotal Rates")
    
    for triggerName, triggerNum in triggerDict.iteritems():
        triggerRatesDict[triggerName] = lumiScaleFactor*prescaleNormalization*numPassedDict[triggerName]*1.0/(nLumiSec * lumiSectionLength)
        rateError = 0.0
        if numPassedDict[triggerName] > 0: 
            rateError = triggerRatesDict[triggerName] / math.sqrt(numPassedDict[triggerName])
        else:
            rateError = triggerRatesDict[triggerName]
        errorsDict[triggerName] = math.sqrt(errorsDict[triggerName]*errorsDict[triggerName] + rateError*rateError)

        # print final output
        print("%s: %f +/- %f"%(triggerNamePadDict[triggerName],triggerRatesDict[triggerName],errorsDict[triggerName]))
        
    
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
