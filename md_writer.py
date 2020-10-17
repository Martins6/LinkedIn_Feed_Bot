import pandas as pd
import io

df = pd.read_csv('data.csv')

f= io.open("test.md","w", encoding="utf-8")

f.write('# Daily Feed' + '\n')

for author, post in zip(df.author_name, df.post):
    f.write('### ' + author + '\n')
    f.write('\n')
    post = post.replace('#', '\#')
    f.write(post + '\n')
    f.write('\n')

#a = ''.join(a)
f.close()
print(f.closed)
