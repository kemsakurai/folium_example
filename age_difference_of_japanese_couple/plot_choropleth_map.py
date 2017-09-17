# -*- coding: utf-8 -
import folium
import pandas as pd
import json


def main():

    # 地図の基準として兵庫県明石市を設定
    japan_location = [35, 135]
    m = folium.Map(location=japan_location, zoom_start=5)
    f = open(r'japan.geojson')
    data = json.load(f)
    f.close()

    # CSVデータの読み込み
    df = pd.read_csv('fuhu_seikei.csv')

    for feature in data["features"]:
        row = df[df["Area Code"] == feature["properties"]["id"]]
        value = row["Ave"]
        # `popupContent` を設定すると、popupContentが出力されそうだが、MultiPoligonだと出力されない。やり方が間違ってるのかもしれない。
        feature["properties"]["popupContent"] = u"年齢差:" + \
            str(float(value)) + u":歳"

    m.choropleth(geo_data=data, data=df,
                 columns=['Area Code', 'Ave'],
                 key_on='feature.properties.id',
                 threshold_scale=[2.2, 2.3, 2.4, 2.5, 2.6, 2.7],
                 fill_color='YlGnBu', reset=True)

    # 地図をhtml形式で出力
    m.save(outfile="choropleth_map.html")

if __name__ == "__main__":
    main()
