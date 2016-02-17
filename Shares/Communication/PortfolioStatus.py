from sendgridEmail import Email
from twilioSMS import SMS
from Shares.share_data import share_data
from manage import db
from Shares.models import User
from flask import render_template
from PortfolioData import PortfolioData


class PortfolioStatus():
    #email.sendEmail("xkv1922c@gmail.com", "alerts@lucasamos.net", "Your portfolio status", html)

    email = Email("lucas_amos", "beadle10")
    sms = SMS("ACb3d2405e15df8441919994ce553eae4b", "41e85a6638606f578860825b750462c1")


    session = db.session()

    #values = share_data.getportfoliovalues(user)


    for user in session.query(User):

        portfoliovalues = share_data.getportfoliovalues(user.username)
        html =PortfolioData.sharedata(user.username)
        email.sendEmail(user.email, "alerts@lucasamos.net", "Your portfolio status", html)


        print user.username
        print user.email


