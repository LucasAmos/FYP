from sendgridEmail import Email
from twilioSMS import SMS


class sendMessage():
    email = Email("lucas_amos", "beadle10")
    sms = SMS("ACb3d2405e15df8441919994ce553eae4b", "41e85a6638606f578860825b750462c1")


    name = "Lucas"

    html = """\
<table style="width:100%">
  <tr>
    <td>{name}</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>""".format(name=name)

    email.sendEmail("xkv1922c@gmail.com", "alerts@lucasamos.net", "Your portfolio status",html)

    sms.sendSMS("+447506292708", "Your share GSK has fallen in price, "
                                 "log in to www.lucasamos.pythonanywhere.com to check it")

