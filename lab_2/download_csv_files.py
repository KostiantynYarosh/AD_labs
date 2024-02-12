import os
import urllib.request
from datetime import datetime

save_directory = 'D:\Desktop\KPI\Kpi_2023\sem_2\AD\lab2\csv_files'

def download(id):
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={id}&year1=1981&year2=2024&type=Mean"
    vhi_url = urllib.request.urlopen(url)

    file_name = os.path.join(save_directory, f'vhi_id_{id}_{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.csv')

    print(vhi_url)
    with open(file_name, 'wb') as out:
        print('writing data')
        out.write(vhi_url.read())

    print(f"{id} VHI is downloaded...")


for i in range(1, 28):
    download(i)
