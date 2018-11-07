#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
Created on July 31  2018

@author: Sjymmd
E-mail:1005965744@qq.com
"""
#
from bs4 import BeautifulSoup
import requests
import time

class Spider():

    def __init__(self,url):

        #import getpass
        self.url = url
        self._gbt_state = 'off'
        #self.password = getpass.getpass('Email_Pwd:')

    def Catching(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        gbt_state_line = soup.find(monitor="todayask_doctor,doctor_select,order")
        if str(gbt_state_line).split(' ')[2] != 'gbt-off"':
            self._gbt_state = 'on'
        else:
            print(gbt_state_line)
        return self._gbt_state


    def Sending(self):

        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        my_sender = '1005965744@qq.com'
        my_pass = '***'
        my_user = '1005965744@qq.com'

        def mail():
            ret = True
            try:
                msg = MIMEText('谢宗平医生预约开放', 'plain', 'utf-8')
                msg['From'] = formataddr(["Python", my_sender])
                msg['To'] = formataddr(["Mjc", my_user])
                msg['Subject'] = "医生订阅推送"

                server = smtplib.SMTP_SSL("smtp.qq.com", 465)
                server.login(my_sender, my_pass)
                server.sendmail(my_sender, [my_user, ], msg.as_string())
                server.quit()
            except Exception:
                ret = False
            return ret

        ret = mail()
        if ret:
            print("邮件发送成功")
        else:
            print("邮件发送失败")

if __name__ == '__main__':

    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()

    def main():
        url = 'https://www.guahao.com/search?q=%E8%B0%A2%E5%AE%97%E5%B9%B3&searchType=search'
        spider = Spider(url)
        if spider.Catching() !='off':
            spider.Sending()

        else:
            print('gbt_state - off')

    #main()

    while True:

        sched.add_job(main, 'interval', seconds=60)
        # sched.add_job(main, 'cron', minute=1)

        try:
            sched.start()
        except:
            print('定时任务出错')
            time.sleep(10)
            continue

