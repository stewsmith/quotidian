import gmail, time, smtplib, re
from secrets import gmail_username, gmail_password, gmail_email
from datetime import timedelta, datetime, date
from email_remover import unquote
import sys

SEND_EMAIL_ALWAYS = False

def get_users(g):
    emails = g.inbox().mail(prefetch=True)

    users = set()

    for email in emails:
        user = email.fr

        # remove noreply addresses
        if 'noreply' in user:
            continue

        users.add(email.fr)
    return users

def get_mail_message(g, user):
    msg = pick_old_message(g, user)
    day = time.strftime("%A %b %d")
    subj = 'It\'s ' + day + ' - How did your day go?'

    message = 'Subject: %s\n\n%s' % (subj, msg)
    return message

def parse_email(user):
    user_email = user
    m = re.search('.+<(.+)>', user)

    if m:
        user_email = m.group(1)
    return user_email

def pick_old_message(g, user):
    TIME_PERIODS = [
        ('year' , 365),
        ('month', 30),
        ('week',  7),
        ('day',   1),
    ]

    TIME_PERIODS = [
        ('year' , 1),
        ('month', 0.75),
        ('week',  0.5),
        ('day',   0.25),
    ]

    TIME_WINDOW = timedelta(days=1)
    TIME_WINDOW = timedelta(hours=1)

    for period, num_days in reversed(TIME_PERIODS):
        # check to see if there's an email
        # return that messag

        after = date.today() - timedelta(num_days)
        after = datetime.now() - timedelta(num_days)
        before  = after + TIME_WINDOW

        print "Checking for message %s between %s and %s" % (period, before, after)

        user_email = parse_email(user)
        result = g.inbox().mail(sender=user_email, before=before, after=after, prefetch=True)

        if result:
            old_messages = ""
            for item in result:
                old_messages += unquote(item.body).strip() + "\n\n"

            body = 'Reply to this email with your entry!\nA %s ago, you wrote...\n\n%s' % (period, old_messages)
            return body


    return None

def send_message(user, message):
    print "Sending a message to %s" % (user)
    from_address = gmail_email
    to_address = user

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(gmail_username, gmail_password)
    server.sendmail(from_address, to_address, message)
    server.quit()

if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) > 1:
        SEND_EMAIL_ALWAYS = (sys.argv[1] == 'demo')

    g = gmail.login(gmail_username, gmail_password)
    users = get_users(g)

    for user in users:
        message = get_mail_message(g, user)

        print message

        if SEND_EMAIL_ALWAYS:
            send_message(user, message)
        else:
            # check if message is sent today.
            today_after  = date.today()
            today_before = today_after + timedelta(days=1)

            result = g.sent_mail().mail(to=parse_email(user), before=today_before, after=today_after, prefetch=True)

            if not result:
                send_message(user, message)
