import pandas as pd
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Define XPath parsers for each domain
def parse_openreview(driver):
    return driver.find_element(By.XPATH, "//div[contains(@class, 'note-content')]").text

def parse_neurips(driver):
    return driver.find_element(By.XPATH, "//div[@class='container-fluid']//p").text

def parse_aaai(driver):
    return driver.find_element(By.XPATH, "//section[@class='item abstract']").text

def parse_arxiv(driver):
    return driver.find_element(By.XPATH, "//blockquote[contains(@class, 'abstract mathjax')]").text

def parse_acm(driver):
    return driver.find_element(By.XPATH, "//section[@id='abstract']").text

def parse_cvpr(driver):
    return driver.find_element(By.XPATH, "//div[@id='abstract']").text

def parse_springer(driver):
    return driver.find_element(By.XPATH, "//section[contains(@aria-labelledby, 'Abs1')]" ).text

def parse_science(driver):
    return driver.find_element(By.XPATH, "//section[contains(@id, 'abstract')]").text

def parse_ieee(driver):
    return driver.find_element(By.XPATH, "//div[contains(@class, 'abstract-text')]").text

def parse_acl(driver):
    return driver.find_element(By.XPATH, "//div[contains(@class, 'acl-abstract')]").text

def parse_blank(driver):
    return ''

# Mapping domain to parser function
PARSER_MAP = {
    "arxiv": parse_arxiv,
    "aclanthology": parse_acl,
    "openreview": parse_openreview,
    "acm": parse_acm,
    "springer": parse_springer,
    "aaai": parse_aaai,
    "neurips": parse_neurips,
    "thecvf": parse_cvpr,
    "ieee": parse_ieee,
    "science": parse_science,
}

# Load CSV file
input_csv_path = "./grpo_citations.csv"
output_csv_path = "./grpo_abstract.csv"
input_csv_path = "./dpo_citations.csv"
output_csv_path = "./dpo_abstract.csv"
df = pd.read_csv(input_csv_path)

def fetch_abstract(row):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service("./chromedriver")  # Update path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = row["URL"]
    domain = url.split("/")[2].split(".")[-2]
    print(f"Fetching {domain}: {url}")
    driver.get(url)
    time.sleep(2)  # Wait for page to load
    
    try:
        parser = PARSER_MAP.get(domain, parse_blank)
        abstract = parser(driver)
    except Exception as e:
        print(f"⚠️ Failed to extract abstract from {domain}: {e}")
        abstract = ''
    
    driver.quit()
    return abstract

# Run extraction in parallel with up to 20 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    df["Abstract"] = list(executor.map(fetch_abstract, [row for _, row in df.iterrows()]))

# Save to new CSV file
df.to_csv(output_csv_path, index=False)
print(f"🎉 Process completed. Results saved to {output_csv_path}.")

