# howbuy
这个是用来练习python selenium自动化控制脚本的项目，目标是写一个主动爬取https://www.howbuy.com/fundtool/filter.htm 基金信息的。
需要添加的功能：关键字查找、数据保存导出、获取更详细的基金数据。
模块化整合，在main函数中集成查找功能，将功能实现放到其它文件中。

模块作用：
datacrud：进行爬取之后对数据库的操作
datasave：爬取数据列表的存储操作
howbuy：数据爬取
main：主函数