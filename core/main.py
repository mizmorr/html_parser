from bs4 import BeautifulSoup, NavigableString
from lxml import etree
from collections import deque
import sys


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
    def __init__(self,source):
        self.source = source
        self.soup = BeautifulSoup(self.read_html(),'html.parser')


    def clear_innertext(self,soup):
        if soup.findChildren is not None:
            for child in soup.children:
                if isinstance(child, NavigableString):
                    child.extract()

    def set_source(self,source):
        self.source = source

    def set_soup(self,soup):
        self.soup = soup

    def get_soup(self):
        return self.soup

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
                                return "",0,"This fragment can not be splitted because of nesting"
                            self.clear_innertext(cur_tag)
                html_root = etree.fromstring(pre_str, parser)
                cur = etree.tostring(html_root,method="html")
                s_oup = BeautifulSoup(cur,'html.parser')
                result = s_oup.find(root_elem.name,attrs=root_elem.attr)
                return result.prettify(),len(str(result)),None
            else:
                stack.append(new_elem)

    def read_html(self):
        f = open(self.source,"r")
        html = f.read()
        f.close()
        return html

    def crop_html(self,max_length):
        number = 0
        while len(str(self.soup))>max_length:
            cropped,length,error = self.make_crop(max_length)
            if error is None:
                print(f"fragment #{number}: {length} chars\n"+cropped)
            else:
                print("error caught: "+error)
                return
            number+=1
        print(f"fragment #{number}: {len(str(self.soup))} chars\n"+self.soup.prettify())


if __name__ == "__main__":
    max_length = int(sys.argv[1].split("=")[1])
    source = sys.argv[2]
    parser = HTML_parser(source)
    parser.crop_html(max_length)
