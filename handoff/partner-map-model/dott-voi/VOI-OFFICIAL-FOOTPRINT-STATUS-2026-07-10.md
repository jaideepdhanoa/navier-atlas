# Voi official footprint status — 2026-07-10

## Executive verdict

- **Current countries:** **13**, exactly matching Voi's official Q1 2026 statement that it operates in 13 countries.
- **Official directory listings:** **133** city/service-area rows. Of these, **130** ordinary rows have live city pages with operating hours, **1** additional live row is explicitly a **London scooter demo** zone, and **2** rows are directory-listed but their generated city URLs returned 404 (**V'Lônes** and **Ålgård**).
- **Lebanon:** **No current Voi operation is supported.** Lebanon is absent from Voi's complete current Available locations directory; the directory's 13 countries exactly match the company's Q1 2026 total; and no official current Lebanon city/service evidence was found.
- **Research status:** **research-complete for official footprint / source-cleanup needed for two city links**. This audit does not bind markets to Atlas or create geometry, routes, boarding points or economics.

## Confirmed current footprint

Voi's official directory says its vehicles are available for hire in the places it lists. The list below preserves Voi's own city/service-area labels rather than silently normalising or splitting regional zones.

| Country | Count | Current official city/service-area listings |
|---|---:|---|
| Austria | 2 | Innsbruck, Vienna |
| Belgium | 2 | Antwerp, Brussels |
| Denmark | 4 | Aalborg, Aarhus, Copenhagen, Odense |
| Finland | 4 | Helsinki, Jyvaskyla, Tampere, Turku |
| France | 7 | Grand Paris Seine et Oise, Grenoble, Le Havre, Marseille, Paris, Saint-Quentin-en-Yvelines, V'Lônes† |
| Germany | 41 | Aachen, Augsburg, Berlin, Bochum, Bonn, Braunschweig, Cologne, Darmstadt, Dortmund, Dresden, Duisburg/Oberhausen, Dusseldorf, Essen, Flensburg, Frankfurt, Hamburg, Hanover, Heidelberg, Karlsruhe, Kiel, Leipzig, Lübeck, Magdeburg, Mainz/Wiesbaden, Mannheim, Mönchengladbach, Muenster, Munich, Nuremberg, Osnabrück, Paderborn, Pforzheim, Potsdam, Regensburg, Reutlingen, Rostock, Schwerin, Stuttgart, Tübingen, Wuppertal, Wurzburg |
| Italy | 5 | Bologna, Genoa, Naples, Reggio Emilia, Turin |
| Netherlands | 2 | Gooi en Vechtstreek–Amersfoort, Groningen |
| Norway | 19 | Ålgård†, Arendal, Askøy, Baerum, Bergen, Bryne, Fredrikstad, Grimstad, Knarvik, Kristiansand, Lillesand, Lillestrøm, Moss, Os, Oslo, Sotra, Stavanger, Trondheim, Vennesla |
| Spain | 1 | Barcelona |
| Sweden | 16 | Boras, Gavle, Gothenburg, Halmstad, Helsingborg, Linköping, Lund, Malmö, Norrkoping, Orebro, Stockholm, Trollhättan, Uppsala, Vasteras, Växjö, Visby |
| Switzerland | 9 | Basel, Bern, Biel, Frauenfeld, Illnau-Effretikon, Nyon, Schaffhausen, Winterthur, Zürich |
| United Kingdom | 21 | Aberdeen, Aylesbury, Braintree, Cambridge, Chelmsford, Cheltenham and Gloucester, Corby, Edinburgh, Glasgow, High Wycombe, Isle of Wight, Kettering, London, London scooter demo‡, Northampton, Oxford, Portsmouth, Rushden and Higham Ferrers, Slough, Southampton, Wellingborough |

† Listed in the official directory, but the generated English city URL returned HTTP 404/no `cityData` on the audit date. Keep as a directory-supported hold pending source cleanup.

‡ Live official page with operating hours, but explicitly a demo zone; not treated as an independent town/city in the ordinary-place count.

## Priority-region findings

- **United Kingdom:** 21 official directory rows: 20 ordinary places/service areas plus the London scooter demo zone. London itself is independently corroborated by Voi's Q1 2026 report, which says Voi operated in 10 boroughs and was preparing to scale e-bikes.
- **Belgium:** Antwerp and Brussels.
- **Germany:** 41 current directory listings, the largest country inventory in the directory.
- **Nordics:** Denmark 4, Finland 4, Norway 19, Sweden 16. Iceland is not in the current directory. Norway's Ålgård row is a source-cleanup hold because its generated city URL is broken.
- **France:** 7 directory rows: Grand Paris Seine et Oise, Grenoble, Le Havre, Marseille, Paris, Saint-Quentin-en-Yvelines and V'Lônes. **Le Havre is confirmed by a live page and is the clearest northern/coastal French operation.** Lille, Dunkirk and Calais are not listed. V'Lônes is held because its generated city URL is broken.
- **Italy:** Bologna, Genoa, Naples, Reggio Emilia and Turin.
- **Spain:** Barcelona only.
- **Poland:** not in the current official directory. Old launch/expansion material does not establish current service.
- **UAE:** not in the current official directory. A country-specific app-store storefront is distribution metadata, not operating-footprint evidence.
- **Lebanon:** not in the current official directory; no current official city evidence found.
- **Other current countries not in the requested examples:** Austria, Netherlands and Switzerland. The Netherlands is specifically identified by Voi as its 13th country, launched in Q1 2026.

## Holds, ambiguities and historical/non-consumer evidence

1. **V'Lônes (France):** current directory listing, but its generated English URL returned 404. Do not silently convert this label to a municipality without an official source; retain the Voi label and `source_cleanup_needed` tier.
2. **Ålgård (Norway):** current directory listing, but its generated English URL returned 404. Retain as directory-supported, not fully city-page-confirmed.
3. **London scooter demo (UK):** the page is live and publishes 24-hour operating hours/pricing, but the label is a demo zone rather than a separate city. It is counted as a directory service-area row, not an independent town/city.
4. **Ireland / Dublin:** Voi's 2022 official post describes a 12-month, 20-bike pilot restricted to Dublin Bus employees. Ireland is absent from the 2026 directory, so this is historical B2B/non-consumer evidence, not current public footprint.

## Lebanon verdict

**Voi does not currently operate in Lebanon, based on the best available official evidence.** This is a high-confidence negative finding, not an inference from a single stale press item:

- Voi's current [Available locations](https://www.voi.com/city) directory presents the complete current list and contains 13 countries; Lebanon is absent.
- Voi's [Q1 2026 report](https://www.voi.com/investor/voi-technology-ab-publ-publishes-first-quarter-report-2026) independently states that the company operates in 13 countries and identifies the Netherlands as country 13. Those 13 countries exactly match the directory.
- Targeted searches found no official Voi Lebanon location, help, blog, investor or current press evidence.
- The existence of an app-store page accessible from a regional storefront would not prove local vehicle service.

## Source hierarchy and limitations

### Primary sources used

1. [Voi — Available locations](https://www.voi.com/city), accessed 2026-07-10. This is the core current city/service-area inventory.
2. Live official city pages linked from the directory, checked 2026-07-10 for HTTP 200, `cityData`, supported vehicles and operating hours.
3. [Voi Technology AB publishes Q1 2026 report](https://www.voi.com/investor/voi-technology-ab-publ-publishes-first-quarter-report-2026), dated 2026-04-27, for the 13-country/130+ city total and direct Netherlands, Paris and London corroboration.
4. [Voi partners with Dublin Bus](https://www.voi.com/blog/voi-partners-with-dublin-bus), dated 2022-06-07, used only to classify the Ireland evidence as a historical employee pilot.

### Limitations

- The directory is a service-area list, not a legal municipality registry. Some rows are regional/combined areas (for example, Duisburg/Oberhausen, Mainz/Wiesbaden and Gooi en Vechtstreek–Amersfoort). No attempt was made to split them into invented cities.
- Voi's 13-country corporate figure is rounded at city level ('over 130'), so it does not validate each individual directory row. City-page checks supply the row-level current signal.
- Seasonality can affect vehicle availability, but none of the 131 live pages showed all seven days closed on the audit date.
- Negative findings are based on absence from an apparently exhaustive current official directory corroborated by the exact corporate country count. They are not quoted standalone statements from Voi saying 'we do not operate' in each excluded country.
- The source JSON is an evidence inventory, not an Atlas binding artifact. `null` is used where country/city does not apply; no routes, piers, IDs, economics or geometry were created.

## Machine-readable artifact

- `voi-official-footprint-2026-07-10.json` contains the complete structured rows, per-row URLs, dates, status, evidence tier, notes and confidence.
