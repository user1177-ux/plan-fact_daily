from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
from datetime import datetime

# Настройка веб-драйвера для Chrome (безголовый режим)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# Открываем страницу с отчётом
driver.get("https://app.powerbi.com/groups/me/reports/c1a3ebc2-ba77-461c-9b00-6a8d8bbc443e/259964b351242eb072d2?experience=power-bi")

# Ждём загрузки страницы
driver.implicitly_wait(10)

try:
    # Ищем нужную строку по XPath
    row = driver.find_element(By.XPATH, "//td[text()='28 августа 2024 г.']/ancestor::tr")

    # Извлекаем данные из ячеек строки
    cells = row.find_elements(By.TAG_NAME, "td")
    extracted_data = [cell.text for cell in cells]

    # Печатаем данные (для отладки)
    print("Извлечённые данные:", extracted_data)

    # Сохраняем данные в CSV файл
    filename = "extracted_data.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Записываем заголовки, если файл новый
            writer.writerow(["Дата", "Количество заявок", "%", "Записано на пробные", "%", "Посетили пробный", "%", "Заключено контрактов", "%", "Получено денег", "%", "Бюджет", "%"])
        writer.writerow(extracted_data)

finally:
    # Закрываем браузер
    driver.quit()
