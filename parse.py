import re
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

def clear_innertext(soup):
    for k in soup.findChild():
        k.extract()

class HTMLElement():
    def __init__(self, name, attr, full_body,text):
        self.name = name
        self.attr = attr
        self.full_body = full_body
        self.text = text

    def length(self):
        return len(self.full_body)+len(self.name)+len(self.text)+3

    def to_string(self):
        return self.full_body + self.text


parser = etree.HTMLParser()

def crop_string(str,max_length):
    return str[:max_length]


# print(crop_string(html_doc,230))
max_length = 180

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

soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup)
# soup.clear('div')
# print(soup.tagStack)

# now = soup.find('div',attrs={'id':'root'})
# for k in now.find_all_previous():
#     print(k.name,1)
# while soup.findChild is not None:
f = open("demo.txt", "a")

stack = deque()
leng = 0

for tag in soup.find_all(True):
    # print(tag.string.replace_with(''))
        current_fb = str(tag).split('>')[0] +">"
        current_text = (str(tag).split('>')[1].split('<')[0])
        new_elem = HTMLElement(tag.name, tag.   attrs,current_fb,current_text)
        leng+=new_elem.length()
        # print(leng)

        if leng>max_length:
            s = ""
            root_elem = stack.popleft()
            s+=root_elem.to_string()
            while len(stack) >0:
                el = stack.popleft()
                s+=el.to_string()
                cur_tag = soup.find(el.name,attrs=el.attr)
                if cur_tag.findChild() is None:
                    cur_tag.decompose()
                else:
                    clear_innertext(cur_tag)
            html_root   = etree.fromstring(s, parser)
            cur = etree.tostring(html_root,pretty_print=True,method="html")
            s = BeautifulSoup(cur,'html.parser')
            f.write(str(s.find(root_elem.name,attrs=root_elem.attr)))
            f.write('\n-----------\n')
            break
        else:
            stack.append(new_elem)



f.write(str(soup))
# f.close()
# k = soup.find('div',attrs={'id':'product_name'})
# k.string.replace_with('')
# new_text = k.string.replace_with('')



# k = get_occurance([4,6,2,3],[0,6,3])
# print(soup.find('div',attrs={'id':'root'}))

# html_doc2 = '''<div id="product_name">
#       Dark Red Energy Potion
#       <div id="product_price">$4.99</div>
#       </div>
# '''

# soup2 = BeautifulSoup(html_doc2,'html.parser')

# clear_innertext(soup2)
# print(soup2)


# lastsoup2.find('div',attrs={'id':= soup2.find('div',attrs={'id':'root'})

# new_div = soup2.new_tag('div',attrs={'class':'test'})
# new_div.string='Test'

# last_div.append(new_div)
# print(soup2)
