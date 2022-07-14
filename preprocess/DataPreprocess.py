"""
Data Preprocess

Combine several metro data and COVID daily cases into one nd.array

Version: 2022-03-20
Author: Quan-En, Li
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from utils import utils

metro_data_path = [
    "../data/original_metro_data/臺北捷運每日分時各站OD流量統計資料_" + str(year) + "{:02d}".format(month) + ".csv"
    for year in [2020, 2021] for month in range(1, 13)
][:-7]


def main():

    metro_data_list = [
        utils.read_metro_data(sub_path)
        for sub_path in tqdm(metro_data_path)
    ]

    metro_data = pd.concat(metro_data_list)

    del metro_data_list

    covid_data = utils.read_covid_case_data("../data/original_covid_data/covidtable_taiwan_cdc4_all.csv")

    for day in tqdm(range(7)):

        if day == 0:
            all_data = pd.merge(
                metro_data, covid_data, how="left", 
                left_on=["lag_"+str(day+1)], right_index=True,
            ).fillna(0)
        else:
            all_data = pd.merge(
                all_data, covid_data, how="left",
                left_on=["lag_" + str(day+1)], right_index=True,
            ).fillna(0)
        
        # v1: Taipei city, v2: New Taipei city, v3: Other city, v4: Imported
        all_data.columns = list(all_data.columns[:-4]) + ["lag_"+str(day+1)+"_v" + str(i+1) for i in range(4)]
    
    # Keep number, drop merge key
    all_data = all_data[list(all_data.columns)[0:4] + list(all_data.columns)[11:]]

    # Save csv
    all_data.to_csv("../data/all_metro_covid_data_202001_202105.csv", index=False)

    
    uniq_time = all_data["time"].unique()

    X = [
        all_data.loc[all_data["time"] == sub_time, list(all_data.columns)[2:]].to_numpy()
        for sub_time in tqdm(uniq_time)
    ]
    X_array = np.array(X)

    np.save('../data/TMCOVID/In_Out_Flow_202001_to_202105', X_array)
    np.save('../data/TM/In_Out_Flow_202001_to_202105', X_array[:,:,:2])

if __name__ == "__main__":
    main()