'''
Call with 'python'

Usage: 
    compare_ntuples.py --file1=PTH --file2=PTH --output_dir=DIR

Options:
    --file1=PTH             Path to the first file for the comparison
    --file2=PTH             Path to the second file for the comparsion
    -- output_dir=PTH       Directory for the resulting comparison plots
'''

import ROOT
import os
from array import array
import numpy as np
import docopt
import math
import plotting_helper as ph
import json



additions = [
        'Jet_pt_nom',
        'MET_T1_pt_jesTotalDown',
        'Jet_pt_jerDown',
        'MET_T1_pt_jerUp',
        'MET_T1_phi_jerUp',
        'MET_T1Smear_pt_jerUp',
        'MET_pt_unclustEnDown',
        'Jet_corr_JEC',
        'Jet_mass_jerDown',
        'MET_T1_pt_jesTotalUp',
        'Jet_pt_raw',
        'Jet_pt_jerUp',
        'MET_T1Smear_pt_jerDown',
        'Jet_mass_jerUp',
        'MET_phi_unclustEnUp',
        'Jet_mass_jesTotalUp',
        'MET_T1Smear_phi_jesTotalUp',
        'MET_T1_pt_jerDown',
        'MET_T1Smear_pt_jesTotalDown',
        'Jet_mass_nom',
        'MET_T1Smear_phi_jerUp',
        'MET_T1_phi_jerDown',
        'MET_pt_unclustEnUp',
        'Jet_pt_jesTotalUp',
        'MET_T1Smear_pt_jesTotalUp',
        'Jet_mass_raw',
        'Jet_mass_jesTotalDown',
        'MET_T1Smear_phi_jesTotalDown',
        'MET_T1_pt',
        'MET_T1_phi_jesTotalUp',
        'MET_T1Smear_pt',
        'MET_phi_unclustEnDown',
        'MET_T1Smear_phi_jerDown',
        'MET_T1_phi',
        'MET_T1Smear_phi',
        'Jet_pt_jesTotalDown',
        'Jet_corr_JER',
        'MET_T1_phi_jesTotalDown'
]

MET_ADDITIONS = [x for x in additions if 'MET' in x]
JET_ADDITIONS = [x for x in additions if 'Jet' in x]

def main(file1, file2, output_dir):
    tfile1 = ROOT.TFile(file1)
    tree1 = tfile1.Get('Events')
    tfile2 = ROOT.TFile(file2)
    tree2 = tfile2.Get('Events')
    hist_info = {}
    for addition in additions:
        hist_info[addition] = {
            'file1': [],
            'file2': [],
        }
    for idx in range(tree2.GetEntries()):
        tree1.GetEntry(idx)
        tree2.GetEntry(idx)
        for met_addition in MET_ADDITIONS:
            hist_info[met_addition]['file1'].append(getattr(tree1, met_addition))
            hist_info[met_addition]['file2'].append(getattr(tree2, met_addition))
        for jet_idx in range(tree2.nJet):
            for addition in JET_ADDITIONS:
                file1_add = getattr(tree1, addition)[jet_idx]
                file2_add = getattr(tree2, addition)[jet_idx]
                hist_info[addition]['file1'].append(file1_add)
                hist_info[addition]['file2'].append(file2_add)
    for addition in additions:
        hist_info[addition]['n_bins'] = int(
            np.sqrt(len(hist_info[addition]['file2'])))
        hist_info[addition]['bin_start'] = 0
        hist_info[addition]['bin_end'] = 3
        # hist_info[addition]['bin_start'] = min(hist_info[addition]['file2'])
        # hist_info[addition]['bin_end'] = max(hist_info[addition]['file2'])
    for addition in additions:
        info = hist_info[addition]
        histogram1 = ROOT.TH1D(
            addition + '_1', addition, info['n_bins'],
            info['bin_start'], info['bin_end']
        )
        histogram2 = ROOT.TH1D(
            addition  + '_2', addition, info['n_bins'],
            info['bin_start'], info['bin_end']
        )
        histogram1.StatOverflows(True)
        histogram2.StatOverflows(True)
        histogram2.SetLineColor(2)
        histogram2.SetLineStyle(7)
        for entry1, entry2 in zip(info['file1'], info['file1']):
            histogram1.Fill(entry1)
            histogram2.Fill(entry2)
        plotting(histogram1, histogram2, addition, output_dir)


def plotting(
        histogram1, histogram2,
        addition, output_dir,
        SetLogy=True, SetLogx=False
):
    outfile = os.path.join(output_dir, addition + '.pdf')
    canvas = ROOT.TCanvas()
    pads = ph.TwoPadSplit(0.27, 0.01, 0.01)
    pads[0].cd()
    pads[0].SetLogy(SetLogy)
    pads[0].SetLogx(SetLogx)
    histogram1.Draw()
    histogram2.Draw('same')
    pads[1].cd()
    pads[1].SetGrid(0,2)
    ratio_hist = ph.MakeRatioHist(histogram1, histogram2, False, False)
    ratio_hist.SetMarkerSize(1)
    ratio_hist.SetMarkerStyle(7)
    ratio_hist.Draw('P')
    ratio_d = {}
    for i in range(ratio_hist.GetNbinsX()):
        ratio = ratio_hist.GetBinContent(i)
        bin_center = ratio_hist.GetBinCenter(i)
        bin_error = ratio_hist.GetBinError(i)
        bin_d = {'ratio': ratio, 'bin_center': bin_center, 'bin_error': bin_error}
        ratio_d['bin_'+str(i)] = bin_d
    jsonFile = os.path.join(output_dir, addition + '.json')
    with open(jsonFile, 'wt') as outFile:
        json.dump(ratio_d, outFile, indent=4)
    ph.FixTopRange(pads[0], ph.GetPadYMax(pads[0]), 0.30)
    ph.SetupTwoPadSplitAsRatio(
        pads, ph.GetAxisHist(
            pads[0]), ph.GetAxisHist(pads[1]), 'Ratio', True, 0.41, 1.59)
    ph.DrawCMSLogo(pads[0], 'CMS', 'Private', 11, 0.15, 0.01, 1.0, '', 0.7)
    ROOT.gStyle.SetOptStat(0)
    legend = ROOT.TLegend(0.67, 0.80, 0.90, 0.91,'','NBNDC')
    legend.AddEntry(histogram1, 'histogram1')
    legend.AddEntry(histogram2, 'histogram2')
    legend.SetTextFont(132)
    legend.SetTextSize(.03)
    legend.Draw()
    canvas.Print(outfile)


if __name__ == '__main__':
    try:
        arguments = docopt.docopt(__doc__)
        output_dir = arguments['--output_dir']
        file1 = arguments['--file1']
        file2 = arguments['--file2']
        main(file1, file2, output_dir)
    except docopt.DocoptExit as e:
        print(e)
