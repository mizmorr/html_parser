from bs4 import BeautifulSoup
from lxml import etree


html_doc = '''<div id="root">
  <div id="products">
    <div class="product">
      <div id="product_name">
      Dark Red Energy Potion
      <div id="product_price">$4.99</div>
      </div>
      <div id="product_rate">4.7</div>
      <div id="product_description">Bring out the best in your gaming performance.</div>
    </div>
  </div>
</div>
'''
from io import StringIO

parser = etree.HTMLParser()

def crop_string(str,max_length):
    return str[:max_length]

parser = etree.HTMLParser()
str_cur = crop_string(html_doc,35)
print(str_cur)
print("---")
html_root   = etree.fromstring(str_cur, parser)
cur = etree.tostring(html_root,method="html")

# print(cur)

soup = BeautifulSoup(cur, 'html.parser')
print(soup.find('div',attrs={'id':'root'}))
# for tag in soup.find_all(True):
#     print(tag.name)
