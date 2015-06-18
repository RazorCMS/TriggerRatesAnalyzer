# TriggerRatesAnalyzer
Lightweight analyzer for measuring the rates of HLT paths

`git clone git@github.com:RazorCMS/TriggerRatesAnalyzer.git HLTriggerOffline/TriggerRatesAnalyzer`

`scram b`

To run: `cmsRun test/TriggerRatesAnalyzer.py`

The variable `listFile` in `test/TriggerRatesAnalyzer.py` specifies the analyzer's input.  The indicated file should contain a list of input EDM files, one per line.  Each EDM file needs to contain a TriggerResults object.

The analyzer produces an output ROOT file containing a TTree with the trigger decision for each path in each event.  

###Measuring rates using QCD pt-binned samples

For each QCD sample, run `test/TriggerRatesAnalyzer.py` to dump the trigger decisions in each event.  Open `computeRates.py` and update lines 8-11 to specify the names of the input files, QCD cross sections, and instantaneous luminosity.  Then compute the total rate for each trigger with `python computeRates.py`.

**Note**: for the rate calculation to make sense, make sure `HLT_ZeroBias_v1` is included in your HLT menu.  If it is not, then events that fail all triggers will not be saved.  The rate calculation involves a division by the total number of processed events, and this number will be incorrect if some events have been thrown out.  
