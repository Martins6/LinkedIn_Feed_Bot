import pandas as pd
import io

def daily_feed_template_md(output_filename, df):
    df = pd.read_csv('data.csv')

    f = io.open(output_filename, "w", encoding="utf-8")

    f.write('# Daily Feed' + '\n')

    for author, title, post in zip(df.author_name, df.author_title, df.post):
        f.write('### ' + author + '\n')
        f.write('### ' + title + '\n')
        f.write('\n')
        # To adjust the hashtags into the md file.
        post = post.replace('#', '\#')
        f.write(post + '\n')
        f.write('\n')

    f.close()
    return f.closed


def weekly_feed_template_md(output_filename, df):
    df = pd.read_csv('data.csv')

    f = io.open(output_filename, "w", encoding="utf-8")

    f.write('# Weekly Feed' + '\n')

    for author, title, post in zip(df.author_name, df.author_title, df.post):
        f.write('### ' + author + '\n')
        f.write('### ' + title + '\n')
        f.write('\n')
        # To adjust the hashtags into the md file.
        post = post.replace('#', '\#')
        f.write(post + '\n')
        f.write('\n')

    f.close()
    return f.closed