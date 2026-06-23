#!/mnt/Prebiomics_Data/tools/anaconda3/bin/python

import pandas as pd
import numpy as np
import argparse as ap
import os

parser = ap.ArgumentParser()
arg = parser.add_argument
arg('-k', type=str, help='KMA folder.')
par = vars(parser.parse_args())

dirs = os.listdir(par['k']+'/')

for d in dirs:
    data = pd.read_csv(par['k']+'/'+d+'/'+d+'.mapstat', index_col=0, sep='\t', skiprows=[0,1,2,3,4])
    meta = pd.read_csv(par['k']+'/'+d+'/'+d+'.res', index_col=0, sep='\t')
    data = data.merge(meta, left_index=True, right_index=True)
    data['RPKM'] = data.readCount / ((data.Template_length / 1000) * (data.readCount.sum() / 1000000))
    data[['RPKM']].to_csv(par['k']+'/'+d+'/'+d+'_profile.tsv', sep='\t')
