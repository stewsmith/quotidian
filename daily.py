import gmail, time, smtplib, re
from secrets import gmail_username, gmail_password, gmail_email
from datetime import timedelta, datetime, date

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

    for period, num_days in TIME_PERIODS:
        # check to see if there's an email
        # return that messag

        before = date.today() - timedelta(num_days)
        before = datetime.now() - timedelta(num_days)
        after  = before + TIME_WINDOW

        print "Checking for message %s between %s and %s" % (period, before, after)


        user_email = parse_email(user)
        result = g.inbox().mail(sender=user_email, before=before, after=after, prefetch=True)

        if result:
            body = 'Reply to this email with your entry!\n A %s ago, you wrote...\n %s' % (period, result[0].body)
            return body


    return None


def send_message(user, message):
    from_address = gmail_email
    to_address = user

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(gmail_username, gmail_password)
    server.sendmail(from_address, to_address, message)
    server.quit()

if __name__ == '__main__':
    g = gmail.login(gmail_username, gmail_password)
    users = get_users(g)

    for user in users:
        message = get_mail_message(g, user)

        print message
        # send_message(user, message)

    # print users
