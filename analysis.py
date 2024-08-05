import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin as pg

df = pd.read_csv('output_for_analysis.csv')

def label_bundles(bundle):
    if bundle in [1, 4]:
        return 'Valid'
    elif bundle in [2, 5]:
        return 'Invalid'
    elif bundle in [3, 6]:
        return 'Neutral'

df['bundle_label'] = df['which_manipulation_bundles'].apply(label_bundles)

df_1_3 = df[df['which_manipulation_bundles'].isin([1, 2, 3])]
df_4_6 = df[df['which_manipulation_bundles'].isin([4, 5, 6])]

model_1_3 = ols('GARP_violations_mirrored ~  age ', data=df_4_6).fit()

def run_ancova(data, dependent_var, reference_group, group_name):
    anova_table = pg.ancova(data=data, dv=dependent_var, covar=['age', 'gender'], between='which_manipulation_bundles')
    
    anova_table.to_csv(f'ANOVA_table_{dependent_var}_{group_name}.csv')
    
    tukey = pairwise_tukeyhsd(endog=data[dependent_var], groups=data['which_manipulation_bundles'], alpha=0.05)
    
    with open(f'TukeyHSD_{dependent_var}_{group_name}.txt', 'w') as f:
        f.write(tukey.summary().as_text())

dependent_vars = ['Varian_sym', 'GARP_violations_mirrored']
reference_groups = [3, 6]
data_groups = [(df_1_3, 3, '1-3'), (df_4_6, 6, '4-6')]

for dep_var in dependent_vars:
    for data, ref_group, group_name in data_groups:
        run_ancova(data, dep_var, ref_group, group_name)

def plot_results(data, dependent_var, title, group_name):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    
    formatted_title = title.replace('_', ' ')
    formatted_ylabel = dependent_var.replace('_', ' ')
    
    sns.barplot(x='bundle_label', y=dependent_var, data=data, order=['Valid', 'Invalid', 'Neutral'], capsize=0.2, errorbar="sd", errwidth=1)
    
    sns.swarmplot(x='bundle_label', y=dependent_var, data=data, color="darkred", order=['Valid', 'Invalid', 'Neutral'])
    
    plt.title(f'{formatted_title}')
    plt.xlabel(' ')
    plt.ylabel(formatted_ylabel)
    
    plt.savefig(f'{dependent_var}_plot_{group_name}.png')
    plt.close()
    
    summary_stats = data.groupby('bundle_label')[dependent_var].describe()
    summary_stats.to_csv(f'summary_stats_{dependent_var}_{group_name}.csv')

for dep_var in dependent_vars:
    plot_results(df_1_3, dep_var, f'{dep_var} for exogenous attention', '1-3')
    plot_results(df_4_6, dep_var, f'{dep_var} for endogenous attention', '4-6')