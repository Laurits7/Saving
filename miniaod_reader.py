import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.gSystem.Load('libDataFormatsFWLite.so')
ROOT.FWLiteEnabler.enable()
from DataFormats.FWLite import Handle, Events


class MiniAODreader:
    def __init__(self, miniaod_file):
        self.jets = Handle('std::vector<pat::Jet>')
        self.jetsLabel = 'slimmedJets'
        self.fatjets = Handle('std::vector<pat::Jet>')
        self.fatjetLabel = 'slimmedJetsAK8'
        self.events = Events('miniAOD.root')
        self.mets = Handle('std::vector<pat::MET>')
        self.metLabel = 'slimmedMETs'
        self.variables = {
            'MET_jesUp': [],
            'MET_jesDown': [],
            'MET_jerUp': [],
            'MET_jerDown': [],
            # --------------
            'MET_pt_nom': [],
            'MET_pt_jer': [],
            'MET_pt_jerUp': [],
            'MET_pt_jerDown': [],
            'MET_pt_jesTotalUp': [],
            'MET_pt_jesTotalDown': [],
            'MET_pt_unclustEnUp': [],
            'MET_pt_unclustEnDown': [],
            'MET_phi_nom': [],
            'MET_phi_jer': [],
            'MET_phi_jerUp': [],
            'MET_phi_jerDown': [],
            'MET_phi_jesTotalUp': [],
            'MET_phi_jesTotalDown': [],
            'MET_phi_unclustEnUp': [],
            'MET_phi_unclustEnDown': [],
            'Jet_pt_nom': [],
            'Jet_pt_raw': [],
            'Jet_pt_jerUp': [],
            'Jet_pt_jerDown': [],
            'Jet_pt_jesTotalUp': [],
            'Jet_pt_jesTotalDown': [],
            'Jet_corr_JER': [],
            'Jet_corr_JEC': [],
            'Jet_mass_nom': [],
            'Jet_mass_raw': [],
            'Jet_mass_jerUp': [],
            'Jet_mass_jerDown': [],
            'Jet_mass_jesTotalUp': [],
            'Jet_mass_jesTotalDown': []
        }

    def load_events(self, max_events):
        for idx, event in enumerate(self.events):
            if idx > max_events:
                break
            self.get_met_variables(event)
            self.get_jet_variables(event)

    def get_met_variables(self, event):
        event.getByLabel(self.metLabel, self.mets)
        met = self.mets.product().front()
        self.variables['MET_jesUp'].append(met.shiftedPt(ROOT.pat.MET.JetEnUp))
        self.variables['MET_jesDown'].append(met.shiftedPt(ROOT.pat.MET.JetEnDown))
        self.variables['MET_jerUp'].append(met.shiftedPt(ROOT.pat.MET.JetResUp))
        self.variables['MET_jerDown'].append(met.shiftedPt(ROOT.pat.MET.JetResDown))

    def get_jet_variables(self, event):
        event.getByLabel(self.jetsLabel, self.jets)
        jet = self.jets.product().front()
        # print(jet.correctedJet(ROOT.pat.Jet.correctedJet))
        # print(jet.currentJECLevel())
        # print(jet.currentJECSet())



reader = MiniAODreader('miniAOD.root')
reader.load_events(10)


################ Needed variables: ####################################

# 'MET_pt_nom',
# 'MET_pt_jer',
# 'MET_pt_jerUp',
# 'MET_pt_jerDown',
# 'MET_pt_jesTotalUp',
# 'MET_pt_jesTotalDown',
# 'MET_pt_unclustEnUp',
# 'MET_pt_unclustEnDown',
# # -----------------------
# 'MET_phi_nom',
# 'MET_phi_jer',
# 'MET_phi_jerUp',
# 'MET_phi_jerDown',
# 'MET_phi_jesTotalUp',
# 'MET_phi_jesTotalDown',
# 'MET_phi_unclustEnUp',
# 'MET_phi_unclustEnDown',
# # ------------------------
# 'Jet_pt_nom',
# 'Jet_pt_raw',
# 'Jet_pt_jerUp',
# 'Jet_pt_jerDown',
# 'Jet_pt_jesTotalUp',
# 'Jet_pt_jesTotalDown',
# # ------------------------
# 'Jet_corr_JER',
# 'Jet_corr_JEC',
# 'Jet_mass_nom',
# 'Jet_mass_raw',
# 'Jet_mass_jerUp',
# 'Jet_mass_jerDown',
# 'Jet_mass_jesTotalUp',
# 'Jet_mass_jesTotalDown'
