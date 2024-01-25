# Heathrow Landings
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

Home Assistant sensors indicating the scheduled runways for the current week at 0600-1500, 1500 until last departure, and Night as published by London Heathrow Airport at [Runway Alterations](https://www.heathrow.com/content/dam/heathrow/web/common/documents/company/local-community/noise/operations/runway-alternation/Runway_Alternation_Programme_2024.pdf).  Ideal for use if you live in the Heathrow flight path and want to be to able to track when aircraft are likely to be flying over your location for display on your Dashboard or perhaps linked to an automation. This reads a static JSON file I converted from the Heathrow published PDFs of scheduled runway useage.  This schedule could change without me realising - no promises the static files are entirely up to date.

I recommend combining this with my [Heathrow Arrival Rwy](http://github.com/anthonyjhicks/heathrow-arrival-rwu) integration for a live sensor of the active Arrivals runway according to the Heathrow (EGLL) ATIS, as this can sometimes vary from the scheduled runway due to operational reasons.

You could also add this superb [Home Assistant Flightradar24](https://github.com/AlexandrErohin/home-assistant-flightradar24) intergation to count the number of aircraft flying over your location (combine it with the Utility Meter Helper to get the counts you need).

## Installation

### HACS (recommended)

Have [HACS](https://hacs.xyz/) installed, this will allow you to update easily.

1. Go to the <b>HACS</b>-><b>Integrations</b>.
2. Add this repository (https://github.com/anthonyjhicks/heathrow-landings) as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/)
3. Click on `+ Explore & Download Repositories`.
4. Search for `Heathrow Landings`. 
5. Navigate to `Heathrow Landings` integration 
6. Press `DOWNLOAD` and in the next window also press `DOWNLOAD`. 
7. After download, restart Home Assistant.

### Manual

1. Locate the `custom_components` directory in your Home Assistant configuration directory. It may need to be created.
2. Copy the `custom_components/heathrow_landings` directory into the `custom_components` directory.
3. Restart Home Assistant.

## Configuration

There is no configuration UI.  You must add the following to the sensor section of your configuration.yaml:

```
sensor:
  - platform: heathrow_landings
```

This will create three sensors:

| Entity | Name | State | Attributes |
| -- | -- | -- | -- |
| sensor.heathrow_arrival_rwy | Heathrow Arrival Rwy | 27L | friendly_name: Heathrow Arrival Rwy |
| sensor.heathrow_landings_0600_1500 | Heathrow Landings 0600-1500 | 27L | friendly_name: Heathrow Landings 0600-1500 |
| sensor.heathrow_landings_1500 | Heathrow Landings 1500 | 27R * |	friendly_name: Heathrow Landings 1500 | 
| sensor.heathrow_night | Heathrow Night | 27L * | friendly_name: Heathrow Night |

## Issues
