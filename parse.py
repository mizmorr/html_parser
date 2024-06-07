from bs4 import BeautifulSoup
from lxml import etree
from collections import deque
from io import StringIO


html_doc = '''<div id="root">
  <div id="products">
    <div class="product">
      <div id="product_name">
      Dark Red Energy Potion
      <div id="product_price">$4.99</div>
      </div>
      <div id="product_rate">4.7</div>
      <div id="product_description"><div id="product_rate">Bring out the best in your gaming performance.</div></div>
    </div>
  </div>
</div>
'''

class HTMLElement():
    def __init__(self, name, attr, full_body,text):
        self.name = name
        self.attr = attr
        self.full_body = full_body
        self.text = text

    def length(self):
        return len(self.full_body)+len(self.name)+len(self.text)+3


parser = etree.HTMLParser()

def crop_string(str,max_length):
    return str[:max_length]


# print(crop_string(html_doc,230))
max_length = 150

def get_occurance(l_1,l_2):
    l = set(l_2)
    return next(i for i in l_1 if i in l)

parser = etree.HTMLParser()
str_cur = crop_string(html_doc,35)
# print(repr(str_cur))
# print("---")
html_root   = etree.fromstring(str_cur, parser)
cur = etree.tostring(html_root,method="html")

# print(cur)
stack = deque()

soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup)
# soup.clear('div')
# print(soup.tagStack)

# now = soup.find('div',attrs={'id':'root'})
# for k in now.find_all_previous():
#     print(k.name,1)
leng = 0
for tag in soup.find_all(True):
    current_fb = str(tag).split('>')[0] +">"
    print(tag.text)
    new_elem = HTMLElement(tag.name, tag.attrs,current_fb,tag.text)
    leng+=new_elem.length()
    print(leng)
    # if tag.findChild() is None and leng>max_length:
    #     while len(stack) >0:
    #         el = stack.popleft()
    #         print(el.full_body)
    # else:
    #     stack.append(new_elem)



# k = get_occurance([4,6,2,3],[0,6,3])
# print(soup.find('div',attrs={'id':'root'}))

