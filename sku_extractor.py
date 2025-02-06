import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

def extract_product_info(string):
    match = re.search(r"Now:\s*£([\d.]+)", string)
    now_price = match.group(1) if match else None
    match = re.search(r"Was:\s*£([\d.]+)", string)
    was_price = match.group(1) if match else None
    match = re.search(r'SKU:\s*(\d+)', string)
    sku = match.group(1) if match else None
    return sku, now_price, was_price

def main(driver):
    fetched_data = []
    num, num1 = 0, 500
    driver.get("https://www.superdrug.com/pricing")
    all_p = driver.find_elements(By.XPATH, "//p[contains(text(), 'SKU:')]")
    for p in all_p:
        text = p.text
        if '€' in text:
            continue
        sku, now_price, was_price = extract_product_info(text)
        if sku:
            fetched_data.append([sku, now_price, was_price])
        num += 1
        if num == num1:
            print(f"Extracted {num1} records")
            num1 += 500
    with open("sku.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(fetched_data)
    print("✅ Data extraction complete! Saved to sku.csv")

if __name__ == "__main__":
    driver = webdriver.Chrome()
    main(driver)
    driver.quit()
