"""Gazetteer-validated coordinates for Thailand Bucket-C boarding points (OSM/Wikidata, 2026-06-22)."""
from __future__ import annotations

# (lng, lat) — validated against OpenStreetMap pier/marina nodes + coastal sanity check
GAZETTEER: dict[str, dict] = {
    "bp-nathon-pier": {
        "lng": 99.9459,
        "lat": 9.5350,
        "source": "OSM way/ferry terminal Nathon, Koh Samui",
        "precision": "gazetteer",
    },
    "bp-bangrak-pier": {
        "lng": 100.0593,
        "lat": 9.5634,
        "source": "OSM Bangrak/Big Buddha tourist pier",
        "precision": "gazetteer",
    },
    "bp-maenam-pier": {
        "lng": 100.0276,
        "lat": 9.5731,
        "source": "OSM Maenam Lomprayah catamaran pier",
        "precision": "gazetteer",
    },
    "bp-lipa-noi-pier": {
        "lng": 99.9338,
        "lat": 9.4516,
        "source": "OSM Lipa Noi Raja car-ferry terminal",
        "precision": "gazetteer",
    },
    "bp-bophut-fishermans-village": {
        "lng": 100.0187,
        "lat": 9.5660,
        "source": "OSM Bophut Fisherman's Village jetty",
        "precision": "gazetteer",
    },
    "bp-thong-sala-pier": {
        "lng": 100.0049,
        "lat": 9.7096,
        "source": "OSM Thong Sala main ferry terminal, Koh Phangan",
        "precision": "gazetteer",
    },
    "bp-haad-rin-pier": {
        "lng": 100.0694,
        "lat": 9.6748,
        "source": "OSM Haad Rin pier (Full Moon Party node)",
        "precision": "gazetteer",
    },
    "bp-mae-haad-pier": {
        "lng": 99.8395,
        "lat": 10.0796,
        "source": "OSM Mae Haad pier, Koh Tao",
        "precision": "gazetteer",
    },
    "bp-bali-hai-pier": {
        "lng": 100.8674,
        "lat": 12.9233,
        "source": "OSM Bali Hai Pier, South Pattaya",
        "precision": "gazetteer",
    },
    "bp-ocean-marina-yacht-club": {
        "lng": 100.8807,
        "lat": 12.8304,
        "source": "OSM Ocean Marina Yacht Club, Na Jomtien",
        "precision": "gazetteer",
    },
    "bp-koh-larn-na-ban-pier": {
        "lng": 100.7814,
        "lat": 12.9231,
        "source": "OSM Na Ban Pier (main Koh Larn landing)",
        "precision": "gazetteer",
    },
    "bp-ao-sapparot-pier": {
        "lng": 102.3584,
        "lat": 12.0873,
        "source": "OSM Ao Sapparot Centrepoint ferry, Koh Chang",
        "precision": "gazetteer",
    },
    "bp-bang-bao-pier": {
        "lng": 102.2959,
        "lat": 11.9972,
        "source": "OSM Bang Bao fishing/tourist pier, Koh Chang",
        "precision": "gazetteer",
    },
    "bp-khong-kha-pier": {
        "lng": 98.9191,
        "lat": 8.0608,
        "source": "OSM Khong Kha Pier, Krabi Town riverfront",
        "precision": "gazetteer",
    },
    "bp-klong-jilad-pier": {
        "lng": 98.9203,
        "lat": 8.0434,
        "source": "OSM Klong Jilad speedboat terminal, Krabi",
        "precision": "gazetteer",
    },
    "bp-ao-nang-pier": {
        "lng": 98.8127,
        "lat": 8.0323,
        "source": "OSM Ao Nang / Nopparat Thara beach pier",
        "precision": "gazetteer",
    },
    "bp-railay-east-pier": {
        "lng": 98.8419,
        "lat": 8.0111,
        "source": "OSM Railay East longtail landing",
        "precision": "gazetteer",
    },
    "bp-tonsai-pier": {
        "lng": 98.7703,
        "lat": 7.7386,
        "source": "OSM Tonsai Pier, Koh Phi Phi Don",
        "precision": "gazetteer",
    },
    "bp-laem-tong-pier": {
        "lng": 98.7791,
        "lat": 7.7643,
        "source": "OSM Laem Tong resort jetty, north Phi Phi Don",
        "precision": "gazetteer",
    },
}

CITY_ANCHOR_GAZETTEER: dict[str, tuple[float, float]] = {
    "koh-samui-thailand": (100.0156, 9.5731),
    "koh-phangan-thailand": (100.0370, 9.7096),
    "koh-tao-thailand": (99.8395, 10.0796),
    "pattaya-thailand": (100.8674, 12.9233),
    "koh-larn-thailand": (100.7814, 12.9231),
    "koh-chang-thailand": (102.3270, 12.0420),
    "krabi-thailand": (98.9191, 8.0608),
    "koh-phi-phi-thailand": (98.7703, 7.7386),
}