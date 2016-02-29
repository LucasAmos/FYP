import xml.sax

from Shares.News import News


class yahooz(xml.sax.ContentHandler):



     stories = News.getNews("twtr,goog, fb")

     for story in stories:

         print "**"
         print story, stories[story]

