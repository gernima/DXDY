from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import pyautogui
import subprocess
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import requests
from random import sample, randint

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ua = UserAgent()


def open_browser(headless, proxy, tf_prefs=False, extension=None):
    global proxies
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=http://%s' % proxy)
    options.add_argument('--dns-prefetch-disable')
    # options.add_extension('MetaMask_v10.0.3.crx') # load metamask
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-browser-side-navigation')
    # options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--start-maximized")
    options.add_argument(f"user-agent={ua.chrome}")
    options.add_argument("--mute-audio")
    options.add_argument('--ignore-certificate-errors')
    prefs = {
        'profile.managed_default_content_setting_values': {
            'cookies': 1,
            'images': 1,
            'javascript': 1,
            'plugins': 2,
            'popups': 2,
            'geolocation': 2,
            'notifications': 2,
            'auto_select_certificate': 2,
            'fullscreen': 2,
            'mixed_script': 1,
            'media_stream': 1,
            'media_stream_mic': 1,
            'media_stream_camera': 2,
            'protocol_handlers': 2,
            'push_messaging': 2,
            'ppapi_broker': 2,
            'automatic_downloads': 2,
            'midi_sysex': 2,
            'ssl_cert_decisions': 2,
            'metro_switch_to_desktop': 2,
            'protected_media_identifier': 2,
            'app_banner': 2,
            'site_engagement': 2,
            'durable_storage': 2
        },
        "media.autoplay.enabled": True,
        'disk-cache-size': 0
    }
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    if tf_prefs:
        options.add_argument("blink-settings=imagesEnabled=false")
        options.add_experimental_option("prefs", prefs)
    capabilities = DesiredCapabilities.CHROME
    # capabilities["pageLoadStrategy"] = "eager"
    options.add_argument('--no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument('--headless')
    driver = get_driver(capabilities, options)
    return driver


def get_driver(capabilities, options):
    return webdriver.Chrome(executable_path="chromedriver.exe",
                            desired_capabilities=capabilities,
                            options=options)


ai = 0
ri = 0
n = 20
while True:
    http = []
    referal_links = {}
    with open("codes.txt","r", encoding="utf-8") as f:
        [referal_links[x] = 0 for x in f.read().strip().split("\n")] 
    print(referal_links)
    input("press")
    with open("http.txt","r", encoding="utf-8") as f:
        [http.append(x) for x in f.read().strip().split("\n")]
    with open("http_used.txt","r", encoding="utf-8") as f:
        [http.remove(x) for x in f.read().strip().split("\n") if x in http]
    access = False
    while access is False:
        if http:
            http_ = sample(http, 1)[0]
            print(http_, len(http))
            driver = open_browser(True, http_)
            try:
                driver.get(f"https://dxdy.finance/{list(referal_links.keys())[ri]}")
                if "Access Denied" not in driver.page_source and "ERR" not in driver.page_source and "security check to access" not in driver.page_source:
                    access = True
                    print("access")
                else:
                    driver.quit()
            except:
                driver.quit()
                pass
        else:
            print("proxy is mt")   
            break

    def get_webdriverwait_element(driver, xpath, time=30):
        return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))

    from secrets import token_bytes
    from coincurve import PublicKey
    from sha3 import keccak_256

    def get_address():
        private_key = keccak_256(token_bytes(32)).digest()
        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
        addr = keccak_256(public_key).digest()[-20:]
        return "0x" + addr.hex()

    if access:
        address = get_address()
        try:
            get_webdriverwait_element(driver, '//*[@id="airdrop-form"]/div/input').send_keys(address)
            get_webdriverwait_element(driver, '//*[@id="airdrop-form"]/div/button').click()
            driver.quit()
            referal_links[list(referal_links.keys())[ri]] += 1
            ri += 1
            if http_ in http:
                http.remove(http_)
            with open("http_used.txt","a") as f:
                f.write(str(http_) + "\n")
            print("referal added", referal_links)
        except:
            print("err")
    if ri >= len(list(referal_links.keys())):
        ri = 0
        n-=1
        sleep_time = randint(60, 100)
        print("sleep", sleep_time)
        sleep(sleep_time)
