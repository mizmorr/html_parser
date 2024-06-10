import unittest
from core.main import HTML_parser
from bs4 import BeautifulSoup

class TestHTML_parser(unittest.TestCase):

    def test_read(self):
        f = open('./src/source.html',"r")
        parser = HTML_parser('./src/source.html')
        self.assertEqual(f.read(),parser.read_html())
        f.close()
    def test_crop_first(self):
        max_length = 180
        target = '''<div id="root">
            <div id="products">
            <div class="product">
            <div id="product_name">
                Dark Red Energy Potion
                <div id="product_price">
                $4.99
                </div>
                </div>
            </div>
            </div>
        </div>'''
        parser = HTML_parser('./src/source.html')
        cropped,cur_length,error = parser.make_crop(max_length)
        self.assertEqual(cropped,BeautifulSoup(target,'html.parser').prettify())# prettifying just to make same format
        self.assertIsNone(error)
        self.assertGreaterEqual(max_length,cur_length)

    def test_first_failed(self):
        max_length = 179
        parser = HTML_parser('./src/source.html')
        cropped,cur_length,error = parser.make_crop(max_length)
        self.assertEqual(cropped,"")
        self.assertEqual(cur_length,0)
        self.assertIsNotNone(error)

    def test_first_split(self):
        max_length = 180
        targets = ['''
        <div id="root">
            <div id="products">
            <div class="product">
            <div id="product_name">
                Dark Red Energy Potion
                <div id="product_price">
                $4.99
                </div>
                </div>
            </div>
            </div>
        </div>''',
        '''
        <div id="root"><div id="products"><div class="product"><div id="product_name">
        <div id="product_rate">4.7</div></div></div></div></div>
        ''',
        '''
        <div id="root">
            <div id="products">
            <div class="product">
            <div id="product_description">
                Bring out the best in your gaming performance.
            </div>
            </div>
            </div>
        </div>
        ''']
        parser = HTML_parser('./src/source.html')
        for target in targets:
            if len(str(parser.get_soup()))<max_length:
                self.assertEqual(parser.get_soup().prettify(),BeautifulSoup(target,'html.parser').prettify())
            else:
                cropped,cur_length,error = parser.make_crop(max_length)
                self.assertEqual(cropped,BeautifulSoup(target,'html.parser').prettify())
                self.assertIsNone(error)
                self.assertGreaterEqual(max_length,cur_length)

    def test_second_crop(self):
        target ='''<div id="root">
 <div id="products">
  <div class="product">
   <div id="product_name">
    Dark Red Energy Potion
    <div id="product_price">
     $4.99
     <ul>
      <li>
       Milk
      </li>
     </ul>
    </div>
   </div>
  </div>
 </div>
</div>
'''
        max_length =220
        parser = HTML_parser('./src/source2.html')
        cropped,cur_length,error = parser.make_crop(max_length)
        self.assertEqual(cropped,target)
        self.assertIsNone(error)
        self.assertGreaterEqual(max_length,cur_length)

    def test_second_split(self):
        targets=['''<div id="root">
 <div id="products">
  <div class="product">
   <div id="product_name">
    Dark Red Energy Potion
    <div id="product_price">
     $4.99
     <ul>
      <li>
       Milk
      </li>
      <li>
       Cheese
       <ul>
        <li>
         Blue cheese
        </li>
        <li>
         Feta
         <div id="product_rate">
          4.7
         </div>
        </li>
       </ul>
      </li>
     </ul>
    </div>
   </div>
  </div>
 </div>
</div>''',
'''<div id="root">
 <div id="products">
  <div class="product">
   <div id="product_name">
    <ul>
     <li>
      <ul>
       <li>
        Blue cheese
       </li>
       <li>
        Feta
       </li>
      </ul>
     </li>
    </ul>
   </div>
   <div id="product_description">
    Bring out the best in your gaming performance.
   </div>
  </div>
 </div>
</div>''']
        max_length=330
        parser = HTML_parser('./src/source2.html')
        for target in targets:
            if len(str(parser.get_soup()))<max_length:
                self.assertEqual(parser.get_soup().prettify(),BeautifulSoup(target,'html.parser').prettify())
                pass
            else:
                cropped,cur_length,error = parser.make_crop(max_length)
                self.assertEqual(cropped,BeautifulSoup(target,'html.parser').prettify())
                self.assertIsNone(error)
                self.assertGreaterEqual(max_length,cur_length)

    def test_second_failed(self):
        max_length = 150
        parser = HTML_parser('./src/source2.html')
        cropped,cur_length,error = parser.make_crop(max_length)
        self.assertEqual(cropped,"")
        self.assertEqual(cur_length,0)
        self.assertIsNotNone(error)

    def test_crop_third(self):
        max_length = 4800
        target = '''<body class="skin-vector-legacy mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject mw-editable page-Веб-скрейпинг rootpage-Веб-скрейпинг skin-vector action-view">
 <div class="noprint" id="mw-page-base">
  <div class="noprint" id="mw-head-base">
   <div class="mw-body" id="content" role="main">
    <a id="top">
     <div class="notheme" id="siteNotice">
      <div class="mw-indicators">
       <h1 class="firstHeading mw-first-heading" id="firstHeading">
        <span class="mw-page-title-main">
         Веб-скрейпинг
         <div class="vector-body" id="bodyContent">
          <div class="noprint" id="siteSub">
           Материал из Википедии — свободной энциклопедии
           <div id="contentSub">
            <div id="mw-content-subtitle">
             <div class="plainlinks flaggedrevs_preview" id="mw-fr-reviewnotice">
              Текущая версия страницы пока
              <a href="/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0_%D1%81%D1%82%D0%B0%D1%82%D0%B5%D0%B9/%D0%9F%D0%BE%D1%8F%D1%81%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5_%D0%B4%D0%BB%D1%8F_%D1%87%D0%B8%D1%82%D0%B0%D1%82%D0%B5%D0%BB%D0%B5%D0%B9" title="Википедия:Проверка статей/Пояснение для читателей">
               не проверялась
              </a>
              <a class="external text" href="https://ru.wikipedia.org/w/index.php?title=%D0%92%D0%B5%D0%B1-%D1%81%D0%BA%D1%80%D0%B5%D0%B9%D0%BF%D0%B8%D0%BD%D0%B3&amp;stable=1">
               версии
              </a>
              <a class="external text" href="https://ru.wikipedia.org/w/index.php?title=%D0%92%D0%B5%D0%B1-%D1%81%D0%BA%D1%80%D0%B5%D0%B9%D0%BF%D0%B8%D0%BD%D0%B3&amp;oldid=132505568&amp;diff=cur&amp;diffonly=0">
               1 правка
               <div class="flaggedrevs_short flaggedrevs_draft_notsynced plainlinks noprint" id="mw-fr-revisiontag">
                <div class="flaggedrevs_short_basic">
                 <span class="flaggedrevs-icon flaggedrevs-icon-block skin-invert" title="Текущая версия">
                  <span class="fr-toggle-arrow flaggedrevs-icon flaggedrevs-icon-expand" id="mw-fr-revisiontoggle" title="показать/скрыть подробности">
                   <div id="mw-fr-revisiondetails-wrapper" style="position:relative;">
                    <div class="flaggedrevs_short_details" id="mw-fr-revisiondetails" style="display:none">
                     Текущая версия страницы пока
                     <a href="/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0_%D1%81%D1%82%D0%B0%D1%82%D0%B5%D0%B9/%D0%9F%D0%BE%D1%8F%D1%81%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5_%D0%B4%D0%BB%D1%8F_%D1%87%D0%B8%D1%82%D0%B0%D1%82%D0%B5%D0%BB%D0%B5%D0%B9" title="Википедия:Проверка статей/Пояснение для читателей">
                      не проверялась
                     </a>
                     <a class="external text" href="https://ru.wikipedia.org/w/index.php?title=%D0%92%D0%B5%D0%B1-%D1%81%D0%BA%D1%80%D0%B5%D0%B9%D0%BF%D0%B8%D0%BD%D0%B3&amp;stable=1">
                      версии
                     </a>
                     <a class="external text" href="https://ru.wikipedia.org/w/index.php?title=%D0%92%D0%B5%D0%B1-%D1%81%D0%BA%D1%80%D0%B5%D0%B9%D0%BF%D0%B8%D0%BD%D0%B3&amp;oldid=132505568&amp;diff=cur&amp;diffonly=0">
                      1 правка
                      <div id="contentSub2">
                       <div id="jump-to-nav">
                        <a class="mw-jump-link" href="#mw-head">
                         Перейти к навигации
                        </a>
                        <a class="mw-jump-link" href="#searchInput">
                         Перейти к поиску
                         <div class="mw-body-content" id="mw-content-text">
                          <div class="mw-content-ltr mw-parser-output" dir="ltr" lang="ru">
                           <figure class="mw-default-size mw-halign-center" typeof="mw:File/Thumb">
                            <a class="mw-file-description" href="/wiki/%D0%A4%D0%B0%D0%B9%D0%BB:Scrapp.jpg">
                             <img alt="Процесс" class="mw-file-element" data-file-height="279" data-file-width="1307" decoding="async" height="47" src="//upload.wikimedia.org/wikipedia/commons/thumb/d/da/Scrapp.jpg/220px-Scrapp.jpg" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/d/da/Scrapp.jpg/330px-Scrapp.jpg 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/d/da/Scrapp.jpg/440px-Scrapp.jpg 2x" width="220"/>
                             <figcaption>
                              Процесс Веб-скрейпинга
                              <p>
                               <i>
                                <b>
                                 Веб-скрейпинг
                                 <a href="/wiki/%D0%90%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA" title="Английский язык">
                                  англ.
                                  <span lang="en" style="font-style:italic;">
                                   web scraping
                                   <sup class="reference" id="cite_ref-:0_1-0">
                                    <a href="#cite_note-:0-1">
                                     [1]
                                     <sup class="reference" id="cite_ref-2">
                                      <a href="#cite_note-2">
                                       [2]
                                       <p>
                                        Веб-скрейпинг используется для синтаксического преобразования
                                        <a href="/wiki/%D0%92%D0%B5%D0%B1-%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0" title="Веб-страница">
                                         веб-страниц
                                         <sup class="reference" id="cite_ref-3">
                                          <a href="#cite_note-3">
                                           [3]
                                          </a>
                                          <a href="/wiki/HTML" title="HTML">
                                           HTML
                                          </a>
                                          <a href="/wiki/XHTML" title="XHTML">
                                           XHTML
                                           <p>
                                            Загрузка и просмотр страницы\xa0— важнейшие составляющие технологии, они являются неотъемлемой частью выборки данных
                                            <sup class="reference" id="cite_ref-4">
                                             <a href="#cite_note-4">
                                              [4]
                                             </a>
                                            </sup>
                                           </p>
                                          </a>
                                         </sup>
                                        </a>
                                       </p>
                                      </a>
                                     </sup>
                                    </a>
                                   </sup>
                                  </span>
                                 </a>
                                </b>
                               </i>
                              </p>
                             </figcaption>
                            </a>
                           </figure>
                          </div>
                         </div>
                        </a>
                       </div>
                      </div>
                     </a>
                    </div>
                   </div>
                  </span>
                 </span>
                </div>
               </div>
              </a>
             </div>
            </div>
           </div>
          </div>
         </div>
        </span>
       </h1>
      </div>
     </div>
    </a>
   </div>
  </div>
 </div>
</body>
'''
        parser = HTML_parser('./src/source3.html')
        cropped,cur_length,error = parser.make_crop(max_length)
        self.assertEqual(cropped,target)
        self.assertIsNone(error)
        self.assertGreaterEqual(max_length,cur_length)

    def test_third_failed(self):
        max_length = 1024
        parser = HTML_parser('./src/source3.html')
        cropped,cur_length,error = parser.make_crop(max_length)
        self.assertEqual(cropped,"")
        self.assertEqual(cur_length,0)
        self.assertIsNotNone(error)



if __name__ == "__main__":
    unittest.main()
