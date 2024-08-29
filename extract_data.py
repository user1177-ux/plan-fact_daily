from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
from datetime import datetime

# Настройка веб-драйвера для Chrome (безголовый режим)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    # Открываем страницу с формой авторизации
    driver.get("https://твой-адрес-с-формой-авторизации")

    # Ждём появления поля ввода электронной почты
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Вводим логин
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys("твой_логин")

    # Отправляем форму
    email_field.send_keys(Keys.RETURN)

    # Ждём загрузки следующей страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[text()='28 августа 2024 г.']")))

    # Открываем страницу с отчётом после авторизации
    driver.get("https://app.powerbi.com/groups/me/reports/c1a3ebc2-ba77-461c-9b00-6a8d8bbc443e/259964b351242eb072d2?experience=power-bi")

    # Ждём загрузки страницы
    driver.implicitly_wait(10)

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
