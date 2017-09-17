# -*- coding: utf-8 -
import folium


def main():

    # 東京都港区芝公園を設定
    tokyo23_location = [35.658593, 139.745441]
    m = folium.Map(location=tokyo23_location,
                   tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}.png',
                   attr='OpenStreetMap',
                   zoom_start=11)
    geojson = r'in/tokyo23.json'
    # geojson読み込み
    m.choropleth(geo_data=geojson)
    # 地図をhtml形式で出力
    m.save(outfile="out/map.html")

if __name__ == "__main__":
    main()
