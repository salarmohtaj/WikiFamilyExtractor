import requests as RQ
from bs4 import BeautifulSoup
import re
import json

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    text = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)
    text = re.sub(clean, ' ', text)
    return text

dic = []
random_page_url = "https://fa.wikipedia.org/wiki/%D9%88%DB%8C%DA%98%D9%87:%D8%B5%D9%81%D8%AD%D9%87%D9%94_%D8%AA%D8%B5%D8%A7%D8%AF%D9%81%DB%8C"

for i in range(400):
    try:
        r = RQ.get(random_page_url)
        html = r.text
        page_id = html.split('"wgWikibaseItemId":')[1].split("}")[0]
        page_id = page_id.replace('"', "")
        soup = BeautifulSoup(html,features="html.parser")
        content = soup.find('main', {"id": "content"})
        content = remove_html_tags(str(content))
        content = re.sub(' +', " ", content)
        content = re.sub(r'\n+', '\n', content)
        content = content.replace("\n", " ")
        content = content.replace(" ", " ")
        content = content.replace("[ ویرایش ]", " ")
        content = content.replace("از ویکی‌پدیا، دانشنامهٔ آزاد", " ")
        content = re.sub(
            '.mw-parser-output cite.citation{font-style:inherit}.m.*?mw-parser-output .cs1-kern-wl-right{padding-right:0.2em}',
            ' ', content, flags=re.DOTALL)
        content = re.sub(' +', " ", content)
        dic.append({"text" : content , "id" : page_id})
    except:
        continue
    if (i % 25 == 0): print(i)

with open("data.json","a+") as f:
    for item in dic:
        f.write(json.dumps(item)+"\n")