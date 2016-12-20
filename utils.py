import json
import os
import random
import re
import time

def get(browser, url, force=False):
  if force or url != browser.current_url:
    browser.get(url)

def extract_username(url):
  m = re.search(r'instagram.com/([^/]*)/', url)
  if m:
    return m.group(1)

def delay(amount):
  delay = amount + random.uniform(-1 * amount / 2, amount / 2)
  if delay < 60:
    print "Sleeping %d secs..." % delay
  else:
    print "Sleeping %d mins..." % (delay / 60)
  time.sleep(delay)

def save_cookies(b, filename):
  fh = open(filename, 'w')
  for cookie in b.get_cookies():
    json.dump(cookie, fh)
    fh.write('\n')
  fh.close()

def load_cookies(b, filename, domain):
  if not os.path.exists(filename):
    return
  for line in open(filename):
    cookie = json.loads(line.strip())
    if domain in cookie['domain']:
      b.add_cookie(cookie)

def load_credentials(filename):
  credentials = {}
  for line in open(filename):
    k, v = [x.strip() for x in line.split('=')]
    credentials[k.lower()] = v
  return credentials['username'], credentials['password']
