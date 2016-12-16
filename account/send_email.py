# -*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class EmailSender(object):
    HEADERS = ['Content-Disposition', 'attachment']
    _FROM = 'yangjun.liu@quvideo.com'
    _TO= ['yangjun.liu@quvideo.com']
    def __init__(self,host,user,password):
        smtpObj = smtplib.SMTP()
        smtpObj.connect(host)
        smtpObj.login(user, password)

        self.sender = smtpObj

    def send(self, subject, receivers, jumper_ip):
        ### 获取 user
        user = ""
        user_part = receivers.split('@')[0]
        for user_p in user_part.split('.'):
            user = user + user_p
        _html_text = """
            <html>
                <span> Hi, """+user+ """</span>
                <span>1. 下载邮件附件中的"""+user+"""_cmdb_login_id_rsa</span>
                <span>2. 打开Xshell或secureCRT等终端仿真程序</soan>
                <span>3. 新建会话: 主机为跳板机login的外网IP有: """+ jumper_ip +""", 用户名为:"""+ user +"""</span>
                <span>4. 连接会话, 用户密钥选择login_id_rsa,即可登陆login</span>
                <span>配置完成后,建议即刻彻底删除该邮件</span>
            </html>
        """
        msg = MIMEMultipart()
        ### 文字部分
        part1 = MIMEText(_html_text, _subtype='html', _charset='utf-8')
        msg.attach(part1)

        part2 = MIMEApplication(open('/web/CMDB/static/upload/'+user+'_cmdb_login_id_rsa', 'rb').read())
        part2.add_header('Content-Disposition', 'attachment', filename="cmdb_id_dsa")
        msg.attach(part2)

        msg['Subject'] = subject
        msg['From'] = self._FROM
        msg['To'] = ";".join(receivers)

        self.sender.sendmail(self._FROM, receivers, msg.as_string())

    def close(self):
        self.sender.close()
