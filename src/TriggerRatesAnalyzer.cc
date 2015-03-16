#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "HLTriggerOffline/TriggerRatesAnalyzer/interface/TriggerRatesAnalyzer.h"

TriggerRatesAnalyzer::TriggerRatesAnalyzer(const edm::ParameterSet& ps)
{
    edm::LogInfo("TriggerRatesAnalyzer") << "Constructor TriggerRatesAnalyzer::TriggerRatesAnalyzer " << std::endl;

    // Get parameters from configuration file
    triggerResults_ = consumes<edm::TriggerResults>(ps.getParameter<edm::InputTag>("TriggerResults"));

    //declare the TFileService for output
    edm::Service<TFileService> fs;

    //set up output tree
    outTree = fs->make<TTree>("TriggerInfo", "Rate info");

    outTree->Branch("numTriggers", &numTriggers, "numTriggers/I"); 
    outTree->Branch("triggerPassed", triggerPassed, "triggerPassed[numTriggers]/O");
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
    for(int i = 0; i < 50; i++){
        triggerPassed[i] = false;
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
        if (hltresults->wasrun(hltIndex)) std::cout << trigNames.triggerName(hltIndex) << endl;
        if (hltresults->wasrun(hltIndex) && hltresults->accept(hltIndex)) triggerPassed[hltIndex] = true;
    }

    outTree->Fill();
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
