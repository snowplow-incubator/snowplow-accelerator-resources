import urllib.request
import json


def data_by_country(df):
    url = urllib.request.urlopen("http://country.io/iso3.json")
    country_codes = json.loads(url.read().decode())
    countries = df.groupby(["geo_country"], as_index=False).sum()

    countries["iso_3"] = countries["geo_country"].map(country_codes)

    return countries
