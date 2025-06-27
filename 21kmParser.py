import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

def scrape_page():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    participant_rows = soup.find_all('tr', class_='results-body')
    data = []
    for participant_row in participant_rows:
        name_span = participant_row.find('span', class_='full-name')
        name = name_span.a.text.strip()

        gender_span = participant_row.find('span', text=lambda text: text and text.strip() in ['М', 'Ж'])
        gender = gender_span.text.strip() if gender_span else None

        age_span = participant_row.find('span', text=lambda text: text and (
                    text.strip().endswith('лет') or text.strip().endswith('год') or text.strip().endswith('года')))
        age = age_span.text.strip() if age_span else None

        time_span = participant_row.find('span', {'data-bind': 'text: absoluteResultFormattedValue'})
        time = time_span.text.strip() if time_span else None

        data.append([name, gender, age, time])

    return data


def scrape_all_pages(url):
    driver.get(url)
    while True:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'show-more'))
            )
            show_more_button = driver.find_element(By.CLASS_NAME, 'show-more')

            if show_more_button.is_displayed() and show_more_button.is_enabled():
                driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(2)
            else:
                break
        except Exception:
            break

    return scrape_page()


def write_to_csv(data):
    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Gender', 'Age', 'Time'])
        writer.writerows(data)

base_url = "https://nomadsport.net/event/SLR2023/results/21km"
scraped_data = scrape_all_pages(base_url)
write_to_csv(scraped_data)

driver.quit()
