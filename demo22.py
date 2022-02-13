from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import os, sys
import time,requests
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
audioToText
    delayTime = 2
    audioToTextDelay = 10

capchaPass 
    filename = '1.mp3'
    googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'

get_url 
    byPassUrl = 'https://www.google.com/recaptcha/api2/demo'
"""


def audioToText(driver, file):

    # -----------------------------------------------------------------
    audioToTextDelay = 10
    googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
    # -----------------------------------------------------------------

    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])

    driver.get(googleIBMLink)
    # Upload file
    time.sleep(1)

    # Upload file
    time.sleep(1)
    root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(file)

    # # Audio to text is processing
    # delayTime = 10
    # time.sleep(delayTime)
    # #btn.send_keys(path)

    # Audio to text is processing
    time.sleep(audioToTextDelay)
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name('span')
    result = " ".join([each.text for each in text])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # print(result)
    return result


def saveFile(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


def driver_init(SeleniumCheckerOFF=True, SeleniumCheckerOFF_2=True):
    # Selenium checker OFF - before ChromeDriver
    # if Site find Selenium and give ReCAPTCHA, SeleniumCheckerOFF must be True
    # That turn off the flags if selenium usage.

    option = webdriver.ChromeOptions()
    #
    #https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904
    if SeleniumCheckerOFF:
        option.add_argument('--disable-blink-features=AutomationControlled')


    if SeleniumCheckerOFF_2:
        # Selenium checker OFF - before ChromeDriver ----------------------
        # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904

        option.add_argument("start-maximized")
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        # ------------------------------------------------------------------

    option.add_argument('--disable-notifications')
    option.add_argument("--mute-audio")
    # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    ###option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
    return option


def get_url(option):

    # -----------------------------------------------------------------
    byPassUrl = 'https://www.google.com/recaptcha/api2/demo'
    # -----------------------------------------------------------------

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    driver.get(byPassUrl)
    return driver


def ReCaptchaPass(driver):

    # -----------------------------------------------------------------
    delayTime = 2
    filename = '1.mp3'
    # -----------------------------------------------------------------
    time.sleep(1)
    try:
        # googleClass = driver.find_elements_by_class_name('g-recaptcha')[0]
        googleClass = driver.find_element_by_class_name('g-recaptcha')
    except Exception as err:
        Error = str(err).split('\n')[0]
        print('ReCaptchaPass(driver) - Error:', Error)
        return False
        # return True
    time.sleep(2)
    outeriframe = googleClass.find_element_by_tag_name('iframe')
    time.sleep(1)
    outeriframe.click()
    time.sleep(2)
    allIframesLen = driver.find_elements_by_tag_name('iframe')
    time.sleep(1)
    audioBtnFound = False
    audioBtnIndex = -1
    # print(f'{len(allIframesLen)=}')
    for index in range(len(allIframesLen)):
    # for index in reversed(range(len(allIframesLen))):
        driver.switch_to.default_content()
        # -- test ------- Error on empty disable window ReCAPTCHA ---------------
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        # print(f'{index=}')
        # time.sleep(5)
        # time.sleep(2)
        time.sleep(1)
        # -- test - end - Error on empty disable window ReCAPTCHA ---------------
        iframe = driver.find_elements_by_tag_name('iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            # print('ReCapchaPass (try Exception): Audio Button not founded')
            pass
    if audioBtnFound:
        try:
            while True:
                href = driver.find_element_by_id('audio-source').get_attribute('src')
                response = requests.get(href, stream=True)
                saveFile(response,filename)

                response = audioToText(driver, os.getcwd() + '/' + filename)
                print(response)
                driver.switch_to.default_content()

                iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)
                inputbtn = driver.find_element_by_id('audio-response')

                inputbtn.send_keys(response)
                inputbtn.send_keys(Keys.ENTER)
                time.sleep(2)
                errorMsg = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
                if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
                    print("Success")
                    return True
        except Exception as e:
                print(e)
                print('Caught. Need to change proxy now')
    else:
        print('Button not found. This should not happen.')
    return False

def after_init(driver, SeleniumCheckerOFF=True):
    # Selenium checker OFF - after ChromeDriver
    # if Site find Selenium and give ReCAPTCHA, SeleniumCheckerOFF must be True
    # That turn off the flags if selenium usage.

    if SeleniumCheckerOFF:
        # Selenium checker OFF - after ChromeDriver ------------------------
        # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        print(driver.execute_script("return navigator.userAgent;"))
        # ------------------------------------------------------------------


if __name__ == '__main__':
    option = driver_init(True, False)
    driver = get_url(option)
    after_init(driver, False)
    if ReCaptchaPass(driver):
        print('Password verified!')
    else:
        print('Password not verified...')
    # driver.close()
    # driver.quit()
