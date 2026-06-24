import os, bz2
import pandas as pd
import seaborn as sns
import matplotlib as plt
from scipy.stats import wilcoxon

retention = pd.read_csv('retention.tsv', sep='\t')
statistic, pvalue = wilcoxon( retention[retention['Group']=='cephalosporins']['Retention'], retention[retention['Group']=='control']['Retention'])
ax = sns.boxplot(data=retention, x='Group', y='Retention', order=['control', 'cephalosporins'])
ax.set_title(f'Retention p = {pvalue}')
plt.pyplot.savefig('retention.png')
