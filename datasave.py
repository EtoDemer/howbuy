import sqlite3
from sqlite3 import Cursor, Error
# from time import sleep
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait

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
