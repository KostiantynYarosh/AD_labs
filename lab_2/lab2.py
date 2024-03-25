import os
import pandas as pd

directory = 'D:\Desktop\KPI\Kpi_2023\sem_2\AD\lab_2\csv_files'

def extract(directory):
  files = os.listdir(directory)
  headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
  main_df = pd.DataFrame()
  for i in range(len(files)):
    file_path = os.path.join(directory, files[i])
    df = pd.read_csv(file_path, header = 1, names = headers)
    df = df.drop(df.loc[df['VHI'] == -1].index)
    df['area'] = i+1
    
    df['Year'] = df['Year'].str.replace('<tt><pre>', '')
    
    df = df.drop(df[df['Year'] == '</pre></tt>'].index)
    df["Year"] = df["Year"].astype(int)
    main_df = pd.concat([main_df, df])
  return main_df


def change_area(df):
  names =  {1: "Cherkasy", 2: "Chernihiv", 3: "Chernivtsi", 4: "Crimea", 5: "Dnipropetrovs'k", 6: "Donets'k", 7: "Ivano-Frankivs'k", 8: "Kharkiv", 9: "Kherson", 10: "Khmel'nyts'kyy", 11: "Kiev", 12: "Kiev City", 13: "Kirovohrad", 14: "Luhans'k", 15: "L'viv", 16: "Mykolayiv", 17: "Odessa", 18: "Poltava", 19: "Rivne", 20: "Sevastopol'", 21: "Sumy", 22: "Ternopil'", 23: "Transcarpathia", 24: "Vinnytsya", 25: "Volyn", 26: "Zaporizhzhya", 27: "Zhytomyr"}
  for name in names:
    df["area"].replace({name:names[name]}, inplace = True)
  return df

def min_vhi(df, area_name, year):
  filtered_df = df[(df["area"] == area_name) & (df["Year"] == year)]
  minimum_vhi = filtered_df["VHI"].min()
  return filtered_df[filtered_df["VHI"] == minimum_vhi]

def max_vhi(df, area_name, year):
  filtered_df = df[(df["area"] == area_name) & (df["Year"] == year)]
  maximum_vhi = filtered_df["VHI"].max()
  
  return filtered_df[filtered_df["VHI"] == maximum_vhi]

'''(df.VHI <= 15)'''
def find_extrim(df, area_name, precent):
  # df_drought = df[(df["area"] == area_name)]
  # years = list(df['Year'].unique())
  # res = []
  # for year in years:
  #   if not df[(df["Year"] == year) & (df.VHI <= precent)].empty:
  #     res.append(year)
  res = df[(df.VHI <= precent)]["Year"].unique()
  return res
  

df = change_area(extract(directory))
print(min_vhi(df, "Chernihiv", 2005))
print(max_vhi(df, "Chernihiv", 2005))
print(df)
print(find_extrim(df, "Chernihiv", 15))


