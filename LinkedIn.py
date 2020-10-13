from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from utils_functions import write_to_element
import secret
import itertools
import pandas as pd

class LinkedInBot:
    def __init__(self, webdriver_path):
        chrome_options = webdriver.chrome.options.Options()
        #chrome_options.add_argument('--headless')

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

    def df_author_post(self, tags=None, authors=None):
        """ Scraping in the feed on the current window the author's name and title along with each post.
        Also, we could filter by tags in the post and author's name. 

        Return: 
                Pandas.DataFrame

        Args:
            tags (list): list of tags to filter the posts. Defaults to None.
            authors (list): list of authors names. Defaults to None.
        """
        feed_boxes = self.driver.find_elements_by_css_selector('.relative.ember-view')
        
        df = pd.DataFrame(columns=('author_name', 'author_title', 'post'))

        for i, fb in enumerate(feed_boxes):
            like_bar =  fb.find_elements_by_css_selector('.feed-shared-social-action-bar--has-social-counts')
            post =  fb.find_elements_by_css_selector('div.feed-shared-update-v2__commentary')
            name =  fb.find_elements_by_css_selector('span.feed-shared-actor__title')
            title =  fb.find_elements_by_css_selector('span.feed-shared-actor__description')

            # The object of feed boxes, is not unique.
            # It repeat itself, so we must drop duplicates.
            df = df.drop_duplicates()
            
            # Populating our dataframe.
            # Checking if this is a regular LinkedIn post where we have the post,
            # the name and title of the author. 
            if(len(post) == len(name) == len(title) == 1):
                    # Acessing the list and retrieving the text from the webelement
                    df.loc[i] = [name[0].text, title[0].text, post[0].text]

        # The object of feed boxes, is not unique.
        # It repeat itself, so we must drop duplicates.
        df = df.drop_duplicates()
        # Filtering for the tags and authors that we wants
        if tags is not None:
            for tag in tags:
                tag = '#' + tag
                # Checking if there a tag in each post
                df = df[df.apply(lambda row: tag in row.post, axis=1)]
        if authors is not None:
            for author in authors:
                # Checking if the author name is the one selected
                df = df[df.apply(lambda row: author in row.author_name, axis = 1)]

        return(df)
    
    def quit(self):
        sleep(1)
        self.driver.close()


webdriver_path_linux = '/home/adriel_martins/Downloads/chromedriver'
webdriver_path_windows = 'C:\Program Files (x86)\chromedriver.exe'

bot = LinkedInBot(webdriver_path_windows)
bot.sign_in(secret.username, secret.password)

print(bot.df_author_post())

for i in range(100):
    sleep(1)
    bot.scroll_down()

df = bot.df_author_post()
print(df)
