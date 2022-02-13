# --------------------------------------------------------------------------------
# UPWORK PARSER
#
# MADE BY ALEXEY LOIK
# 2022-02-10  VERSION 1.0
# --------------------------------------------------------------------------------

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains

# my function
from translator import translate

# import urllib.request
from bs4 import BeautifulSoup
from lxml import html

from time import sleep
import datetime

# import logging
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     handlers=[logging.FileHandler('./upwork_scraper.log'), logging.StreamHandler()])

TIME_SLEEP = (2, 6)
delayTime  = 2
waitTime   = 50

# All - IT & Networking
# python  https://www.upwork.com/nx/jobs/search/?q=python&sort=recency&user_location_match=2&category2_uid=531770282580668419&page=4
# all https://www.upwork.com/nx/jobs/search/?sort=recency&user_location_match=2&category2_uid=531770282580668419&page=4
# subcategory  https://www.upwork.com/nx/jobs/search/?sort=recency&user_location_match=2&subcategory2_uid=531770282589057033,531770282589057037,531770282589057035

# SEARCH_URL = 'https://www.upwork.com/nx/jobs/search/?page=' # '2&sort=recency'
SEARCH_URL = "https://www.upwork.com/nx/jobs/search/?sort=recency&user_location_match=2&category2_uid=531770282580668419&page="
SEARCH_CAT_URL = "https://www.upwork.com/o/jobs/browse/c/%s/?page="

cats = {
    'All Categories': 'all',
    'Data Science & Analytics': 'data-science-analytics',
    'Web, Mobile & Software Dev': 'web-mobile-software-dev',
    'IT & Networking': 'it-networking',
    'Engineering & Architecture ': 'engineering-architecture',
    'Design & Creative': 'design-creative',
    'Writing': 'writing',
    'Translation': 'translation',
    'Legal': 'legal',
    'Admin Support': 'admin-support',
    'Customer Service': 'customer-service',
    'Sales & Marketing': 'sales-marketing',
    'Accounting & Consulting': 'accounting-consulting'
}


URL = 'https://www.upwork.com'

import demo22 as demo
import GoogleLogIn as GL
from random import uniform


def CheckReCAPTCHA(driver, url=None):
    # print('CheckReCAPTCHA(driver): running...' )
    main_page = driver.page_source
    soup = BeautifulSoup(main_page, 'lxml')

    ## Save HTML page to file -------------------------
    # with open('page.html', 'w', encoding='utf-8') as file:
    #     file.write(main_page)
    #     print('Save page to file PAGE.HTML')
    # -------------------------------------------------
    count = 1
    MAX_COUNT = 5
    while True:
        ref = soup.find('a', class_='g-recaptcha')
        ref2 = soup.find('div', class_='g-recaptcha')
        if ref or ref2:
            print('BeautifulSoup: ReCAPTCHA founded!')
            if demo.ReCaptchaPass(driver):
                print('Password verified!')
            else:
                print('Password NOT verified...')
                if count > MAX_COUNT:
                    print('Exit from CheckReCAPTCHA()')
                    return False
                else:
                    print(f'Try again[{count}/{MAX_COUNT}]')
                    if url:
                        driver.get(url)
                        main_page = driver.page_source
                        soup = BeautifulSoup(main_page, 'lxml')
        else:
            print('BeautifulSoup: ReCAPTCHA NOT founded')
            #
            return True
            #
        sleep(delayTime/10)
        count += 1

    return True


def local_init(url):
    print('- driver_init()')
    option = demo.driver_init(True, False)

    ## Add User acount in to chrome browser -------------------------------
    ## https://stackoverflow.com/questions/31062789/how-to-load-default-profile-in-chrome-using-python-selenium-webdriver
    # C:\Users\Дом\AppData\Local\Google\Chrome\User Data\Default
    # option.add_argument(r"user-data-dir=C:\Users\Дом\AppData\Local\Google\Chrome\User Data\Default")
    # option.add_argument( 'user-data-dir=C:\\Users\\Дом\\AppData\\Local\\Google\\Chrome\\User Data\\' )

    option.add_argument(r"user-data-dir=C:\Users\Дом\AppData\Local\Google\Chrome\User Data\Profile 2")

    option.add_argument('--disable-web-security')
    option.add_argument('--allow-running-insecure-content')

    # # USE THIS IF YOU NEED TO HAVE MULTIPLE PROFILES
    # option.add_argument('--profile-directory=Default')

    # # ----------------------------------------------------------------------
    print('-')
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=option)
    demo.after_init(driver, False)
    return driver


def GoogleLogin(driver):
    # Start --- Login in google account block -------------------------------------------
    # https://stackoverflow.com/questions/44856887/log-into-gmail-using-selenium-in-python
    import auth_data as data
    driver.get("https://accounts.google.com/signin")
    # driver.get(
    #     "https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier")
    email_phone = driver.find_element(By.XPATH, "//input[@id='identifierId']")
    email_phone.send_keys(data.GOOGLE_LOGIN)
    driver.find_element(By.ID, "identifierNext").click()
    password = WebDriverWait(driver, 5).until(
         EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
    password.send_keys(data.GOOGLE_PASSWORD)
    driver.find_element(By.ID, "passwordNext").click()
    WebDriverWait(driver, 100).until(
         EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[1]/div[3]/c-wiz/nav/ul/li[1]/a/div[2]')))
    # End ----- Login in google account block --------------------------------------------
    return driver


def UpWorkLogin(driver):
    print('0')
    driver.get(URL)
    CheckReCAPTCHA(driver, URL)
    # # Get Driver Version

    # str1 = driver.capabilities['browserVersion']
    # str2 = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    # print(str1)
    # print(str2)
    # print(str1[0:2])
    # print(str2[0:2])

    # WebDriverWait(driver, waitTime).until(
    #     EC.presence_of_element_located((By.XPATH, "//*[@id='nav-main']/div/a[2][text()='Sign Up']")))
    # sleep(5)
    # print('1')
    #
    # CheckReCAPTCHA(driver)

    #Sign_Up_button = driver.find_element(By.XPATH, "//button[text()='Sign Up']")
    Sign_Up_button = WebDriverWait(driver, waitTime).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-main']/div/a[2][text()='Sign Up']")))
        # EC.presence_of_element_located((By.XPATH, "//*[@id='nav-main']/div/a[2][text()='Sign Up']")))
    sleep(5)
    # Sign_Up_button = driver.find_element(By.XPATH, "//*[@id='nav-main']/div/a[2][text()='Sign Up']")
    Sign_Up_button.click()

    print('2')
    # driver.close()
    # driver.quit()
    print('3')
    sleep(5)
    CheckReCAPTCHA(driver)
    print('4')
    # //*[@id="main"]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/button/div/span/span
    # WebDriverWait(driver, waitTime).until(
    #     EC.presence_of_element_located((By.XPATH,
    #        "//*[@id='main']/div/div/div/div/div[1]/div[2]/div[1]/div[1]/button/div/span/span[text()='Continue with Google']")))
    print('5')
    Continue_with_Google = WebDriverWait(driver, waitTime).until(
        EC.element_to_be_clickable((By.XPATH,
        # EC.presence_of_element_located((By.XPATH,
           "//*/span[text()='Continue with Google']")))
    print('6')
    sleep(5)
    CheckReCAPTCHA(driver)
    # Continue_with_Google = driver.find_element(By.XPATH, "//*/span[text()='Continue with Google']")
    Continue_with_Google.click()
    sleep(5)
    print('7')
    return driver


def ClearFiles(filename, filename2):
    with open(filename, "w", encoding='utf-8') as file:
        file.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"+'\n\n'))
    with open(filename2, "w", encoding='utf-8') as file:
        time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"+'<br>\n<br>\n')
        string = '<!doctype html>\n<html lang="ru">\n<head>\n    <meta charset="UTF=8">\n</head>\n<body>\n\n' + time
        file.write(string)


def text(job):
    try:
        text = job.find('a').get_text()
    except Exception as err:
        text = ''
        print('text Error:', err)
    print(f'{text=}')
    return text


def href(job):
    try:
        href = job.find('a').attrs['href']
    except Exception as err:
        href = None
        print('href Error:', err)
    return href


def published_time(job):
    try:
        cur_published_time = job.find("span", {"data-test": "posted-on"}).getText()
    except Exception as err:
        cur_published_time = ''
        print('published_time Error:', err)
    print(f'{cur_published_time=}')
    return cur_published_time


def budget(job):
    try:
        budget = job.find("span", {"data-test": "budget"})
        if budget:
            cur_budget = budget.getText().replace('\n', '').replace('$', '').strip()
        else:
            cur_budget = ''
    except Exception as err:
        cur_budget = ''
        print('budget Error:', err)
    print(f'{cur_budget=}')
    return cur_budget


def job_type(job):
    try:
        cur_job_type = job.find("strong", {"data-test": "job-type"}).getText()
    except Exception as err:
        cur_job_type = ''
        print('job_type Error:', err)
    print(f'{cur_job_type=}')
    return cur_job_type


def level(job):
    try:
        cur_contactor_tier = job.find("span", {"data-test": "contractor-tier"}).getText()
    except Exception as err:
        cur_contactor_tier = ''
        print('level Error:', err)
    print(f'level={cur_contactor_tier}')
    return cur_contactor_tier


def job_desc(job):
    try:
        cur_job_desc = job.find("span", {"data-test": "job-description-text"}).getText()
    except Exception as err:
        cur_job_desc = ''
        print('job_desc Error:', err)
    return cur_job_desc


def skills(job):
    cur_skills = []
    try:
        list_of_skils = job.find_all('a', class_='up-skill-badge text-muted')
        if list_of_skils:
            for skill in list_of_skils:
                try:
                    cur_skills.append(skill.getText())
                except Exception as err:
                    print('cur_skills.append(skil.getText()) Error:', err)
    except Exception as err:
        print('kills Error:', err)
    if cur_skills:
        return ','.join(cur_skills)
    else:
        return ''


def country(job):
    try:
        cur_country = job.find("small", {"data-test": "client-country"}).getText().split("\n")[-1].strip()
    except Exception as err:
        print('country Error:', err)
        cur_country = ''
    print(f'{cur_country=}')
    return cur_country


def total_pay(job):
    try:
        total_pay = job.find("small", {"data-test": "client-spendings"})
        if total_pay:
            cur_total_pay = total_pay.getText().split(" ")[0].replace('$', '').replace('+', '').strip()
        else:
            cur_total_pay = ''
    except Exception as err:
        print('total_pay Error:', err)
        cur_total_pay = ''
    print(f'{cur_total_pay=}')
    return cur_total_pay


def payment_verified(job):
    try:
        payment_verified = job.find("small", {"data-test": "payment-verification-status"})
        if payment_verified:
            cur_payment_verified = payment_verified .getText().split("\n")[-1].strip()
        else:
            cur_payment_verified = ''
    except Exception as err:
        print('payment_verified Error:', err)
        cur_payment_verified = ''
    print(f'{cur_payment_verified=}')
    return cur_payment_verified


def duration(job):
    try:
        duration = job.find("span", {"data-test": "duration"})
        if duration:
            cur_duration = duration.getText().split("\n")[-1].strip()
        else:
            cur_duration = ''
    except Exception as err:
        print('duration Error:', err)
        cur_duration = ''
    print(f'{cur_duration=}')
    return cur_duration


def proposals(job):
    try:
        propos = job.find("small", class_="d-inline-block mr-10")
        if propos:
            cur_proposals = propos.getText().split("\n")[-1].split(' ', 1)[-1].strip()
        else:
            cur_proposals = ''
    except Exception as err:
        print('proposals Error:', err)
        cur_proposals = ''
    print(f'{cur_proposals=}')
    return cur_proposals

def format_output_string(txt_file_text, row, HTML=True):
    # Red block ---------------
    if HTML:
        txt_file_text += '<font color="red">'
    txt_file_text += 'LEVEL: ' + row['level']
    txt_file_text += '    COUNTRY: ' + row['country']
    txt_file_text += '    PUBLISHED TIME: ' + row['published_time']
    if row['budget'] != '':
        txt_file_text += '    BUDGET: ' + row['budget']
    if row['job_type'] != '':
        txt_file_text += '    ' + row['job_type'] + '    Duration: ' + row['duration']
    if row['total_pay'] != '':
        txt_file_text += '   TOTAL PAY: ' + row['total_pay']
    else:
        txt_file_text += '   TOTAL PAY: 0'
    if row['payment_verified'] != '':
        txt_file_text += '    Payment Verified: '.upper() + row['payment_verified']
    else:
        txt_file_text += '    Payment NOT verified! '.upper()
    txt_file_text += '   Proposals: '.upper() + row['proposals'] + '\n\n'
    if HTML:
        txt_file_text += '</font>'
    # Red block (end) ---------------

    txt_file_text += row['job'] + '\n\n'
    txt_file_text += row['job_rus'] + '\n\n'
    if HTML:
        txt_file_text = txt_file_text.replace('\n', '<br>\n')
        txt_file_text += "<a href=\"" + URL + row['url_link'] + "\">" + URL + row['url_link'] + "</a>" + '<br>\n<br>\n'
    else:
        txt_file_text += URL + row['url_link'] + '\n\n'

    txt_file_text2 = 'DESCRIBE: \n\n' + row['desc'] + '\n\n'
    # blue  block -----------------
    if HTML:
        txt_file_text2 += '<font color="blue">'
    txt_file_text2 += 'RUSSIAN DESCRIBE: \n\n' + row['desc_rus'] + '\n\n\n'
    if HTML:
        txt_file_text2 += '</font>'
    # blue  block (end)--------------
    if HTML:
        txt_file_text2 = txt_file_text2.replace('\n', '<br>\n')
    txt_file_text += txt_file_text2
    return txt_file_text


def write_txt_file(filename, row, i, number):
    with open(filename, "a", encoding='utf-8') as txt_file:
        num = f'[{i + 1:02d}/{number:02d}]  '
        txt_file_text = '\n' + num + ' '
        txt_file_text = format_output_string(txt_file_text, row, HTML=False)
        txt_file.write(txt_file_text)


def write_html_file(filename, row, i, number):
    with open(filename, "a", encoding='utf-8') as html_file:
        num = f'[{i + 1:02d}/{number:02d}]  '
        html_file_text = '<br>\n' + num + ' '
        html_file_text = format_output_string(html_file_text, row, HTML=True)
        html_file.write(html_file_text)


def GetDataFromPageToHTML(driver, number):
    mainfileHTML = f'pages/main{number:03d}.html'
    print(f'\n--- GetHTMLDataFromPage[{number}]... ------')
    try:
        main_page = driver.page_source
    except Exception as err:
        print('main_page Error: ', err)
        return 0

    # Check validate block --------------
    # soup = BeautifulSoup(main_page, 'lxml')
    #
    # try:
    #     jobs_section = soup.find_all('section', class_='up-card-section up-card-list-section up-card-hover')
    #     jobs_len = len(jobs_section)
    # except Exception as err:
    #     print('jobs_section Error: ', err)
    #     jobs_len = 0
    #
    # print(f'{jobs_len=}')
    # Check validate block (end) ---------
    jobs_section, jobs_len = TryToFindListOfJobs(main_page)

    with open(mainfileHTML, 'w', encoding='utf-8') as main_file:
        main_file.write(main_page)

    print(f'\n--- GetHTMLDataFromPage[{number}] End -----')
    return jobs_len+1   # TODO not need to refresh page


def TryToFindListOfJobs(HTML):
    soup = BeautifulSoup(HTML, 'lxml')
    try:
        # jobs_section = soup.find_all('section', class_='up-card-section up-card-list-section up-card-hover')
        # https://stackoverflow.com/questions/31004430/regular-expression-for-class-using-beautifulsoup
        jobs_section = soup.find_all('section', {'class': lambda x: x and x.startswith("up-card-section up-card-list-section up-card-hover")})
        jobs_len = len(jobs_section)
    except Exception as err:
        print('jobs_section Error: ', err)
        jobs_len = 0
    return jobs_section, jobs_len


def GetDataFromHTML(HTML, number):

    jobs_section, jobs_len = TryToFindListOfJobs(HTML)
    print(f'{jobs_len=}')

    for i, job in enumerate(jobs_section):
        data = []
        # job_rus = translate(text(job))
        # desc_rus = translate(job_desc(job))

        print(f'\n--- Page Number: {number} --------------', )
        row = {
            'job'             : text(job),
            'url_link'        : href(job),
            'duration'        : duration(job),
            'level'           : level(job),
            'desc'            : job_desc(job),
            'skills'          : skills(job),
            'published_time'  : published_time(job),
            'budget'          : budget(job),
            'job_type'        : job_type(job),
            'total_pay'       : total_pay(job),
            'payment_verified': payment_verified(job),
            'proposals'       : proposals(job),
            'country'         : country(job),
            'job_rus'         : translate(text(job)),
            'desc_rus'        : translate(job_desc(job))
        }
        print()
        # sleep(5)

        filenameTXT = 'pages/url_pages.txt'
        filenameHTML = 'pages/url_pages.html'

        # write_txt_file(filenameTXT, row, i, number)
        write_html_file(filenameHTML, row, i, number)

    return jobs_len


def GetDataFromFile(number):
    mainfileHTML = f'pages/main{number:03d}.html'
    print(f'\n--- GetDataFromFile[{number}] ---------')

    try:
        with open(mainfileHTML, 'r', encoding='utf-8') as main_file:
            main_page = main_file.read()
    except Exception as err:
        print('main_page Error: ', err)
        return 0

    jobs_len = GetDataFromHTML(main_page, number)

    print(f'\n--- GetDataFromFile[{number}] -- End -----')
    return jobs_len+1


def GetDataFromPage(driver, number):
    print(f'\n--- GetDataFromPage[{number}]... ------')
    try:
        main_page = driver.page_source
    except Exception as err:
        print('main_page Error: ', err)
        return 0

    jobs_len = GetDataFromHTML(main_page, number)
    print(f'\n--- GetDataFromPage[{number}] -- End ----')
    return jobs_len


def UpWorkParsePages(driver, max_pages=10):
    for page in range(1, max_pages+1):
        url = SEARCH_URL+str(page)
        print('driver.get(\"'+url+'\")')
        driver.get(SEARCH_URL+str(page))
        sleep(3)
        CheckReCAPTCHA(driver,url=url)
        # sleep(5) # TODO >> ?
        DownLoadTryCount = 10
        for i in range(DownLoadTryCount):
            # pagesCount = GetDataFromPage(driver, page)        # read from site to parsing
            pagesCount = GetDataFromPageToHTML(driver, page)  # read from site to HTML file
            if pagesCount > 0:
                break
            else:
                driver.get(SEARCH_URL + str(page))
                sleep(3)
                CheckReCAPTCHA(driver, url=url)
    return 0

"""
def UpWorkParseLinks(driver):
    print('UpWorkParseLinks...')

    FindWorkBtn = WebDriverWait(driver, waitTime).until(
        EC.element_to_be_clickable((By.XPATH, "//*/a/span[1][text()='Find Work']")))
        # EC.presence_of_element_located((By.XPATH, "//*/a/span[1][text()='Find Work']")))
    FindWorkBtn.click()

    print('7')
    WebDriverWait(driver, waitTime).until(
        EC.presence_of_element_located((By.XPATH,
           "//*/h2[contains(@class, 'col mb-10')]")))
    print('8')
    print('Parsing...')
    main_page = driver.page_source
    soup = BeautifulSoup(main_page, 'lxml')

    with open('pages/main_page.html', "w", encoding='utf-8') as file:
        file.write(main_page)

    jobs = soup.find_all('h4', class_='my-0 p-sm-right job-tile-title')
    print(len(jobs))
    # main_url = 'https://www.upwork.com'

    # ClearFile(f'pages/url_pages.html')

    with open(f'pages/url_pages.html', "a") as file:
        for i, job in enumerate(jobs):
            text = job.find('a').get_text()
            print(text)
            href = job.find('a').attrs['href']
            print(href)
            print()
            # with open(f'pages/href_page{i:03d}.html', "w") as file:
            #     file.write(href)

            # file.write(text + '\n')
            translate_text = str(translate(text))
            file.write('\n' + text + '\n\n' + translate_text + '\n\n' + URL + href + '\n\n\n')

    # Scrolling block ------------

    # Delay time for UpWork
    sleep(2)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(uniform(TIME_SLEEP[0], TIME_SLEEP[1]))
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
    # Scrolling block - end ------

    # xpath1 = '//*/footer/button/text()'
    # ---- xpath1 = '//*/footer/button[@text()]'
    # xpath1 = '//*/footer/button'
    xpath1 = '//*/footer/button[@type="button"]'
    # ---- xpath1 = r'//*/footer/button[@text()=" \n        Load More Jobs\n      "]'
    # ----- xpath1 = r'//*/footer/button[@text()="Load More Jobs"]'
    xpath2 = "//*/button[@data-test='load-more-button']/text()"
    print('finding Load More Jobs = ' + xpath1)

    try:
        print('Wait Button')
        # WebDriverWait(driver, waitTime).until(
        #     EC.element_to_be_clickable((By.XPATH, xpath1)))
        # find_element_by_xpath("//input[@type='file']")
        # print('Find Button')
        # NextBtn = driver.find_element(By.XPATH, xpath1)
        NextBtn = WebDriverWait(driver, waitTime).until(
             EC.element_to_be_clickable((By.XPATH, xpath1)))
        print('Button1 found')
    except Exception as Error:
        print('Button1 not found', Error)
        NextBtn = None
    # print('finding2 Load More Jobs  =' + xpath1)
    # try:
    #     NextBtn = WebDriverWait(driver, waitTime).until(
    #         EC.presence_of_element_located((By.XPATH, xpath2)))
    #     print('Button2 found')
    # except Exception as Error:
    #     print('Button2 not found:', Error)
    print(isBSfindInHTML(main_page, xpath1), '   ', xpath1)
    # print(isBSfindInHTML(main_page, xpath2), '   ', xpath2)
    print('end finding Load More Jobs\n\n\n')
    sleep(delayTime)
    if NextBtn:
        print('before NextBtn.click()')
        if NextBtn.is_enabled():
            print('Enabled')
            try:
                # # print(f'{len(NextBtn)=}')
                # print(f'{type(NextBtn)=}')
                # print(f'{type(NextBtn[0])=}')
                
                # print('driver.refresh()')
                # driver.refresh()
                # sleep(5)

                print('action = ActionChains(driver)')
                action = ActionChains(driver)
                print('action.move_to_element(NextBtn).perform()')
                action.move_to_element(NextBtn).perform()
                sleep(10)
                # # wait.until(
                # #     EC.presence_of_element_located((By.XPATH, xpath1))).send_keys(Keys.RETURN)
                # sleep(5)
                print('\naction.send_keys(Keys.RETURN)')
                action.send_keys(Keys.RETURN)
                sleep(10)
                print('\nNextBtn.send_keys(Keys.RETURN)')
                NextBtn.send_keys(Keys.RETURN)
                sleep(10)
                print('\naction.move_to_element(NextBtn).click().perform()')
                action.move_to_element(NextBtn).click().perform()
                # action.move_to_element(NextBtn).click().perform()
                # sleep(5)
                # print('driver.execute_script("arguments[0].click();", NextBtn)')
                # driver.execute_script("arguments[0].click();", NextBtn)
                sleep(10)
                print('\nNextBtn.click()')
                NextBtn.click()
                sleep(10)
                print('\nNextBtn.send_keys(Keys.ENTER)')
                NextBtn.send_keys(Keys.ENTER)
                # sleep(5)
                # print('NextBtn.submit()')
                # NextBtn.submit()
                # print('NextBtn.submit()')
                # print(f'{(NextBtn)=}')
                print(f'{type(NextBtn)=}')
                print(f'{dir(NextBtn)=}')
                sleep(10)
                print("\ndriver.execute_script(\"document.getElementsByClassName(\'up-btn up-btn-default up-btn-sm mb-0\')[0].click();\")")
                driver.execute_script("document.getElementsByClassName('up-btn up-btn-default up-btn-sm mb-0')[0].click();")

                # driver.execute_script("document.getElementById('theIdName').click()")
                # print( "driver.execute_script(\"document.getElementByXpath('//*/footer/button[@type=\"button\"]').click()\")")
                # driver.execute_script("document.getElementByXpath('//*/footer/button[@type=\"button\"]').click()")
                sleep(10)
                print("driver.execute_script(\"\n(document.evaluate(\"//*/footer/button[@type=\'button\']\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).click();\")")

                driver.execute_script(
                    "\n(document.evaluate(\"//*/footer/button[@type=\'button\']\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).click();")
                sleep(10)
                print('driver.execute_script("arguments[0].click();", NextBtn)')
                driver.execute_script("arguments[0].click();", NextBtn)
                # sleep(2)
                # print(f'{NextBtn.getText()=}')
                # # release()
            except Exception as Err:
                print('Error: ', Err)
    else:
        print('if NextBtn: else !!!!')
    sleep(delayTime)
    return driver
    """

def get_selenium_html_page(url, max_pages=10, headless=False):
    # driver = local_init(url)
    driver = GL.GoogleAccountInit(headless)
    demo.after_init(driver, True)
    driver.implicitly_wait(2)
    #
    driver.maximize_window()
    #
    if headless:
        print('Submit google account owner by smartphone')
    driver = GoogleLogin(driver)
    driver = UpWorkLogin(driver)
    CheckReCAPTCHA(driver)

    driver = UpWorkParsePages(driver, max_pages)
    #sleep(2000)


def getContentFromFiles(max_pages = 10):
    for page in range(1, max_pages+1):
        GetDataFromFile(page)


def isBSfindInFile(filename, xpath):
    with open(filename, "r") as file:
        main_page = file.read()
    tree = html.fromstring(main_page)
    text = tree.xpath(xpath)
    if text:
        print(text)
        return True
    else:
        return False


def isBSfindInHTML(source_html, xpath):
    tree = html.fromstring(source_html)
    text = tree.xpath(xpath)
    if text:
        print(type(text), ' | ', text)
        filename = 'text-'+str(text).replace('<','').replace('>','').replace('\n','')\
            .replace('/','').replace('\\','')+'.txt'
        print(f'{filename=}')
        with open(f'{filename}', 'w', encoding='utf-8') as file:
            file.write(str(dir(text)))
        return True
    else:
        return False


if __name__ == '__main__':
    max_pages = 10
    get_selenium_html_page(URL, max_pages=max_pages)

    ClearFiles('pages/url_pages.txt', 'pages/url_pages.html')
    getContentFromFiles(max_pages)
    print('OK   ')
    # run()