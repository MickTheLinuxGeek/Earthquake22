# from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import plotly.express as px

if __name__ == "__main__":
    # South Carolina Zip codes
    # url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/sc_south_carolina_zip_codes_geo.min.json'

    sc_zipcode_file = r"./data/sc_south_carolina_zip_codes_geo.min.json"
    with open(sc_zipcode_file) as fin:
        sc_zip_json = json.load(fin)

    # with urlopen(url) as response:
    #     sc_zip_json = json.load(response)

    zip_code = []
    for i in range(len(sc_zip_json['features'])):
        code = sc_zip_json['features'][i]['properties']['ZCTA5CE10']
        zip_code.append(code)

    df = pd.DataFrame({'zip_code': zip_code, 'value': np.random.randint(0, 30, len(sc_zip_json['features']))})
    df['zip_code'] = df['zip_code'].astype(str)

    fig = px.choropleth(df,
                        geojson=sc_zip_json,
                        locations='zip_code',
                        featureidkey="properties.ZCTA5CE10",
                        color='value',
                        color_continuous_scale="blues",
                        projection="mercator",
                        )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.show()
