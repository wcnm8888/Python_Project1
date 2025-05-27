from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(
    service=Service('chromedriver.exe'),
    options=chrome_options
)

try:
    driver.get("https://bbs.nga.cn/nuke.php?__lib=login&__act=account&login")
    sleep(2)

    # 进入 iframe
    iframe = driver.find_element(By.XPATH, '//iframe[@id="iff"]')
    driver.switch_to.frame(iframe)
    sleep(2)

    # 密码登录流程
    driver.find_element(By.LINK_TEXT, "使用密码登录").click()
    sleep(2)
    driver.find_element(By.ID, 'name').send_keys('Pixel-w')
    driver.find_element(By.ID, 'password').send_keys('123456789wym!')
    driver.find_element(By.XPATH, '//*[@id="main"]/div/a[1]').click()

    # 等待登录完成
    sleep(15)

    cookies = driver.get_cookies()
    for cookie in cookies:
        print(cookie)

    with open('cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)

    print("✅ Cookie 已保存到 cookies.json 文件")

finally:
    driver.quit()
