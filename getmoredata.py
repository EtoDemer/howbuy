from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

browser = webdriver.Edge()
browser.implicitly_wait(10)
# browser.minimize_window()

browser.get("https://www.howbuy.com/fundtool/filter.htm")

#点掉浮窗
browser.find_element(By.CSS_SELECTOR,"div.guide_box_btn.box_btn_yellow>a").click()

#基金筛选 点按基金类型筛选
browser.find_element(By.CSS_SELECTOR,"li[id='nTab1_t0']>a").click()

#选类型
browser.find_element(By.CSS_SELECTOR,"#nTab1_0_1_t3").click()

#点击可购买
browser.find_element(By.CSS_SELECTOR,"input[id='buy_fund_intent']").click()

#搜索
input_box = browser.find_element(By.CSS_SELECTOR,"#fund_keywords")
input_box.clear()
# keyword = input("请输入关键词：")
keyword = "白酒"
input_box.send_keys(keyword)

#搜索按钮
browser.find_element(By.ID,"keywords_btn").click()
sleep(2)

#页码
browser.find_element(By.CSS_SELECTOR,"div.bottom>div.pages>span.ts>a:nth-child(3)").click()
sleep(2)





# etf_num = browser.find_element(By.CSS_SELECTOR,"div.filter_left>span.cRed").text
etf_num_data = browser.find_element(By.CSS_SELECTOR,"div.filter_left").text
etf_num = int(browser.find_element(By.CSS_SELECTOR,"div.filter_left>span.cRed").text)
print(etf_num_data)
# print(f"数量：{etf_num}")

#当前handle
window1 = browser.window_handles[0]
# print(window1)
window2 = None
etf_name_list = browser.find_element(By.CSS_SELECTOR,"#selectedJson+table>tbody")
for etf_page in range(1,etf_num+1):
    tr_list = etf_name_list.find_element(By.CSS_SELECTOR,f"tr:nth-child({etf_page})")
    etf_data_page = tr_list.find_element(By.CSS_SELECTOR,"td:nth-child(2)>a")
    etf_data_page.click()
    for window in browser.window_handles:
        if window != window1:
            window2 = window
    browser.switch_to.window(window2)
    # print(browser.current_window_handle)
    print(browser.title)
    """
    详细数据爬取
    """

    browser.close()
    browser.switch_to.window(window1)



print("任务完成")
# input("确认")
