# DiDi × Navier Mexico — T3 finance evidence

**As of:** 2026-07-09  
**Status:** Complete with explicit modeled fields and diligence blockers  
**JSON:** `DIDI-MEXICO-T3-FINANCE-EVIDENCE-2026-07-09.json`

## Decision summary

| Item | T3 treatment | Confidence |
|---|---:|---|
| Playa del Carmen–Cozumel 2025 gross corridor one-way journeys | **3,853,770**; do **not** divide or multiply | High |
| Puerto Juárez–Isla Mujeres 2025 gross corridor one-way journeys | **5,458,304** from the official decomposable table; do **not** divide or multiply | High |
| APIQROO prose value for Isla Mujeres | 5,457,733; retain only as a discrepancy note (571 below table) | Medium |
| Fare FX basis | 2025 official period-average **19.2375083333333 MXN/USD** | High |
| Provisional Mexico country row | captain **$14,000/yr**; energy **$0.23/kWh**; grid **0.444 kgCO2e/kWh**; marina overhead **$11,000/yr**; cost index **0.54** | Mixed; see tiers |

## 1. APIQROO passenger-count adjudication

The official government/APIQROO article says:

> “En cuanto a la ruta federal Cozumel-Playa del Carmen se consolida como un eje estratégico para la movilidad turística y cotidiana, al registrar **3 millones 853 mil 770 pasajeros**, lo que representa un incremento del 8% respecto a 2024, así como 27 mil 920 salidas de ferris…”

For Isla Mujeres it says:

> “Durante 2025 se registraron **5 millones 457 mil 733 pasajeros**”

The official APIQROO route table is more diagnostic because it labels the passenger columns **“ENTRADAS / SALIDAS / TOTAL”**:

- **Cozumel:** 1,932,907 entradas + 1,920,863 salidas = **3,853,770 total**.
- **Playa del Carmen:** the same two direction counts are reversed. This is the mirrored endpoint view of the same corridor, so **do not add the Playa and Cozumel rows**.
- **Isla Mujeres:** 2,692,716 entradas + 2,765,588 salidas = **5,458,304 total**.

### Model meaning

These are passenger movements / one-way crossing journeys, with both directions already combined. One passenger boarding in one direction contributes one journey. Therefore:

- Set `corridor_annual_oneway_pax = 3,853,770` for Playa–Cozumel.
- Set `corridor_annual_oneway_pax = 5,458,304` for Puerto Juárez–Isla Mujeres.
- **Do not divide by two** (that would approximate round trips).
- **Do not multiply by two** (both directions are already included).
- Do not allocate the entire count to a single operator, DiDi, Navier, or one operator-specific Atlas edge.

The Isla article differs from the official table by **571 passengers (0.010462%)**. Structurally, 5,457,733 refers to the same gross two-direction movement concept and would not need division or multiplication, but it should not be the canonical input while the table gives a decomposable 5,458,304. Request a frozen APIQROO workbook or confirmation if exact tie-out is material.

Primary URLs:

- Article: <https://cgc.qroo.gob.mx/logra-quintana-roo-crecimiento-sostenido-en-la-actividad-maritima-durante-2025/>
- APIQROO route table: <https://servicios.apiqroo.com.mx/estadistica/datos/informeRutaPasaje.php?anio=2025>
- APIQROO Isla monthly detail: <https://servicios.apiqroo.com.mx/estadistica/datos/puertoRutaPasaje.php?puerto=5&anio=2025>

## 2. MXN/USD conversion and public-fare comparables

Use the World Bank WDI 2025 **Official exchange rate (LCU per US$, period average)** for Mexico: **19.2375083333333 MXN per USD**. This is a completed-period basis matching the 2025 demand year. It is conservative for revenue comparability versus the stronger-peso 2026 monthly averages, which would translate the same MXN ticket into more USD.

Formula: `USD = MXN / 19.2375083333333`.

| Public fare | Exact USD | Publish at |
|---:|---:|---:|
| MXN 290 | 15.0747173166 | **$15.07** |
| MXN 320 | 16.6341708321 | **$16.63** |
| MXN 335 | 17.4138975898 | **$17.41** |
| MXN 350 | 18.1936243476 | **$18.19** |

World Bank annual series: <https://api.worldbank.org/v2/country/MEX/indicator/PA.NUS.FCRF?format=json&per_page=10>  
Banxico FIX table (primary transaction/settlement reference): <https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF86&locale=es&sector=6>

Keep full precision in calculations and round published comparables to cents. Do not mix annual-average, spot, and FIX bases within one fare table. These are public sticker-fare comparables, not realized yield.

## 3. Provisional Mexico country-reference row

| Repo field | Proposed value | Source tier / treatment |
|---|---:|---|
| `captain_usd_yr` | **14,000** | **Modeled, low confidence.** Data México reports MXN 9.12k/month national cash wage in 2026 Q1, which annualizes to $5,688.89 at the 2025 FX basis. The proposal adds an unverified commercial licensing/employer/tourist-market allowance. Obtain operator payroll quotes. Sensitivity: $6k / $14k / $26k. |
| `energy_usd_kwh` | **0.23** | Source-anchored comparator, medium-low confidence. Quintana Roo PDBT energy MXN 3.9680/kWh divided by Banxico June 2026 average 17.3819 = $0.228283/kWh. A third-party mirror supplied the exact CFE-linked row because direct CFE automation was blocked. PDBT is **not** a fast-charge all-in tariff; VAT, demand, connection, capacity and higher-load classifications are excluded. |
| `grid_co2_kg_kwh` | **0.444** | **Mexican official, high confidence.** SEMARNAT says 2026 COA reporting must use the 2024 National Electric System factor, 0.444 tCO2e/MWh, while the 2025 factor is pending. Numerically equal to 0.444 kgCO2e/kWh. |
| `marina_overhead_usd_yr` | **11,000** | **Modeled, low confidence.** Existing Singapore model anchor $20k × Mexico relative-price proxy 0.536917 = $10,738, rounded. This is model-on-model, not a Mexico marina quote. Obtain endpoint berth/port/admin quotes. Sensitivity: $8k / $11k / $18k. |
| `cost_index` | **0.54** | **Modeled from official macro series, medium-low confidence.** 2025 PPP factor 10.328951 MXN/int$ ÷ official FX 19.2375083333333 = 0.536917, rounded. Use only as a broad price-level proxy, not maritime OPEX evidence. |

Key source URLs:

- Data México captain profile: <https://www.economia.gob.mx/datamexico/es/profile/occupation/capitanes-y-conductores-de-transporte-maritimo>
- Quintana Roo PDBT mirror: <https://airegulasolutions.com/cfe/tarifas?year=2026&month=5&tariffCode=PDBT&state=QUINTANA%20ROO&page=1&pageSize=100>
- Official CFE selector: <https://app.cfe.mx/aplicaciones/ccfe/tarifas/tarifascrenegocio/tarifas/pequenademandabt.aspx>
- SEMARNAT factor notice: <https://www.gob.mx/cms/uploads/attachment/file/1081506/aviso_factor_de_emision_electrico_coa_2026.pdf>
- World Bank PPP series: <https://api.worldbank.org/v2/country/MEX/indicator/PA.NUS.PPP?format=json&per_page=10>

## Blocking diligence

1. APIQROO confirmation/frozen workbook for the 571-passenger Isla discrepancy.
2. Operator and fare-product mix before turning gross corridor journeys into obtainable demand or yield.
3. Quintana Roo employer-loaded licensed-captain payroll quotes.
4. CFE interconnection/load study for actual charging kW, tariff class, demand/capacity and capex.
5. Endpoint annual berth, port, passenger/embarkation and local-admin quotations.
6. Replace the 2024 grid factor once SENER publishes Mexico’s 2025 factor.

**No repository edits were made.** JSON was parsed and arithmetic assertions passed with Python.
