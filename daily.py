import gmail, time, smtplib
from secrets import gmail_username, gmail_password, gmail_email

def get_users(g):
    emails = g.inbox().mail(prefetch=True)

    users = set()

    for email in emails:
        email.fetch()

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

def pick_old_message(g, user):
    pass


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
        send_message(user, message)

    print users
