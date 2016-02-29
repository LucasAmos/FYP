from News import News


class yahooz():


     stories = News.getNews("reindert")

     for story in stories:

         print "**"
         print story, stories[story]

