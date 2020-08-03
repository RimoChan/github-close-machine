import logging
import json
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

import requests
from github import Github

import 配置


def 获取所有邮箱():
    if Path('邮箱表.json').is_file():
        return json.load(open('邮箱表.json'))
    g = Github(配置.用户名, 配置.密码)
    我 = g.get_user()
    邮箱表 = {i.login:i.email for i in 我.get_followers() if i.email}
    json.dump(邮箱表, open('邮箱表.json', 'w', encoding='utf8'))
    return 邮箱表


def 发邮件(目标):
    message = MIMEText('你是沙币！', 'plain', 'utf-8')
    message['Subject'] = '我是乳骂邮件'
    message['From'] = 配置.邮件账户['用户名']
    message['To'] = 目标
    sender = 配置.邮件账户['用户名']
    s = smtplib.SMTP()
    s.connect(配置.邮件账户['smtp主机'], 25)
    s.login(sender, 配置.邮件账户['密码']) 
    s.sendmail(sender, 目标, message.as_string()) 
    s.quit()


目标组 = 获取所有邮箱().values()

for 目标 in 目标组:
    发邮件(目标)
    logging.warning(f'「{目标}」骂好了。')
