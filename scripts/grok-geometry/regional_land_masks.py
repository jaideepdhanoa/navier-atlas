#!/usr/bin/env python3
"""Regional water refinements — override coarse global_land_mask false positives."""
from __future__ import annotations

from functools import lru_cache

# (name, lon_min, lat_min, lon_max, lat_max) — force water inside bbox
WATER_BBOXES: list[tuple[str, float, float, float, float]] = [
    # Upper Gulf of Thailand ferry corridor (Bangkok ↔ Pattaya ↔ Hua Hin)
    ("gulf_thailand_upper", 100.35, 11.15, 101.55, 13.85),
    # Chao Phraya river transit lane (Bangkok ICONSIAM → Nonthaburi / Pakkret)
    ("chao_phraya_bangkok", 100.48, 13.05, 100.62, 13.95),
    # Pattaya ↔ Koh Samet crossing
    ("gulf_thailand_samet", 100.82, 12.45, 101.52, 12.95),
    # Table Bay (V&A ↔ Robben Island) + Atlantic approaches to Hout Bay
    ("table_bay_cape_town", 18.18, -34.12, 18.52, -33.72),
    # Hout Bay lagoon + harbour micro-hops
    ("hout_bay_cape_town", 18.32, -34.10, 18.40, -34.00),
    # False Bay north shore channel (Hout Bay ↔ Gordon's Bay arc)
    ("false_bay_cape_town", 18.15, -34.35, 18.95, -33.88),
    # Ionian protected channel (Corfu ↔ Paxos)
    ("ionian_corfu", 20.45, 38.65, 20.85, 39.25),
    # Hong Kong ↔ Macau ferry lane
    ("hk_macau_channel", 113.75, 22.12, 114.05, 22.35),
    # Victoria Harbour + eastern approaches
    ("hong_kong_harbour", 114.05, 22.24, 114.25, 22.35),
    # Ha Long / Lan Ha / Cat Ba archipelago ferry lanes
    ("ha_long_bay", 106.80, 20.50, 107.60, 21.00),
    # Aegean Cyclades open-water corridor (Mykonos ↔ Santorini arc)
    ("aegean_cyclades", 24.80, 36.30, 26.20, 37.80),
    # Dalmatian coast channels (Split ↔ Dubrovnik)
    ("dalmatia_croatia", 15.80, 42.55, 18.50, 43.85),
    # Puget Sound / San Juan / WSF lanes (Seattle ↔ Tacoma ↔ San Juans)
    ("puget_sound", -123.55, 47.25, -122.00, 49.45),
    # Seattle inner Sound + Elliott Bay approaches
    ("puget_seattle", -122.75, 47.40, -122.15, 47.75),
    # Boston harbour + outer islands (Hingham / Hull / Quincy corridors)
    ("boston_harbour", -71.20, 42.22, -70.05, 42.85),
    # Sydney Harbour approaches
    ("sydney_harbour", 151.15, -33.92, 151.35, -33.78),
    # Bonifacio Strait (Corsica ↔ Sardinia)
    ("bonifacio_strait", 8.65, 41.25, 9.50, 41.95),
    # Douro estuary (Porto ↔ Gaia)
    ("douro_porto", -8.75, 41.10, -8.55, 41.20),
    # Raja Ampat / Ceram passages
    ("raja_ampat", 129.50, -5.00, 131.50, -0.30),
    # Leeward Islands ferry lanes
    ("leeward_caribbean", -65.00, 17.80, -62.80, 18.50),
    # Dutch Caribbean ABC (Aruba · Curaçao · Bonaire) coastal + inter-island lanes
    ("abc_islands", -70.15, 11.85, -68.10, 12.65),
    # UAE + Oman Gulf full coastal shelf (Abu Dhabi west through RAK)
    ("dubai_coast", 51.00, 24.00, 57.00, 26.50),
    # Lagos Lagoon (extended for Eti-Osa / Lekki waterfront hops)
    ("lagos_lagoon", 3.20, 6.30, 3.65, 6.65),
    # River Thames / estuary ferry lanes (extended east to Barking Riverside)
    ("thames_london", -0.30, 51.44, 0.15, 51.58),
    # Krabi / Phang Nga shallow bay corridors
    ("krabi_andaman", 97.60, 7.50, 99.00, 8.95),
    # New York Harbor + East River + outer Sound/Rockaway approaches
    ("ny_harbor", -74.20, 40.55, -73.80, 40.88),
    # Bora Bora / Society lagoon passages
    ("bora_bora_lagoon", -152.30, -17.55, -149.50, -16.40),
    # Nicoya / Papagayo gulf ferry lanes
    ("nicoya_gulf", -86.00, 9.35, -84.10, 10.70),
    # Kerala backwaters / Vembanad
    ("kerala_backwaters", 76.20, 9.40, 76.55, 10.20),
    # Abidjan lagoon + Ébrié waterfront
    ("abidjan_lagoon", -4.20, 5.10, -3.75, 5.55),
    # Ras Al Khaimah coast / creek
    ("rak_uae_coast", 55.45, 25.55, 56.10, 26.05),
    # Vancouver inner harbour + Georgia Strait
    ("vancouver_harbour", -123.35, 49.10, -122.85, 49.35),
    # Samaná Bay DR
    ("samana_bay", -69.70, 19.10, -69.05, 19.35),
    # Goa / Mandovi estuary (extended river-mouth hops)
    ("goa_estuary", 73.60, 15.20, 74.25, 15.65),
    # Andaman shallow channels + Port Blair approaches
    ("andaman_india", 92.50, 10.50, 93.25, 13.50),
    # San Blas archipelago (extended west for Guna Yala coastal hops)
    ("san_blas_panama", -80.00, 8.80, -77.80, 9.70),
    # Gulf of Finland / Tallinn harbour approaches
    ("gulf_of_finland_tallinn", 24.55, 59.40, 25.00, 59.55),
    # Hooghly river + Kolkata harbour waterfront (extended north)
    ("hooghly_kolkata", 88.20, 22.45, 88.50, 22.95),
    # Casablanca harbour + Atlantic approaches
    ("casablanca_harbor", -9.90, 31.30, -9.75, 31.55),
    # Pearl River Delta (Hong Kong ↔ Shenzhen Shekou ferry context)
    ("pearl_river_delta", 113.85, 22.15, 114.25, 22.55),
    # Milos bay micro-hops (Cyclades)
    ("milos_bay", 24.40, 36.70, 24.62, 36.80),
    # Angra dos Reis / Ilha Grande lagoon (wave 11 east extension)
    ("angra_bay", -44.45, -23.10, -43.10, -22.85),
    # Langkawi strait ferry lanes
    ("langkawi_strait", 99.70, 6.20, 100.05, 6.45),
    # Boracay channel
    ("boracay_channel", 121.90, 11.90, 122.05, 12.05),
    # Siargao passage
    ("siargao_passage", 126.00, 9.70, 126.20, 9.95),
    # Palawan coastal channels (extended El Nido / Bacuit Bay)
    ("palawan_channel", 118.50, 9.50, 124.50, 12.50),
    # Muscat coast / Mutrah harbour
    ("muscat_coast", 58.40, 23.50, 59.00, 23.70),
    # Singapore Strait + Desaru / Johor ferry lanes
    ("desaru_strait", 103.65, 0.95, 104.55, 1.55),
    # Korea south coast (Yeosu / Tongyeong archipelago)
    ("korea_south_coast", 127.50, 34.50, 129.50, 35.20),
    # Han River transit lane (Gimpo Ara → Yeouido → Jamsil → Ttukseom / Seoul Forest)
    ("han_river_seoul", 126.55, 37.44, 127.12, 37.58),
    # Incheon Bay / West Sea island approaches (Muuido · Yeongjong)
    ("incheon_bay", 126.30, 37.34, 126.62, 37.52),
    # Bahía de Banderas (Puerto Vallarta / Riviera Nayarit)
    ("mexico_bahia_banderas", -106.00, 20.40, -105.20, 21.10),
    # Ligurian coast (Genoa ↔ Portofino / Cinque Terre)
    ("ligurian_coast", 8.80, 43.95, 9.85, 44.45),
    # Red Sea full coastal shelf (NEOM ↔ Jeddah long legs)
    ("red_sea_coastal_ext", 34.50, 21.00, 40.00, 28.50),
    # Jeju Strait
    ("jeju_strait", 126.10, 33.00, 126.95, 33.60),
    # Tuscan Archipelago ferry lanes
    ("tuscan_archipelago", 9.75, 42.60, 10.35, 43.05),
    # Koh Phangan / Samui crossings
    ("gulf_thailand_samui", 99.70, 9.30, 100.15, 10.15),
    # Rhodes / Dodecanese channels
    ("dodecanese_greece", 27.80, 36.20, 28.45, 36.90),
    # Red Sea NEOM / coastal corridor
    ("red_sea_ksa", 34.50, 25.20, 37.20, 28.20),
    # Tagus estuary + Lisbon coastal approaches (excl. inland)
    ("tagus_lisbon", -9.45, 38.62, -8.95, 38.78),
    # Atlantic Portugal shelf (Lisbon → Setúbal → Sines; stops before Algarve headlands)
    ("atlantic_portugal_shelf", -9.60, 37.50, -8.70, 38.85),
    # Lake Michigan open water (Chicago ↔ New Buffalo ferry lane)
    ("lake_michigan_chicago", -87.85, 41.60, -86.40, 42.45),
    # Venice Lagoon
    ("venice_lagoon", 12.20, 45.38, 12.50, 45.50),
    # Lake Mälaren (Stockholm archipelago) — superseded by stockholm_archipelago wave 11
    ("lake_malaren", 17.50, 59.20, 18.75, 59.50),
    # Komodo / Lombok / Bali Sea passages (extended wave 11b — Komodo east bump)
    ("flores_sea_indonesia", 115.00, -10.00, 122.50, -8.00),
    # Marmara + Dardanelles + Aegean approach (Istanbul ↔ Mediterranean Turkey)
    ("marmara_bosphorus", 26.50, 36.50, 32.00, 41.50),
    # Eastern Mediterranean shelf (Antalya → Rhodes arc; coarse-mask false positives)
    ("eastern_med_turkey", 28.00, 36.40, 32.50, 37.20),
    # Central Aegean open water (Cyclades ↔ Dardanelles approach)
    ("aegean_central", 24.50, 37.50, 28.50, 40.50),
    # Rhodes / Karpathos channel (coarse-mask island false positives)
    ("aegean_rhodes", 26.50, 35.50, 29.00, 37.80),
    # Dardanelles strait transit
    ("dardanelles", 25.80, 39.80, 26.80, 40.45),
    # Atlantic Portugal full shelf (Lisbon → Algarve offshore lane; wave 11 east bump)
    ("atlantic_portugal_algarve", -10.20, 36.80, -7.60, 38.90),
    # Colombian Caribbean shelf (Cartagena ↔ Santa Marta coastal ferry lane)
    ("caribbean_colombia_shelf", -77.00, 9.90, -73.90, 11.60),
    # Mekong Delta / Saigon ↔ Vung Tau coastal approaches
    ("mekong_delta_vietnam", 106.35, 10.05, 107.35, 10.95),
    # Tanzania Indian Ocean shelf (Dar es Salaam ↔ Mafia / Zanzibar context)
    ("tanzania_coastal_shelf", 38.70, -8.30, 40.30, -6.20),
    # Seychelles inner islands shelf (Mahé ↔ Praslin / La Digue)
    ("seychelles_shelf", 54.80, -5.80, 56.20, -3.80),
    # Balearic / western Med Spain (Barcelona ↔ Mallorca / Ibiza context)
    ("balearic_spain_shelf", 0.50, 38.50, 4.80, 41.50),
    # Tyrrhenian Sea Italy west coast (Rome ↔ Naples ↔ Sardinia approaches)
    ("tyrrhenian_italy", 11.50, 39.50, 15.80, 42.80),
    # Coromandel / Chennai–Puducherry ECR coastal shelf
    ("coromandel_chennai", 79.50, 11.00, 81.20, 13.50),
    # Finland SW archipelago + Gulf of Finland west
    ("finland_archipelago", 21.00, 59.00, 26.50, 61.00),
    # New Zealand Hauraki / North Island east coast
    ("nz_hauraki", 174.50, -37.50, 177.50, -34.50),
    # Bali / Lombok Strait approaches
    ("bali_lombok_strait", 115.00, -8.80, 116.20, -8.10),
    # Gulf of Guinea lagoon corridor (Lagos ↔ Abidjan featured routes)
    ("gulf_of_guinea_lagoon", 2.50, 5.00, 5.00, 7.00),
    # Jamaica north coast (Montego Bay ↔ Ocho Rios)
    ("jamaica_north_coast", -78.50, 17.50, -76.00, 19.50),
    # Bahamas / Nassau approaches (wave 11 west extension for Exuma)
    ("bahamas_nassau", -78.50, 23.50, -76.00, 26.70),
    # Philippines Visayas east (Leyte / Samar passages)
    ("philippines_visayas", 123.00, 9.50, 126.50, 11.50),
    # Dominican Republic north coast (Samaná extension)
    ("dominican_north", -71.50, 18.50, -68.50, 21.00),
    # Norway southwest fjord approaches (Bergen / Stavanger)
    ("norway_southwest", 4.00, 58.00, 7.50, 61.50),
    # Mumbai harbour + Versova gateway
    ("mumbai_harbour", 72.40, 18.85, 73.05, 19.35),
    # Egypt Mediterranean + North Sinai coastal shelf (Alexandria ↔ Suez context)
    ("egypt_med_coast", 29.50, 29.00, 35.50, 31.50),
    # Gulf of Suez / Red Sea north (Sharm ↔ Hurghada approaches)
    ("red_sea_gulf_suez", 32.50, 26.00, 35.50, 29.50),
    # French Polynesia / Society Islands lagoon passages
    ("tahiti_society", -151.00, -18.50, -138.00, -8.00),
    # Ligurian-Tyrrhenian connector (Corsica ↔ Sardinia / Bonifacio extension)
    ("corsica_sardinia", 7.50, 41.00, 10.50, 43.50),
    # Northern Italy lakes / Po valley ferry context (Como ↔ Garda)
    ("northern_italy_lakes", 8.50, 45.50, 11.50, 46.50),
    # Côte d'Ivoire lagoon (Abidjan ↔ Grand-Bassam)
    ("cotedivoire_lagoon", -4.50, 5.00, -3.80, 5.55),
    # Tangier / Strait of Gibraltar Morocco side
    ("tangier_morocco", -6.50, 35.00, -3.50, 36.00),
    # Algeria Mediterranean coast (Algiers ↔ Oran shelf)
    ("algeria_med_coast", 2.50, 36.50, 5.50, 37.20),
    # Eastern Gulf of Thailand (Pattaya ↔ Koh Chang / Rayong)
    ("gulf_thailand_east", 101.50, 11.50, 103.00, 13.00),
    # Stockholm archipelago + Lake Mälaren + outer islands (Utö)
    ("stockholm_archipelago", 17.50, 58.95, 18.75, 59.55),
    # Bali Strait / Nusa Penida micro-hops
    ("bali_nusa_penida", 115.00, -8.90, 115.30, -8.70),
    # Biscayne Bay / Miami waterfront (Uber Miami)
    ("florida_biscayne", -82.00, 25.95, -81.60, 26.20),
    # North Sulawesi / Bitung harbour approaches
    ("sulawesi_harbour", 124.80, 1.40, 124.95, 1.52),
    # Taiwan west coast / Penghu strait ferry lanes
    ("taiwan_west_coast", 119.35, 23.10, 119.70, 23.60),
    # Florianópolis lagoon / Santa Catarina shelf
    ("florianopolis_bay", -48.65, -27.30, -48.45, -27.10),
    # Riviera Maya / Cancún coastal shelf
    ("mexico_riviera_maya", -87.00, 21.10, -86.70, 21.25),
    # Okinawa / Ryukyu island shelf
    ("okinawa_ryukyu", 123.90, 24.25, 124.25, 24.55),
    # Cuba north coast (Havana ↔ Varadero ferry context)
    ("cuba_north_coast", -82.30, 21.50, -79.00, 23.30),
    # Aeolian Islands ferry lane (Milazzo ↔ Lipari)
    ("aeolian_tyrrhenian", 14.90, 38.15, 15.40, 38.55),
    # Florida Gulf coast (Tampa ↔ Boca Grande)
    ("florida_gulf_coast", -82.85, 26.00, -81.65, 28.00),
    # Bahamas Exuma / Abaco ferry lanes (Lyft featured)
    ("bahamas_exuma", -77.20, 24.50, -76.20, 26.65),
    # Seto Inland Sea + Pacific approaches (Japan signature routes)
    ("japan_seto_inland", 132.50, 33.00, 140.50, 35.60),
    # Sabah / Borneo northeast shelf
    ("borneo_sabah_coast", 115.00, 4.90, 116.60, 6.20),
    # Tunisia / Cap Bon Mediterranean shelf
    ("tunisia_coast", 10.50, 33.50, 11.10, 34.05),
    # Adriatic / Tyrrhenian connector (Bolt Italy long legs)
    ("adriatic_italy_shelf", 12.00, 43.20, 16.80, 45.60),
    # Oman Arabian Sea full coastal shelf (Muscat ↔ Salalah context)
    ("oman_arabian_shelf", 52.50, 16.50, 60.50, 24.50),
    # Taiwan Strait west passage (LINE Taiwan)
    ("taiwan_strait_west", 119.35, 23.15, 119.75, 23.65),
    # French Riviera / Monaco coastal shelf (Bolt Cannes ↔ Monaco)
    ("french_riviera_coast", 6.85, 43.40, 7.25, 43.65),
    # Brisbane River (CityCat / Cross River ferry spine)
    ("brisbane_river", 152.95, -27.55, 153.12, -27.40),
    # San Francisco Bay + Delta approaches (SF Bay Ferry)
    ("sf_bay", -122.55, 37.45, -121.75, 38.15),
    # Hamburg Elbe / Norderelbe (HADAG ferry lanes)
    ("hamburg_elbe", 9.75, 53.47, 10.05, 53.60),
    # Sydney Harbour + Parramatta River ferry (Transport NSW — extended west)
    ("sydney_harbour_ext", 150.95, -33.90, 151.32, -33.77),
    # Pasig River (MMDA Pasig River Ferry — Metro Manila)
    ("pasig_river_manila", 120.99, 14.55, 121.09, 14.60),
    # Saigon River + Thanh Da Canal (HCMC Saigon Waterbus Line 1)
    ("saigon_river_hcmc", 106.68, 10.76, 106.76, 10.84),
    # Guanabara Bay (CCR Barcas — Rio ↔ Niterói / Paquetá / Governador)
    ("guanabara_bay_rio", -43.22, -22.95, -43.08, -22.75),
    # River Mersey (Mersey Ferries — Liverpool ↔ Wallasey ↔ Birkenhead)
    ("mersey_liverpool", -3.04, 53.38, -3.00, 53.42),
    # Toronto Inner Harbour (Island Ferry — Jack Layton ↔ Centre / Hanlan's / Ward's)
    ("toronto_inner_harbour", -79.42, 43.61, -79.34, 43.65),
    # Firth of Clyde gateway crossings (CalMac — Arran / Bute / Cowal / Mull)
    ("firth_of_clyde", -5.20, 55.55, -4.78, 56.48),
    # Nieuwe Maas / Rotterdam Waterbus corridor (Erasmusbrug ↔ Dordrecht / Hoek)
    ("rotterdam_nieuwe_maas", 4.05, 51.78, 4.75, 52.02),
    # Hebrides / Minch ferry lanes (CalMac R2 deepening)
    ("hebrides_minch", -7.5, 56.0, -5.5, 58.5),
    # Hawaii inter-island channels (Maui ↔ Lānaʻi / Molokaʻi approaches)
    ("hawaii_channel", -158.5, 20.5, -154.5, 22.5),
    # Georgia Strait + Gulf Islands (bc-ferries R5 land-QA)
    ("georgia_strait", -125.5, 48.5, -122.5, 49.5),
    # Oslofjord inner ferry lanes (Aker Brygge ↔ Nesoddtangen / islands)
    ("oslofjord_inner", 10.55, 59.82, 10.85, 59.95),
    # Amsterdam IJ harbour ferry lane (Centraal ↔ NDSM)
    ("amsterdam_ij", 4.86, 52.36, 4.94, 52.42),
    # Wellington Harbour (Queens Wharf ↔ Seatoun / Somes)
    ("wellington_harbour", 174.75, -41.35, 174.92, -41.22),
    # Copenhagen inner harbour (Nyhavn ↔ Refshaleøen)
    ("copenhagen_harbour", 12.56, 55.66, 12.62, 55.70),
    # Gothenburg southern archipelago (Saltholmen ↔ Vrångö channel)
    ("gothenburg_archipelago", 11.72, 57.58, 11.88, 57.68),
]

# Simplified land exclusions inside water bboxes (lon, lat vertices)
LAND_EXCLUSIONS: list[tuple[str, list[tuple[float, float]]]] = [
    (
        "gulf_thailand_upper",
        [
            (100.15, 12.45), (100.45, 12.35), (100.75, 12.55), (100.92, 12.78),
            (100.88, 13.05), (100.55, 13.55), (100.35, 13.35), (100.15, 12.85),
        ],
    ),
    (
        "gulf_thailand_samet",
        [(101.38, 12.48), (101.48, 12.52), (101.46, 12.62), (101.36, 12.58)],
    ),
]


@lru_cache(maxsize=1)
def _land_polys():
    try:
        from shapely.geometry import Polygon

        return {
            name: Polygon(verts)
            for name, verts in LAND_EXCLUSIONS
        }
    except Exception:
        return {}


def in_water_override(lon: float, lat: float) -> bool:
    """True when coarse land should be treated as water (shallow sea / ferry lane)."""
    for name, lo, la, hi, ha in WATER_BBOXES:
        if not (lo <= lon <= hi and la <= lat <= ha):
            continue
        land = _land_polys().get(name)
        if land is not None:
            try:
                from shapely.geometry import Point

                if land.contains(Point(lon, lat)):
                    continue
            except Exception:
                pass
        return True
    return False