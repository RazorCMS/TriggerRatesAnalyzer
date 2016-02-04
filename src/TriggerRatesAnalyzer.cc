#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "HLTriggerOffline/TriggerRatesAnalyzer/interface/TriggerRatesAnalyzer.h"

//string/vector
#include <string>
#include <iostream>
#include <vector>
TriggerRatesAnalyzer::TriggerRatesAnalyzer(const edm::ParameterSet& ps)
{
    edm::LogInfo("TriggerRatesAnalyzer") << "Constructor TriggerRatesAnalyzer::TriggerRatesAnalyzer " << std::endl;

    // Get parameters from configuration file
    triggerResults_ = consumes<edm::TriggerResults>(ps.getParameter<edm::InputTag>("TriggerResults"));    
    puInfo_ = consumes<std::vector<PileupSummaryInfo> >(ps.getParameter<edm::InputTag>("puInfo"));    
    puMin = ps.getParameter<int>("puMin");
    puMax = ps.getParameter<int>("puMax");

    //declare the TFileService for output
    edm::Service<TFileService> fs;

    //set up output tree
    outTree = fs->make<TTree>("TriggerInfo", "Rate info");

    //myTriggerNames = new std::vector<std::string>; myTriggerNames->clear();
    outTree->Branch("numTriggers", &numTriggers, "numTriggers/I"); 
    outTree->Branch("triggerPassed", triggerPassed, "triggerPassed[numTriggers]/O");
    //outTree->Branch("triggerNames", "std::vector<std::string>",&myTriggerNames);
    
    firstEvent = true;
}

TriggerRatesAnalyzer::~TriggerRatesAnalyzer()
{
    edm::LogInfo("TriggerRatesAnalyzer") << "Destructor TriggerRatesAnalyzer::~TriggerRatesAnalyzer " << std::endl;
}

void TriggerRatesAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const& lumiSeg, edm::EventSetup const& context)
{
    edm::LogInfo("TriggerRatesAnalyzer") << "TriggerRatesAnalyzer::beginLuminosityBlock" << std::endl;
}

void TriggerRatesAnalyzer::analyze(edm::Event const& e, edm::EventSetup const& eSetup){

    edm::LogInfo("TriggerRatesAnalyzer") << "TriggerRatesAnalyzer::analyze" << std::endl;

    using namespace std;
    using namespace edm;
    using namespace reco;

    //reset tree variables
    numTriggers = 0;
    for(int i = 0; i < NUM_TRIGGERS_MAX; i++){
        triggerPassed[i] = false;
        //myTriggerNames->clear();
    }

    //check if the event has the desired number of pileup interactions
    if (puMin > 0 || puMax < 999) { //these are the default values 
        edm::Handle<std::vector<PileupSummaryInfo> > puInfo;
        e.getByToken(puInfo_,puInfo);
        if (!puInfo.isValid()) {
            edm::LogError ("TriggerRatesAnalyzer") << "invalid collection: puInfo\n";
        }

        int nPU = -1;
        for(const PileupSummaryInfo &pu : *puInfo){
            int BunchXing = pu.getBunchCrossing();
            if (BunchXing == 0) {
                nPU = pu.getTrueNumInteractions();
                break;
            }
        }
        if (nPU < 0) {
            edm::LogError ("TriggerRatesAnalyzer") << "didn't find bunch crossing 0\n";
        }
        else if (nPU < puMin || nPU > puMax) {
            //std::cout << "Pileup is " << nPU << ", not between " << puMin << " and " << puMax << "\n";
            return;
        }
        else {
            //std::cout << "Pileup is " << nPU << ", which is within the desired range\n";
        }
    }

    //check what is in the menu
    edm::Handle<edm::TriggerResults> hltresults;
    e.getByToken(triggerResults_,hltresults);
    if(!hltresults.isValid()){
        edm::LogError ("TriggerRatesAnalyzer") << "invalid collection: TriggerResults" << "\n";
        return;
    }

    const edm::TriggerNames& trigNames = e.triggerNames(*hltresults);
    numTriggers = trigNames.size();
    //loop over triggers
    for( unsigned int hltIndex=0; hltIndex<numTriggers; ++hltIndex ){
        if (hltIndex > NUM_TRIGGERS_MAX) break; //avoid memory leaks from too many triggers

      if (hltresults->wasrun(hltIndex) && firstEvent) {
	std::cout << hltIndex << " " << trigNames.triggerName(hltIndex) << endl;
      }
      //myTriggerNames->push_back(trigNames.triggerName(hltIndex));
      if (hltresults->wasrun(hltIndex) && hltresults->accept(hltIndex)) triggerPassed[hltIndex] = true;
    }
    
    outTree->Fill();    
    firstEvent = false;
}

void TriggerRatesAnalyzer::endLuminosityBlock(edm::LuminosityBlock const& lumiSeg, edm::EventSetup const& eSetup)
{
    edm::LogInfo("TriggerRatesAnalyzer") << "TriggerRatesAnalyzer::endLuminosityBlock" << std::endl;
}


void TriggerRatesAnalyzer::endRun(edm::Run const& run, edm::EventSetup const& eSetup)
{
    edm::LogInfo("TriggerRatesAnalyzer") << "TriggerRatesAnalyzer::endRun" << std::endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerRatesAnalyzer);
