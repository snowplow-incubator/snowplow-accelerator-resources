import urllib.request
import json


def data_by_country(df):
    url = urllib.request.urlopen("http://country.io/iso3.json")
    country_codes = json.loads(url.read().decode())
    countries = df.groupby(["GEO_COUNTRY"], as_index=False).sum()

    countries["ISO_3"] = countries["GEO_COUNTRY"].map(country_codes)

    return countries
