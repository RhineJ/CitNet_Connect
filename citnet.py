from PyQt5 import uic
# 导入 动态加载 ui文件 库
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings,QTimer
import subprocess
import requests
import time
import json
import os
import sys

#连接WiFi的参数
def connect_to_open_wifi(ssid):
    try:
        # 使用netsh命令连接到开放的WiFi网络
        cmd_connect = f'netsh wlan connect name="{ssid}"'
        subprocess.run(cmd_connect, shell=True, check=True)
        #print(f"已成功连接到开放的WiFi: {ssid}")
    except subprocess.CalledProcessError as e:
        pass
        #print(f"连接WiFi时发生错误: {e}")
    except Exception as ex:
        pass
        #print(f"发生未知错误: {ex}")

connect_to_open_wifi("CIT-Chinanet")    
time.sleep(2.5)




class Stats():
    
    file_path = os.path.dirname(os.path.realpath(__file__))
    
    #print(file_path)

    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi(self.file_path+"/citnet.ui")

        #前置文件执行
        self.profile()

        #当按钮按下时执行handlecalc函数
        self.ui.line_Button.clicked.connect(self.handleCalc)

        #当用户名一栏改动时执行username函数
        self.ui.username_Edit.textChanged.connect(self.username)  

        #当密码栏改动时执行passwoed函数
        self.ui.password_Edit.textChanged.connect(self.password)   

        #当记住密码框选变化
        #self.ui.checkBox.clicked.connect(self.checkBox)
        #开机启动项
        self.ui.startBox.clicked.connect(self.startup)

        self.ui.password_Edit.returnPressed.connect(self.handleCalc)

        #self.ui.setWindowOpacity(1)  # 1.0 表示不透明


 


    def profile(self):
        #导入用户名
        with open(self.file_path + '/username.txt', 'r') as file:
            content = file.read()
        self.ui.username_Edit.setText(content)
        
        content = ""

        with open(self.file_path + '/password.txt', 'r') as file:
            content = file.read()
        
        if content != "" :
            pass
            #self.ui.checkBox.setChecked(True)
        self.ui.password_Edit.setText(content)

        #导入开机启动选定
        with open(self.file_path + '/startup.txt', 'r') as file:
            cstartup = file.read()
        if cstartup == "1" :
            self.ui.startBox.setChecked(True)
            self.handleCalc()

        else:
            self.ui.startBox.setChecked(False) 
        
        #wifi名称检查
        """
        wifi_name = self.get_wifi_name_windows()
        if wifi_name == "CIT-Chinanet":
            #print("当前WiFi名称:", wifi_name)     
        else:
            #print("未连接到WiFi网络1")
            QMessageBox.information(None, "注意", "未连接到CIT-Chinanet网络") 
        """




    



    def handleCalc(self):
        wifi_name = self.get_wifi_name_windows()
        #print(wifi_name)
        if wifi_name == "CIT-Chinanet":
            pass
            #print("当前WiFi名称:", wifi_name)     
        else:
            #print("未连接到WiFi网络")
            QMessageBox.information(None, "请检查网络连接", "未连接到CIT-Chinanet网络") 
        
        self.ui.line_Button.setEnabled(False)
        self.ui.line_Button.setText("连接中")
        self.citnetconnt()

        self.ui.line_Button.setEnabled(True)
        self.ui.line_Button.setText("连接")




#主执行连接函数
    def citnetconnt(self):
        #获取用户名和密码
        userName = self.ui.username_Edit.text()  
        pwdVal =  self.ui.password_Edit.text()


        def do_encrypt_rc4(src, passwd):
            src = src.strip()
            passwd = str(passwd)
            plen = len(passwd)
            size = len(src)
            key = [ord(passwd[i % plen]) for i in range(256)]
            sbox = [i for i in range(256)]
            j = 0
            for i in range(256):
                j = (j + sbox[i] + key[i]) % 256
                sbox[i], sbox[j] = sbox[j], sbox[i]
            a = b = c = 0
            output = []
            for i in range(size):
                a = (a + 1) % 256
                b = (b + sbox[a]) % 256
                sbox[a], sbox[b] = sbox[b], sbox[a]
                c = (sbox[a] + sbox[b]) % 256
                temp = ord(src[i]) ^ sbox[c]
                temp = hex(temp)[2:]
                if len(temp) == 1:
                    temp = '0' + temp
                elif len(temp) == 0:
                    temp = '00'
                output.append(temp)
            return ''.join(output)

        auth_tag = str(int(time.time()))
        pwd = do_encrypt_rc4(pwdVal, auth_tag)

        #print(pwd)

        url = 'http://1.1.1.4/ac_portal/login.php'

        form_data = {
            'opr': 'pwdLogin',
            'userName': userName,
            'pwd': pwd,
            'auth_tag': auth_tag,
            'rememberPwd': '0'
        }

        response = requests.post(url, data=form_data)

        #print(response.status_code)
        #print(response.text)

        if response.status_code == 200:
            pass
            #print("1")
    
        if response.status_code == 200:
            response_text = response.text.replace("'", "\"")  # 将单引号替换为双引号
            try:
                response_data = json.loads(response_text)  # 手动解析响应内容
                if response_data.get('success'):
                    #简单弹窗
                    #message_box = QMessageBox.information(None, "连接成功", f"用户名: {response_data.get('userName')}") 
                    """"
                    message_box = QMessageBox()
                    message_box.setWindowTitle("连接成功(三秒后关闭)")
                    message_box.setText(f"用户名: {response_data.get('userName')}")

                    # 创建定时器，延时3秒后关闭消息框
                    timer = QTimer()
                    timer.timeout.connect(message_box.close)
                    timer.timeout.connect(QCoreApplication.quit())
                    timer.start(3000)  # 3000毫秒 = 3秒
                    message_box.exec_()
                    """
                    # 创建消息框
                    message_box = QMessageBox()
                    message_box.setWindowTitle("连接成功(三秒后关闭)")
                    message_box.setText(f"用户名: {response_data.get('userName')}")
                    # 设置弹窗大小和位置
                    #message_box.setGeometry(100, 100, 400, 200)

                    # 创建定时器
                    timer = QTimer()

                        # 定时器的槽函数，用于关闭消息框和退出应用
                    def close_message_box_and_quit():
                        message_box.close()
                        time.sleep(1)
                        sys.exit()
                        #QCoreApplication.quit()

                    # 连接定时器的timeout信号到槽函数
                    timer.timeout.connect(close_message_box_and_quit)

                    # 启动定时器，设置定时时间为3秒（3000毫秒）
                    timer.start(3000)
    
                    # 显示消息框
                    message_box.exec_()

                    #print("连接成功")

                
                else:
                    QMessageBox.information(None, "连接失败", "请检查用户名和密码") 
                    #print("连接失败")
            except json.JSONDecodeError as e:
                QMessageBox.information(None, "连接失败", "无法解析JSON响应:")
        else:
            QMessageBox.information(None, "连接失败", "请检查用户名和密码")
    


    #记住密码操作
    def checkBox(self):
        if self.ui.checkBox.isChecked():
                        #获取密码信息
            info = self.ui.password_Edit.text()
            #写入密码进文件
            with open(self.file_path + '/password.txt', 'w') as file:
                file.write(info)        
        else:
            #print("CheckBox 未被勾选")
            #清除密码文件
            with open(self.file_path + '/password.txt', 'w') as file:
                file.write("")
    #密码文件
    def password (self):
        #if self.ui.checkBox.isChecked():
            #print("记住密码中")
            #获取密码信息
        info = self.ui.password_Edit.text()
            #写入密码进文件
        with open(self.file_path + '/password.txt', 'w') as file:
            file.write(info)        
    #用户名文件
    def username(self):

        info = self.ui.username_Edit.text()
        #写入用户名进文件
        with open(self.file_path + '/username.txt', 'w') as file:
            file.write(info)
    
    #开机启动代码
    def startup(self):
        #根据勾选状态写入
        if self.ui.startBox.isChecked():
            with open(self.file_path + '/startup.txt', 'w') as file:
                file.write("1")
            script_dir = os.path.dirname(os.path.realpath(__file__))
            settings = QSettings("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run", QSettings.NativeFormat)
            settings.setValue("Citnet_connt", script_dir + "\citnet.exe")
            QMessageBox.information(None, "Success", "程序已成功设置为开机自启！")      
        else:
            with open(self.file_path + '/startup.txt', 'w') as file:
                file.write("0")
                
            settings = QSettings("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run", QSettings.NativeFormat)
            settings.remove("Citnet_connt")
            QMessageBox.information(None, "Success", "开机自启功能已成功取消！")
     

    #获取WiFi名称
    def get_wifi_name_windows(self):
        try:
            result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("latin-1")
            lines = result.split("\n")
            for line in lines:
                if "SSID" in line:
                    wifi_name = line.split(":")[1].strip()
                    return wifi_name
        except subprocess.CalledProcessError as e:
            pass
            #print("Error:", e)
        return None
    


app = QApplication([])
app.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__))+'/logo.png'))    
stats = Stats()
stats.ui.show()
app.exec_()
#with open(os.path.dirname(os.path.realpath(__file__)) + '/startup.txt', 'r') as file:
    #cstartup = file.read()
#if cstartup == "1" :
    #stats.handleCalc()  
    #time.sleep(1)
    #QCoreApplication.quit()
