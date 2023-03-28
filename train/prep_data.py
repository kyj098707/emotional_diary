import os, glob
import pandas as pd

def combine_csv(origin_path, target_path):
    o_path = os.path.join(origin_path, '*.csv')
    t_path = os.path.join(target_path, 'target.csv')
    csv_files = glob.glob(o_path)
    dataframes = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding='cp949', sep=',').replace('\t', '', regex=True)
        dataframes.append(df)
    combined_df = pd.concat(dataframes, axis=0, ignore_index=True)
    combined_df = combined_df.rename(columns={'4번감정세기' : '4번 감정세기'})
    data_col = ['발화문']
    for i in range(1, 6):
        combined_df[f'{i}번 감정'] = combined_df[f'{i}번 감정'].str.lower()
        data_col.append(f'{i}번 감정')
        data_col.append(f'{i}번 감정세기')

    combined_df = combined_df[data_col]
    combined_df.to_csv(t_path, index=False)

    return t_path