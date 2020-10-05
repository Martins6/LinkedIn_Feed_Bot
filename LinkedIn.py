from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from utils_functions import write_to_element
import secret
import pandas as pd

class LinkedInBot:
    def __init__(self, webdriver_path):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('headless')

        self.driver = webdriver.Chrome(webdriver_path, options=chrome_options)
        self.driver.get('https://www.linkedin.com/')
        sleep(5)
        
    def sign_in(self, username, password, use_js = True):
        if(self.driver.current_url != 'https://www.linkedin.com/'):
            raise Exception("Sorry, LinkedIn has probably thrown a captcha. Try again some other time.")
        
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

    def _posts(self):
        posts = self.driver.find_elements_by_css_selector('.feed-shared-update-v2__commentary span')
        posts = list(set([post.text for post in posts]))
        return(posts)

    def _authors(self):
        authors_name = self.driver.find_elements_by_css_selector('.feed-shared-actor__title .feed-shared-actor__name')
        authors_titles = self.driver.find_elements_by_css_selector('.feed-shared-actor__description')
        
        authors_name = pd.Series([author.text for author in authors_name]).drop_duplicates().tolist()
        authors_titles = pd.Series([author_title.text for author_title in authors_titles]).drop_duplicates().tolist()

        authors = {
            'name': authors_name,
            'title': authors_titles
        }

        return(authors)

    def df_author_post(self, tags=None, authors=None) :
        df = pd.DataFrame(
            {'author_name': self._authors().get('name'),
            'author_title': self._authors().get('title'),
            'post': self._posts()}
        )

        # Filtering propagand on the Feed
        df['propaganda'] = df.apply(lambda row: 'followers' in row.author_title, axis = 1)
        df = df[df.propaganda == False]
        df = df.drop(columns='propaganda')

        # Filtering for the tags and authors that we wants
        if tags is not None:
            for tag in tags:
                tag = '#' + tag
                df = df[df.apply(lambda row: tag in row.post, axis=1)]
        if authors is not None:
            for author in authors:
                df = df[df.apply(lambda row: author in row.author_title, axis = 1)]

        return(df)
    
    def quit(self):
        sleep(1)
        self.driver.close()


webdriver_path_linux = '/home/adriel_martins/Downloads/chromedriver'
webdriver_path_windows = 'C:\Program Files (x86)\chromedriver.exe'

bot = LinkedInBot(webdriver_path_windows)
bot.sign_in(secret.username, secret.password)
sleep(1)

for i in range(3):
    sleep(4)
    bot.scroll_down()

sleep(1)
df = bot.df_author_post()
print(df)

bot.quit()
