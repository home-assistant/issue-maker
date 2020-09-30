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

Here's an example of a pull request that rewrote a module of `unittest.TestCase` tests to standalone pytest test functions:
https://github.com/home-assistant/core/pull/40749

Here's an example command to run a single test module with pytest inside tox on Python 3.8:

```sh
tox -e py38 -- --cov-report term-missing --cov=homeassistant.components.command_line.switch tests/components/command_line/test_switch.py
```

It will print coverage information with lines that are missing coverage.

## Prerequisites

- A working [development environment](https://developers.home-assistant.io/docs/development_environment).

## Task

- Rewrite the tests one module at a time and submit the changes as a pull request to this repository.
- We want to limit the change scope to a single module to not have the pull request be too long, which would take longer time to review.
- Remember to reference this issue in your pull request, but don't close or fix the issue until all tests for the integration are updated.
