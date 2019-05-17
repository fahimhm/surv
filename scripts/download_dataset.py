# module/library
import os
import time
import datetime as dt
from os.path import join
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

def download(url):
    # delete old file
    if os.path.isfile(join(os.getcwd(), 'datasets', 'filling_event.csv')):
        os.remove(join(os.getcwd(), 'datasets', 'filling_event.csv'))
    
    # driver setting
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2) # not to choose default download setting directory
    fp.set_preference("browser.download.manager.ShowWhenStarting", False)
    fp.set_preference("browser.download.dir", join(os.getcwd(), 'datasets'))
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # get the url and navigating
    driver = webdriver.Firefox(executable_path = join(os.getcwd(), 'driver', 'geckodriver.exe'), firefox_profile = fp)
    driver.get(url)
    driver.find_element_by_link_text('Data_Mentah').click()
    driver.find_element_by_id('ctl32_ctl04_ctl03_txtValue').click()
    driver.find_element_by_id('ctl32_ctl04_ctl03_divDropDown_ctl03').click()
    driver.find_element_by_id('ctl32_ctl04_ctl05_txtValue').click()
    driver.find_element_by_id('ctl32_ctl04_ctl05_divDropDown_ctl00').click()
    driver.find_element_by_id('ctl32_ctl04_ctl07_txtValue').send_keys('10/1/2018')
    driver.find_element_by_id('ctl32_ctl04_ctl09_txtValue').send_keys(dt.date.today().strftime("%m/%d/%Y"))
    driver.find_element_by_id('ctl32_ctl04_ctl11_txtValue').send_keys('ciawi')
    driver.find_element_by_id('ctl32_ctl04_ctl00').click()

    # give delay for process
    time.sleep(1)
    try:
        while driver.find_element_by_link_text('Cancel'):
            time.sleep(1)
    except NoSuchElementException:
        pass

    # navigating download menu
    action = ActionChains(driver)
    dropdownmenu = driver.find_element_by_css_selector("#ctl32_ctl05_ctl04_ctl00_ButtonLink > span")
    action.move_to_element(dropdownmenu).perform()
    dropdownmenu.click()
    csvtoclick = driver.find_element_by_link_text("CSV (comma delimited)")
    action.move_to_element(csvtoclick).perform()
    csvtoclick.click()

    # give delay for download process
    time.sleep(1)
    name = 'Data%5FMentah'
    while os.path.isfile(join(os.getcwd(), 'datasets', name + '.csv')) == False:
        time.sleep(1)
    else:
        while int(os.path.getsize(join(os.getcwd(), 'datasets', name + '.csv'))) == 0:
            time.sleep(1)

    # close driver
    driver.quit()

    # rename file
    if os.path.isfile(join(os.getcwd(), 'datasets', 'Data%5FMentah.csv')):
        os.rename(join(os.getcwd(), 'datasets', 'Data%5FMentah.csv'), join(os.getcwd(), 'datasets', 'filling_event.csv'))