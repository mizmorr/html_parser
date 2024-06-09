import re
from bs4 import BeautifulSoup, NavigableString
from lxml import etree
from collections import deque
import sys

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


class HTML_parser():
    def __init__(self,soup,source):
        self.soup = BeautifulSoup(soup, 'html.parser')
        self.source = source

    def clear_innertext(self,soup):
        if soup.findChildren is not None:
            for child in soup.children:
                if isinstance(child, NavigableString):
                    child.extract()

    def set_source(self,source):
        self.source = source

    def set_soup(self,soup):
        self.soup = soup

    def make_crop(self,max_length):
        stack = deque()
        leng = 0
        parser = etree.HTMLParser()
        for tag in self.soup.find_all(True):
            current_fb = str(tag).split('>')[0] +">"
            current_text = (str(tag).split('>')[1].split('<')[0])
            new_elem = HTMLElement(tag.name, tag.   attrs,current_fb,current_text)
            leng+=new_elem.length()

            if leng>max_length:
                pre_str = ""
                root_elem = stack.popleft()
                pre_str+=root_elem.to_string()
                while len(stack) > 0:
                    el = stack.popleft()
                    pre_str+=el.to_string()
                    cur_tag = self.soup.find(el.name,attrs=el.attr)
                    if cur_tag is not None:

                        if cur_tag.findChild() is None:
                            cur_tag.decompose()
                        else:
                            if len(stack)==0:
                                return "","This fragment can not be splitted because of nesting"
                            self.clear_innertext(cur_tag)
                html_root = etree.fromstring(pre_str, parser)
                cur = etree.tostring(html_root,method="html")
                s_oup = BeautifulSoup(cur,'html.parser')
                result = s_oup.find(root_elem.name,attrs=root_elem.attr)
                return result.prettify(),""
            else:
                stack.append(new_elem)

    def crop_html(self,max_length):
        f = open(self.source, "w")
        while len(str(self.soup))>max_length:
            cropped,error = self.make_crop(max_length)
            if error == "":
                f.write(cropped)
                f.write('\n--------\n')
            print("error caught: "+error)
        f.write(str(self.soup))
        f.close()



if __name__ == "__main__":

    max_length = sys.argv[1].split("=")[1]
    source = sys.argv[2]
    print(max_length,source)
    parser = HTML_parser(html_doc,source)
    parser.crop_html(max_length)
