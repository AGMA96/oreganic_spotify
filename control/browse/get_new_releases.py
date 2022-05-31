countries = ("AD",    "AE",    "AG",    "AL",    "AM",    "AO",    "AR",    "AT",    "AU",    "AZ",
    "BA",    "BB",    "BD",    "BE",    "BF",    "BG",    "BH",    "BI",    "BJ",    "BN",    "BO",
    "BR",    "BS",    "BT",    "BW",    "BY",    "BZ",
    "CA",    "CD",    "CG",    "CH",    "CI",    "CL",    "CM",    "CO",    "CR",    "CV",    "CW",
    "CY",    "CZ",    "DE",
    "DJ",    "DK",    "DM",    "DO",    "DZ",
    "EC",    "EE",    "EG",    "ES",
    "FI",    "FJ",    "FM",    "FR",
    "GA",    "GB",    "GD",    "GE",    "GH",    "GM",    "GN",    "GQ",    "GR",    "GT",    "GW",
    "GY",
    "HK",    "HN",    "HR",    "HT",    "HU",
    "ID",    "IE",    "IL",    "IN",    "IQ",    "IS",    "IT",
    "JM",    "JO",    "JP",
    "KE",    "KG",    "KH",    "KI",    "KM",    "KN",    "KR",    "KW",    "KZ",
    "LA",    "LB",    "LC",    "LI",    "LK",    "LR",    "LS",    "LT",    "LU",    "LV",    "LY",
    "MA",    "MC",    "MD",    "ME",    "MG",    "MH",    "MK",    "ML",    "MN",    "MO",    "MR",
    "MT",    "MU",    "MV",    "MW",    "MX",    "MY",    "MZ",
    "NA",    "NE",    "NG",    "NI",    "NL",    "NO",    "NP",    "NR",    "NZ",
    "OM",
    "PA",    "PE",    "PG",    "PH",    "PK",    "PL",    "PS",    "PT",    "PW",    "PY",
    "QA",
    "RO",    "RS",    "RU",    "RW",
    "SA",    "SB",    "SC",    "SE",    "SG",    "SI",    "SK",    "SL",    "SM",    "SN",    "SR",
    "ST",    "SV",    "SZ",
    "TD",    "TG",    "TH",    "TJ",    "TL",    "TN",    "TO",    "TR",    "TT",    "TV",    "TW",
    "TZ",
    "UA",    "UG",    "US",    "UY",    "UZ",
    "VC",    "VE",    "VN",    "VU",
    "WS",
    "XK",
    "ZA",    "ZM",    "ZW",
)

import json
import os
import time

from oreganic_spotify.generate import formatter

from control.client import HeadlessAuth

today = formatter.generate_formated_date()
os.makedirs(os.path.join(os.getcwd(), 'jsons', 'Browse', 'GetNewReleases', today), exist_ok=True)

sp = HeadlessAuth().create_spotipy_client()

for country in countries:
    for offset in (0,50):
        new_releases = sp.new_releases(country=country, limit=50, offset=offset)

        with open(os.path.join(os.getcwd(), 'jsons', 'Browse', 'GetNewReleases', today, country + '_{:02d}.json'.format(offset)), 'w', encoding='utf-8') as new_releases_file:
            json.dump(new_releases, new_releases_file, indent=4, ensure_ascii=False)

        time.sleep(1)

    


