import random
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from dotenv import load_dotenv

from tests import UnitTestResponse


load_dotenv()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def open_firefox():
    """Open Firefox and navigate to google.com."""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(executable_path=os.environ.get("GECKODRIVER_PATH"))
    driver = webdriver.Firefox(options=options, service=service)
    driver.implicitly_wait(10)

    return driver

def test_batch(browser, tests):
    for test in tests:
        result = None
        message = ""
        try:
            result, message = test["function"](browser)
        except Exception as e:
            print("Test " + test["name"] + f" {bcolors.FAIL}FAILED WITH EXCEPTION{bcolors.ENDC}")
            print(str(e))
            continue
        if result == UnitTestResponse.SUCCESS:
            print("Test " + test["name"] + f" {bcolors.OKGREEN}PASSED{bcolors.ENDC}")
        elif result == UnitTestResponse.ERROR:
            print("Test " + test["name"] + f" {bcolors.FAIL}FAILED WITH MESSAGE{bcolors.ENDC}")
            print(message)
        elif result == UnitTestResponse.WARNING:
            print("Test " + test["name"] + f" {bcolors.WARNING}PASSED WITH WARNING{bcolors.ENDC}")
            print(message)
        else:
            print("Test " + test["name"] + f" {bcolors.FAIL}UNDEFINED STATUS CODE{bcolors.ENDC}")

def test_pokemons_list(browser):
    pokemons_list = browser.find_element(By.ID, "pokemons-list")

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#pokemons-list .pokemon-instance")))

    instances = browser.find_elements(By.CSS_SELECTOR, "#pokemons-list .pokemon-instance")

    for instance in instances:
        try:
            instance.find_element(By.CSS_SELECTOR, ".pokemon-name")
        except Exception as e:
            return UnitTestResponse.ERROR, "pokemon name not found!"
        try:
            instance.find_element(By.CSS_SELECTOR, ".pokemon-image")
        except Exception as e:
            return UnitTestResponse.ERROR, "pokemon image not found!"

    return UnitTestResponse.SUCCESS, "success"

def test_pokemons_search(browser):
    searchbox = browser.find_element(By.CSS_SELECTOR, "#searchInput")
    searchbox.click()
    searchbox.clear()
    searchbox.send_keys("bulbasaur")
    instance = browser.find_element(By.CSS_SELECTOR, "#pokemons-list .pokemon-instance .pokemon-name")
    if instance.text != "bulbasaur":
        return UnitTestResponse.ERROR, "pokemon not found!"
    return UnitTestResponse.SUCCESS, "success"

def test_pokemon_page(browser):
    try:
        browser.find_element(By.CSS_SELECTOR, ".pokemon-name")
    except Exception as e:
        return UnitTestResponse.ERROR, "pokemon name not found!"
    try:
        browser.find_element(By.CSS_SELECTOR, ".pokemon-image")
    except Exception as e:
        return UnitTestResponse.ERROR, "pokemon image not found!"
    return UnitTestResponse.SUCCESS, "success"

def test_battle_round(browser):

    user_pokemon_hp = browser.find_element(By.CSS_SELECTOR, "#user-pokemon-hp").text
    enemy_pokemon_hp = browser.find_element(By.CSS_SELECTOR, "#enemy-pokemon-hp").text
    score = browser.find_element(By.CSS_SELECTOR, "#score").text

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".user-choosing-number")))

    numbers_list = browser.find_elements(By.CSS_SELECTOR, ".user-choosing-number")

    number = random.choice(numbers_list)

    number.click()

    time.sleep(0.5)

    if (user_pokemon_hp == browser.find_element(By.CSS_SELECTOR, "#user-pokemon-hp").text and \
        enemy_pokemon_hp == browser.find_element(By.CSS_SELECTOR, "#enemy-pokemon-hp").text and \
        score == browser.find_element(By.CSS_SELECTOR, "#score").text):
        return UnitTestResponse.ERROR, "pokemons hp and score are not changing!"

    return UnitTestResponse.SUCCESS, "success"

if __name__ == "__main__":
    browser = open_firefox()

    browser.get("http://localhost:5000")
    tests = [
        {
            "name": "Список покемонов",
            "function": test_pokemons_list,
        },
        {
            "name": "Поиск покемонов",
            "function": test_pokemons_search,
        },
    ]
    test_batch(browser, tests)

    browser.get("http://localhost:5000/pokemon/bulbasaur")
    tests = [
        {
            "name": "Страница покемона",
            "function": test_pokemon_page,
        },
    ]
    test_batch(browser, tests)

    browser.get("http://localhost:5000/battle/bulbasaur")
    tests = [
        {
            "name": "Ход игрока в бою",
            "function": test_battle_round,
        },
    ]
    test_batch(browser, tests)

    #browser.quit()
