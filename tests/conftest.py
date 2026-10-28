"""
This module contains shared fixtures.
"""

import pytest
import selenium.webdriver
import json

@pytest.fixture(scope="session")
def config():
    with open("config.json", encoding="utf-8") as config_file:
        settings = json.load(config_file)

    assert settings["browser"] in ["Firefox", "Chrome", "Headless Chrome"]
    assert isinstance(settings["implicit_wait"], int)
    assert settings["implicit_wait"] > 0

    return settings

@pytest.fixture
def browser(config):
    if config["browser"] == "Firefox":
        b = selenium.webdriver.Firefox()

    elif config["browser"] == "Chrome":
        b = selenium.webdriver.Chrome()

    elif config["browser"] == "Headless Chrome":
        options = selenium.webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        b = selenium.webdriver.Chrome(options=options)

    else:
        raise Exception(f'Browser "{config["browser"]}" is not supported')

    b.implicitly_wait(config["implicit_wait"])

    yield b

    b.quit()