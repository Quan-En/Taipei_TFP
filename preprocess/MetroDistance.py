
"""
Convert station names to indices
(metro_distance.csv -> distance.csv)

Data Source: 
    - metro_distance.csv: http://data.but.tw/trtc/price.html
    
Version: 2022-03-22
Author: Quan-En, Li
"""


import numpy as np
import pandas as pd

def main():
    distance_df = pd.read_csv("../data/metro_distance.csv", encoding='big5')

    # Convert stations name to idx

    values_from, indices_from = np.unique(distance_df["from"], return_inverse=True)
    values_to, indices_to = np.unique(distance_df["to"], return_inverse=True)

    distance_df["from"] = indices_from
    distance_df["to"] = indices_to


    # Avoid "0" distance
    distance_df["distance"] = distance_df["distance"] + 0.01 * (distance_df["distance"] == 0)

    # Save distance.csv
    distance_df.to_csv("../data/TM/distance.csv", index=False)
    distance_df.to_csv("../data/TMCOVID/distance.csv", index=False)

if __name__ == "__main__":
    main()