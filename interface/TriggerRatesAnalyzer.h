#ifndef TriggerRatesAnalyzer_H
#define TriggerRatesAnalyzer_H

//ROOT
#include "TTree.h"

//event
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

// Trigger
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"

//string
#include <string>
#include <iostream>
#include <vector>

using namespace edm;
const int NUM_TRIGGERS_MAX = 500;

class TriggerRatesAnalyzer: public EDAnalyzer{

  public:
  TriggerRatesAnalyzer(const edm::ParameterSet& ps);
  virtual ~TriggerRatesAnalyzer();

  protected:
  void analyze(edm::Event const& e, edm::EventSetup const& eSetup);
  void beginLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& eSetup) ;
  void endLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& eSetup);
  void endRun(edm::Run const& run, edm::EventSetup const& eSetup);

  private:

  //variables from config file
  edm::EDGetTokenT<edm::TriggerResults> triggerResults_;
  edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puInfo_;
  int puMin, puMax; //min & max pileup considered

  std::string triggerPath_;
  edm::InputTag triggerFilter_;
  edm::InputTag caloFilter_;

  //tree for output
  TTree *outTree;

  //variables
  unsigned int numTriggers;
  bool triggerPassed[NUM_TRIGGERS_MAX];
  bool firstEvent;
  std::vector<std::string>  *myTriggerNames;
  
};

#endif
