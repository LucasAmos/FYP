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
                print ""
                print "** sms's enabled for: %s **" %(user.username)

                for share in session.query(Userownedshare).filter_by(user=user.username):

                    ticker = share.ticker
                    name = str(share.name.name)
                    print name
                    change = float(share_data.JSONShareFall(ticker)['query']['results']['quote']['Change'])
                    print "rise/fall: %s" %float(share_data.JSONShareFall(ticker)['query']['results']['quote']['Change'])


                    print "triggerlevel: %s" \
                          " " %share.triggerlevel

                    if share.smsalert:

                        if share.triggerlevel < 0:

                            if change < share.triggerlevel:

                                #sms.sendSMS(user.phonenumber, "Your share %s has fallen by %s" % (name, change))

                                print "alert: Sent"
                                print""

                            else:
                                print "alert: False"
                                print""

                        elif share.triggerlevel > 0:
                            if change > share.triggerlevel:
                                name = str(share.name.name)
                                #sms.sendSMS(user.phonenumber, "Your share %s has risen by %s" % (name, change))

                                print "alert: Sent"
                                print""

                            else:
                                print "alert: False"
                                print""


                    else:
                        print "alert disabled for this share"

                        print ""
            else:
                print "** sms's disabled for: %s **" %(user.username)
                print""
