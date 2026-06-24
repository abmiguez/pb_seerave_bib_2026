import os, bz2
import pandas as pd

for sgb in os.listdir('RaymondF_2016/'):
    print(sgb)
    mutation_rates = f'RaymondF_2016/{sgb}/{sgb}.mutation'
    mutation_rates = pd.read_csv(mutation_rates, sep='\t', index_col=0)
    mutation_rates_mat = []
    for i, x in enumerate(mutation_rates.columns):
        for j, y in enumerate(mutation_rates.index):
            if j <= i:
                pass
            else:
                mutation_rates_mat.append([x,y,mutation_rates.loc[x,y]])
    mutation_rates = pd.DataFrame(mutation_rates_mat, columns = ['S1', 'S2', 'Distance'])
    mutation_rates.to_csv(f'distances/{sgb}.tsv', sep='\t')
