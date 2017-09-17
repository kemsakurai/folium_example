# -*- coding: utf-8 -
import folium
import pandas as pd
import json


def main():

    # --------------------------------------------------
    # Mapの準備
    # ------------------------------------
    # 東京都港区芝公園を設定
    tokyo23_location = [35.658593, 139.745441]
    m = folium.Map(location=tokyo23_location,
                   tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}.png',
                   attr='OpenStreetMap',
                   zoom_start=11)

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
    f = open(r'in/tokyo23.json')
    data = json.load(f)
    f.close()

    m.choropleth(geo_data=data, data=df,
                 columns=['A', 'AF'],
                 key_on='feature.id',
                 fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.3,
                 threshold_scale=[50, 150, 300, 400, 500, 600],
                 reset=True)

    # 区の中央部の経度緯度をgeojsonから計算
    city_center = __calulate_city_center(data)

    # popupを付与する
    for k, v in city_center.items():
        city_name = df.loc[(df['A'] == k), 'B'].values[0]
        poput_text = u"区の名前:" + city_name.decode('utf-8') + "<br/>"
        square_meter = df.loc[(df['A'] == k), 'AH'].values[0]
        poput_text = poput_text + u"区の人口一人当たりの公園面積:" + \
            str(square_meter) + " " + "m2" + "<br/>"
        park_count = df.loc[(df['A'] == k), 'AF'].values[0]
        poput_text = poput_text + u"区の総公園数:" + str(park_count)

        folium.features.Circle(
            radius=60 * square_meter,
            location=[v.get("latitude"), v.get("longitude")],
            popup=poput_text,
            color='green',
            fill_opacity=0.6, line_opacity=1,
            fill=True,
            fill_color='green'
        ).add_to(m)

    # 地図をhtml形式で出力
    m.save(outfile="out/choropleth_map_with_popup.html")


def __calulate_city_center(data):
    import numpy as np
    # 結果を収集する辞書
    result_dict = {}
    for feature in data.get("features"):
        feature_id = feature.get("id")
        row_element = result_dict.get(feature_id)
        if row_element is None:
            row_element = {}
        count = row_element.get("count")
        sum_result = row_element.get("sum_result")
        if count is None:
            count = 0
        if sum_result is None:
            sum_result = np.array([0, 0])
        for coordinate in feature.get("geometry").get("coordinates"):
            A = np.array(coordinate)
            row_sum = np.sum(A, axis=0)
            sum_result = sum_result + row_sum
            count = count + len(coordinate)
        result_dict.update(
            {feature_id: {"count": count, "sum_result": sum_result}})

    for k, v in result_dict.items():
        avg = v.get("sum_result") / v.get("count")
        result_dict.update({k: {"longitude": avg[0], "latitude": avg[1]}})

    return result_dict

if __name__ == "__main__":
    main()
