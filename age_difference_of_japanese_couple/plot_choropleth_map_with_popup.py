# -*- coding: utf-8 -
import folium
import pandas as pd
import json

area_la_lo_dict = {1: {"La": 43.06417, "Lo": 141.34694},
                   2: {"La": 40.82444, "Lo": 140.74},
                   3: {"La": 39.70361, "Lo": 141.1525},
                   4: {"La": 38.26889, "Lo": 140.87194},
                   5: {"La": 39.71861, "Lo": 140.1025},
                   6: {"La": 38.24056, "Lo": 140.36333},
                   7: {"La": 37.75, "Lo": 140.46778},
                   8: {"La": 36.34139, "Lo": 140.44667},
                   9: {"La": 36.56583, "Lo": 139.88361},
                   10: {"La": 36.39111, "Lo": 139.06083},
                   11: {"La": 35.85694, "Lo": 139.64889},
                   12: {"La": 35.60472, "Lo": 140.12333},
                   13: {"La": 35.68944, "Lo": 139.69167},
                   14: {"La": 35.44778, "Lo": 139.6425},
                   15: {"La": 37.90222, "Lo": 139.02361},
                   16: {"La": 36.69528, "Lo": 137.21139},
                   17: {"La": 36.59444, "Lo": 136.62556},
                   18: {"La": 36.06528, "Lo": 136.22194},
                   19: {"La": 35.66389, "Lo": 138.56833},
                   20: {"La": 36.65139, "Lo": 138.18111},
                   21: {"La": 35.39111, "Lo": 136.72222},
                   22: {"La": 34.97694, "Lo": 138.38306},
                   23: {"La": 35.18028, "Lo": 136.90667},
                   24: {"La": 34.73028, "Lo": 136.50861},
                   25: {"La": 35.00444, "Lo": 135.86833},
                   26: {"La": 35.02139, "Lo": 135.75556},
                   27: {"La": 34.68639, "Lo": 135.52},
                   28: {"La": 34.69139, "Lo": 135.18306},
                   29: {"La": 34.68528, "Lo": 135.83278},
                   30: {"La": 34.22611, "Lo": 135.1675},
                   31: {"La": 35.50361, "Lo": 134.23833},
                   32: {"La": 35.47222, "Lo": 133.05056},
                   33: {"La": 34.66167, "Lo": 133.935},
                   34: {"La": 34.39639, "Lo": 132.45944},
                   35: {"La": 34.18583, "Lo": 131.47139},
                   36: {"La": 34.06583, "Lo": 134.55944},
                   37: {"La": 34.34028, "Lo": 134.04333},
                   38: {"La": 33.84167, "Lo": 132.76611},
                   39: {"La": 33.55972, "Lo": 133.53111},
                   40: {"La": 33.60639, "Lo": 130.41806},
                   41: {"La": 33.24944, "Lo": 130.29889},
                   42: {"La": 32.74472, "Lo": 129.87361},
                   43: {"La": 32.78972, "Lo": 130.74167},
                   44: {"La": 33.23806, "Lo": 131.6125},
                   45: {"La": 31.91111, "Lo": 131.42389},
                   46: {"La": 31.56028, "Lo": 130.55806},
                   47: {"La": 26.2125, "Lo": 127.68111}, }


def main():

    # 地図の基準として兵庫県明石市を設定
    japan_location = [35, 135]
    m = folium.Map(location=japan_location, zoom_start=5)
    f = open(r'japan.geojson')
    data = json.load(f)
    f.close()

    # CSVデータの読み込み
    df = pd.read_csv('fuhu_seikei.csv')

    for feature in data['features']:
        #------------------------------------
        # [Custom icons in folium](https://ocefpaf.github.io/python4oceanographers/blog/2015/11/02/icons/)
        # を見る限り、Multipoligon に対して、Popupの設定はできない? 中心点にポップアップをおければよさそう
        # なので、県庁所在地に試しにプロットしてみる
        #------------------------------------
        area_cd = feature["properties"]["id"]
        lon, lat = area_la_lo_dict.get(area_cd).get(
            "Lo"), area_la_lo_dict.get(area_cd).get("La")
        row = df[df["Area Code"] == area_cd]
        value = row["Ave"]
        popup = u"年齢差:" + str(float(value)) + u":歳"

        # ポリゴンマーカを付与する
        # folium.RegularPolygonMarker(location=[lat, lon], popup=popup,
        # fill_color='#132b5e', number_of_sides=3, radius=10).add_to(m)
        
        # サークルマーカーを付与する
        # folium.CircleMarker(location=[lat, lon], radius=10,
        #             popup=popup, color='#3186cc',
        #             fill_color='#3186cc').add_to(m)

        # マーカーを付与する
        marker = folium.map.Marker([lat, lon], popup=folium.map.Popup(
            popup), icon=folium.Icon(color='blue', icon='comment'))
        
        # add_to(m) ではなく、mapにadd_childもできる    
        m.add_child(marker)
        
    m.choropleth(geo_data=data, data=df,
                 columns=['Area Code', 'Ave'],
                 key_on='feature.properties.id',
                 threshold_scale=[2.2, 2.3, 2.4, 2.5, 2.6, 2.7],
                 fill_color='YlOrRd', reset=True)

    # 地図をhtml形式で出力
    m.save(outfile="map_choropleth_with_popup.html")

if __name__ == "__main__":
    main()
