import time
import tweepy
import schedule
from datetime import datetime
from pytz import timezone
from functools import partial
from itertools import takewhile
from bosonnlp import BosonNLP
from config import consumer_key, consumer_secret, \
    access_token, access_token_secret, bosonnlp_token, tz


time_difference = (datetime.now(timezone(tz)).utcoffset().total_seconds() +
                   time.timezone)
exec_time = '{:0>2d}:59'.format((24 - int(time_difference / (60 * 60)) - 1) % 24)  # noqa

template = """\
Today emotional analysis result:
Positive: {}
Negative: {}
from goo.gl/RKywab
"""

nlp = BosonNLP(bosonnlp_token)
sentiment = partial(nlp.sentiment, model='weibo')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def kibun_job():
    today = datetime.utcnow().date()
    recent_tweets = api.user_timeline()
    tweets = takewhile(lambda x: x.created_at.date() == today, recent_tweets)

    grouped_probability = zip(*map(lambda x: sentiment(x.text).pop(), tweets))
    result = map(lambda nums: sum(nums) / len(nums), grouped_probability)
    api.update_status(template.format(*result))


if __name__ == '__main__':
    import os
    from daemon import DaemonContext, pidfile
    current_path = os.getcwd()
    pid_path = os.path.join(current_path, 'kibun.pid')
    with DaemonContext(working_directory=current_path,
                       pidfile=pidfile.PIDLockFile(pid_path)):
        schedule.every().day.at(exec_time).do(kibun_job)
        while True:
            schedule.run_pending()
            time.sleep(1)
