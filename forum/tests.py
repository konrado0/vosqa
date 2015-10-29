# encoding:utf-8
from django.utils import unittest
from forum.actions.node import autolink, get_html_cleaner, filter_style, download_image_file
from lxml import etree
from lxml.html import fromstring
from copy import deepcopy
from django.core.exceptions import ValidationError
import re

class UtilsTest(unittest.TestCase):
    def testDownloadingImages(self):
        good_url = ur"http://media-cache-ec0.pinimg.com/236x/30/29/95/302995ee78f19d5ccb0d8061f1f4cadc.jpg"
        self.assertIsNotNone(download_image_file(good_url))
        
        image_too_large = ur"https://sites.google.com/site/dressbookproject/xxx"
        with self.assertRaises(ValidationError):
            download_image_file(image_too_large)
            
        not_image = ur"http://www.gazeta.pl/0,0.html"
        with self.assertRaises(ValidationError):
            download_image_file(not_image)
    
    def testFilteringStyle(self):
        html = u"""
            <div style="color: #ffff00;"><p style="float: left;"><img src="http://cdnimg.visualizeus.com/thumbs/3e/37/hairstyles-3e37929b6847d0216b0aabe296ed9a76_h.jpg?ts=93246" alt="" width="248" height="400" style="width: 500px; color: blue;"><a href="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_4.jpg" class="clb cboxElement"><img src="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_4.jpg" alt="" width="400" height="544"></a><a href="http://womeninfashion.net/wp-content/uploads/2013/11/heart-face-shape-hairstyles-jennifer-aniston.jpg" class="clb cboxElement"><img src="http://womeninfashion.net/wp-content/uploads/2013/11/heart-face-shape-hairstyles-jennifer-aniston.jpg" alt="" width="420" height="560"></a><a href="http://thisgirlscity.com/wp-content/uploads/2013/07/reese.jpg" class="clb cboxElement"><img src="http://thisgirlscity.com/wp-content/uploads/2013/07/reese.jpg" alt="" width="420" height="560"></a><a href="http://images.beautyriot.com/photos/200/hairstyles_heart_shape_face-200.jpg" class="clb cboxElement"><img src="http://images.beautyriot.com/photos/200/hairstyles_heart_shape_face-200.jpg" alt="" width="200" height="272"></a></p>
            <p><a href="http://www.youbeauty.com/p/482031/thumbnail/entry_id/0_hmc2pi25/width/0/height/0/quality/90" class="clb cboxElement"><img src="http://www.youbeauty.com/p/482031/thumbnail/entry_id/0_hmc2pi25/width/0/height/0/quality/90" alt="" width="200" height="290"></a><a href="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_11.jpg" class="clb cboxElement"><img src="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_11.jpg" alt="" width="520" height="780"></a><a href="http://www.allure.com/images/hair-ideas/2012/05/heart-face-shape-hairstyles-reese-witherspoon.jpg" class="clb cboxElement"><img src="http://www.allure.com/images/hair-ideas/2012/05/heart-face-shape-hairstyles-reese-witherspoon.jpg" alt="" width="420" height="560"></a><a href="http://slodive.com/wp-content/uploads/2012/03/hairstyles-for-heart-shaped-faces/heart-shape-glasses.jpg" class="clb cboxElement"><img src="http://slodive.com/wp-content/uploads/2012/03/hairstyles-for-heart-shaped-faces/heart-shape-glasses.jpg" alt=""></a><a href="http://www.beautifulhairstyle.net/wp-content/uploads/2014/02/Long-Hairstyles-For-Heart-Shaped-Faces.jpg" class="clb cboxElement"><img src="http://www.beautifulhairstyle.net/wp-content/uploads/2014/02/Long-Hairstyles-For-Heart-Shaped-Faces.jpg" alt=""></a><a href="http://beautyhairtotoe.com/wp-content/uploads/2013/08/rby-heart-shaped-reese-marked-mdn.jpg" class="clb cboxElement"><img src="http://beautyhairtotoe.com/wp-content/uploads/2013/08/rby-heart-shaped-reese-marked-mdn.jpg" alt=""></a><a href="http://www.prettydesigns.com/wp-content/uploads/2013/09/Hairstyle-for-Oval-shaped-Women.jpg" class="clb cboxElement"><img src="http://www.prettydesigns.com/wp-content/uploads/2013/09/Hairstyle-for-Oval-shaped-Women.jpg" alt="" width="550" height="775"></a><a href="http://www.hairnext.com/wp-content/uploads/2014/05/Heart-Shaped-Face-Best-Short-Bangs-Hairstyle-For-Fine-Hair.jpg" class="clb cboxElement"><img src="http://www.hairnext.com/wp-content/uploads/2014/05/Heart-Shaped-Face-Best-Short-Bangs-Hairstyle-For-Fine-Hair.jpg" alt="Heart Shaped Face Best Short Bangs Hairstyle For Fine Hair"></a><a href="http://www.hairnext.com/wp-content/uploads/2014/05/Short-Bob-Side-Swept-For-Long-Face-Shape.jpg" class="clb cboxElement"><img src="http://www.hairnext.com/wp-content/uploads/2014/05/Short-Bob-Side-Swept-For-Long-Face-Shape.jpg" alt="Short Bob Side Swept  For Long Face Shape"></a></p>
            <p>&nbsp; <img src="http://www.hairnext.com/wp-content/uploads/2014/05/Short-blonde-Curly-hairstyle.jpg" alt="Short blonde Curly hairstyle:"></p></div>
            """
        print etree.tounicode(filter_style(fromstring(html)))
     
    def testRemplacingImage(self):
        html = u"""
            <div><p><a href="http://cdnimg.visualizeus.com/thumbs/3e/37/hairstyles-3e37929b6847d0216b0aabe296ed9a76_h.jpg?ts=93246" class="clb cboxElement"><img src="http://cdnimg.visualizeus.com/thumbs/3e/37/hairstyles-3e37929b6847d0216b0aabe296ed9a76_h.jpg?ts=93246" alt="" width="248" height="400"></a><a href="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_4.jpg" class="clb cboxElement"><img src="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_4.jpg" alt="" width="400" height="544"></a><a href="http://womeninfashion.net/wp-content/uploads/2013/11/heart-face-shape-hairstyles-jennifer-aniston.jpg" class="clb cboxElement"><img src="http://womeninfashion.net/wp-content/uploads/2013/11/heart-face-shape-hairstyles-jennifer-aniston.jpg" alt="" width="420" height="560"></a><a href="http://thisgirlscity.com/wp-content/uploads/2013/07/reese.jpg" class="clb cboxElement"><img src="http://thisgirlscity.com/wp-content/uploads/2013/07/reese.jpg" alt="" width="420" height="560"></a><a href="http://images.beautyriot.com/photos/200/hairstyles_heart_shape_face-200.jpg" class="clb cboxElement"><img src="http://images.beautyriot.com/photos/200/hairstyles_heart_shape_face-200.jpg" alt="" width="200" height="272"></a></p>
            <p><a href="http://www.youbeauty.com/p/482031/thumbnail/entry_id/0_hmc2pi25/width/0/height/0/quality/90" class="clb cboxElement"><img src="http://www.youbeauty.com/p/482031/thumbnail/entry_id/0_hmc2pi25/width/0/height/0/quality/90" alt="" width="200" height="290"></a><a href="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_11.jpg" class="clb cboxElement"><img src="http://www.hairstyles123.com/hairstylepics/faces/hairstyles_for_heart_shaped_faces/heart_shaped_faces_hairstyle_11.jpg" alt="" width="520" height="780"></a><a href="http://www.allure.com/images/hair-ideas/2012/05/heart-face-shape-hairstyles-reese-witherspoon.jpg" class="clb cboxElement"><img src="http://www.allure.com/images/hair-ideas/2012/05/heart-face-shape-hairstyles-reese-witherspoon.jpg" alt="" width="420" height="560"></a><a href="http://slodive.com/wp-content/uploads/2012/03/hairstyles-for-heart-shaped-faces/heart-shape-glasses.jpg" class="clb cboxElement"><img src="http://slodive.com/wp-content/uploads/2012/03/hairstyles-for-heart-shaped-faces/heart-shape-glasses.jpg" alt=""></a><a href="http://www.beautifulhairstyle.net/wp-content/uploads/2014/02/Long-Hairstyles-For-Heart-Shaped-Faces.jpg" class="clb cboxElement"><img src="http://www.beautifulhairstyle.net/wp-content/uploads/2014/02/Long-Hairstyles-For-Heart-Shaped-Faces.jpg" alt=""></a><a href="http://beautyhairtotoe.com/wp-content/uploads/2013/08/rby-heart-shaped-reese-marked-mdn.jpg" class="clb cboxElement"><img src="http://beautyhairtotoe.com/wp-content/uploads/2013/08/rby-heart-shaped-reese-marked-mdn.jpg" alt=""></a><a href="http://www.prettydesigns.com/wp-content/uploads/2013/09/Hairstyle-for-Oval-shaped-Women.jpg" class="clb cboxElement"><img src="http://www.prettydesigns.com/wp-content/uploads/2013/09/Hairstyle-for-Oval-shaped-Women.jpg" alt="" width="550" height="775"></a><a href="http://www.hairnext.com/wp-content/uploads/2014/05/Heart-Shaped-Face-Best-Short-Bangs-Hairstyle-For-Fine-Hair.jpg" class="clb cboxElement"><img src="http://www.hairnext.com/wp-content/uploads/2014/05/Heart-Shaped-Face-Best-Short-Bangs-Hairstyle-For-Fine-Hair.jpg" alt="Heart Shaped Face Best Short Bangs Hairstyle For Fine Hair"></a><a href="http://www.hairnext.com/wp-content/uploads/2014/05/Short-Bob-Side-Swept-For-Long-Face-Shape.jpg" class="clb cboxElement"><img src="http://www.hairnext.com/wp-content/uploads/2014/05/Short-Bob-Side-Swept-For-Long-Face-Shape.jpg" alt="Short Bob Side Swept  For Long Face Shape"></a></p>
            <p>&nbsp; <img src="http://www.hairnext.com/wp-content/uploads/2014/05/Short-blonde-Curly-hairstyle.jpg" alt="Short blonde Curly hairstyle:"></p></div>
            """
        doc = fromstring(html)
        
        for el in doc.iter('img'):
#             el.tag = 'img'
            if el.getparent().tag == u"a":
                el.set("src", "www.google.com")
            else:
                e = etree.Element('a')
                e.set("href", el.get("src"))
                e.set("class", "clb")
                el.set("src", "www.yahoo.com")
                e.append(deepcopy(el))
                el.getparent().replace(el, e)
        
        print etree.tostring(doc)

    def testLinksSubstitution(self):
        html =u"""
            <div class="answer-body">
            <p>w New Looku, czy Top Shopie często mają ciuchy inspirowane folklorem. a Top Shop ma sklep on-line z dostwą do PL, bo w stacjonarnych sklepach kolekcja jest niewielka.</p>
            <p><a href="http://www.topshop.com/en/tsuk/product/clothing-427/folklore-2722975/folk-embroidered-jumper-2961591?bi=1&amp;ps=20">http://www.topshop.com/en/tsuk/product/clothing-427/folklore-2722975/folk-embroidered-jumper-2961591?bi=1&amp;ps=20</a></p>
            <p><a href="http://www.topshop.com/en/tsuk/product/clothing-427/folklore-2722975/folklore-print-dress-2884141?bi=1&amp;ps=20">http://www.topshop.com/en/tsuk/product/clothing-427/folklore-2722975/folklore-print-dress-2884141?bi=1&amp;ps=20</a></p>
            <p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://media.topshop.com/wcsstore/TopShop/images/catalog/23N02FBLK_2_thumb.jpg" class="clb cboxElement"><img src="http://media.topshop.com/wcsstore/TopShop/images/catalog/23N02FBLK_2_thumb.jpg" alt="Folk Embroidered Jumper"></a></p>
            <p><a href="http://www.topshop.com/en/tsuk/product/clothing-427/folklore-2722975/folklore-print-dress-2884141?bi=1&amp;ps=20" target="_blank">http://www.topshop.com/en/tsuk/product/clothing-427/folklore-2722975/folklore-print-dress-2884141?bi=1&amp;ps=20</a></p>
            <p><a href="http://media.topshop.com/wcsstore/TopShop/images/catalog/10S27FMUL_2_thumb.jpg" class="clb cboxElement"><img src="http://media.topshop.com/wcsstore/TopShop/images/catalog/10S27FMUL_2_thumb.jpg" alt="Folklore Print Dress"></a></p>
            </div>
            """
        reg = re.compile('<a\s((?![^>]*\starget=)[^>]*)>', re.IGNORECASE)
        self.assertIsNotNone(reg.search(html), "Test data with no links to update")
        html = autolink(html)
        self.assertIsNone(reg.search(html), "Some links were not succesfully updated with targe=_blank \n%s" % html)
           
    def testHtmlClean(self):
        html = ur'<iframe width="420" height="315" src="//www.youtube.com/embed/dkcZb0GhQEg" frameborder="0" allowfullscreen></iframe>'
        html_cleaner = get_html_cleaner()
        self.assertTrue(html_cleaner.clean_html(html), "Iframe got whacked")
           
        html = ur'<p>&lt;iframe width="420" height="315" src="//www.youtube.com/embed/dkcZb0GhQEg" frameborder="0" allowfullscreen&gt;&lt;/iframe&gt;</p>'
        cleaned = html_cleaner.clean_html(html)
        self.assertGreater(cleaned.find(ur'<iframe'), -1, "Iframe got whacked")
        self.assertGreater(cleaned.find(ur'frameborder'), -1, "frameborder attribute got whacked")
        self.assertGreater(cleaned.find(ur'allowfullscreen'), -1, "Iframe got whacked")
