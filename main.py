from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Configure Selenium to use Chrome in headless mode
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your chromedriver executable
chromedriver_path = "./chromedriver"  # Update this path

# Initialize the WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(
  service=service, options=chrome_options
)

# Step size for pagination (Google Scholar shows 10 results per page)
STEP = 10

# Base URL pattern with pagination
# GRPO
BASE_URL = "https://scholar.google.com/scholar?start={}&hl=en&as_sdt=2005&sciodt=0,5&cites=10831144174319627990&scipsc="
# End page index (last page is 990, so max start=990)
MAX_PAGE = 190

# DPO
BASE_URL = "https://scholar.google.com.tw/scholar?start={}&hl=en&as_sdt=2005&sciodt=0,5&cites=9445085131248455366&scipsc="
MAX_PAGE = 990

# Storage for citation data
citations = []

# Scraping loop (pagination)
# Open CSV file in append mode
with open(
  "dpo_citations.csv", "a", newline="", encoding="utf-8"
) as file:
  writer = csv.writer(file)
  writer.writerow(["Title", "Cited By", "URL"])

  # Scraping loop (pagination)
  for start in range(0, MAX_PAGE + 1, STEP):
    url = BASE_URL.format(start)
    print(f"Scraping: {url}")

    driver.get(url)
    time.sleep(5)  # Allow page to load

    # Detect CAPTCHA and allow manual resolution
    if "not a robot" in driver.page_source:
      print(
        "🔴 CAPTCHA detected! Please solve it manually in the browser..."
      )
      while (
        "Please show you're not a robot" in driver.page_source
      ):
        time.sleep(5)  # Wait until CAPTCHA is solved manually

    # Extract citation entries using XPath
    entries = driver.find_elements(
      By.XPATH, "//div[@class='gs_r gs_or gs_scl']"
    )

    for entry in entries:
      try:
        # Extract title using XPath
        title_tag = entry.find_element(
          By.XPATH, ".//h3[@class='gs_rt']/a"
        )
        title = title_tag.text if title_tag else "No title"

        # Extract URL using XPath
        url = (
          title_tag.get_attribute("href")
          if title_tag
          else "No URL"
        )

        # Extract 'Cited by' count using XPath
        try:
          cited_by_tag = entry.find_element(
            By.XPATH, ".//a[contains(text(), 'Cited by')]"
          )
          cited_by = (
            cited_by_tag.text if cited_by_tag else "Cited by 0"
          )
          cited_by_ind = cited_by.find("by") + 2
          cited_by = int(cited_by[cited_by_ind:].strip())
        except:
          cited_by = 0

        # Store data
        citations.append([title, cited_by, url])
        writer.writerow(
          [title, cited_by, url]
        )  # Append each entry immediately to CSV

      except Exception as e:
        print(f"⚠️ Error extracting data: {e}")

    # Simulate user interaction (scroll, click) to extend session
    driver.execute_script(
      "window.scrollBy(0, 500);"
    )  # Scroll down slightly

    print(f"✅ Scraped {len(citations)} entries so far...")

    # Delay to prevent Google from blocking requests
    time.sleep(5)

print(
  f"🎉 Scraped {len(citations)} citation entries and saved to citations.csv."
)

# Close the browser
driver.quit()
