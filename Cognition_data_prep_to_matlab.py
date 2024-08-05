import pandas as pd
import numpy as np
import ast
import os
import glob

arrays_mapping = {
    'a1': [[0, 84], [17, 76], [34, 67], [56, 56], [67, 50], [84, 42], [101, 34], [118, 25], [134, 17], [151, 8], [168, 0]],
    'a2': [[0, 54], [20, 49], [43, 43], [65, 38], [86, 32], [108, 27], [130, 22], [151, 16], [173, 11], [194, 5], [216, 0]],
    'a3': [[0, 225], [15, 203], [30, 180], [45, 158], [60, 135], [75, 113], [90, 90], [105, 68], [120, 45], [135, 23], [150, 0]],
    'a4': [[0, 111], [18, 101], [36, 91], [54, 81], [71, 71], [92, 59], [117, 45], [137, 33], [156, 22], [176, 11], [195, 0]],
    'a5': [[0, 108], [15, 96], [29, 85], [46, 71], [60, 60], [71, 52], [81, 43], [95, 32], [108, 22], [122, 11], [135, 0]],
    'a6': [[0, 270], [6, 243], [12, 216], [18, 189], [24, 162], [30, 135], [36, 108], [43, 78], [49, 49], [55, 24], [60, 0]],
    'a7': [[0, 150], [23, 135], [45, 120], [68, 105], [90, 90], [113, 75], [135, 60], [158, 45], [180, 30], [203, 15], [225, 0]],
    'a8': [[0, 165], [17, 149], [33, 132], [50, 116], [66, 99], [83, 83], [99, 66], [116, 50], [132, 33], [149, 17], [165, 0]],
    'a9': [[0, 102], [26, 92], [51, 82], [73, 73], [102, 61], [128, 51], [153, 41], [179, 31], [204, 20], [230, 10], [255, 0]],
    'a10': [[0, 168], [8, 151], [17, 134], [25, 118], [34, 101], [42, 84], [50, 67], [56, 56], [67, 34], [76, 17], [84, 0]],
    'a11': [[0, 216], [5, 194], [11, 173], [16, 151], [22, 130], [27, 108], [32, 86], [38, 65], [43, 43], [49, 20], [54, 0]],
    'a12': [[0, 255], [10, 230], [20, 204], [31, 179], [41, 153], [51, 128], [61, 102], [73, 73], [82, 51], [92, 26], [102, 0]],
    'a13': [[0, 90], [33, 79], [68, 68], [90, 60], [111, 53], [135, 45], [162, 36], [189, 27], [216, 18], [243, 9], [270, 0]],
    'a14': [[0, 270], [9, 243], [18, 216], [27, 189], [36, 162], [45, 135], [53, 111], [60, 90], [68, 68], [79, 33], [90, 0]],
    'a15': [[0, 60], [24, 55], [49, 49], [78, 43], [108, 36], [135, 30], [162, 24], [189, 18], [216, 12], [243, 6], [270, 0]],
    'a16': [[0, 195], [11, 176], [22, 156], [33, 137], [45, 117], [59, 92], [71, 71], [81, 54], [91, 36], [101, 18], [111, 0]],
    'a17': [[0, 135], [11, 122], [22, 108], [32, 95], [43, 81], [52, 71], [60, 60], [71, 46], [85, 29], [96, 15], [108, 0]],
    'a18': [[0, 58], [23, 53], [48, 48], [80, 42], [115, 35], [144, 29], [173, 23], [202, 17], [230, 12], [259, 6], [288, 0]],
    'a19': [[0, 288], [6, 259], [12, 230], [17, 202], [23, 173], [29, 144], [35, 115], [42, 80], [48, 48], [53, 23], [58, 0]],
    'a20': [[0, 195], [20, 176], [39, 156], [59, 137], [78, 117], [98, 98], [117, 78], [137, 59], [156, 39], [176, 20], [195, 0]]
}

columns_to_extract = ['ID_test', 'graph_number', 'finalchoice', 'rt', 'which_manipulation_bundles', 'gender', 'handedness', 'birth_year', 'occupation',]

def process_csv(file_path, subject):
    df = pd.read_csv(file_path)
    new_df = df[columns_to_extract]
    filtered_df = new_df.dropna(subset=['graph_number']).drop([12, 16], axis=0)
    
    subject_ID = subject
    
    first_row_2 = filtered_df.iloc[1, 4:]
    final_2_df = pd.DataFrame([first_row_2], columns=[
        'subject_ID', 'which_manipulation_bundles', 'gender', 'handedness', 'birth_year', 'occupation' ])
    final_2_df['subject_ID'] = subject
    final_2_df['age'] = 2024 - final_2_df['birth_year']
    final_2_df.drop(columns=['birth_year'], inplace=True)
    
    final_rows = []

    for index, row in filtered_df.iterrows():
        graph_number = row['graph_number']
        finalchoice_array = np.array(ast.literal_eval(row['finalchoice']), dtype=float)
        trial = int(row['graph_number'][1:]) + (20 if index >= 80 else 0)
        rt = float(row['rt']) / 1000
        choice_array = arrays_mapping[graph_number]
        
        for pair_index, (num1, num2) in enumerate(choice_array):
            if (finalchoice_array[0] == 0 and finalchoice_array[1] == 0):
                choice = None 
            elif (finalchoice_array[0] == num1 and finalchoice_array[1] == num2):
                choice = 1 
            else:
                choice = 0
                
            final_rows.append([
                subject_ID, int(num1), int(num2), trial, int(pair_index + 1), 0,
                choice, rt
            ])

    final_df = pd.DataFrame(final_rows, columns=[
        'subject_ID', 'number_1', 'number_2', 'trial', 'pair', 'start_pair', 'choice', 
        'reaction_time' ])

    final_df.sort_values(by=['trial', 'pair'], inplace=True)

    return final_df, final_2_df, filtered_df

def process_multiple_csv(input_dir):
    
    df_final = pd.DataFrame(columns=[
        'subject_ID', 'number_1', 'number_2', 'trial', 'pair', 'start_pair', 'choice', 
        'reaction_time' ])
    df_final_2 = pd.DataFrame(columns=[
        'subject_ID', 'which_manipulation_bundles', 'gender', 'handedness', 'age', 'occupation'])
        
    subject_var = 0
    
    csv_files = sorted(glob.glob(os.path.join(input_dir, '*.csv')))
    
    for file in csv_files:
       
        subject_var += 1
        final_df, final_2_df  = process_csv(file, subject_var)
        df_final = pd.concat([df_final, final_df], ignore_index=True)
        df_final_2 = pd.concat([df_final_2, final_2_df], ignore_index=True)
        

    return df_final, df_final_2

input_dir = 'input_folder'
df_final, df_final_2 , new123= process_multiple_csv(input_dir)

df_final.to_excel('output_data.xlsx', index=False)
df_final_2.to_csv('output_Demo.csv', index=False)
