from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
# Loading CSV with Data
file = pd.read_csv("./Files/Cleaned_Emotion.csv", usecols=["question", "answer"])

# with open("Files/human_chat.txt", encoding="UTF-8") as myfile:
#     data = myfile.readlines()

# Reformatting dataframe data to new dataframe
# final_data = pd.DataFrame(columns=["Name", "Line"])
# for i in range(len(data)):
#     row = data[i].split(":")[-1].strip()
#     if "<REDACTED_TERM>" in row or "<REDACTED_LINK>" in row:
#         last_row_ind = len(final_data) - 1
#         final_data.drop(final_data.index[last_row_ind])
#         continue

#     clean_pattern = re.compile('[^a-zA-Z0-9\.,;:?!\'\" ]+')
#     row = clean_pattern.sub('', row)
#     if i % 2 == 0:
#         final_data = final_data.append(
#             {"Name": "User", "Line": row}, ignore_index=True)
#     else:
#         final_data = final_data.append(
#             {"Name": "Mai", "Line": row}, ignore_index=True)
        
# file = final_data

# DataFrame for Storing Responses
responses = pd.DataFrame(columns=file.columns)

# Getting Latest Drivers
option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument('--allow-running-insecure-content')

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=option)
driver.implicitly_wait(5)

# Opening the tabs
# Opening Roman Urdu tab
driver.get(
    "https://www.ijunoon.com/transliteration/urdu-to-roman/?type=1622023175553")
Roman_Urdu = driver.window_handles[0]
print("Opened")

# Opening Google Translate
driver.execute_script("window.open('');")
Google_Translate = driver.window_handles[1]
driver.switch_to.window(Google_Translate)
driver.get("https://www.google.com/search?q=translate&oq=translate&aqs=chrome.0.0i131i433i512j0i433i512j0i131i433i512l2j0i512l2j69i60l2.3165j0j9&sourceid=chrome&ie=UTF-8")

# Selecting the from language
From_menu = driver.find_element(By.ID, "tw-sl")
From_menu.click()

lang_list = driver.find_elements(By.CLASS_NAME, "language_list_item")
available_langs = []

for i in lang_list:
    if i.text != '':
        available_langs.append(i.text)
        if i.text == 'English':
            english = i

english.click()

# Selecting the to language
To_menu = driver.find_element(By.ID, "tw-tl")
To_menu.click()

lang_list = driver.find_elements(By.CLASS_NAME, "language_list_item")
available_langs_to = []

for i in lang_list:
    if i.text != '':
        available_langs_to.append(i.text)
        if i.text == 'Urdu':
            urdu = i

urdu.click()

driver.switch_to.window(Google_Translate)


def translate_Urdu_Google(text):
    # Google
    # Finding the text area in Urdu translation site
    text_area = driver.find_element(By.ID, "tw-source-text-ta")
    text_area.send_keys(Keys.CONTROL + 'a')
    text_area.send_keys(Keys.BACK_SPACE)
    text_area.send_keys(text)

    time.sleep(2)

    result_area = driver.find_element(By.ID, "tw-target-text")
    previoustext = result_area.text

    # Finding the translate button on the site
    text_area.send_keys(Keys.RETURN)
    time.sleep(2)

    # Generating Intent Translation
    if EC.text_to_be_present_in_element((By.ID, "tw-target-text"), previoustext):
        time.sleep(5)

    return result_area.text


def translate_roman(text):
    # Finding the text area on Roman Urdu site
    roman_text_area = driver.find_element(By.CLASS_NAME, "translatetext")

    # Adding Intent text to be translated
    roman_text_area.send_keys(Keys.CONTROL + 'a')
    roman_text_area.send_keys(Keys.BACK_SPACE)

    roman_text_area.send_keys(text)

    # Finding the Translate Button
    roman_translate_button = driver.find_element(By.ID, "submit")

    # Translating the text
    result_area = driver.find_element(By.ID, "ctl00_inpageResult")
    previoustext = result_area.text
    roman_translate_button.click()
    time.sleep(2)

    # Finding the translation
    if EC.text_to_be_present_in_element((By.ID, "ctl00_inpageResult"), previoustext):
        time.sleep(5)

    return driver.find_element(By.ID, "ctl00_inpageResult").text

# 309, 
print("Starting Translation")
max_index = 35000
fname = "Emotion_Complete_" + str(max_index//100) +".xlsx"

print(fname)
for index, row in file.iterrows():

    if index <=max_index-101 or index >=max_index:
        continue

    print("Index:", index)
    Urdu_Intent_Result = {}
    for i in file.columns:

        clean_pattern = re.compile('[^a-zA-Z0-9\.,;:?!\'\" ]+')
        user = clean_pattern.sub('', str(row[i]))
        # Urdu Website
        Urdu_Intent_Result[i] = translate_Urdu_Google(user)

    # Roman Urdu Website
    # Switching tabs
    driver.switch_to.window(Roman_Urdu)

    Roman_Intent_Result = {}

    for i in list(Urdu_Intent_Result.keys()):
        Roman_Intent_Result[i] = translate_roman(Urdu_Intent_Result[i])

    # print(row["Intent"])
    # print(row["Response"])
    print(Urdu_Intent_Result)
    # print(Urdu_Response_Result)
    print(Roman_Intent_Result)
    # print(Roman_Response_Result)
    responses = responses.append(Roman_Intent_Result, ignore_index=True)

    driver.switch_to.window(Google_Translate)

    responses.to_excel(fname)
driver.close()
