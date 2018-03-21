# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#在程序前加上这段代码
from selenium import webdriver
#options = webdriver.ChromeOptions()
#options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
#driver = webdriver.Chrome(chrome_options=options)

driver = webdriver.Chrome()
#driver.get("https://www.douban.com")
driver.get("https://accounts.douban.com/login?alias=")

time.sleep(30)
driver.find_element_by_name("form_email").send_keys("15*******")
driver.find_element_by_name("form_password").send_keys("********")

driver.find_element_by_xpath("//input[@class='bn-submit']").click()

#driver.find_element_by_xpath('//div[@class="login_btn_panel"]/a[@title="点击登录"]').click()


#driver.save_screenshot("douban.png")

#driver.quit()