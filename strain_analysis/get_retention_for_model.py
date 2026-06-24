import os, bz2
import pandas as pd

metadata = pd.read_csv('RaymondF_2016_metadata.tsv', sep='\t', index_col=1)
strain_identity_threshold = 0.0001
comparison = '0-7'

for sgb in os.listdir('RaymondF_2016/'):
    print(sgb)
    mutation_rates = f'distances/{sgb}.tsv'
    mutation_rates = pd.read_csv(mutation_rates, sep='\t', index_col=0)
    same_individual_distances = pd.DataFrame()
    for i in mutation_rates.index:
        if metadata.loc[mutation_rates.loc[i,'S1'], 'subject_id'] == metadata.loc[mutation_rates.loc[i,'S2'], 'subject_id']:
            same_individual_distances = pd.concat([same_individual_distances, mutation_rates.loc[[i]]])
    same_individual_distances['Group'] = metadata.loc[same_individual_distances['S2']]['study_condition'].tolist()
    same_individual_distances['Comparison'] = [x.split('E')[-1].split('C')[-1]+ '-'+ y.split('E')[-1].split('C')[-1] for x, y in zip(same_individual_distances['S1'],same_individual_distances['S2'])]
    same_individual_distances['Distance'] = same_individual_distances['Distance'].astype(float)
    same_individual_distances['Retention'] = same_individual_distances['Distance'] < strain_identity_threshold
    same_individual_distances['Retention'] = same_individual_distances['Retention'].astype(int)
    same_individual_distances.to_csv(f'retention/{sgb}.tsv', sep='\t')
