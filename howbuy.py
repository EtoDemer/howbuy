from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

wd = webdriver.Edge()
wd.implicitly_wait(10)

wd.get("https://www.howbuy.com/fundtool/filter.htm")

wd.find_element(By.CSS_SELECTOR,".guide_box_btn.box_btn_yellow a[code='zt']").click()
# sleep(2)

wd.find_element(By.CSS_SELECTOR,"li[id=nTab1_t0]").click()
wd.find_element(By.CSS_SELECTOR,"li[id=nTab1_0_1_t3]").click()
sleep(2)

wd.find_element(By.CSS_SELECTOR,"input[id=buy_fund_intent]").click()

input_box = wd.find_element(By.CSS_SELECTOR,"input[id=fund_keywords]")
input_box.clear()
#etf_keyword = input("请输入你要查找的基金关键词：")
input_box.send_keys("白酒")

search_button = wd.find_element(By.CSS_SELECTOR,"a[id=keywords_btn]")
search_button.click()


input("请输入")