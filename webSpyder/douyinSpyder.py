# 根据appium技术去爬取抖音的信息
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC

class DouyinSpyder:
    def __init__(self, platformName, deviceName, appPackage,appActivity, noReset, fullReset):
        self.desired_capabilities = {
        'platformName': platformName,  # 操作系统
        'deviceName': deviceName,  # 设备 ID
          # 设备版本号，在手机设置中查看
        'appPackage': appPackage,  # app 包名
        'appActivity': appActivity,  # app 启动时主 Activity
        'noReset': noReset,  # 是否保留 session 信息 避免重新登录
        "fullReset": fullReset
        }

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_capabilities)
        wait = WebDriverWait(self.driver, 60)

        input = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/he6')))
        # 显式等待相关节点出现

    def spy(self):
        pass


if __name__ == '__main__':
    platformName = 'Android'
    deviceName = 'HWNOH'
    appPackage = 'com.ss.android.ugc.aweme'
    appActivity = 'ui.LauncherUI'
    noReset = True
    fullReset = False
    dou = DouyinSpyder(platformName, deviceName, appPackage, appActivity, noReset, fullReset)
    dou.spy()