# Heathrow Landings

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

Home Assistant sensors telling you which runway Heathrow is scheduled to land on this week — morning, afternoon and overnight.

If you live under the flight path, runway alternation is the difference between a quiet morning and a stream of aircraft over the garden. This integration reads Heathrow's published [Runway Alternation Programme][programme] so you can put the week's pattern on a Dashboard, or drive an automation from it — close the windows, pause the outdoor speakers, or just know whether today is a noisy one.

It reads a static JSON file I converted from the Heathrow published PDF, so there's nothing to poll and no API key. The flip side is that the schedule could change without me realising, so no promises this is always up to date ;)

## How runway alternation works

Heathrow has two parallel runways and alternates which one handles landings, so that the communities beneath each approach get predictable periods of quiet.

**Daytime** runs from 06:00 until the last departure, with the switchover at 15:00. One runway takes landings in the morning, the other takes them in the afternoon. This only happens during *westerly operations* — wind from the west, aircraft arriving from the east over London — which is roughly 70% of the year. On easterly operations the daytime sensors still report the scheduled runway, but the actual arrival flow will differ.

**Night** runs from after the last departure until 06:00, on a four-week cycle. Because so few aircraft move at night, Heathrow can alternate both the runway and the direction of approach.

Two quirks worth knowing:

- Both runways are used for arrivals between **06:00 and 07:00** — the busiest arrivals hour of the day.
- There's a transitional period from Sunday into Monday, so **Monday flights before 06:00** still follow the previous week's night pattern.

### Runway codes

| Code | Runway | Aircraft approach |
| -- | -- | -- |
| `27R` | Northern | from the east |
| `27L` | Southern | from the east |
| `09L` | Northern | from the west |
| `09R` | Southern | from the west |

Daytime only ever uses `27R` and `27L`. Night uses all four.

## Installation

### HACS (recommended)

Have [HACS](https://hacs.xyz/) installed, this will allow you to update easily.

1. Go to <b>HACS</b> -> <b>Integrations</b>.
2. Add this repository (https://github.com/anthonyjhicks/heathrow-landings) as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/).
3. Click on `+ Explore & Download Repositories`.
4. Search for `Heathrow Landings`.
5. Navigate to the `Heathrow Landings` integration.
6. Press `DOWNLOAD`, and in the next window press `DOWNLOAD` again.
7. Restart Home Assistant.

### Manual

1. Locate the `custom_components` directory in your Home Assistant configuration directory. It may need to be created.
2. Copy the `custom_components/heathrow_landings` directory into it.
3. Restart Home Assistant.

## Configuration

There is no configuration UI. Add the following to the sensor section of your `configuration.yaml` and restart Home Assistant:

```yaml
sensor:
  - platform: heathrow_landings
```

## Sensors

Three sensors, all reporting the schedule for the current week:

| Entity | Name | Period | Example state |
| -- | -- | -- | -- |
| `sensor.heathrow_landings_0600_1500` | Heathrow Landings 0600-1500 | 06:00 until 15:00 | `27R` |
| `sensor.heathrow_landings_1500` | Heathrow Landings 1500 | 15:00 until the last departure | `27L` |
| `sensor.heathrow_night` | Heathrow Night | After the last departure until 06:00 | `09R` |

The state is the runway code on its own, so you can compare it directly:

```jinja
{% if states('sensor.heathrow_landings_0600_1500') == '27L' %}
  Landing over us this morning
{% endif %}
```

The week rolls over on Monday. For the night schedule Heathrow also publishes a secondary runway — the same runway approached from the opposite direction, used when the weather doesn't suit the primary — and the sensor reports the primary.

## Accuracy

These sensors report the **scheduled** runway, not the one in use right now. Heathrow does its best to stick to the programme, but delays can put arrivals outside the pattern, and alternation is sometimes suspended altogether for bad weather or runway repairs. Heathrow has also flagged that planned runway resurfacing will force deviations from the published plan, particularly overnight — see [heathrow.com/runwayresurfacing](https://www.heathrow.com/runwayresurfacing) or [@HeathrowRunways](https://x.com/HeathrowRunways).

For what's actually happening, pair this with my [Heathrow Arrivals](http://github.com/anthonyjhicks/heathrow-arrivals) integration, which reads the live arrival runway from the Heathrow (EGLL) ATIS.

The bundled schedule covers 2026 and is refreshed here each year when Heathrow publishes the next programme.

## Also worth a look

- [Heathrow Arrivals](http://github.com/anthonyjhicks/heathrow-arrivals) — the live arrival runway from the EGLL ATIS.
- [Home Assistant Flightradar24](https://github.com/AlexandrErohin/home-assistant-flightradar24) — counts aircraft overhead. Combine it with the Utility Meter helper to get the count range you want.

## Issues

Please report any [Issues](http://github.com/anthonyjhicks/heathrow-landings/issues).

***

[heathrow-landings]: https://github.com/anthonyjhicks/heathrow-landings
[programme]: https://www.heathrow.com/content/dam/heathrow/web/common/documents/company/local-community/noise/operations/runway-alternation/Runway_Alternation_Programme_2026.pdf
[buymecoffee]: https://www.buymeacoffee.com/anthonyjhicks
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/anthonyjhicks/heathrow-landings.svg?style=for-the-badge
[commits]: https://github.com/anthonyjhicks/heathrow-landings/commits/main
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/anthonyjhicks/heathrow-landings.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Anthony%20Hicks%20%40anthonyjhicks-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/anthonyjhicks/heathrow-landings.svg?style=for-the-badge
[releases]: https://github.com/anthonyjhicks/heathrow-landings/releases
