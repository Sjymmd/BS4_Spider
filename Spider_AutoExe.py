#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
Created on Sep 3  2018

@author: Sjymmd
E-mail:1005965744@qq.com
"""
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import pytesseract
#

class Web_Access(object):

    def error_protect(txt=''):
        def exe(func):
            def wrap(self):
                try:
                    func(self)
                except:
                    self.exit(self.driver)
                    print(txt)
                    if txt:
                        print(txt)
                    else:
                        raise Exception
            return wrap
        return exe

    def decorator(txt):
        def exe(func):
            def wrap(self):
                fun = func(self)
                input_txt = self.__getattribute__(txt)
                fun.clear()
                fun.click()
                fun.send_keys(input_txt)
            return wrap
        return exe

    def print(*txt):
        import functools
        print_self = functools.partial(print, end=' ')
        def exe(func):
            def wrap(self):
                func(self)
                for words in txt:
                    if hasattr(self,words):
                        print_self(self.__getattribute__(words))
                    else:
                        print_self(words)
                print()
            return wrap
        return exe

    def exit(self,driver):
        return driver.quit()

class Login(Web_Access):

    def __init__(self, driver,url,username, password):

        self.driver = driver
        self.__username = username
        self.__password = password
        self.__url = url

    @Web_Access.print('Success','usr','_Login__username','pwd','*'*len('_Login__password'),'vr_code', '_Login__vr_txt')
    def __call__(self, *args, **kwargs):
        while True:
            self.__loginning()
            if self.driver.current_url != self.__url:
                break

    def __save_verification_pic(self):
        self.pic_element = driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='扫码下载APP'])[1]/following::img[1]")
        pic_full = self.driver.get_screenshot_as_png()
        location = self.pic_element.location
        size = self.pic_element.size
        im = Image.open(BytesIO(pic_full))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((left * 2, top * 2, right * 2, bottom * 2))
        # im.save('screenshot.png')
        return im

    def __get_verifiaction_pic(self):
        # img = Image.open("screenshot.png")
        img = self.__save_verification_pic()
        self.__vr_txt = pytesseract.image_to_string(img, lang="eng")
        return self.__vr_txt

    @Web_Access.decorator('_Login__username')
    def __get_username(self):
        return self.driver.find_element_by_id("loginId")

    @Web_Access.decorator('_Login__password')
    def __get_password(self):
        return self.driver.find_element_by_id("password")

    @Web_Access.decorator('_Login__vr_txt')
    def __get_verifiaction_txt(self):
        return self.driver.find_element_by_id("validCode")

    def __loginning(self):
        self.__get_username()
        self.__get_password()
        while True:
            if len(self.__get_verifiaction_pic())==4:
                self.__get_verifiaction_txt()
                self.driver.find_element_by_id("J_LoginSubmit").click()
                break
            self.pic_element.click()


class Appointment(Web_Access):

    def __init__(self,driver,doctor_name,):
        self.driver = driver
        self.__doctor_name = doctor_name

    @Web_Access.error_protect()
    def __call__(self, *args, **kwargs):
        self.__search_doctor()
        self.__registered()
        self.__choosing_day()
        self.__appointment()

    @Web_Access.decorator('_Appointment__doctor_name')
    def __get_doctor(self):
        return self.driver.find_element_by_name("q")

    def __search_doctor(self):
        self.__get_doctor()
        self.driver.find_element_by_link_text(u'搜索').click()

    @Web_Access.error_protect('挂号未开放')
    @Web_Access.print('挂号开放')
    def __registered(self):
        button = self.driver.find_element_by_link_text(u'挂号')
        if button.get_attribute('class')== 'gbn gbt-blue':
            button.click()


    @Web_Access.error_protect()
    @Web_Access.print('最早预约时间', '_Appointment__date')
    def __choosing_day(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])
        hospitals = self.driver.find_elements_by_tag_name('a')
        self.driver.find_element_by_link_text(u"挂号").click()
        date = []
        for h in hospitals:
            try:
                if h.get_attribute('monitor')=='doctor,doctor_service,order_hospital':
                    h.click()
                    days = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_any_elements_located((By.XPATH,"//li[@class='J_SchedulesItem schedules-item expert']")))
                    for d in days:
                        if d.find_element_by_class_name('date').text:
                            date.append(d.find_element_by_class_name('date').text)
                    # print(self.driver.find_element_by_xpath("//li[@monitor='doctor,doctor_service,order_order']"))
            except Exception:
                continue
        self.__date = min(date)
        self.driver.find_element_by_xpath("//p[text()='%s']"%self.__date).click()

    @Web_Access.print('预约成功')
    def __appointment(self):
        self.driver.find_element_by_id('visitTypeRadio0').click()
        self.driver.find_element_by_xpath("//span[text()='尚未确诊']").click()
        self.driver.find_element_by_class_name('J_Agreement').click()
        self.driver.execute_script("window.scrollBy(0, 200)")
        # self.driver.find_element_by_id('J_Booking').click()

if __name__ == '__main__':

    username = input('Usr:')
    import getpass
    password = getpass.getpass('Password:')
    doctor_name = input('Doctor_Name:')
    driver = webdriver.Chrome()
    url = 'https://www.guahao.com/user/login'
    driver.get(url)
    
    login = Login(driver,url,username,password)
    appointment = Appointment(driver,doctor_name)

    login()
    appointment()

