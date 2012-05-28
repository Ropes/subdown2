#!/usr/bin/python

import sys
import urllib2
import time
import gui
import os
import download
import simplejson


helptext = """
(C) 2012, Kunal Mehta, under the MIT License

Syntax: subdown2 subreddit[,subreddit] pages [--force]

 - You can add as many subreddits as you wish, just split them with a comma (no spaces).
 - If an integer for pages is not set (or is not understood) it will be set to 1.
 - The force option will re-download all images and overwrite them. Default option is not to do so.
"""








class Client:

  def __init__(self, name, pages, force):
    self.name = name
    self.headers = {
      'User-agent': 'subdown2 by /u/legoktm -- https://github.com/legoktm/subdown2'
    }
    self.pages = pages
    self.force = force
    self.r = 'r/%s' %(self.name)
    print 'Starting %s' %(self.r)
    self.dl = download.Downloader(self.name, self.force)
    try:
      os.mkdir(self.name.lower())
    except OSError:
      pass
    
  def parse(self, page):
    print 'Grabbing page %s of %s from %s' %(page, self.pages, self.r)
    if page != 1:
      url = 'http://reddit.com/%s/.json?after=%s' %(self.r, self.after)
    else:
      url = 'http://reddit.com/%s/.json' %(self.r)
    req = urllib2.Request(url, headers=self.headers)
    obj = urllib2.urlopen(req)
    text = obj.read()
    obj.close()
    try:
      data = simplejson.loads(text)
    except simplejson.decoder.JSONDecodeError:
      print text
      sys.exit(1)
    try:
      self.after = data['data']['after']
      items = data['data']['children']
    except KeyError:
      try:
        if data['error'] == 429:
          print 'Too many requests on the reddit API, taking a break for a minute'
          time.sleep(60)
          self.parse(page)
          return
      except KeyError:
        print data    
        sys.exit(1)
    for item in items:
      item2 = item['data']
      #print item2
      self.dl.setTime(item2['created'])
      try:
        self.process_url(item2)
      except KeyboardInterrupt:
        print 'Signal recieved'
        sys.exit(1)
      except urllib2.HTTPError:
        print 'HTTP Error on %s.' %(item2['url'])
      except:
        print 'Error-on %s.' %(item2['url'])

  def process_url(self, object):
    domain = object['domain']
    url = object['url']
    if domain == 'imgur.com':
      self.dl.Imgur(url)
    elif domain == 'i.imgur.com':
      self.dl.Raw(url)
    elif domain == 'twitter.com':
      try:
        self.dl.Twitter(url)
      except:
        print 'Skipping %s since it is not supported yet' %(url)
    elif domain == 'pagebin.com':
      self.dl.Pagebin(url)
    elif 'media.tumblr.com' in domain:
      self.dl.Raw(url)
    elif 'self.' in domain:
      print 'Skipping self post: "%s"' %(item2['title'])
    elif (domain == 'quickmeme.com') or (domain == 'qkme.me'):
      self.dl.qkme(url)
    elif domain == 'bo.lt':
      self.dl.bolt(url)
    else: #Download all the images on the page
      self.dl.All(url)
  def run(self):
    for pg in range(1,self.pages+1):
      self.parse(pg)

def cleanup():
  try:
    os.remove('bad_imgur.jpg')
  except OSError:
    pass


def main():
  try:
    subreddits = sys.argv[1]
    if len(sys.argv) >= 3:
      pg = int(sys.argv[2])
    else:
      pg = 1
    force = False
    for arg in sys.argv:
      if arg == '--force':
        force = True
        
    for subreddit in subreddits.split(','):
      app = Client(subreddit,pg, force)
      app.run()
  except IndexError: #no arguments provided
    print helptext
    #gui.main()
  finally:
    cleanup()
    




if __name__ == "__main__":
  main()
