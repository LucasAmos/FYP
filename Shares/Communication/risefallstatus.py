import sys
sys.path.append("/home/lucasamos/FYP")

from Shares.models import User, Userownedshare
from twilioSMS import SMS
from manage import db
from Shares.share_data import share_data
import datetime


class risefallstatus():

    sms = SMS("ACb3d2405e15df8441919994ce553eae4b", "41e85a6638606f578860825b750462c1")
    session = db.session()
    today = datetime.datetime.today().weekday()

    if today is not 6 or not 7:

        for user in session.query(User):


            if user.smsenabled:

                print "** sms's enabled: **"

                for share in session.query(Userownedshare).filter_by(user=user.username):

                    print ""
                    print user.username
                    ticker = share.ticker
                    print ticker
                    change = float(share_data.JSONShareFall(ticker)['query']['results']['quote']['Change'])
                    print "rise/fall: %s" %float(share_data.JSONShareFall(ticker)['query']['results']['quote']['Change'])


                    print "triggerlevel: %s" \
                          " " %share.triggerlevel

                    if share.smsalert:

                        if share.triggerlevel < 0:

                            if change < share.triggerlevel:
                                print "alert: Sent"

                            else:
                                print "alert: False"

                        elif share.triggerlevel > 0:
                            if change > share.triggerlevel:
                                print "alert: Sent"

                            else:
                                print "alert: False"


                    else:
                        print "alert disbaled for this share"

                        print ""
                        # else:
                        #     print ""
                        #     print "** sms's disabled: **"

        for user in session.query(User):

            if not user.smsenabled:

                print "** sms's disabled: **"
                for share in session.query(Userownedshare).filter_by(user=user.username):

                    print user.username
                    ticker = share.ticker
                    print ticker
                    print float(share_data.JSONShareFall("RBS")['query']['results']['quote']['Change'])
                    print user.smsenabled
                    print ""
