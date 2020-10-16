'''
Creates a cutflow table for the settings given in the info directory and in
the global_settings

Call with 'python'

'''
import os
import ROOT
import pandas
from machineLearning.machineLearning import data_loading_tools as dlt
from machineLearning.machineLearning import universal_tools as ut
from machineLearning.machineLearning import hh_aux_tools as hhat


def main():
    channel_dir, info_dir, global_settings = ut.find_settings()
    preferences = hhat.get_hh_parameters(
        channel_dir,
        global_settings['tauID_training'],
        info_dir
    )
    total_df = pandas.DataFrame()
    for era in preferences['included_eras']:
        input_path_key = 'inputPath' + str(era)
        preferences['era_inputPath'] = preferences[input_path_key]
        preferences['era_keys'] = preferences['keys' + str(era)]
        era_df, labels = load_one_era(preferences, global_settings)
        total_df.append(era_df, ignore_index=True)
    create_latex_table(total_df, labels, global_settings['output_dir'])


def load_one_era(preferences, global_settings):
    total_era_cutflow_df = pandas.DataFrame()
    for folder_name in preferences['era_keys']:
        sample_name, _ = dlt.find_sample_info(
            folder_name, global_settings['bdtType'], preferences['masses']
        )
        paths = dlt.get_all_paths(
            preferences['era_inputPath'],
            folder_name,
            global_settings['bdtType']
        )
        input_tree = os.path.join(
            preferences['channelInTree'], 'sel/cutFlow', sample_name, 'cutFlow')
        for path in paths:
            tfile = ROOT.TFile(path)
            cutflow_dict, labels = load_cutflow(input_tree, tfile)
            single_cutflow_df = pandas.DataFrame(cutflow_dict)
            total_era_cutflow_df.append(single_cutflow_df, ignore_index=True)
    return total_era_cutflow_df, labels


def create_latex_table(total_df, labels, output_dir):
    labels = total_df.keys()
    table = []
    for cut in labels:
        table_row = str(cut) + ' & ' + str(sum(total_df[cut])) + '\\\\'
        table.append(table_row)
    cutflow_file = os.path.join(output_dir, 'cutflow.tex')
    with open(cutflow_file, 'wt') as out_file:
        out_file.write('\\begin{tabular}{c|c}')
        out_file.write('\n')
        for line in table:
            out_file.write(line)
            out_file.wite('\n')
        out_file.write('\\end{tabular}')


def load_cutflow(input_tree, tfile):
    cutflow_dict = {}
    histo = tfile.Get(input_tree)
    print(input_tree)
    print(histo)
    number_bins = histo.GetNbinsX()
    x_axis = histo.GetXaxis()
    labels = []
    for i in range(1, number_bins + 1):
        bin_label = x_axis.GetBinLabel(i)
        number_events = histo.GetBinContent(i)
        cutflow_dict[bin_label] = number_events
        labels.append(bin_label)
    return cutflow_dict, labels


if __name__ == '__main__':
    main()
