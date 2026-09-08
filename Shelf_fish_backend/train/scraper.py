import undetected_chromedriver as uc
import time
import os
import base64
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from random import uniform
import csv
import requests
import itertools
import functools
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil

search_queries = [
    "package image transparent background",
    "front pack",
    "grocery store photo",
    "in hand",
    "on shelf",
    "on white background",
    "on table",
    "back label",
    "advertisement",
]
XPath = f"//div[@role='main']//img[@data-deferred or @src]"

times = []
fastest_time = 0
slowest_time = float('inf')
average_time = 0



USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
]

ua_iterator = itertools.cycle(USER_AGENTS)
not_searched_queries = []

def time_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time= time.perf_counter()
        elapsed = end_time - start_time
        times.append(elapsed)
        minutes, seconds = divmod(elapsed, 60)
        print(f"Execution time for {func.__name__}: {int(minutes)}m {int(seconds)}s")
        return result
    return wrapper

def get_valid_count(driver, images):
    valid_count = 0
    for img in images:
        try:
            w = driver.execute_script("return arguments[0].naturalWidth;", img)
            h = driver.execute_script("return arguments[0].naturalHeight;", img)
            if w >=100 and h >=100:
                valid_count +=1
        except Exception as e:
            continue
    return valid_count

def get_valid_src(driver, min_dim=100):
    js = """
    const minDim = arguments[0];
    const imgs = Array.from(document.querySelectorAll("div[role='main'] img"));
    return imgs
        .filter(img => img.naturalWidth >= minDim && img.naturalHeight >= minDim)
        .map(img => img.src)
        .filter(src => src && (src.startsWith("http") || src.startsWith("data:image")));
    """
    return driver.execute_script(js, min_dim);

@time_execution
def scrape_images(driver, query, item, target_num):
    os.makedirs(f"images/{item}", exist_ok=True)
    os.makedirs("all_images", exist_ok=True)

    ua_string = next(ua_iterator)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua_string})
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"

    try:
        driver.get(search_url)
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='main']"))
            )
            print(f"Search Results loaded for {item}")
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, 800);")
                time.sleep(uniform(0.3, 0.5))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(uniform(0.4, 0.8))
                try:
                    show_more = driver.find_element(By.XPATH, "//input[@type='button' and @value='Show more results'] | //button[contains(., 'Show more results')] | //input[@type='button' and @value='Next'] | //button[contains(., 'Next')] | //input[@type='button' and @value='More results'] | //button[contains(., 'More results')] | //input[@type='button' and @value='See more anyway'] | //button[contains(., 'See more anyway')] | //span[contains(., 'Show more results')] | //span[contains(., 'Next')] | //span[contains(., 'More results')] | //span[contains(., 'See more anyway')]")
                    if show_more.is_displayed():
                        driver.execute_script("arguments[0].click();", show_more)
                        print(f"Clicked 'Show more results' for {item}")
                except NoSuchElementException:
                    pass
                valid_srcs = get_valid_src(driver)
                if len(valid_srcs) >= target_num:
                    print(f"Found {len(valid_srcs)} valid images for {item}. Stopping scroll...")
                    break
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print(f"Reached the end of the page for {item}. Stopping scroll...")
                    print(f"Found {len(valid_srcs)} valid images for {item}, target is {target_num}.")
                    break
                last_height = new_height

            time.sleep(uniform(0.1, 0.5))

            images = driver.find_elements(By.XPATH, XPath)
            all_src = get_valid_src(driver)
            
            def fetch_image(src):
                if src.startswith("data:image"):
                    try:
                        _, encoded = src.split(",", 1)
                        return base64.b64decode(encoded)
                    except Exception as e:
                        return None
                elif src.startswith("http"):
                    headers = {"User-Agent": ua_string}
                    try:
                        response = requests.get(src, headers=headers, timeout=10)
                        if response.status_code==200:
                            return response.content
                    except Exception as e:
                        return None
                return None
            
            saved_count = 0

            with ThreadPoolExecutor(max_workers=16) as executor:
                future_to_src = {executor.submit(fetch_image, src): src for src in all_src}

                for future in as_completed(future_to_src):
                    if saved_count >= target_num:
                        break

                    img_data = future.result()
                    if img_data:
                        saved_count += 1
                        filename_1 = f"images/{item}/{query}_{str(saved_count).zfill(6)}.jpg"
                        filename_2 = f"all_images/{query}_{str(saved_count).zfill(6)}.jpg"

                        with open(filename_1, "wb") as f1:
                            f1.write(img_data)
                            shutil.copyfile(filename_1, filename_2)
                        print(f"[{saved_count}/{target_num}] Downloaded {filename_1}")
                            

                

        
        
        except TimeoutException as e:
            print(f"Timed out loading image search result: {e}")
            not_searched_queries.append({
                "item" : item,
                "query": query
            })
            os.makedirs("timeouts", exist_ok=True)
            driver.save_screenshot(f"timeouts/{query}_timeout.png")
            print(f"Used UA string {ua_string} for query '{query}'")
            return

    except Exception as e:
        print(f"Error occurred while scraping images for query '{query}': {e}")
        not_searched_queries.append({
                        "item" : item,
                        "query": query
        })


def load_items_from_csv(path):
    items = []

    if not os.path.exists(path):
        print(f"CSV file not found at {path}")
        return items

    with open(path, "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            if "Item Name" in row and row["Item Name"].strip():
                items.append(row["Item Name"])

    return items

def remove_item(path, item):
    if not os.path.exists(path):
        print(f"CSV file not found at {path}")
        return

    with open(path, "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    item_clean = item.strip().lower()
    updated_rows = [
        row for row in rows
        if row.get("Item Name","").strip().lower() != item_clean
    ]
    if len(rows) == len(updated_rows):
        print(f"Item {item} not found")
        return 

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"{item} removed from {path}")


if __name__ == "__main__":
    PATH = "list.csv"

    # item_list = load_items_from_csv(PATH)
    item_list = ["Oreo"]

    if not item_list:
        print(f"No item found in {PATH}")
        exit()

    print(f"Total items in CSV: {len(item_list)}")

    options = uc.ChromeOptions()
    options.add_argument("--window-size=1366,640")
    # options.add_argument("--headless-new")

    print("Launching global browser instance...")

    driver = uc.Chrome(options=options, version_main=151)
    start_time_global = time.perf_counter()

    try:

        for item in item_list:
            print(f"\n---Starting {item}---")
            for query in search_queries:
                scrape_images(driver, f"{item} {query}", item, 125)

            print(f"Finished scraping all queries for {item}...")
            print(f"Removing {item} from {PATH}")
            remove_item(PATH, item)
            print(f"\n---Finished {item}---\n")
            

    finally:
        print("Closing browser instance")
        end_time_global = time.perf_counter()

    total_time_global = end_time_global - start_time_global
    hours, rem = divmod(total_time_global, 3600)
    minutes, seconds = divmod(rem, 60)
    
    print(f"Total time taken for all items: {int(hours)}h {int(minutes)}m {int(seconds)}s")

    average_time = sum(times) / len(times) if times else 0
    max_time = max(times) if times else 0
    min_time = min(times) if times else 0

    print(f"Average time per item: {average_time:.2f}s")
    print(f"Max time taken for an item: {max_time:.2f}s")
    print(f"Min time taken for an item: {min_time:.2f}s")

    if len(not_searched_queries) > 0:
        print(f"\n\nThe following queries were not searched successfully:")

        for query in not_searched_queries:
            print(f"- Item: {query['item']}, Query: {query['query']}")

        headers= ["item", "query"]

        with open("not_searched_queries.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(not_searched_queries)