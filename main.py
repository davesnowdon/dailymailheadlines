import SimpleHTTPServer
import urllib
import SocketServer
import HTMLParser
import re
import markov

PORT = 8080


class Parser(HTMLParser.HTMLParser):
    def __init__(self, *args, **kwargs):
        self.tagstack = set()
        self.headlines = []
        HTMLParser.HTMLParser.__init__(self, *args, **kwargs)

    def handle_starttag(self, tag, attrs):
        self.tagstack.add(tag)

    def handle_endtag(self, tag):
        self.tagstack.discard(tag)

    def handle_data(self, data):
        if self.tagstack & set(("h2", "h3", "strong")) and "script" not in self.tagstack and "style" not in self.tagstack:
            if len(data.strip()) > 10:
                self.headlines.append(data.strip())


class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not (self.path.startswith("http://dailymail.co.uk") or
          self.path.startswith("http://www.dailymail.co.uk")):
            #print self.path
            self.copyfile(urllib.urlopen(self.path), self.wfile)
            return

        f = urllib.urlopen(self.path)
        if f.info().gettype() != "text/html":
            self.copyfile(f, self.wfile)
            return

        data = f.read()
        p = Parser()
        p.feed(data)
        p.close()

        print p.headlines

        for headline, replacement in zip(p.headlines, markov.gimme_headlines(p.headlines)):
#             data = data.replace(headline, "Fury as fluffy kittens steal British jobs!")
            data = data.replace(headline, replacement)

        self.wfile.write(data)


httpd = SocketServer.ThreadingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()