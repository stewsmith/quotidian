import gmail
from secrets import gmail_username, gmail_password, gmail_email

def get_senders(g):
    emails = g.inbox().mail(prefetch=True)

    senders = set()

    for email in emails:
        email.fetch()

        sender = email.fr

        # remove noreply addresses
        if 'noreply' in sender:
            continue

        senders.add(email.fr)
    return senders

def get_mail_message(g):
    pass

if __name__ == '__main__':
    g = gmail.login(gmail_username, gmail_password)
    senders = get_senders(g)

    print senders
