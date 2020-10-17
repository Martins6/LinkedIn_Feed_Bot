from time import sleep
import LinkedInBot
import secret


webdriver_path_linux = '/home/adriel_martins/Downloads/chromedriver'
webdriver_path_windows = 'C:\Program Files (x86)\chromedriver.exe'

bot = LinkedInBot.bot(webdriver_path_windows)
bot.sign_in(secret.username, secret.password)

print(bot.df_author_post())

for i in range(10):
    sleep(1)
    bot.scroll_down()

df = bot.df_author_post()
print(df)

df.to_csv('data.csv')

bot.quit()
