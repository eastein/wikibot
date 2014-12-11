import optparse
import datetime
import wikichanges
import mediorc
import time


POLL_TIME = 10

class WikiBot(mediorc.IRC):

    def __init__(self, server, nick, chan, wc):
        self.last_polled = 0
        self.wc = wc
        mediorc.IRC.__init__(self, server, nick, chan)

    def do_work(self):
        now = time.time()
        if now < self.last_polled + POLL_TIME :
            return

        # try :
        for msg in self.wc.poll():
            self.connection.privmsg(self._chan, msg)
        # except : sfjslfdkj

        self.last_polled = now


class WikiBotThread(mediorc.IRCThread):

    def __init__(self, server, nick, chan, wc):
        self.bot_create = lambda: WikiBot(server, nick, chan, wc)
        mediorc.IRCThread.__init__(self)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--gapi-key', dest='gapi_key', default=None,
                      help="GAPI key to use to shorten URLs. Skip it if you don't want URL shortening.")
    (options, args) = parser.parse_args()

    s, n, c, u = args

    k = options.gapi_key

    wc = wikichanges.WikiChanges(u, emit_start=False, max_age=datetime.timedelta(hours=1), gapi_key=k)

    try:
        s = WikiBotThread(s, n, c, wc)
    except IndexError:
        print 'usage: wikibot.py server nick channel atom_url'
        sys.exit(1)

    # threading,? NOPE
    s.run()
