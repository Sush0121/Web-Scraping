from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

# 📁 Generate a unique log file name with timestamp
log_filename = f"meta_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

# ⏱️ Generate log message timestamp
def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# 📝 Function to write a log entry
def log_to_file(message):
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp()} {message}\n")

# ------------------- Script Start -------------------

log_to_file("🔧 Setting up Chrome options...")
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

log_to_file("📦 Installing and setting up ChromeDriver...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.rnz.co.nz/"
log_to_file(f"🌐 Navigating to {url} ...")
driver.get(url)

log_to_file(" Waiting for 3 seconds to allow page load...")
time.sleep(3)

log_to_file("🔍 Finding all <meta> tags on the page...")
meta_tags = driver.find_elements(By.TAG_NAME, "meta")
log_to_file(f"📄 Total meta tags found: {len(meta_tags)}")

log_to_file("🧠 Extracting SEO, Open Graph, and Twitter meta tags:")

target_names = ["description", "keywords", "robots"]
target_properties = ["og:title", "og:description", "og:image", "og:url", "og:type",
                     "twitter:title", "twitter:description", "twitter:image"]

found = 0
for index, tag in enumerate(meta_tags):
    name = tag.get_attribute("name")
    prop = tag.get_attribute("property")
    content = tag.get_attribute("content")

    if name and name.lower() in target_names:
        log_to_file(f"🔹 Meta name: {name} | Content: {content}")
        found += 1
    elif prop and prop.lower() in target_properties:
        log_to_file(f"🔸 Meta property: {prop} | Content: {content}")
        found += 1

if found == 0:
    log_to_file("⚠️ No SEO or OG meta tags found.")

log_to_file("🛑 Closing browser...")
driver.quit()
log_to_file("✅ Done.\n")
print(f"✅ Done. Check '{log_filename}' for detailed logs.")
