from __future__ import annotations

from datetime import datetime, timedelta
import json
import os

from homeassistant.components.sensor import SensorEntity

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LANDINGS_DAY_FILE = os.path.join(SCRIPT_DIR, "landings_day_2024.json")
LANDINGS_NIGHT_FILE = os.path.join(SCRIPT_DIR, "landings_night_2024.json")


# Base class for Heathrow sensors
class HeathrowSensorBase(SensorEntity):
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

    def get_values_for_current_week(self):
        start_of_week_str = self.find_start_of_week().strftime("%d/%m/%Y")
        for entry in self.data:
            if entry["Week"] == start_of_week_str:
                return entry["Primary"], entry["Alternate"]
        return None, None


class HeathrowLandingsMorning(HeathrowSensorBase):
    _attr_name = "Heathrow Landings 0600-1500"

    def update(self) -> None:
        day_morning, _ = self.get_values_for_current_week()
        self._attr_native_value = day_morning or "No data"


class HeathrowLandingsAfternoon(HeathrowSensorBase):
    _attr_name = "Heathrow Landings 1500"

    def update(self) -> None:
        _, day_afternoon = self.get_values_for_current_week()
        self._attr_native_value = day_afternoon or "No data"


class HeathrowLandingsNight(HeathrowSensorBase):
    _attr_name = "Heathrow Night"

    def update(self) -> None:
        night_primary, _ = self.get_values_for_current_week()
        self._attr_native_value = night_primary or "No data"


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
