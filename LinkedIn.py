from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from utils_functions import write_to_element
import secret
import pandas as pd

class LinkedInBot:
    def __init__(self, webdriver_path):
        self.driver = webdriver.Chrome(webdriver_path)
        self.driver.get('https://www.linkedin.com/')
        sleep(5)
        
    def sign_in(self, username, password, use_js = True):
        if(self.driver.current_url != 'https://www.linkedin.com/'):
            return('Must be in the LinkedIn initial website.')
        
        write_to_element(self.driver, '//*[(@id = "session_key")]', username, use_js)
        sleep(2)
        self.driver.find_element_by_css_selector("#session_password").clear()
        sleep(0.5)
        write_to_element(self.driver, '//*[(@id = "session_password")]', password)
        sleep(1)
        self.driver.find_element_by_xpath('//*[(@id = "session_password")]').send_keys(Keys.RETURN)
        sleep(5)

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def posts(self):
        posts = self.driver.find_elements_by_css_selector('.feed-shared-update-v2__commentary span')
        posts = list(set([post.text for post in posts]))
        return(posts)

    def authors(self):
        authors = self.driver.find_elements_by_css_selector('.feed-shared-actor__title .feed-shared-actor__name')
        authors = list(set([author.text for author in authors]))
        return(authors)

    def df_author_post(self):
        res = pd.DataFrame(
            {'authors' : self.authors(),
            'post': self.posts()}
        )
        return(res)
    
    def quit(self):
        sleep(1)
        self.driver.close()


webdriver_path_linux = '/home/adriel_martins/Downloads/chromedriver'
webdriver_path_windows = 'C:\Program Files (x86)\chromedriver.exe'

bot = LinkedInBot(webdriver_path_windows)
bot.sign_in(secret.username, secret.password)
sleep(1)

print(bot.df_author_post())

bot.quit()
