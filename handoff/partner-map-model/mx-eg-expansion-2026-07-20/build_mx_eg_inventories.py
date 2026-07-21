#!/usr/bin/env python3
"""
Mexico + Egypt coastal expansion — Phase 1 inventory builder (Tasklet, 2026-07-20).
Emits boarding-points/, demand-records/, route-inventories/ in the Brazil-expansion layout.

Grounding rule: every boarding point is a NAMED official terminal/marina/pier with a source URL.
Per exact-data discipline, individual BP coordinates are left null with coord_status="gazetteer_pending"
and are delegated to Grok's gazetteer/ID-match promotion (see grok-seal-handoff SKILL). city_anchor is a
coarse city centroid only. No pier coordinates are invented. Aspirational routes are flagged, never mixed.
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
GEN = "2026-07-20"

def bp(id, name, type, operator, notes, source, relevance="P1", status="open"):
    return {"id": id, "name": name, "lng": None, "lat": None, "coord_status": "gazetteer_pending",
            "type": type, "relevance": relevance, "status": status, "operator": operator,
            "notes": notes, "source": source}

def rt(id, frm, to, name, distance_nm, description, signature=False, aspirational=False, source=""):
    return {"id": id, "from_bp": frm, "to_bp": to, "name": name, "distance_nm": distance_nm,
            "signature": signature, "aspirational": aspirational, "description": description, "source": source}

# ============================================================ MEXICO
MARKETS = {}

MARKETS["cancun-riviera-maya-mexico"] = {
  "city_name": "Cancún & the Riviera Maya, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "marquee", "anchor": [-86.85, 21.16], "action": "densify_existing",
  "bps": [
    bp("cancun-puerto-juarez","Puerto Juárez Maritime Terminal","ferry_terminal","APIQROO; Ultramar",
       "Primary Cancún ferry terminal for the Isla Mujeres crossing; ~20-min crossing, high-frequency Ultramar service.",
       "https://www.apiqroo.com.mx/ ; https://www.ultramarferry.com/en/","P0"),
    bp("cancun-gran-puerto","Gran Puerto Cancún","ferry_terminal","Ultramar",
       "Modern Ultramar passenger terminal adjacent to Puerto Juárez serving Isla Mujeres.",
       "https://www.ultramarferry.com/en/","P0"),
    bp("cancun-punta-sam","Punta Sam Terminal","ferry_terminal","Marítima Isla Mujeres (car ferry)",
       "Vehicle + passenger ferry terminal north of Puerto Juárez to Isla Mujeres; limited daily schedule.",
       "https://www.apiqroo.com.mx/","P1"),
    bp("cancun-playa-tortugas","Playa Tortugas (Zona Hotelera)","pier","Ultramar / tour operators",
       "Hotel-zone embarkation pier used for Isla Mujeres day service; hotel-zone mesh node.",
       "https://www.ultramarferry.com/en/","P1"),
    bp("isla-mujeres-main-dock","Isla Mujeres Passenger Dock","ferry_terminal","APIQROO; Ultramar",
       "Island-side terminal for all Cancún crossings; APIQROO-administered.",
       "https://www.apiqroo.com.mx/","P0"),
  ],
  "routes": [
    rt("cancun-r1","cancun-puerto-juarez","isla-mujeres-main-dock","Puerto Juárez ↔ Isla Mujeres",4.0,
       "The signature Cancún island crossing: a fast, frequent hop from mainland Puerto Juárez to Isla Mujeres, the busiest passenger corridor in Quintana Roo.",True,False,
       "APIQROO port statistics; Ultramar"),
    rt("cancun-r2","cancun-gran-puerto","isla-mujeres-main-dock","Gran Puerto Cancún ↔ Isla Mujeres",4.2,
       "Parallel Ultramar service from the modern Gran Puerto terminal to Isla Mujeres.",False,False,"Ultramar"),
    rt("cancun-r3","cancun-playa-tortugas","isla-mujeres-main-dock","Playa Tortugas ↔ Isla Mujeres",7.0,
       "Hotel-zone embarkation direct to Isla Mujeres, saving guests the transfer to Puerto Juárez.",True,False,"Ultramar"),
    rt("cancun-r4","cancun-punta-sam","isla-mujeres-main-dock","Punta Sam ↔ Isla Mujeres",4.5,
       "Northern crossing paralleling the car-ferry lane; premium passenger alternative.",False,False,"Marítima Isla Mujeres"),
  ],
  "demand": {"market":"cancun-riviera-maya-mexico","demand_series":[
    {"period":"2018 (full year)","pax":604150,"source_label":"APIQROO — Puerto Juárez maritime terminal passenger movement 2018 (reported +9.3% vs 2017)","source_url":"https://www.apiqroo.com.mx/en-2018-el-numero-de-pasajeros-en-las-terminales-maritimas-que-opera-y-administra-la-apiqroo-aumento-9-3-en-comparacion-con-2017/"},
    {"period":"current","pax":None,"source_label":"APIQROO operates/administers 5 maritime terminals in Quintana Roo; live annual series on the statistics portal (pin exact Isla Mujeres annual pax at Phase 3)","source_url":"https://servicios.apiqroo.com.mx/estadistica/"}
  ],"fare_anchor_usd":30.0,"fare_status":"APPROVED (Jaideep) — $30 Uber Black comparable, Cancún–Isla Mujeres"},
}

MARKETS["cozumel-mexico"] = {
  "city_name": "Cozumel, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "marquee", "anchor": [-86.95, 20.51], "action": "fix_members_missing_and_densify",
  "members_missing_fix": True,
  "bps": [
    bp("cozumel-san-miguel","San Miguel Passenger Terminal (Muelle Fiscal)","ferry_terminal","APIQROO; Ultramar/Winjet",
       "Main downtown Cozumel passenger terminal for the Playa del Carmen crossing.","https://www.apiqroo.com.mx/","P0"),
    bp("cozumel-punta-langosta","Punta Langosta Terminal","ferry_terminal","Winjet/Xailing",
       "Secondary Cozumel passenger/cruise-adjacent terminal used by fast-ferry operators.","https://winjet.mx/en/home-2-2/","P1"),
  ],
  "routes": [
    rt("cozumel-r1","playa-del-carmen-terminal","cozumel-san-miguel","Playa del Carmen ↔ Cozumel",10.0,
       "The signature Cozumel crossing: the busy Playa del Carmen↔Cozumel passenger corridor, one of the highest-volume ferry runs in the Americas (~10,000 passengers a day across Ultramar and Winjet).",True,False,
       "Riviera Maya News (Cozumel mayor, ~10,000/day); Ultramar/Winjet schedules"),
    rt("cozumel-r2","playa-del-carmen-terminal","cozumel-punta-langosta","Playa del Carmen ↔ Punta Langosta",10.2,
       "Parallel fast-ferry lane serving the Punta Langosta terminal.",False,False,"Winjet"),
  ],
  "demand": {"market":"cozumel-mexico","demand_series":[
    {"period":"~2021 (operational statement)","pax":3650000,"source_label":"Cozumel mayor / Riviera Maya News: ~10,000 people a day used the Playa del Carmen–Cozumel crossing (Ultramar 3 vessels + Winjet 2). ~10k/day ≈ 3.65M/yr run-rate.","source_url":"https://riviera-maya-news.com/cozumel-mayor-reports-agreements-with-ultramar-winjet-ferry-companies/2021.html"},
    {"period":"current","pax":None,"source_label":"APIQROO administers the Cozumel/Playa terminals; pin exact current annual pax from the statistics portal / PMDP at Phase 3","source_url":"https://servicios.apiqroo.com.mx/estadistica/"}
  ],"fare_anchor_usd":30.0,"fare_status":"PROPOSED — $30 (mirror Cancún–Isla Mujeres premium comparable; awaiting Jaideep)"},
}

MARKETS["playa-del-carmen-mexico"] = {
  "city_name": "Playa del Carmen, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "full", "anchor": [-87.08, 20.63], "action": "fix_members_missing",
  "members_missing_fix": True,
  "bps": [
    bp("playa-del-carmen-terminal","Playa del Carmen Maritime Terminal (Muelle)","ferry_terminal","APIQROO; Ultramar/Winjet",
       "Mainland terminal for the Cozumel crossing; heart of Playa's Quinta Avenida tourism district.","https://www.ultramarferry.com/en/","P0"),
  ],
  "routes": [
    rt("playa-r1","playa-del-carmen-terminal","cozumel-san-miguel","Playa del Carmen ↔ Cozumel",10.0,
       "Mainland endpoint of the signature Cozumel crossing (see Cozumel market).",True,False,"Ultramar/Winjet"),
    rt("playa-r2","playa-del-carmen-terminal","puerto-aventuras-marina","Playa del Carmen ↔ Puerto Aventuras",8.0,
       "Coastal run south to the Puerto Aventuras marina, the gateway to Tulum by sea.",False,False,"Playa Yachting / charter operators"),
  ],
  "demand": None,
}

MARKETS["isla-holbox-mexico"] = {
  "city_name": "Isla Holbox, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "full", "anchor": [-87.38, 21.52], "action": "new_city",
  "bps": [
    bp("chiquila-terminal","Chiquilá Ferry Terminal","ferry_terminal","Holbox Express; 9 Hermanos",
       "Mainland terminal for the Holbox crossing; departures roughly every 30 minutes across two operators.","https://holboxexpress.com/holbox-ferry-rates-and-departures-timetable/","P0"),
    bp("holbox-town-pier","Isla Holbox Town Pier","ferry_terminal","Holbox Express; 9 Hermanos",
       "Island terminal serving the car-free town of Holbox.","https://holboxferry.com/","P0"),
  ],
  "routes": [
    rt("holbox-r1","chiquila-terminal","holbox-town-pier","Chiquilá ↔ Isla Holbox",5.0,
       "The signature Holbox crossing: a scheduled half-hourly run to a celebrated car-free island, today served by two competing panga-style operators — a natural fit for a quieter, premium tier.",True,False,
       "Holbox Express / 9 Hermanos schedules (every ~30 min, 05:00–22:00)"),
  ],
  "demand": {"market":"isla-holbox-mexico","demand_series":[
    {"period":"current schedule","pax":None,"source_label":"Two operators (Holbox Express, 9 Hermanos) run Chiquilá↔Holbox roughly every 30 minutes, ~05:00–22:00; APIQROO covers Chiquilá/Holbox. Pin annual pax from APIQROO series at Phase 3.","source_url":"https://www.islaholbox-info.com/en/getting-there/ferry-to-holbox/"}
  ],"fare_anchor_usd":12.0,"fare_status":"PROPOSED — $12 (short high-frequency island hop, mirror Ilha do Mel/Santos tier; awaiting Jaideep)"},
}

MARKETS["tulum-mexico"] = {
  "city_name": "Tulum (Puerto Aventuras gateway), Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "display", "anchor": [-87.42, 20.21], "action": "new_city_experiences",
  "experiences": True,
  "bps": [
    bp("puerto-aventuras-marina","Puerto Aventuras Marina","marina","Puerto Aventuras marina",
       "The closest working marina between Tulum and Playa del Carmen; the practical sea gateway to the Tulum area and hub for the luxury charter market.","https://www.google.com/search?q=puerto+aventuras+marina","P0"),
  ],
  "routes": [
    rt("tulum-r1","puerto-aventuras-marina","cozumel-san-miguel","Puerto Aventuras ↔ Cozumel (El Cielo)",12.0,
       "A premium Navier Experiences run from the Tulum-side marina across to Cozumel's El Cielo sandbar — today served by luxury yacht charters starting around $950 per boat.",True,False,
       "Playa Yachting / Cozumel charter market"),
    rt("tulum-r2","puerto-aventuras-marina","playa-del-carmen-terminal","Puerto Aventuras ↔ Playa del Carmen",8.0,
       "Coastal Experiences/transfer run linking the Tulum-corridor marina to Playa del Carmen, bypassing the congested Highway 307.",False,False,"charter operators"),
  ],
  "demand": None,
  "note": "Experiences/charter basis. No scheduled regulated pax series → null hard economics until a series is pinned. Tulum's beach lacks a formal harbour; Puerto Aventuras is the sealed marine endpoint.",
}

MARKETS["puerto-vallarta-mexico"] = {
  "city_name": "Puerto Vallarta & Banderas Bay, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "full", "anchor": [-105.23, 20.62], "action": "densify_existing",
  "bps": [
    bp("pv-los-muertos-pier","Los Muertos Beach Pier (Muelle de Playa Los Muertos)","pier","Municipal / water-taxi cooperative",
       "Main Puerto Vallarta water-taxi pier for scheduled southbound pangas to the road-less villages.","https://www.go2yelapa.com/","P0"),
    bp("pv-boca-de-tomatlan","Boca de Tomatlán","pier","Water-taxi cooperative",
       "Southern water-taxi hub; frequent pangas (~every 20 min) to Las Ánimas, Quimixto and Yelapa.","https://www.go2yelapa.com/","P0"),
    bp("pv-las-animas","Playa Las Ánimas","pier","Water-taxi cooperative","Road-less beach village reachable only by boat.","https://www.go2yelapa.com/","P1"),
    bp("pv-quimixto","Quimixto","pier","Water-taxi cooperative","Road-less village + waterfall; water-taxi stop.","https://www.go2yelapa.com/","P1"),
    bp("pv-yelapa","Yelapa","pier","Water-taxi cooperative","Iconic road-less cove village, the marquee southern destination on the water-taxi line.","https://www.go2yelapa.com/","P0"),
    bp("pv-marina-vallarta","Marina Vallarta","marina","Marina Vallarta","City marina for charters/Experiences and northbound bay runs.","https://www.google.com/search?q=marina+vallarta","P1"),
  ],
  "routes": [
    rt("pv-r1","pv-boca-de-tomatlan","pv-yelapa","Boca de Tomatlán ↔ Las Ánimas ↔ Quimixto ↔ Yelapa",6.5,
       "The signature Banderas Bay water-taxi line: the only practical way to reach a string of road-less cove villages, today served by shared pangas on a fixed schedule — a clear premium-tier opportunity.",True,False,
       "Go2Yelapa water-taxi schedules"),
    rt("pv-r2","pv-los-muertos-pier","pv-yelapa","Los Muertos ↔ Yelapa",9.0,
       "Direct scheduled panga from the main Vallarta pier to Yelapa.",True,False,"Go2Yelapa"),
    rt("pv-r3","pv-marina-vallarta","pv-las-animas","Marina Vallarta ↔ southern coves",8.0,
       "Charter/Experiences run from the city marina down the wild southern shore.",False,False,"charter operators"),
  ],
  "demand": {"market":"puerto-vallarta-mexico","demand_series":[
    {"period":"current schedule","pax":None,"source_label":"Scheduled shared water taxis (Boca de Tomatlán ~every 20 min; Los Muertos fixed departures) serve road-less villages. Operator/municipal pax series owed before economics.","source_url":"https://www.go2yelapa.com/"}
  ],"fare_anchor_usd":None,"fare_status":"CONDITIONAL — hold economics until an operator/municipal pax series is pinned"},
}

MARKETS["sayulita-riviera-nayarit-mexico"] = {
  "city_name": "Sayulita & Punta Mita (Riviera Nayarit), Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "display", "anchor": [-105.44, 20.87], "action": "new_city_experiences", "experiences": True,
  "bps": [
    bp("punta-mita-pier","Punta Mita Pier (Muelle de Punta de Mita)","pier","Local cooperative / tour operators",
       "Departure pier for Islas Marietas boats and the Sayulita↔Punta Mita shuttle.","https://www.google.com/search?q=punta+mita+pier","P0"),
    bp("la-cruz-marina","Marina Riviera Nayarit (La Cruz de Huanacaxtle)","marina","Marina Riviera Nayarit",
       "Full-service marina at the north of Banderas Bay; charter/Experiences hub.","https://www.marinarivieranayarit.com/","P1"),
  ],
  "routes": [
    rt("sayulita-r1","punta-mita-pier","punta-mita-pier","Punta Mita → Islas Marietas (Experiences)",4.0,
       "A Navier Experiences run to the protected Islas Marietas (the famous Hidden Beach), today reached by cooperative pangas from Punta Mita on permit-controlled trips.",True,False,
       "Punta Mita / Marietas tour operators"),
    rt("sayulita-r2","la-cruz-marina","punta-mita-pier","La Cruz ↔ Punta Mita coastal",5.0,
       "Coastal Experiences link across the north shore of Banderas Bay.",False,False,"charter operators"),
  ],
  "demand": None, "note": "Experiences node in the Banderas Bay orbit; null economics.",
}

MARKETS["los-cabos-mexico"] = {
  "city_name": "Los Cabos, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "full", "anchor": [-109.91, 22.89], "action": "densify_existing",
  "bps": [
    bp("cabo-san-lucas-marina","Cabo San Lucas Marina","marina","Marina Cabo San Lucas",
       "Central Cabo marina; departure point for El Arco / Playa del Amor water taxis and charters.","https://www.google.com/search?q=cabo+san+lucas+marina","P0"),
    bp("puerto-los-cabos-marina","Puerto Los Cabos Marina (San José del Cabo)","marina","Puerto Los Cabos",
       "Upscale marina minutes from San José del Cabo; charter/Experiences hub.","https://www.puertoloscabos.com/","P1"),
    bp("cabo-playa-del-amor","Playa del Amor / El Arco landing","landing","Water-taxi cooperative",
       "Beach landing at Land's End reachable only by boat; the marquee Cabo water-taxi destination.","https://www.google.com/search?q=playa+del+amor+cabo","P1"),
  ],
  "routes": [
    rt("cabos-r1","cabo-san-lucas-marina","cabo-playa-del-amor","Cabo Marina ↔ El Arco / Playa del Amor",1.5,
       "The signature Cabo run: a short, iconic hop from the marina out to Land's End, El Arco and the boat-only Playa del Amor — today a constant stream of water taxis and pangas.",True,False,
       "Cabo water-taxi operators"),
    rt("cabos-r2","cabo-san-lucas-marina","puerto-los-cabos-marina","Cabo San Lucas ↔ San José del Cabo (coastal)",12.0,
       "Coastal corridor along the Tourist Corridor linking the two Cabos marinas.",False,True,
       "aspirational — no scheduled service today"),
  ],
  "demand": None,
}

MARKETS["mazatlan-mexico"] = {
  "city_name": "Mazatlán, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "display", "anchor": [-106.42, 23.19], "action": "new_city",
  "bps": [
    bp("mazatlan-playa-sur-embarcadero","Playa Sur Embarcadero","pier","Local lancha cooperative",
       "Downtown embarkation for the Stone Island crossing.","https://www.google.com/search?q=mazatlan+stone+island+embarcadero","P0"),
    bp("mazatlan-stone-island","Isla de la Piedra (Stone Island) landing","landing","Local lancha cooperative",
       "Beach landing on Stone Island, a daily-use crossing for residents and visitors.","https://www.google.com/search?q=isla+de+la+piedra+mazatlan","P0"),
  ],
  "routes": [
    rt("mazatlan-r1","mazatlan-playa-sur-embarcadero","mazatlan-stone-island","Mazatlán ↔ Isla de la Piedra (Stone Island)",1.0,
       "The signature Mazatlán crossing: a short, constant panga hop to Stone Island — a genuine daily-use corridor, not just a tour.",True,False,
       "Stone Island lancha operators"),
  ],
  "demand": None, "note": "Display + brief; null economics (regulated pax series unlikely).",
}

MARKETS["la-paz-mexico"] = {
  "city_name": "La Paz, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "display", "anchor": [-110.31, 24.16], "action": "new_city",
  "bps": [
    bp("la-paz-malecon-marina","La Paz Malecón / Marina","marina","Marinas de La Paz",
       "Waterfront marina and malecón; departure point for island Experiences.","https://www.google.com/search?q=marina+la+paz+bcs","P1"),
    bp("la-paz-pichilingue","Pichilingue Terminal","ferry_terminal","Baja Ferries (context)",
       "Deep-water terminal north of the city (long-haul Gulf ferry context; not a Navier corridor).","https://www.bajaferries.com/","P2"),
    bp("la-paz-espiritu-santo-landing","Isla Espíritu Santo landing","landing","Permit tour operators",
       "Protected UNESCO island group reached by permit-controlled boats.","https://www.google.com/search?q=isla+espiritu+santo+la+paz","P1"),
  ],
  "routes": [
    rt("lapaz-r1","la-paz-malecon-marina","la-paz-espiritu-santo-landing","La Paz ↔ Isla Espíritu Santo (Experiences)",12.0,
       "A Navier Experiences run out to the protected Espíritu Santo island group — sea lions, coves and white-sand beaches reached only by boat.",True,False,
       "La Paz permit tour operators"),
  ],
  "demand": None, "note": "Display + Experiences; null economics.",
}

MARKETS["acapulco-mexico"] = {
  "city_name": "Acapulco, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "display", "anchor": [-99.87, 16.85], "action": "new_city",
  "bps": [
    bp("acapulco-playa-caleta","Playa Caleta embarcadero","pier","Local lancha cooperative",
       "Traditional embarkation beach for the Roqueta Island crossing and bay hops.","https://www.google.com/search?q=playa+caleta+acapulco","P0"),
    bp("acapulco-isla-roqueta","Isla de la Roqueta landing","landing","Local lancha cooperative",
       "Island landing off Acapulco Bay reached by frequent pangas and glass-bottom boats.","https://www.google.com/search?q=isla+la+roqueta+acapulco","P0"),
    bp("acapulco-malecon","Acapulco Malecón / Muelle","pier","Municipal","Central bay waterfront for bay-hop service.","https://www.google.com/search?q=acapulco+malecon+muelle","P1"),
  ],
  "routes": [
    rt("acapulco-r1","acapulco-playa-caleta","acapulco-isla-roqueta","Playa Caleta ↔ Isla de la Roqueta",1.2,
       "The signature Acapulco crossing: the short, popular hop from Caleta out to Roqueta Island — a constant daily-use panga corridor across the bay.",True,False,
       "Caleta/Roqueta lancha operators"),
  ],
  "demand": None, "note": "Display; null economics. Security context to be stated honestly in the brief.",
}

MARKETS["puerto-escondido-mexico"] = {
  "city_name": "Puerto Escondido, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "display", "anchor": [-97.07, 15.86], "action": "new_city_experiences", "experiences": True,
  "bps": [
    bp("escondido-playa-principal","Playa Principal launch","pier","Local lancha cooperative",
       "Main beach launch for coastal Experiences and dolphin/turtle boat trips.","https://www.google.com/search?q=playa+principal+puerto+escondido","P0"),
    bp("manialtepec-launch","Laguna de Manialtepec launch","landing","Lagoon tour cooperative",
       "Launch on the Manialtepec coastal lagoon ~18 km west; bioluminescence and birdlife boat network.","https://www.google.com/search?q=laguna+de+manialtepec","P1"),
  ],
  "routes": [
    rt("escondido-r1","escondido-playa-principal","manialtepec-launch","Puerto Escondido ↔ Laguna de Manialtepec (Experiences)",9.0,
       "A Navier Experiences run west to the Manialtepec coastal lagoon, famous for bioluminescence and birdlife — today reached by lancha cooperatives.",True,False,
       "Manialtepec tour operators"),
  ],
  "demand": None, "note": "Experiences/lagoon basis; null economics.",
}

MARKETS["huatulco-mexico"] = {
  "city_name": "Bahías de Huatulco, Mexico", "cluster": "mexico", "country_tag": "mexico",
  "tier": "full", "anchor": [-96.13, 15.75], "action": "new_city",
  "bps": [
    bp("huatulco-santa-cruz-marina","Marina Santa Cruz (Bahía de Santa Cruz)","marina","APIQROO/FONATUR; Marinautica Huatulco",
       "Central Huatulco marina from which the nine-bays water-taxi network departs; a larger pier is under construction.","https://www.marinautica.com/","P0"),
    bp("huatulco-bahia-maguey","Bahía Maguey landing","landing","Water-taxi cooperative","Boat-only bay beach in the nine-bays network.","https://www.google.com/search?q=bahia+maguey+huatulco","P1"),
    bp("huatulco-bahia-organo","Bahía El Órgano landing","landing","Water-taxi cooperative","Boat-only bay beach in the nine-bays network.","https://www.google.com/search?q=bahia+organo+huatulco","P1"),
    bp("huatulco-bahia-cacaluta","Bahía Cacaluta landing","landing","Water-taxi cooperative","Protected boat-only bay in the nine-bays network.","https://www.google.com/search?q=bahia+cacaluta+huatulco","P1"),
  ],
  "routes": [
    rt("huatulco-r1","huatulco-santa-cruz-marina","huatulco-bahia-maguey","Santa Cruz Marina ↔ the Nine Bays",4.0,
       "The signature Huatulco service: a water-taxi network from Santa Cruz Marina out to the boat-only bays (Maguey, Órgano, Cacaluta and more) — the only practical way to reach most of them.",True,False,
       "Marinautica Huatulco; Santa Cruz water-taxi cooperative"),
  ],
  "demand": {"market":"huatulco-mexico","demand_series":[
    {"period":"current","pax":None,"source_label":"Established nine-bays water-taxi network off Santa Cruz Marina (new larger pier under construction). Operator/marina pax series owed before economics.","source_url":"https://www.marinautica.com/"}
  ],"fare_anchor_usd":None,"fare_status":"CONDITIONAL — pin operator series first"},
}

# ============================================================ EGYPT
MARKETS["alexandria-egypt"] = {
  "city_name": "Alexandria, Egypt", "cluster": "egypt", "country_tag": "egypt",
  "tier": "full", "anchor": [29.92, 31.20], "action": "thin_to_full_display",
  "bps": [
    bp("alex-eastern-harbour","Eastern Harbour (Anfoushi)","harbour","Alexandria Port / local craft",
       "Historic crescent harbour below the Qaitbay Citadel; hub for local pleasure craft and harbour hops.","https://www.google.com/search?q=alexandria+eastern+harbour","P0"),
    bp("alex-qaitbay","Qaitbay Citadel waterfront","pier","Local craft","Landmark waterfront point at the harbour mouth.","https://www.google.com/search?q=qaitbay+citadel+alexandria","P1"),
    bp("alex-montaza","Montaza marina","marina","Montaza / local craft","Royal-gardens marina at the east end of the corniche.","https://www.google.com/search?q=montaza+marina+alexandria","P1"),
    bp("alex-abu-qir","Abu Qir","harbour","Local craft","Fishing/pleasure harbour at the far east; bay-hop endpoint.","https://www.google.com/search?q=abu+qir+alexandria","P1"),
  ],
  "routes": [
    rt("alex-r1","alex-eastern-harbour","alex-montaza","Eastern Harbour ↔ Montaza (Corniche)",9.0,
       "The signature Alexandria coastal run: a sea line along the famous Corniche from the historic Eastern Harbour to the Montaza gardens, skipping the city's chronic seafront traffic.",True,False,
       "Alexandria corniche / local craft"),
    rt("alex-r2","alex-eastern-harbour","alex-qaitbay","Eastern Harbour ↔ Qaitbay",1.0,
       "Short harbour hop to the landmark citadel.",False,False,"local craft"),
    rt("alex-r3","alex-montaza","alex-abu-qir","Montaza ↔ Abu Qir",5.0,
       "Eastern bay extension toward Abu Qir.",False,True,"aspirational — no scheduled service today"),
  ],
  "demand": None, "note": "No regulated scheduled pax series expected → display + rich brief, null economics unless a series is found.",
}

MARKETS["cairo-egypt"] = {
  "city_name": "Cairo (Nile lane), Egypt", "cluster": "egypt", "country_tag": "egypt",
  "tier": "display", "anchor": [31.23, 30.05], "action": "add_nile_lane_to_existing_member",
  "geometry_only": True,
  "bps": [
    bp("cairo-maadi-nile-taxi","Maadi Nile Taxi pier (52 Zaghloul)","pier","Nile Taxi",
       "Southern Nile Taxi pier in Maadi; scheduled ~30-min river service.","https://www.niletaxi.net/","P0"),
    bp("cairo-zamalek-nile-taxi","Zamalek / Downtown Nile Taxi pier","pier","Nile Taxi",
       "Central Nile Taxi pier serving Downtown/Zamalek.","https://www.niletaxi.net/","P0"),
    bp("cairo-giza-nile-taxi","Giza Nile Taxi pier","pier","Nile Taxi","Western-bank Nile Taxi pier toward Giza.","https://www.niletaxi.net/","P1"),
  ],
  "routes": [
    rt("cairo-r1","cairo-maadi-nile-taxi","cairo-zamalek-nile-taxi","Maadi ↔ Downtown (Nile Taxi)",5.0,
       "The signature Cairo river lane: a scheduled Nile Taxi service linking Maadi and Downtown along the river, bypassing some of the world's worst road congestion.",True,False,
       "Nile Taxi scheduled service (~30 min)"),
    rt("cairo-r2","cairo-zamalek-nile-taxi","cairo-giza-nile-taxi","Downtown ↔ Giza (Nile Taxi)",6.0,
       "River link toward the Giza bank.",False,False,"Nile Taxi"),
  ],
  "demand": None, "note": "Riverine lane like Belém/Manaus — geometry-only presence; economics explicitly OUT of scope.",
}

MARKETS["marsa-alam-wadi-el-gemal-egypt"] = {
  "city_name": "Marsa Alam & Wadi El Gemal, Egypt", "cluster": "egypt", "country_tag": "egypt",
  "tier": "full", "anchor": [34.90, 24.38], "action": "new_market",
  "may_fold_into": "redsea-egypt",
  "bps": [
    bp("hamata-marina","Hamata Marina","marina","Wadi El Gemal boat operators",
       "Southern Red Sea marina; departure point for Wadi El Gemal National Park island trips.","https://www.google.com/search?q=hamata+marina+wadi+el+gemal","P0"),
    bp("qulaan-islands-landing","Qulaan / Hamata Islands landing (Siyul, Showarit, Um El Sheikh)","landing","Park boat operators",
       "Protected island archipelago inside Wadi El Gemal National Park reached only by boat.","https://www.google.com/search?q=hamata+islands+qulaan","P0"),
    bp("marsa-alam-port","Marsa Alam port","harbour","Local operators","Town harbour to the north; broader Marsa Alam access point.","https://www.google.com/search?q=marsa+alam+port","P1"),
  ],
  "routes": [
    rt("marsaalam-r1","hamata-marina","qulaan-islands-landing","Hamata ↔ Qulaan Islands (Wadi El Gemal)",7.0,
       "The signature Marsa Alam run: a boat-only crossing from Hamata Marina to the protected Qulaan/Hamata islands inside Wadi El Gemal National Park — the same near-monopoly, boat-only access logic that anchors the Giftun corridors up the coast.",True,False,
       "Wadi El Gemal boat operators (Hamata)"),
  ],
  "demand": {"market":"marsa-alam-wadi-el-gemal-egypt","demand_series":[
    {"period":"current","pax":None,"source_label":"Daily boat trips into Wadi El Gemal National Park (Hamata/Qulaan islands) are boat-only and park-permit gated. Pin park-permit / operator volumes at Phase 3.","source_url":"https://www.google.com/search?q=wadi+el+gemal+hamata+islands+boat+trip"}
  ],"fare_anchor_usd":None,"fare_status":"CONDITIONAL — pin park-permit/operator volumes first"},
}

MARKETS["el-gouna-egypt"] = {
  "city_name": "El Gouna, Egypt", "cluster": "egypt", "country_tag": "egypt",
  "tier": "display", "anchor": [33.68, 27.40], "action": "densify_within_hurghada_basis",
  "attach_to_city_id": "hurghada-el-gouna-egypt",
  "bps": [
    bp("el-gouna-abu-tig-marina","Abu Tig Marina","marina","El Gouna (Orascom)",
       "Flagship El Gouna marina 25 km north of Hurghada; hub of a purpose-built lagoon town with live water-taxi service.","https://www.google.com/search?q=abu+tig+marina+el+gouna","P0"),
    bp("el-gouna-downtown-marina","El Gouna Downtown Marina","marina","El Gouna (Orascom)","Second marina in the lagoon network.","https://www.google.com/search?q=el+gouna+downtown+marina","P1"),
  ],
  "routes": [
    rt("elgouna-r1","el-gouna-abu-tig-marina","el-gouna-downtown-marina","Abu Tig ↔ lagoon water-taxi network",2.0,
       "The signature El Gouna service: a lagoon water-taxi mesh linking the marinas and island hotels of a purpose-built waterfront town — everyday transport, not just excursions.",True,False,
       "El Gouna marinas / lagoon water taxis"),
  ],
  "demand": None, "note": "Folded into the existing Hurghada–El Gouna basis; densify only.",
}

MARKETS["dahab-egypt"] = {
  "city_name": "Dahab, Egypt", "cluster": "egypt", "country_tag": "egypt",
  "tier": "display", "anchor": [34.51, 28.50], "action": "new_city_experiences", "experiences": True,
  "may_fold_into": "sharm-el-sheikh-egypt",
  "bps": [
    bp("dahab-lagoon-launch","Dahab Lagoon launch","pier","Local dive/boat operators",
       "Launch for Blue Hole and Gabr El Bint boat access along the Sinai shore.","https://www.google.com/search?q=dahab+blue+hole+boat","P0"),
  ],
  "routes": [
    rt("dahab-r1","dahab-lagoon-launch","dahab-lagoon-launch","Dahab ↔ Gabr El Bint / Blue Hole (Experiences)",4.0,
       "A Navier Experiences run along the Sinai shore to boat-access dive sites such as Gabr El Bint — today reached by local dive boats.",True,False,
       "Dahab dive/boat operators"),
  ],
  "demand": None, "note": "Experiences basis; null economics.",
}

# hurghada-el-gouna + sharm existing: aspirational Hurghada<->Sharm crossing flagged (not a new market file;
# recorded in the seal spec as an aspirational route addition to the existing Red Sea network).

def main():
    for cid, m in MARKETS.items():
        bpf = {"city_id": cid, "city_name": m["city_name"], "cluster": m["cluster"],
               "country_tag": m["country_tag"], "city_anchor": m["anchor"], "generated": GEN,
               "tier": m["tier"], "action": m["action"], "seed_method": "web_verified_official_named_terminals",
               "coord_note": "BP lat/lng null → delegated to Grok gazetteer/ID-match promotion (grok-seal-handoff SKILL). Named official terminals + sources are authoritative.",
               "boarding_points": m["bps"]}
        for k in ("experiences","geometry_only","members_missing_fix","attach_to_city_id","may_fold_into","note"):
            if m.get(k): bpf[k] = m[k]
        json.dump(bpf, open(f"{BASE}/boarding-points/{cid}.json","w"), indent=2, ensure_ascii=False)

        rtf = {"market": cid, "city_name": m["city_name"], "cluster": m["cluster"], "generated": GEN,
               "tier": m["tier"], "routes": m["routes"],
               "counts": {"total": len(m["routes"]),
                          "signature": sum(1 for r in m["routes"] if r["signature"]),
                          "aspirational": sum(1 for r in m["routes"] if r["aspirational"])}}
        json.dump(rtf, open(f"{BASE}/route-inventories/{cid}.json","w"), indent=2, ensure_ascii=False)

        if m.get("demand"):
            d = m["demand"]; d["generated"] = GEN
            json.dump(d, open(f"{BASE}/demand-records/{cid}.json","w"), indent=2, ensure_ascii=False)

    print(f"markets: {len(MARKETS)}")
    print(f"BPs: {sum(len(m['bps']) for m in MARKETS.values())}")
    print(f"routes: {sum(len(m['routes']) for m in MARKETS.values())}")
    print(f"signature routes: {sum(1 for m in MARKETS.values() for r in m['routes'] if r['signature'])}")
    print(f"aspirational: {sum(1 for m in MARKETS.values() for r in m['routes'] if r['aspirational'])}")
    print(f"demand records: {sum(1 for m in MARKETS.values() if m.get('demand'))}")

if __name__ == "__main__":
    main()
