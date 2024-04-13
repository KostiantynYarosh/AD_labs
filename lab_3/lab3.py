from spyre import server
import pandas as pd
import os

class StockExample(server.App):
    title = "NOAA data visualization"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA data dropdown', 
            "options": [
                {"label": "VCI", "value": "VCI"}, 
                {"label": "TCI", "value": "TCI"}, 
                {"label": "VHI", "value": "VHI"}
            ], 
            "key": 'ticker', 
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Area', 
            "options": [
                {"label": "Cherkasy", "value": "Cherkasy"},
                {"label": "Chernihiv", "value": "Chernihiv"},
                {"label": "Chernivtsi", "value": "Chernivtsi"},
                {"label": "Crimea", "value": "Crimea"},
                {"label": "Dnipropetrovs'k", "value": "Dnipropetrovs'k"},
                {"label": "Donets'k", "value": "Donets'k"},
                {"label": "Ivano-Frankivs'k", "value": "Ivano-Frankivs'k"},
                {"label": "Kharkiv", "value": "Kharkiv"},
                {"label": "Kherson", "value": "Kherson"},
                {"label": "Khmel'nyts'kyy", "value": "Khmel'nyts'kyy"},
                {"label": "Kiev", "value": "Kiev"},
                {"label": "Kiev City", "value": "Kiev City"},
                {"label": "Kirovohrad", "value": "Kirovohrad"},
                {"label": "Luhans'k", "value": "Luhans'k"},
                {"label": "L'viv", "value": "L'viv"},
                {"label": "Mykolayiv", "value": "Mykolayiv"},
                {"label": "Odessa", "value": "Odessa"},
                {"label": "Poltava", "value": "Poltava"},
                {"label": "Rivne", "value": "Rivne"},
                {"label": "Sevastopol'", "value": "Sevastopol'"},
                {"label": "Sumy", "value": "Sumy"},
                {"label": "Ternopil'", "value": "Ternopil'"},
                {"label": "Transcarpathia", "value": "Transcarpathia"},
                {"label": "Vinnytsya", "value": "Vinnytsya"},
                {"label": "Volyn", "value": "Volyn"},
                {"label": "Zaporizhzhya", "value": "Zaporizhzhya"},
                {"label": "Zhytomyr", "value": "Zhytomyr"}], 
            "key": 'Area', 
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'year_range', 
            "key": 'year_range', 
            "value": "1985-1988",
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'weeks_range', 
            "key": 'week_range', 
            "value": "5-10",
            "action_id": "update_data"
        }
    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]
    
    tabs = ["Plot", "Table"]


    outputs = [
        {
            "type":"plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type":"table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        start_week, end_week = map(int, params['week_range'].split('-'))
        start_year, end_year = map(int, params['year_range'].split('-'))
        plot_data = df[(df["area"] == params['Area']) & 
                       (df["Year"].between(start_year, end_year))][["Year", "Week", params['ticker']]]
        plot_data = plot_data[~((plot_data['Year'] == start_year) & (plot_data['Week'] < start_week))]
        plot_data = plot_data[~((plot_data['Year'] == end_year) & (plot_data['Week'] > end_week))]
        print(plot_data)
        print(plot_data.columns)
        plot_data['Date'] = pd.to_datetime(plot_data['Year'].astype(str) + plot_data['Week'].astype(str) + '0', format='%Y%W%w')
        plot_data = plot_data.drop(['Year', 'Week'], axis=1)
        return plot_data

    def getPlot(self, params):
        selected_column = params['ticker']
        plot_data = self.getData(params)
        plot = plot_data.plot(x='Date', y=selected_column)
        fig = plot.get_figure()
        return fig

    



    
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
    df["Week"] = df["Week"].astype(int)
    main_df = pd.concat([main_df, df])
  return main_df

def change_area(df):
  names =  {1: "Cherkasy", 2: "Chernihiv", 3: "Chernivtsi", 4: "Crimea", 5: "Dnipropetrovs'k", 6: "Donets'k", 7: "Ivano-Frankivs'k", 8: "Kharkiv", 9: "Kherson", 10: "Khmel'nyts'kyy", 11: "Kiev", 12: "Kiev City", 13: "Kirovohrad", 14: "Luhans'k", 15: "L'viv", 16: "Mykolayiv", 17: "Odessa", 18: "Poltava", 19: "Rivne", 20: "Sevastopol'", 21: "Sumy", 22: "Ternopil'", 23: "Transcarpathia", 24: "Vinnytsya", 25: "Volyn", 26: "Zaporizhzhya", 27: "Zhytomyr"}
  for name in names:
    df["area"].replace({name:names[name]}, inplace = True)
  return df

df = change_area(extract(directory))
print(df)
app = StockExample()
app.launch()
