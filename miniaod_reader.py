import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()
from DataFormats.FWLite import Handle, Events


class MiniAODreader:
    def __init__(self, miniaod_file):
        self.jets = Handle("std::vector<pat::Jet>")
        self.jetsLabel = "slimmedJets"
        self.fatjets = Handle("std::vector<pat::Jet>")
        self.fatjetLabel = "slimmedJetsAK8"
        self.events = Events('miniAOD.root')
        self.mets = Handle("std::vector<pat::MET>")
        self.metLabel = "slimmedMETs"
        self.variables = {
            'MET_jesUp': [],
            'MET_jesDown': []
        }

    def load_events(self, max_events):
        for idx, event in enumerate(self.events):
            if idx > max_events:
                break
            # self.get_met_variables(event)

    def get_met_variables(self, event):
        event.getByLabel(self.metLabel, self.mets)
        met = self.mets.product().front()
        self.variables['MET_jesUp'].append(met.shiftedPt(ROOT.pat.MET.JetEnUp))
        self.variables['MET_jesDown'].append(met.shiftedPt(ROOT.pat.MET.JetEnDown))

    # def get_jet_variables(self, event):
    #     event.getByLabel(self.jetsLabel, self.jets)
    #     jet = self.jets.product().front()
    #     print(jet.)


reader = MiniAODreader('miniAOD.root')
reader.load_events(10)


################ Needed variables: ####################################

# 'MET_pt_jerUp',
# 'Jet_pt_jerDown',
# 'MET_phi_jer',
# 'MET_phi_jesTotalDown',
# 'Jet_pt_nom',
# 'Jet_pt_raw',
# 'MET_pt_jer',
# 'MET_phi_unclustEnDown',
# 'MET_pt_nom',
# 'MET_phi_jesTotalUp',
# 'MET_phi_unclustEnUp',
# 'Jet_pt_jesTotalDown',
# 'Jet_corr_JER',
# 'MET_pt_jesTotalDown',
# 'MET_phi_jerDown',
# 'MET_pt_unclustEnDown',
# 'Jet_mass_jerDown',
# 'MET_pt_unclustEnUp',
# 'Jet_mass_jesTotalUp',
# 'Jet_pt_jerUp',
# 'Jet_corr_JEC',
# 'Jet_mass_nom',
# 'MET_pt_jerDown',
# 'MET_pt_jesTotalUp',
# 'Jet_mass_jerUp',
# 'MET_phi_jerUp',
# 'Jet_pt_jesTotalUp',
# 'Jet_mass_jesTotalDown',
# 'MET_phi_nom',
# 'Jet_mass_raw'
