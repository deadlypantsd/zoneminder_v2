from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import (
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_PATH,
    CONF_PATH_ZMS,
    CONF_SSL,
    CONF_VERIFY_SSL,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    DEFAULT_HOST,
    DEFAULT_PATH,
    DEFAULT_PATH_ZMS,
    DEFAULT_TIMEOUT,
    DEFAULT_SSL,
    DEFAULT_VERIFY_SSL
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_PATH, default=DEFAULT_PATH): str,
        vol.Required(CONF_PATH_ZMS, default=DEFAULT_PATH_ZMS): str,

        vol.Optional(CONF_SSL, default=DEFAULT_SSL): str,
        vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): str,
        

    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Validate the user input allows us to connect."""
### TODO


class ZoneMinderFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle ZoneMinder config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})
            try:
                await validate_input(self.hass, user_input)
                return self.async_create_entry(
                    title=user_input[CONF_HOST], data=user_input
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""