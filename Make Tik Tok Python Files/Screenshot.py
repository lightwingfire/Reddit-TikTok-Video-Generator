from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
import json

#WIP WIP WIP WIP WIP 
#WIP WIP WIP WIP WIP 
#WIP WIP WIP WIP WIP 
class screenshot:

    def __init__(self):
        self.drv = None
        self.started = False
        self.timeout = 10

        self.passwordPath = "Config Files\\passwords.json"
        with open(self.passwordPath,"r") as f:
             codes = json.load(f)

        self.redditUserName = codes["redditUserName"]
        self.redditPassword = codes["redditPassword"]

        return
    
    def startFireFox(self):
            print("starting firefox")
            binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\Firefox.exe") # selinium issues resolved with this
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            opts.set_preference("dom.push.enabled", False)  # kill notification popup
            self.drv = Firefox(firefox_binary = binary, options=opts)
            self.drv.set_window_size(720,1920)
            print("loaded firefox")
    
    def login(self):
        print("logging into reddit on firefox")

        self.drv.get("https://www.reddit.com/login")

        user = self.drv.find_element(By.ID, "loginUsername")
        user.send_keys(self.redditUserName)

        pwd = self.drv.find_element(By.ID, "loginPassword")
        pwd.send_keys(self.redditPassword)

        btn = self.drv.find_element(By.CSS_SELECTOR, "button[type='submit']")
        btn.click()

        sleep(self.timeout)

        print("logged in to reddit on firefox")


    def setRedditPost(self,url):
          cmts = "https://www.reddit.com" + url
          self.drv.get(cmts)
          print("Post:"+cmts)
          return
    
    def screenshot(self,id):
        try:
            print("post id:"+id)
            #looks through elements on webpage looking for said element with that id
            cmt = WebDriverWait(self.drv, self.timeout).until(
            lambda x: x.find_element(By.ID,id))
        except TimeoutException:
            print("Page load timed out...")
        else:
            cmt.screenshot(id + ".png")

        return
    
    def start(self):
         self.startFireFox()
         self.login()
         self.started = True

    def getStarted(self):
         return self.started