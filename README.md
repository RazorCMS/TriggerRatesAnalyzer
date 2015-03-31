# TriggerRatesAnalyzer
Lightweight analyzer for measuring the rates of HLT paths

Clone into HLTriggerOffline/TriggerRatesAnalyzer in CMSSW.

Run the analyzer on a collection of EDM files that contain TriggerResults objects.  For each trigger, the analyzer will store the trigger decision in each event.  

To compute the total rate of each trigger, run the script computeRates.py on the output of this analyzer.  For the rate calculation to make sense, make sure HLT_ZeroBias_v1 is included in the trigger menu, so that every event gets saved in the input EDM file.
