import sys
print sys.path
from Shares.share_data import share_data
from sendgridEmail import Email
from twilioSMS import SMS
from manage import db
from Shares.models import User
from PortfolioData import PortfolioData
import datetime

class PortfolioStatus():
    email = Email("lucas_amos", "beadle10")
    sms = SMS("ACb3d2405e15df8441919994ce553eae4b", "41e85a6638606f578860825b750462c1")
    session = db.session()
    today = datetime.datetime.today().weekday()

    noemail = 0
    daily =0
    weekly =0

    for user in session.query(User):

        if user.emailfrequency is 0:
            portfoliovalues = share_data.getportfoliovalues(user.username)
            html =PortfolioData.sharedata(user.username)
            email.sendEmail(user.email, "alerts@lucasamos.net", "Your portfolio status", html)

            print "no emails: "
            print user.username
            noemail+=1


        if user.emailfrequency is 1:
            portfoliovalues = share_data.getportfoliovalues(user.username)
            html =PortfolioData.sharedata(user.username)
            email.sendEmail(user.email, "alerts@lucasamos.net", "Your portfolio status", html)

            print "once a day email: "
            print user.username
            print user.email
            daily+=1


        if user.emailfrequency is 2 and today is 3:
            portfoliovalues = share_data.getportfoliovalues(user.username)
            html =PortfolioData.sharedata(user.username)
            email.sendEmail(user.email, "alerts@lucasamos.net", "Your portfolio status", html)

            print "once a week email:"
            print user.username
            weekly+=1


    print "No emails: %s" %noemail
    print "Daily emails: %s" %daily
    print "Weekly emails: %s" %weekly






        # portfoliovalues = share_data.getportfoliovalues(user.username)
        # html =PortfolioData.sharedata(user.username)
        # email.sendEmail(user.email, "alerts@lucasamos.net", "Your portfolio status", html)




