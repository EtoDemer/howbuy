from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wd = webdriver.Edge()
wd.implicitly_wait(10)
wait = WebDriverWait(wd,15) #最多等待15秒

wd.get("https://www.howbuy.com/fundtool/filter.htm")

#浮窗
wd.find_element(By.CSS_SELECTOR,".guide_box_btn.box_btn_yellow a[code='zt']").click()
#筛选和类型
wd.find_element(By.CSS_SELECTOR,"li[id='nTab1_t0']").click()
wd.find_element(By.CSS_SELECTOR,"li[id='nTab1_0_1_t3']").click()
#checkbox选择框
wd.find_element(By.CSS_SELECTOR,"input[id='buy_fund_intent']").click()
#关键词查询
input_box = wd.find_element(By.CSS_SELECTOR,"input[id='fund_keywords']")
input_box.clear()

#页码
wd.find_element(By.CSS_SELECTOR,"div.bottom>div.pages>span.ts>a:nth-child(3)").click()

#输入模块
#etf_keyword = input("请输入你要查找的基金关键词：")
input_box.send_keys("卫星")

#搜索按钮
search_button = wd.find_element(By.CSS_SELECTOR,"a[id='keywords_btn']")
search_button.click()
sleep(1)

# 这个模块代替 sleep(2)
# wait.until(
#     EC.text_to_be_present_in_element(
#         (By.CSS_SELECTOR,"div.filter_left span"),
#         ""
#     )
# )

#搜索结果
search_result = wd.find_element(By.CSS_SELECTOR,"div[class='filter_left']")
print(search_result.text)

search_num = search_result.find_element(By.CSS_SELECTOR,"span.cRed")
result_num = int(search_num.text)
# print(f"数量{result_num}")
# print(f"{search_num.text}")

result_list = wd.find_element(By.CSS_SELECTOR,"div.filter_result_list>div.result_list_table tbody")
for num in range(1,result_num+1):
    result_data = result_list.find_element(By.CSS_SELECTOR,"tr:nth-child("+str(num)+")")
    #基金名字和代码
    # etf_name = result_data.find_element(By.CSS_SELECTOR,"td:nth-child(2)>a[target='_blank']").text
    # etf_code = result_data.find_element(By.CSS_SELECTOR,"td:nth-child(2)>a[target='_blank']>span").text
    etf_ele = result_data.find_element(By.CSS_SELECTOR,"td:nth-child(1)>input[type='checkbox']")
    etf_name = etf_ele.get_attribute("jjjc")
    etf_code = etf_ele.get_attribute("value")
    #近3个月涨幅
    etf_3_month_change = result_data.find_element(By.CSS_SELECTOR,"td:nth-child(7)").text
    etf_6_month_change = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(8)").text
    etf_year_to_Date = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(12)").text
    #手续费
    apply_fee = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(13)>span:nth-child(1)").text

    print(f"{etf_code} {etf_name} "
          f"近3个月涨幅{etf_3_month_change} "
          f"近6个月涨幅{etf_6_month_change} "
          f"今年以来{etf_year_to_Date} "
          f"手续费{apply_fee}")
    sleep(1)

print("结束")

input("请输入")

