import sqlite3
from sqlite3 import Cursor, Error
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

wd = webdriver.Edge()
wd.implicitly_wait(10)
wait = WebDriverWait(wd, 15)  # 最多等待15秒

wd.get("https://www.howbuy.com/fundtool/filter.htm")

# 浮窗
wd.find_element(By.CSS_SELECTOR, ".guide_box_btn.box_btn_yellow a[code='zt']").click()
# 筛选和类型
wd.find_element(By.CSS_SELECTOR, "li[id='nTab1_t0']").click()
wd.find_element(By.CSS_SELECTOR, "li[id='nTab1_0_1_t3']").click()
# checkbox选择框
wd.find_element(By.CSS_SELECTOR, "input[id='buy_fund_intent']").click()
# 关键词查询
input_box = wd.find_element(By.CSS_SELECTOR, "input[id='fund_keywords']")
input_box.clear()

# 页码
wd.find_element(By.CSS_SELECTOR, "div.bottom>div.pages>span.ts>a:nth-child(3)").click()

# 输入模块
etf_keyword = input("请输入你要查找的基金关键词：")
input_box.send_keys(etf_keyword)
# input_box.send_keys("卫星")

# 搜索按钮
search_button = wd.find_element(By.CSS_SELECTOR, "a[id='keywords_btn']")
search_button.click()
sleep(1)

# 这个模块代替 sleep(2)
# wait.until(
#     EC.text_to_be_present_in_element(
#         (By.CSS_SELECTOR,"div.filter_left span"),
#         ""
#     )
# )

# 搜索结果
search_result = wd.find_element(By.CSS_SELECTOR, "div[class='filter_left']")
print(search_result.text)

search_num = search_result.find_element(By.CSS_SELECTOR, "span.cRed")
result_num = int(search_num.text)
# print(f"数量{result_num}")
# print(f"{search_num.text}")

etf_brief_data_list = []
result_list = wd.find_element(By.CSS_SELECTOR, "div.filter_result_list>div.result_list_table tbody")
for num in range(1, result_num + 1):
    result_data = result_list.find_element(By.CSS_SELECTOR, "tr:nth-child(" + str(num) + ")")
    # 基金名字和代码
    # etf_name = result_data.find_element(By.CSS_SELECTOR,"td:nth-child(2)>a[target='_blank']").text
    # etf_code = result_data.find_element(By.CSS_SELECTOR,"td:nth-child(2)>a[target='_blank']>span").text
    etf_ele = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(1)>input[type='checkbox']")
    etf_name = etf_ele.get_attribute("jjjc")
    etf_code = etf_ele.get_attribute("value")
    # 近3个月涨幅
    etf_3_month_change = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
    etf_6_month_change = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(8)").text
    etf_year_to_Date = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(12)").text
    # 手续费
    apply_fee = result_data.find_element(By.CSS_SELECTOR, "td:nth-child(13)>span:nth-child(1)").text

    row_tuple = (etf_code, etf_name, etf_3_month_change, etf_6_month_change, etf_year_to_Date, apply_fee)
    etf_brief_data_list.append(row_tuple)

    print(f"{etf_code} {etf_name} "
          f"近3个月涨幅{etf_3_month_change} "
          f"近6个月涨幅{etf_6_month_change} "
          f"今年以来{etf_year_to_Date} "
          f"手续费{apply_fee}")
    sleep(1)

print("爬取结束")


# 数据库存储模块
def etf_data_list_save(fund_data_list, db_path="etf_data.db"):
    if not fund_data_list:
        print("数据为空，跳过存储")
        return

    # 真正执行SQL语句（SELECT / INSERT / UPDATE / DELETE）全部用cursor（游标cur）
    # `conn`不执行SQL，它只管 ** 事务、打开关闭、配置 **。
    # brief是简洁的意思
    create_sql = """
    CREATE TABLE IF NOT EXISTS fund_brief(       
        fund_code TEXT PRIMARY KEY, -- 基金代码
        fund_name TEXT,             -- 基金名称
        return_3m INTEGER,          -- 近三月涨幅 ×100
        return_6m INTEGER,          -- 近六月涨幅 ×100
        return_ytd INTEGER,         -- 今年以来 ×100
        fee_rate INTEGER            -- 手续费 ×100
        );
        """

    insert_sql = """
        INSERT OR REPLACE INTO fund_brief
        (fund_code,fund_name,return_3m,return_6m,return_ytd,fee_rate)
        VALUES (?,?,?,?,?,?)
        """
    try:
        # 文件不存在 → 函数内部自动新建数据库文件
        with sqlite3.connect(db_path) as conn:
            cur: Cursor = conn.cursor()
            cur.execute(create_sql)  # 内部建表
            cur.executemany(insert_sql, fund_data_list)
            print(f"成功写入 {len(fund_data_list)} 条基金数据")

    except sqlite3.OperationalError as e:
        print(f"数据库操作错误（锁文件、路径错误、SQL语法）: {e}")
    except sqlite3.IntegrityError as e:
        print(f"数据完整性错误（主键冲突）: {e}")
    except Error as e:
        print(f"SQLite通用异常: {e}")
    except Exception as e:
        print(f"未知异常: {e}")


# if __name__ == "__main__":
etf_data_list_save(etf_brief_data_list)

# input("请输入")
wd.quit()
