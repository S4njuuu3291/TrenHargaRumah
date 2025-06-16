import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import random
import os
from time import sleep
import pandas as pd

path = "D:\\chromedriver-win64\\chromedriver.exe"
service = webdriver.chrome.service.Service(path)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
]

user_agent = random.choice(user_agents)

browser = webdriver.Chrome(service=service)

csv_file = "..\\data\\dataset_properti_medan_raw_2.csv"
is_first_write = not os.path.exists(csv_file)

url = "https://www.rumah123.com/jual/cari/?location=medan&propertyTypes=rumah%2Capartemen%2Cruko&page=1"
browser.get(url)

dict_properti = []

try:
    for page in range(0, 500):
        print(f"[INFO] Scraping halaman {page+1}...")

        # Scroll sampai tombol next muncul atau sampai batas max scroll
        max_scroll = 10000
        scroll_step = 2000
        scroll_pos = 0
        wait = WebDriverWait(browser, 1)

        while scroll_pos < max_scroll:
            scroll_pos += scroll_step
            browser.execute_script(f"window.scrollTo(0, {scroll_pos});")
            sleep(random.uniform(0.3, 0.6))

            try:
                button_next = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "a[aria-label='Next page'][rel='next']"))
                )
                print("[INFO] Tombol next ditemukan, stop scroll.")
                break
            except TimeoutException:
                pass

        # Parsing halaman
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        list_property = soup.find_all(
            'div', class_='card-featured__content-wrapper')

        if not list_property:
            print("[WARNING] Tidak ditemukan properti di halaman ini.")
            break

        for property in list_property:
            # Set default semua atribut None supaya kolom lengkap dan tidak tertukar
            result_atribut = {
                'jumlah_kamar_tidur': None,
                'jumlah_kamar_mandi': None,
                'garasi': None,
                'luas_tanah': None,
                'luas_bangunan': None,
            }

            harga_div = property.find(
                'div', class_='card-featured__middle-section__price')
            harga_property = harga_div.strong.get_text(
                strip=True) if harga_div and harga_div.strong else None

            nama_tag = property.find('h2')
            nama_property = nama_tag.get_text(strip=True) if nama_tag else None

            a_tag = property.find(
                'a', href=lambda x: x and '/properti/medan' in x)
            lokasi = None
            if a_tag:
                span_tag = a_tag.find_next_sibling('span')
                if span_tag:
                    lokasi = span_tag.get_text(strip=True)

            # Ambil jenis properti dari badge-depth pertama
            badge_depth_elem = property.find(
                'div', attrs={'data-test-id': 'badge-depth'})
            jenis_properti = badge_depth_elem.get_text(
                strip=True) if badge_depth_elem else None

            # Ambil atribut kamar mandi, kamar tidur, garasi berdasar ikon SVG
            for grid_div in property.find_all('div', class_='attribute-grid'):
                use_tag = grid_div.find('use')
                if use_tag and use_tag.has_attr('xlink:href'):
                    href = use_tag['xlink:href']
                    if 'bed-small' in href:
                        attr_name = 'jumlah_kamar_tidur'
                    elif 'bath-small' in href:
                        attr_name = 'jumlah_kamar_mandi'
                    elif 'car-small' in href:
                        attr_name = 'garasi'
                    else:
                        attr_name = None

                    if attr_name:
                        value_span = grid_div.find(
                            'span', class_='attribute-text')
                        value = value_span.get_text(
                            strip=True) if value_span else None
                        result_atribut[attr_name] = value

            # Ambil luas tanah dan bangunan
            for info_div in property.find_all('div', class_='attribute-info'):
                text = info_div.get_text(strip=True)
                if text.startswith('LT'):
                    lt_span = info_div.find('span')
                    result_atribut['luas_tanah'] = lt_span.get_text(
                        strip=True) if lt_span else None
                elif text.startswith('LB'):
                    lb_span = info_div.find('span')
                    result_atribut['luas_bangunan'] = lb_span.get_text(
                        strip=True) if lb_span else None

            properti_data = {
                'nama': nama_property,
                'lokasi': lokasi,
                'harga': harga_property,
                'jenis_properti': jenis_properti,
                **result_atribut
            }

            dict_properti.append(properti_data)

        # Simpan ke CSV
        df = pd.DataFrame(dict_properti)
        df.to_csv(csv_file, mode='a', index=False,
                  header=is_first_write, encoding='utf-8')
        print(
            f"[INFO] Data halaman {page+1} tersimpan ke CSV, jumlah baris: {len(df)}")
        is_first_write = False
        dict_properti.clear()

        # Klik tombol next
        try:
            button_next = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a[aria-label='Next page'][rel='next']"))
            )
            browser.execute_script(
                "arguments[0].scrollIntoView();", button_next)
            sleep(random.uniform(1.5, 3))
            try:
                button_next.click()
            except ElementClickInterceptedException:
                browser.execute_script("arguments[0].click();", button_next)
            sleep(random.uniform(1.5, 3))
        except TimeoutException:
            print("[INFO] Tombol next tidak ditemukan, scraping selesai.")
            break
finally:
    browser.quit()
