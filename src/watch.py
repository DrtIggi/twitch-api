import time
from selenium import webdriver
import threading, logging
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

logging.basicConfig(filename='log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
chromedriver_path = "/usr/local/bin/chromedriver"
DURATION = 100
PROXY_LIST = []
PROXY_USERNAME = ''
PROXY_PASSWORD = ''
CHANNEL_NAME = ''


def watch_stream(channel_name, proxy, proxy_username, proxy_password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'--proxy-server=https://{proxy_username}:{proxy_password}@{proxy}')
    chrome_options.add_argument('--no-proxy=localhost,127.0.0.1')

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    chrome_options.add_argument(f"--user-agent={user_agent}")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(f"https://www.twitch.tv/{channel_name}")
    time.sleep(DURATION)
    driver.quit()

if __name__ == "__main__":
    threads = []
    for proxy in PROXY_LIST:
        try:
            thread = threading.Thread(target=watch_stream, args=(CHANNEL_NAME, proxy, PROXY_USERNAME, PROXY_PASSWORD))
            thread.start()
            threads.append(thread)
        except Exception as e:
            logging.error(f"{e}")

    for thread in threads:
        thread.join()

