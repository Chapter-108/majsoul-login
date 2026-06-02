import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

acccounts = int(len(sys.argv[1:])/2)
print(f'Config {acccounts} accounts')
for i in range(acccounts):
    email = sys.argv[1+i]
    passwd = sys.argv[1+i+acccounts]
    print('----------------------------')

    # 雀魂网页端已从 Laya 引擎迁移到 Unity（画布 id: layaCanvas -> unity-canvas，
    # 旧的 HTML 输入框也没了），这里改为等待 canvas 标签 + 直接向画布发送按键。
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("https://game.maj-soul.net/1/")
    print(f'Account {i+1} loading game...')

    try:
        screen = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
    except Exception:
        driver.save_screenshot(f"error_canvas_{i+1}.png")
        driver.quit()
        raise

    sleep(60)  # Unity WebGL 加载比 Laya 慢，留足时间

    # 坐标按窗口 1280x800、新版登录界面校准；雀魂改版后可能需重调
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 350, -135)\
        .click()\
        .perform()
    sleep(2)
    ActionChains(driver).send_keys(email).perform()
    print('Input email successfully')
    sleep(3)

    ActionChains(driver)\
        .move_to_element_with_offset(screen, 350, -50)\
        .click()\
        .perform()
    sleep(3)
    ActionChains(driver).send_keys(passwd).perform()
    print('Input password successfully')
    sleep(3)

    ActionChains(driver)\
        .move_to_element_with_offset(screen, 350, 60)\
        .click()\
        .perform()
    print('Entering game...')

    sleep(60)  # loading...
    driver.save_screenshot(f"login_success_{i+1}.png")
    print(f'Account {i+1} login completed')

    driver.quit()
