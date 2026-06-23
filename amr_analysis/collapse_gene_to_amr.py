#!/mnt/Prebiomics_Data/tools/anaconda3/envs/prebiomics/bin/python

import pandas as pd
import argparse as ap
import os
import math
import time

def produce_amr_report(sample, output_folder, database, verbose):
    phenotypes = pd.read_csv('{}_phenotypes.txt'.format(database), sep='\t', index_col=[0])

    data = pd.read_csv('{}/{}.mapstat'.format(sample, sample.split('/')[-1]), index_col=0, sep='\t', skiprows=[0,1,2,3,4,5])
    meta = pd.read_csv('{}/{}.res'.format(sample, sample.split('/')[-1]), index_col=0, sep='\t')
    data = data.merge(meta, left_index=True, right_index=True)
    data['RPKM'] = data.readCount / ((data.Template_length / 1000) * (data.readCount.sum() / 1000000))
    profile = data[['RPKM']]

    for analysis_type in ['Phenotype']:
        all_classes = set()
        for x in phenotypes[analysis_type]:
            for y in x.split(','):
                all_classes.add(y.strip())

        for_df = []
        for clas in all_classes:
            targets = [ x for x in profile.index if clas in phenotypes.loc[x,analysis_type] ]
            if len(targets) > 0:
                for_df.append([clas] + profile.loc[targets, ['RPKM']].sum().tolist())

        collapsed_profile = pd.DataFrame(for_df, columns=[analysis_type, 'RPKM']).set_index(analysis_type, drop=True)
        collapsed_profile.to_csv('{}/{}_collapsed.tsv'.format(output_folder,  sample.split('/')[-1]), sep='\t')


def read_params():
    p = ap.ArgumentParser(description="")
    p.add_argument('-i', '--input_folder', type=str, default=None,
                   help="The path to the KMA results folder")
    p.add_argument('-o', '--output_folder', type=str, default=None,
                   help="The folder where to store the results")
    p.add_argument('--database', type=str, default='resfinder_2.3.0',
                   help="The AMR database employed")
    p.add_argument('--verbose', action='store_true', default=False,
                   help="Verbose execution")
    return p.parse_args()


def check_params(args):
    if not args.input_folder:
        print('-i / --input_folder must be specified')
        exit(1)
    if not args.output_folder:
        print('-o / --output_folder must be specified')
        exit(1)


if __name__ == "__main__":
    t0 = time.time()
    args = read_params()
    check_params(args)
    if args.verbose:
        print("Start execution")
    produce_amr_report(args.input_folder,args.output_folder, args.database, args.verbose)
    exec_time = time.time() - t0
    if args.verbose:
        print("Finish execution - {} seconds".format(round(exec_time, 2)))
