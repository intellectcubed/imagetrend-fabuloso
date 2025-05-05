import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import traceback
from selenium.common.exceptions import TimeoutException

# Use built-in driver manager
# from selenium.webdriver.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import time

class ImageTrend:
    def __init__(self):
        # Read ../config/config.yaml and save user, password, and url
        self.user = None
        self.password = None
        self.url = None
        self.incidentsUrl = None
        self.driver = None
        self._load_config()
        # self._load_driver()
        # self.login()

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config/login_details.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.user = self.config['imagetrend']['username']
        self.password = self.config['imagetrend']['password']
        self.url = self.config['imagetrend']['url']
        self.incidentsUrl = self.config['imagetrend']['incidents_url']
        self.chromepath = self.config['chrome']['path']


    def _load_driver(self):
        self.driver = webdriver.Chrome()

    def _load_driver2(self):
        # Check if there's an existing session (assuming we have some method of checking)
        # If you have some logic to verify if a session exists, you can handle it here.
        if not self.driver:
            print("Starting a new Chrome driver instance.")
            options = Options()
            # options.add_argument("--start-maximized")
            # Optional: Headless mode (no UI)
            # options.add_argument("--headless")
            
            # Define the path to the ChromeDriver executable
            chrome_driver_path = self.chromepath

            # Set up the service and driver
            service = Service(executable_path=chrome_driver_path)
            # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Wait for the driver to start
            time.sleep(2)  # Wait for the driver to initialize, adjust timing if needed
        else:
            print("Using existing Chrome driver session.")

        return self.driver


    def connect_to_existing_chrome(self):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

        # Initialize WebDriver with ChromeOptions
        driver = webdriver.Chrome(options=chrome_options)        

        # Now you can interact with the browser
        # driver.get("https://www.google.com")
        # print('Got the page')
        # print(driver.title)

        print('Connected to existing Chrome session.')
        self.driver = driver

    def login(self):
        if not self.driver:
            print("Driver not initialized. Loading driver.")
            return
        self.driver.get(self.url)
        time.sleep(2)
        try:
            # On my Chrome, the user and pwd are already populated!
            # print(f'User field contents: {self.driver.find_element(By.ID, "username").get_attribute("value")}')
            # self.driver.find_element(By.ID, "username").send_keys(self.user)
            # self.driver.find_element(By.ID, "password").send_keys(self.password)
            self.driver.find_element(By.ID, "login").click()
            print("Login button clicked.")

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "security-release-yes"))
            )
            self.driver.find_element(By.ID, "security-release-yes").click()
            # Wait for the page to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "agency-picker"))
            )

            print("Login successful.")
        except Exception as e:
            print(f"Login failed: {e}")
            # print stack trace
            traceback.print_exc()

    def list_incidents(self):
        try:
            self.driver.get(self.incidentsUrl)
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "incidentlist"))
            )
        except TimeoutException:
            print("Timeout while waiting for the incident list to load.")
            return
        
        self.get_incidents()

    def get_incidents(self):
        pass


# To connect to an existing browser, first start Chrome with the remote debugging port:
# ```
# First, shut down Chrome
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
# ```


if __name__ == "__main__":
    it = ImageTrend()
    it.connect_to_existing_chrome()
