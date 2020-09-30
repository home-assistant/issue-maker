## Problem

The {{ DOMAIN }} integration still contains `unittest.TestCase` based unit tests. We want to rewrite them to standalone pytest test functions.

## Background

The Home Assistant core standard is to write tests as standalone pytest test functions. We still have some old tests that are based on `unittest.TestCase`. We want all these tests to be rewritten as pytest test functions.

Here are the docs for pytest: https://docs.pytest.org/en/stable/

Here's an example of an async pytest test function in Home Assistant core:

https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/tests/components/tradfri/test_light.py#L156-L176

There are many pytest fixtures to help writing the tests. See:

- https://docs.pytest.org/en/stable/reference.html#fixtures
- https://github.com/home-assistant/core/blob/dev/tests/conftest.py
- The most common fixture to use is [`hass`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/tests/conftest.py#L107) which will set up a [`HomeAssistant`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/core.py#L166) instance and start it.

## Task

- Rewrite the tests one module at a time and submit the changes as a pull request to this repository.
- We want to limit the change scope to a single module to not have the pull request be too long, which would take longer time to review.
- Make sure to not interact with any integration details in tests of integrations.
  - Set up the integration with the core interface either [`async_setup_component`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/setup.py#L44-L46) or [`hass.config_entries.async_setup`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/config_entries.py#L693) if the integration supports config entries.
  - Assert the entity state via the core state machine [`hass.states`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/core.py#L887).
  - Call services via the core service registry [`hass.services`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/core.py#L1133).
  - Assert `DeviceEntry` state via the [device registry](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/helpers/device_registry.py#L101).
  - Assert entity registry `RegistryEntry` state via the [entity registry](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/helpers/entity_registry.py#L120).
  - Modify a `ConfigEntry` via the config entries interface [`hass.config_entries`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/config_entries.py#L570).
  - Assert the state of a config entry via the [`ConfigEntry.state`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/homeassistant/config_entries.py#L169) attribute.
  - Mock a config entry via the `MockConfigEntry` class in [`tests/common.py`](https://github.com/home-assistant/core/blob/4cce724473233d4fb32c08bd251940b1ce2ba570/tests/common.py#L658)
- Remember to reference this issue in your pull request, but don't close or fix the issue until all tests for the integration are updated.
