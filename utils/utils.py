

import pandas as pd


def read_metro_data(data_path):
    # Read raw data
    raw_data = pd.read_csv(data_path)

    # Input/Output flow
    input_flow = raw_data.groupby(["日期", "時段", "進站"], as_index=False).sum()
    output_flow = raw_data.groupby(["日期", "時段", "出站"], as_index=False).sum()

    # Rename
    input_flow.columns = ["day", "hour", "station", "input_flow"]
    output_flow.columns = ["day", "hour", "station", "output_flow"]

    # Merge two DataFrame(input flow, output flow)
    all_data = input_flow.merge(output_flow, how="outer", on=["day", "hour", "station"])

    # Reformat time
    all_data["day"] = pd.to_datetime(all_data["day"])
    all_data["time"] = all_data["day"] + pd.to_timedelta(all_data["hour"], unit="h")

    # Rename
    all_data = all_data[["time", "station", "input_flow", "output_flow"]]
    all_data = all_data.sort_values(by=["time", "station"]).reset_index(drop=True)

    # Different i lag-day
    for i in range(7): all_data["lag_"+str(i+1)] = (all_data["time"] - pd.DateOffset(days=i+1)).dt.strftime("%Y/%m/%d")

    return all_data

def read_covid_case_data(data_path="covidtable_taiwan_cdc4_all.csv"):

    # Read data
    all_covid_data = pd.read_csv(data_path)

    # Select columns
    all_covid_data = all_covid_data[['日期', '縣市別', '區域', '新增確診人數']]

    # Reformat time
    all_covid_data.loc[:,'日期'] = pd.to_datetime(all_covid_data['日期']).dt.strftime("%Y/%m/%d")

    # Rename
    all_covid_data.columns = ['announce_day', '縣市別','區域', '新增確診人數']

    # Reformat data
    all_covid_data.loc[~all_covid_data['縣市別'].isin(['境外移入','台北市','新北市']), '縣市別'] = '其他縣市'    
    all_covid_data = all_covid_data.groupby(['announce_day', '縣市別'], as_index=False).sum()

    all_covid_data = all_covid_data.pivot(index='announce_day', columns='縣市別', values='新增確診人數').fillna(0)

    for area_type in ['台北市', '新北市', '其他縣市', '境外移入']:
        if area_type not in all_covid_data.columns: all_covid_data[area_type] = 0
    
    all_covid_data = all_covid_data[['台北市', '新北市', '其他縣市', '境外移入']]
    return all_covid_data