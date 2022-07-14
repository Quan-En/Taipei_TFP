

import pandas as pd

wiki_url = "https://zh.wikipedia.org/wiki/"

Rline_url = wiki_url + "Template:%E5%8F%B0%E5%8C%97%E6%8D%B7%E9%81%8B%E8%BB%8A%E7%AB%99%E5%88%97%E8%A1%A8/%E6%B7%A1%E6%B0%B4%E4%BF%A1%E7%BE%A9%E7%B7%9A"
BRline_url = wiki_url + "Template:%E5%8F%B0%E5%8C%97%E6%8D%B7%E9%81%8B%E8%BB%8A%E7%AB%99%E5%88%97%E8%A1%A8/%E6%96%87%E6%B9%96%E7%B7%9A"
Gline_url = wiki_url + "Template:%E5%8F%B0%E5%8C%97%E6%8D%B7%E9%81%8B%E8%BB%8A%E7%AB%99%E5%88%97%E8%A1%A8/%E6%9D%BE%E5%B1%B1%E6%96%B0%E5%BA%97%E7%B7%9A"
Oline_url = wiki_url + "Template:%E5%8F%B0%E5%8C%97%E6%8D%B7%E9%81%8B%E8%BB%8A%E7%AB%99%E5%88%97%E8%A1%A8/%E4%B8%AD%E5%92%8C%E6%96%B0%E8%98%86%E7%B7%9A"
BLline_url = wiki_url + "Template:%E5%8F%B0%E5%8C%97%E6%8D%B7%E9%81%8B%E8%BB%8A%E7%AB%99%E5%88%97%E8%A1%A8/%E6%9D%BF%E5%8D%97%E7%B7%9A"
Yline_url = wiki_url + "Template:%E5%8F%B0%E5%8C%97%E6%8D%B7%E9%81%8B%E8%BB%8A%E7%AB%99%E5%88%97%E8%A1%A8/%E7%92%B0%E7%8B%80%E7%B7%9A"

def main():
    
    R = pd.read_html(Rline_url)
    R = R[0][['車站名稱', '所在地.1']][1:]
    R.columns = ['車站名稱', '行政區']

    BR = pd.read_html(BRline_url)
    BR = BR[0][['車站名稱（車站顏色[a]）.1', '所在地.1']][1:]
    BR.columns = ['車站名稱', '行政區']

    G = pd.read_html(Gline_url)
    G = G[0][['車站名稱', '所在地.1']][1:]
    G.columns = ['車站名稱', '行政區']

    O = pd.read_html(Oline_url)
    O = O[0][['車站名稱', '所在地.1']][1:]
    O.columns = ['車站名稱', '行政區']

    BL = pd.read_html(BLline_url)
    BL = BL[0][['車站名稱', '所在地.1']][1:]
    BL.columns = ['車站名稱', '行政區']

    Y = pd.read_html(Yline_url)
    Y = Y[1][['車站名稱', '所在地.1']][1:]
    Y.columns = ['車站名稱', '行政區']



    all_station_location = pd.concat([R, BR, G, O, BL, Y])

    # Split two district

    ## Copy
    all_station_location.columns = ['車站名稱', '行政區_1']
    all_station_location['行政區_2'] = all_station_location['行政區_1']

    ## Split
    for i in range(len(all_station_location)):
        if len(str(all_station_location.iloc[i,1])) > 3:
            all_station_location.iloc[i,1] = all_station_location.iloc[i,1][:3]
            all_station_location.iloc[i,2] = all_station_location.iloc[i,2][3:]

    # Delete duplicates
    all_station_location = all_station_location.drop_duplicates()

    all_station_location.to_csv("../data/metro_location.csv", index=False)

    
if __name__ == "__main__":
    main()