import random
import undetected_chromedriver as uc
import requests
import time
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

inStock_urls = {
    'birmingham': 'https://discord.com/api/webhooks/1334484492991336481/0WlxONG7M3q83i4f2C-RcvbXZ7Ol7jePN8pN5Gugd9xjEY_T3l5byuYNgXQrvb16w0AY',
    'leicester': 'https://discord.com/api/webhooks/1334484511534092368/V5A4sh8lYaeFk46POiOPJYwDBJJa2wgyt8ZeYeEaM_eHD60lPkSc-pPHIR94FqhL5Oti',
    'lincoln': 'https://discord.com/api/webhooks/1334484503347068958/aenPLYX8L1R3Sw8Uy8PlTe_h4MFUjnkQIgXITu5kYGKQtetpBpBtuMHR8p-_AvvrKPUF',
    'mansfield': 'https://discord.com/api/webhooks/1334484505976639580/fNMF4WCBeXgdlU2byGLiEGrGEVdb3kUtyT24Vl48ZoqM8Pxk_NO4uRaSKr3l-U2a1Tsy',
    'nottingham': 'https://discord.com/api/webhooks/1334484500603731968/hyRrrq2ibJPEFm5BTIN3qovXiVxMiKhvnsHMne_2mDYoc-K7A6d-XoScoPHBMGvjG4_f',
    'ripley': 'https://discord.com/api/webhooks/1334484848676569161/DT2mlkK3gnJfpsr1J2kJNWNf_cq8kQGyr0fo9UXxEQ8XCy_A7Wz1EkL05E2ICfYi5LxP'
    }
outOfStock_url = 'https://discord.com/api/webhooks/1334155791535444048/16GO8H21QD46FiJyU2E0syKez5mKeKIWtuSf3Gf0KcApAlOeafNXEcDyfTtZWu2kc4CA'
# outOfStock_url = 'https://discord.com/api/webhooks/1333578983803060275/k3lB3MSspKusRcacoAP-1LU3pTDitmCBi1e7G7UkKKinyeQIdaId5m1cUUtroNeNZ1lb'

def send_discord_message(message, webhook_url):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print(f"Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")

def send_discord_message_with_image(stock_availability, product_name, product_url, city, image_url, sale_price, price):
    stock_status = "Yes" if stock_availability == 'In stock' or stock_availability == 'Low stock' else "No"
    webhook_url = inStock_urls[city.lower()] if stock_status == "Yes" else outOfStock_url
    color = 0x00ff00 if stock_status == "Yes" else 0xff0000
    if image_url == 'Not Found':
        image_url = 'https://cdn.discordapp.com/attachments/1334484492991336481/1334484511534092368/unknown.png'
    try:
        embed = {
            "title": product_name,
            "description": f"**Stock Status:** {stock_status}\n**Location:** {city.capitalize()}\n**Price:** £{sale_price} (£{price})\n[View Product]({product_url})",
            "color": color,
            "thumbnail": {"url": image_url}
        }
        payload = {"embeds": [embed]}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("✅ Message sent successfully!")
        else:
            print(f"⚠️ Failed to send message. Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def get_undetected_driver(headless=False, max_retries=3):
    try:
        # User-agent rotation
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/132.0.6834.100 Mobile/15E148 Safari/604.1"
        ]
        random_user_agent = random.choice(user_agents)

        options = uc.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={random_user_agent}")

        if not headless:
            options.add_argument("--start-maximized")
        else:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        # Initialize undetected Chrome driver
        driver = uc.Chrome(options=options)
        time.sleep(2)  # Allow the browser to fully initialize

        # Additional fingerprinting tweaks (remove WebDriver flag)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )
        return driver

    except Exception as e:
        print(f"Error: {e}")
        if max_retries > 0:
            print(f"Retrying... Attempts left: {max_retries}")
            time.sleep(2)
            return get_undetected_driver(headless=headless, max_retries=max_retries - 1)
        else:
            print("Max retries exceeded. Could not create the driver.")
            return None

def get_element_attribute(driver, by_locator, attribute_name):
    element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(by_locator))
    return element.get_attribute(attribute_name)

def input_element(driver, by_locator, text):
    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(by_locator))
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})", element)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(by_locator)).send_keys(Keys.CONTROL, '\A',
                                                                                            '\b')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

def click_using_js(driver, by_locator):
    element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(by_locator))
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})", element)
    driver.execute_script("arguments[0].click();", element)


def status_element(driver):
    try:
        status_ele = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "(//p[@class='store-product-item__stock-status'])[1]")))
        if status_ele:
            return True
    except:
        return False

def product_is_available(driver):
    product_availability = []
    print('checking stock status')
    if status_element:
        all_status = driver.find_elements(By.XPATH, "//p[@class='store-product-item__stock-status']")
        for status in all_status:
            if 'In stock' in status.text or 'Low stock' in status.text or 'Out of stock' in status.text:
                product_availability.append(status.text)
        if 'In stock' in product_availability:
            return 'In stock'
        elif 'Low stock' in product_availability:
            return 'Low stock'
        elif 'Out of stock' in product_availability:
            return 'Out of stock'
        else:
            return False
    else:
        return False

def get_element_text(driver, by_locator):
    element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(by_locator))
    return element.text

def accept_cookies(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept Cookies']"))).click()
        print("Cookies accepted!")
    except:
        pass

def get_image_url(driver):
    try:
        url = get_element_attribute(driver, (By.XPATH, "(//div[contains(@class,'product-images__container')]//img)[1]"), 'src')
        print('image url fetched')
        return url
    except:
        return 'Not Found'

def error_message(driver):
    try:
        get_element_text(driver, (By.XPATH, "//div[@class='error-message']"))
        return True
    except:
        pass

def main():
    city = input("Enter the city name(e.g. Nottingham): ")
    driver = get_undetected_driver()
    current_driver_count = 0
    driver_interval = 45
    try:
        with open('sku.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                sku, sale_price, price = row[0], row[1], row[2]
                with open('done_sku.txt', 'r', encoding='utf-8') as f1:
                    if sku in f1.read():
                        continue
                url = f'https://superdrug.com/p/{sku}'
                driver.get(url)
                time.sleep(2)
                if error_message(driver):
                    continue
                if not driver.current_url.endswith(sku):
                    driver.quit()
                    driver = get_undetected_driver()
                    continue
                accept_cookies(driver)
                product_name = get_element_text(driver, (By.XPATH, "//div[@class='product-details-title__text'] | //h1[@class='product-details-title__text']"))
                image_url = get_image_url(driver)
                try:
                    click_using_js(driver, (By.XPATH, "//span[text()=' See Store Availability ']/parent::button"))
                    print('availability button clicked')
                except:
                    continue
                input_element(driver, (By.XPATH, "//input[@name='search']"), city)
                click_using_js(driver, (By.XPATH, "//span[text()='Check ']/parent::button"))
                time.sleep(2)
                stock_availability = product_is_available(driver)
                if not stock_availability:
                    continue
                send_discord_message_with_image(stock_availability, product_name, url, city, image_url, sale_price, price)
                with open('done_sku.txt', 'a', encoding='utf-8') as f1:
                    f1.write(f'{sku}\n')
                current_driver_count += 1
                if current_driver_count % driver_interval == 0:
                    driver.quit()
                    driver = get_undetected_driver()
                    print('New driver launched')
    except Exception as e:
        print(e),
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
