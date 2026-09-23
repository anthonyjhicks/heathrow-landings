from __future__ import annotations

from datetime import datetime, timedelta
import json
import os

from homeassistant.components.sensor import SensorEntity

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LANDINGS_DAY_FILE = os.path.join(SCRIPT_DIR, "landings_day_2026.json")
LANDINGS_NIGHT_FILE = os.path.join(SCRIPT_DIR, "landings_night_2026.json")

# Which way aircraft approach, and which of the two parallel runways they use.
# 27x is flown westbound, so arrivals come in from the east over London;
# 09x is flown eastbound, so arrivals come in from the west.
RUNWAYS = {
    "27R": ("east", "northern"),
    "27L": ("east", "southern"),
    "09L": ("west", "northern"),
    "09R": ("west", "southern"),
}


# Base class for Heathrow sensors
class HeathrowSensorBase(SensorEntity):
    _attr_icon = "mdi:airplane-landing"
    # Which column of the weekly schedule this sensor reports.
    _column = "Primary"

    def __init__(self, data):
        self.data = data

    @staticmethod
    def load_json_data(file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    @staticmethod
    def find_start_of_week():
        today = datetime.now()
        return today - timedelta(days=today.weekday())

    def entry_for_week(self, weeks_ahead=0):
        monday = self.find_start_of_week() + timedelta(weeks=weeks_ahead)
        week = monday.strftime("%d/%m/%Y")
        for entry in self.data:
            if entry["Week"] == week:
                return entry
        return None

    def update(self) -> None:
        entry = self.entry_for_week()
        runway = entry[self._column] if entry else None
        self._attr_native_value = runway or "No data"

        attributes = {
            "week_commencing": self.find_start_of_week().strftime("%d/%m/%Y")
        }
        if runway:
            # Tolerate any footnote marker Heathrow may add to a runway code.
            approach = RUNWAYS.get(runway.split()[0])
            if approach:
                attributes["approach_from"], attributes["runway_position"] = approach
        next_entry = self.entry_for_week(weeks_ahead=1)
        if next_entry:
            attributes["next_week"] = next_entry[self._column]
        self._attr_extra_state_attributes = attributes


class HeathrowLandingsMorning(HeathrowSensorBase):
    _attr_name = "Heathrow Landings 0600-1500"
    _column = "Primary"


class HeathrowLandingsAfternoon(HeathrowSensorBase):
    _attr_name = "Heathrow Landings 1500"
    _column = "Alternate"


class HeathrowLandingsNight(HeathrowSensorBase):
    _attr_name = "Heathrow Night"
    _column = "Primary"

    def update(self) -> None:
        super().update()
        # At night Heathrow also publishes a secondary runway, used when the
        # weather does not suit the primary.
        entry = self.entry_for_week()
        if entry:
            self._attr_extra_state_attributes["alternate_runway"] = entry["Alternate"]


# In setup_platform, load JSON data once and pass to sensor instances
def setup_platform(hass, config, add_entities, discovery_info=None):
    day_data = HeathrowSensorBase.load_json_data(LANDINGS_DAY_FILE)
    night_data = HeathrowSensorBase.load_json_data(LANDINGS_NIGHT_FILE)
    add_entities(
        [
            HeathrowLandingsMorning(day_data),
            HeathrowLandingsAfternoon(day_data),
            HeathrowLandingsNight(night_data),
        ]
    )
