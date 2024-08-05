import pandas as pd

input_file = 'GARP_Measures_Rationality_Results.txt'
input_file_demo = 'output_demo.csv'
output_file = 'output_for_analysis.csv'

columns_to_extract = ['SubID', 'GARP_violations_mirrored', 'Varian_sym', 'which_manipulation_bundles', 'gender', 'handedness', 'age']
    
df = pd.read_csv(input_file)
df_2 =  pd.read_csv(input_file_demo)

final_df = pd.concat([df,df_2], axis=1)
final_df =final_df.drop(columns=['subject_ID'])

end_df = final_df[columns_to_extract].copy()

end_df['gender'] = end_df['gender'].replace({'Male': 0, 'Female': 1})
end_df['handedness'] = end_df['handedness'].replace({'Right': 0, 'Left': 1, 'Ambidextrous': 2})
end_df.to_csv(output_file, index=False)  