# -*- coding: utf-8 -*-
import pprint
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# for selections
from selenium.webdriver.common.by import By

import undetected_chromedriver as UC


def gather(places):
    for place in places:
        driver = UC.Chrome(use_subprocess=True)

        w = WebDriverWait(driver, 15)
        driver.get(f"https://www.numbeo.com/cost-of-living/in/{place}?displayCurrency=GEL")

        w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.data_wide_table.new_bar_table tr')))
        driver.execute_script("window.stop();")

        # html ელემენტების  ცხრილი
        data_table = driver.find_elements(
            By.CSS_SELECTOR, ".data_wide_table.new_bar_table tr")
        rows = []
        for i in data_table:
            try:
                el = i.find_elements(By.CSS_SELECTOR, "td") 
                avg = i.find_element(By.CSS_SELECTOR, ".first_currency").text
                min_ = i.find_element(By.CSS_SELECTOR, ".barTextLeft").text
                max_ = i.find_element(By.CSS_SELECTOR, ".barTextRight").text
                row = [i.text for i in el]
                if row != []:
                    # {"average":row[1].split("-")[0],"min":row[2].split("-")[0], "max":row[2].split("-")[1]}
                    rows.extend([row[0], avg.replace(" GEL","").replace(",",""), min_.replace(",",""), max_.replace(",","")])
            except:
                pass

        names = rows[::4]
        avgs = rows[1::4]
        min_ = rows[2::4]
        max_ = rows[3::4]

        df = pd.DataFrame(names, columns=['სახელი'])
        df["საშუალო"] = avgs
        df["მინიმალური"] = min_
        df["მაქსიმალური"] = max_
        filename = f"{place}_data.xlsx"
        df.to_excel(filename)
