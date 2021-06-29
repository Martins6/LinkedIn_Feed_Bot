import unittest
from linkedin_feed_bot.LinkedInBot import bot as LI_bot


class LinkedInBot_Tester(unittest.TestCase):
    def test_signin(self):
        """
        Test that it can sign in.
        """
        bot = LI_bot('chrome')
        secret = {
            'username': input('LinkedIn username: '),
            'password': input('LinkedIn password: ')
        }
        bot.sign_in(secret['username'], secret['password'])
        
        self.assertTrue(True)
        
    def test_crawler(self):
        """
        Test the crawling of information.
        """
        bot = LI_bot('chrome')
        secret = {
            input('LinkedIn username: '),
            input('LinkedIn password: ')
        }
        bot.sign_in(secret['username'], secret['password'])
        
        for i in range(10):
            bot.scroll_down()

        df = bot.df_author_post()
        if not df.empty:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()