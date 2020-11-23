from urllib import request
import bs4
import xlwt


class Spider:
    article_num = 0  # 文章总数
    pic_max_num = 0  # 单篇文章最多图片数量

    def __fetch_content(self, url, sheet):
        # 请求网页
        req = request.Request(url)
        r = request.urlopen(req)

        # 获取HTML字节码
        html = r.read()

        # 定位内容
        soup = bs4.BeautifulSoup(html, 'lxml')
        news = soup.select('.c54969')

        # 遍历每篇文章，爬取具体内容
        server_url = "http://xcb.tjut.edu.cn/"
        for n in news:
            # 跳过外链
            if not n['href'].startswith('info'):
                continue

            req = request.Request(server_url + n['href'])
            r = request.urlopen(req)

            # 获取HTML字节码
            html = r.read()

            # 定位内容
            soup = bs4.BeautifulSoup(html, 'lxml')
            title = soup.select('.titlestyle54971').pop().text
            time = soup.select('.timestyle54971').pop().string.strip()
            img = soup.select('.contentstyle54971 img')

            # 输出excel
            Spider.article_num += 1
            sheet.write(Spider.article_num, 0, title)
            sheet.write(Spider.article_num, 1, time)

            # 对图片进行遍历
            current_pic_num = 0
            for i in img:

                current_pic_num += 1
                if Spider.pic_max_num < current_pic_num:
                    Spider.pic_max_num += 1
                    sheet.write(0, 1 + Spider.pic_max_num, '图片链接' + str(Spider.pic_max_num))

                try:
                    sheet.write(Spider.article_num, 1 + current_pic_num, server_url + i['src'])
                except Exception as e:
                    print(e.__str__())
                    print(title + "爬取错误", '，时间：' + time)

            # print("第" + str(Spider.article_num) + "个文章爬取完毕")

    def go(self):
        print("    ______ ___ ______                  __    \n" +
              "   / ____/<  // ____/_____ ____   ____/ /___ \n" +
              "  /___ \\  / //___ \\ / ___// __ \\ / __  // _ \\ \n" +
              " ____/ / / /____/ // /__ / /_/ // /_/ //  __/\n" +
              "/_____/ /_//_____/ \\___/ \\____/ \\__,_/ \\___/\n" + "我在这里，静静地爬取你的网站，我的blog:) 515code.com")

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("新闻数据")
        sheet.write(0, 0, '新闻标题')
        sheet.write(0, 1, '发布日期')

        # 爬取网站1-2页
        for index in range(1, 3):
            self.__fetch_content(
                url="http://xcb.tjut.edu.cn/zxdt.jsp?a3t=128&a3p=" + str(
                    index) + "&a3c=15&urltype=tree.TreeTempUrl&wbtreeid=1009",
                sheet=sheet)
            print('第' + str(index) + '页爬取完毕')

        # 结果存储到news.xls中
        workbook.save('news.xls')


spider = Spider()
spider.go()
