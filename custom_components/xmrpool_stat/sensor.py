"""XMR Pool Statistics sensor platform."""

from collections.abc import Awaitable, Iterable, Mapping
import logging
from typing import Any, Dict, Optional

from voluptuous.validators import Switch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, STATE_UNKNOWN

# from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.typing import StateType

###
from random import randint

from .const import (
    DATA_CONTROLLER,
    DOMAIN,
)
from .xmrpoolstat_controller import XmrPoolStatController

_LOGGER = logging.getLogger(__name__)

_SENSORS = {
    "Balance": {"factory": lambda: XmrPoolStatisticsSensorBalance, "unit": "XMR"},
    "hashrate": {"factory": lambda: XmrPoolStatisticsSensorHashrate},
    "hashrate-raw": {
        "factory": lambda: XmrPoolStatisticsSensorHashrateRaw,
        "unit": "H/s",
    },
}


async def async_setup_entry(
    hass: HomeAssistant, configEntry: config_entries.ConfigEntry, async_add_entities
):
    """Set up XMR pool statistics sensor."""
    _LOGGER.debug(
        "async_setup_entry({0}), state: {1}".format(
            configEntry.data["name"], configEntry.state
        )
    )

    instanceName: str = configEntry.data[CONF_NAME]
    controller: XmrPoolStatController = hass.data[DOMAIN][DATA_CONTROLLER][
        configEntry.entry_id
    ]
    sensors = {}

    @callback
    def controllerUpdatedCallback():
        """Update the values of the controller."""
        UpdateItems(instanceName, controller, async_add_entities, sensors)

    controller.listeners.append(
        async_dispatcher_connect(
            hass, controller.UpdateSignal, controllerUpdatedCallback
        )
    )


@callback
def UpdateItems(
    instanceName: str,
    controller: XmrPoolStatController,
    async_add_entities,
    sensors: dict,
) -> None:
    """Update sensor state"""
    _LOGGER.debug("UpdateItems({})".format(instanceName))
    sensorsToAdd = []

    for sensor in _SENSORS:
        sensorId = "{}-{}".format(instanceName, sensor)
        if sensorId in sensors:
            if sensors[sensorId].enabled:
                sensors[sensorId].async_schedule_update_ha_state()
        else:
            sensorDefinition = _SENSORS[sensor]
            sensorFactory = sensorDefinition["factory"]()
            sensorInstance = sensorFactory(
                instanceName, sensor, controller, sensorDefinition
            )
            sensors[sensorId] = sensorInstance
            sensorsToAdd.append(sensorInstance)
    if sensorsToAdd:
        async_add_entities(sensorsToAdd)


################################################
class XmrPoolStatisticsSensor(SensorEntity):
    """Define XMR Pool sensor"""

    def __init__(
        self,
        instanceName: str,
        sensorName: str,
        controller: XmrPoolStatController,
        sensorDefinition: dict,
    ) -> None:
        """Initialize"""
        self._instanceName = instanceName
        self._sensorName = sensorName
        self._controller = controller
        self._unit = sensorDefinition.get("unit")
        self._privateInit()

    @property
    def name(self) -> str:
        """Return name"""
        return "{} {}".format(self._instanceName, self._sensorName)

    @property
    def state(self) -> StateType:
        """Return the state."""
        if self._controller.InError:
            return STATE_UNKNOWN
        else:
            return self._stateInternal

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    async def async_update(self):
        """Synchronize state with controller."""
        _LOGGER.debug("async_update")
        # self._val = randint(800, 1200)

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        _LOGGER.debug("async_added_to_hass({})".format(self.name))

    ### Overrides
    @property
    def _stateInternal(self) -> StateType:
        """Return the internal state."""
        return "OK"

    def _privateInit(self) -> None:
        """Private instance intialization"""
        pass


################################################
class XmrPoolStatisticsSensorHashrate(XmrPoolStatisticsSensor):
    @property
    def _stateInternal(self) -> StateType:
        """Return the internal state."""
        if self._value == None:
            return STATE_UNKNOWN
        return self._value[0]

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        if self._unit != None:
            return self._unit
        if self._value == None:
            return None
        return self._value[1]

    async def async_update(self):
        """Synchronize state with controller."""
        _LOGGER.debug("XmrPoolStatisticsSensorHashrate.async_update")
        self._value = self._controller.GetHashrate(None).split()

    def _privateInit(self) -> None:
        """Private instance intialization"""
        self._value = None


################################################
class XmrPoolStatisticsSensorHashrateRaw(XmrPoolStatisticsSensorHashrate):
    @property
    def _stateInternal(self) -> StateType:
        """Return the internal state."""
        if self._value == None:
            return STATE_UNKNOWN
        multiplier = 0.0
        unit = self._value[1]
        if unit == "H":
            multiplier = 1000.0
        elif unit == "KH":
            multiplier = 1000.0
        elif unit == "MH":
            multiplier = 1000000.0
        return int(float(self._value[0]) * multiplier)


################################################
class XmrPoolStatisticsSensorBalance(XmrPoolStatisticsSensor):
    @property
    def _stateInternal(self) -> StateType:
        return self._controller.Balance
