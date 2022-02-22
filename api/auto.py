from operator import le
from time import sleep
import uiautomator2 as u2
from re import findall

class JDLoginUIauto(object):
    def __init__(self,*args,**kwargs):
        self.ipaddress = kwargs.get("ipaddress")
        self.number = kwargs.get("number")
        self.passwordSource = kwargs.get("source")  # 批量登录用户密码文件
        if self.ipaddress:
            # 需要安装ADB WIFI 
            # adb connect <ip address>:5555
            self.devices = u2.connect(self.ipaddress) 
        if self.number:
            # 通过USB连接电脑
            self.devices = u2.connect(self.number)
        if not all([self.ipaddress,self.number]):
            # 默认连接设备 
            self.devices = u2.connect()
        self.get_virtual_packages()
        self.parse_password_source()


    def get_virtual_packages(self):
        output,code = self.devices.shell(['pm', 'list', 'packages'])
        # print(output)
        packages = findall("package:(dkplugin.*?)\s",output)
        if len(packages) != 10:
            raise Exception("检查一下你是否用小x分身,小x分身只分身了{}个APP".format(len(packages)))
        else:
            self.packages = packages

    def parse_password_source(self):
        self.pwds = []
        with open(self.passwordSource,encoding='utf8') as f:
            for line in f.readlines():
                # line ====> username,password\n
                self.pwds.append(line.strip().split(','))
        pass
    
    def jd_login(self,package,username,password):
        self.devices.app_start(package)
        self.devices.wait_activity("com.jingdong.app.mall.MainFrameActivity")
        sleep(3)
        self.devices.xpath('//*[@resource-id="com.jingdong.app.mall:id/tj"]/android.widget.FrameLayout[last()]').click(timeout=5)
        sleep(2)
        self.devices(resourceId="com.jd.lib.personal.feature:id/jv").click(timeout=5)
        self.devices.wait_activity("com.jd.lib.login.LoginActivity")
        self.devices(resourceId="com.jd.lib.login.feature:id/jd").click(timeout=5)
        self.devices(resourceId="com.jd.lib.login.feature:id/ce").set_text(username,timeout=5)
        self.devices(resourceId="com.jd.lib.login.feature:id/cg").set_text(password,timeout=5)
        self.devices(resourceId="com.jd.lib.login.feature:id/gk").click(timeout=5)
        self.devices(resourceId="com.jd.lib.login.feature:id/d").click(timeout=5)

    def run(self):
        for a,b in zip(self.packages,self.pwds):
            try:
                self.jd_login(a,b[0],b[1])
                input("手动完成滑块|验证码验证请按回车键.........\n")
                self.devices.app_stop(a)
            except:
                sleep(1)
                print("APP:{} 账号已登录".format(a))
                self.devices.app_stop(a)

# 模拟登录时,需要Android手机上安装uiautomator2驱动、服务
# python -m uiautomator2 init  
# 命令关闭JD APP
# uiautomator2 stop com.jingdong.app.mall
# NOTE 虚拟化APP需要预先手动去赋予权限、同意用户协议
ju = JDLoginUIauto(ipaddress='192.168.1.134',source=r"settings\password.txt")
ju.run()