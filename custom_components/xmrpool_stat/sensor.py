"""XMR Pool Statistics sensor platform."""

from collections.abc import Awaitable, Iterable, Mapping
import logging
from typing import Any, Dict, Optional

from voluptuous.validators import Switch

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, STATE_UNKNOWN

# from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.typing import StateType

from .const import (
    DATA_CONTROLLER,
    DOMAIN,
)
from .helpers import DefaultTo
from .xmrpoolstat_controller import XmrPoolStatController

_LOGGER = logging.getLogger(__name__)

SETUP_FACTORY = "facktory"
SETUP_ICON = "icon"
SETUP_NAME = "name"
SETUP_UNIT = "unit"

_SENSORS = {
    "balance": {
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorBalance,
        SETUP_NAME: "Balance",
        SETUP_UNIT: "XMR",
        SETUP_ICON: "mdi:bitcoin",
    },
    "hashrate": {
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorHashrate,
        SETUP_NAME: "Hashrate",
        SETUP_ICON: "mdi:gauge",
    },
    "hashrate-raw": {
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorHashrateRaw,
        SETUP_NAME: "Hashrate Raw",
        SETUP_UNIT: "H/s",
        SETUP_ICON: "mdi:gauge",
    },
}


async def async_setup_entry(
    hass: HomeAssistant, configEntry: config_entries.ConfigEntry, async_add_entities
):
    """Set up XMR pool statistics sensor."""
    _LOGGER.debug(
        "async_setup_entry({0}), state: {1}".format(
            configEntry.data[CONF_NAME], configEntry.state
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
            sensorFactory = sensorDefinition[SETUP_FACTORY]()
            sensorInstance = sensorFactory(
                instanceName, sensor, controller, sensorDefinition
            )
            sensors[sensorId] = sensorInstance
            sensorsToAdd.append(sensorInstance)
    if sensorsToAdd:
        async_add_entities(sensorsToAdd, True)


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
        self._name = "{} {}".format(
            self._instanceName,
            DefaultTo(sensorDefinition.get(SETUP_NAME), self._sensorName),
        )
        self._icon = sensorDefinition.get(SETUP_ICON)
        self._unit = sensorDefinition.get(SETUP_UNIT)
        self._privateInit()

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._controller.entity_id + self._sensorName

    @property
    def name(self) -> str:
        """Return name"""
        return self._name

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

    @property
    def icon(self) -> str:
        """Return the icon."""
        return self._icon

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
