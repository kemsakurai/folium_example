# -*- coding: utf-8 -
import folium
import pandas as pd
import json


def main():

    # 東京都港区芝公園を設定
    tokyo23_location = [35.658593, 139.745441]
    m = folium.Map(location=tokyo23_location,
                   tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}.png',
                   attr='OpenStreetMap',
                   zoom_start=11)

    f = open(r'in/tokyo23.json')
    data = json.load(f)
    f.close()

    # --------------------------------------------------
    # CSVデータの読み込み、データを加工
    # ------------------------------------
    df = pd.read_csv('in/koen.csv')
    # カラムを再設定
    df.columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ"]
    # 列Aをint型に変換
    df['A'] = df['A'].fillna(0).astype(int)
    # 23区の地域コードに合致する列のみを抽出
    df = df[df['A'].isin([13101, 13102, 13103, 13104, 13105, 13106, 13107, 13108, 13109, 13110,
                          13111, 13112, 13113, 13114, 13115, 13116, 13117, 13118, 13119, 13120, 13121, 13122, 13123])]

    # 列、A を文字列に変換 (これをやらないと、数値側と文字列の突き合わせになり、マッピングができない。)
    df['A'] = df['A'].astype('str')

    # --------------------------------------------------
    # コロプレス図を描画
    # ------------------------------------
    m.choropleth(geo_data=data, data=df,
                 columns=['A', 'AH'],
                 key_on='feature.id',
                 fill_color='YlGn',
                 threshold_scale=[0.9, 3.5, 7, 10, 15, 27],
                 line_opacity=0.5,
                 reset=True)

    # 地図をhtml形式で出力
    m.save(outfile="out/choropleth_map.html")

if __name__ == "__main__":
    main()
