from News import News
import xml.sax

class yahooz(xml.sax.ContentHandler):



     stories = News.getNews("twtr,goog, fb")

     for story in stories:

         print "**"
         print story, stories[story]

