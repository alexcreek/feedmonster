import os
import time
import sqlite3
import smtplib
from email.mime.text import MIMEText
import feedparser

class FeedMonster(object):
    def __init__(self):
        """main"""
        self.db = 'feed.db'
        self.url = 'https://www.reddit.com/r/Invites/.rss'
        while True:
            self.init_db()
            feed = self.pull_feed()
            self.process_feed(feed)
            time.sleep(600)

    def init_db(self):
        if os.path.isfile(self.db):
            return
        else:
            conn = sqlite3.connect(self.db)
            c = conn.cursor()
            c.execute('''CREATE TABLE feed (title text UNIQUE)''')
            conn.commit()
            conn.close()

    def pull_feed(self):
        try:
            return feedparser.parse(self.url)
        except:
            print 'shits down'

    def process_feed(self, feed):
        # open db
        conn = sqlite3.connect(self.db)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()

        # get old junk
        saved_feeds = c.execute('SELECT title FROM feed').fetchall()

        # get busy
        for i in feed['items']:
            if i['title'] in saved_feeds:
                pass
            else:
                # email
                print i['title'], i['link']
                self.send_email(i['title'], i['link'])

            # save
            try:
                c.execute('INSERT INTO feed VALUES (?)',(i['title'],))
            except sqlite3.IntegrityError:
                pass

        # close db
        conn.commit()
        conn.close()

    def send_email(self, subject, message):
        sender = 'feedmonster@totallylegitfqdn.com'
        receivers = 'me@alexcreek.com'

        email = MIMEText(message)
        email['Subject'] = subject
        email['From'] = sender
        email['To'] = receivers
        s = smtplib.SMTP('smtp')
        s.sendmail(sender, [receivers], email.as_string())
        s.quit()


if __name__ == '__main__':
    FeedMonster()
