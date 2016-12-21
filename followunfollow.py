import random
import sys

from selenium import webdriver

import instagram
import utils


import sys

import gflags

gflags.DEFINE_string('credentials', None,
                     'Login credentials.  Filename for file with USERNAME= and PASSWORD= on separate lines')
FLAGS = gflags.FLAGS

def main(argv):
  USERNAME, PASSWORD = utils.load_credentials(FLAGS.credentials)
  b = webdriver.PhantomJS()
  b.set_window_size(1120, 550)
  b.implicitly_wait(5)
  print "Created webdriver"

  utils.get(b, 'https://www.instagram.com/')
  print "Loaded homepage"
  utils.load_cookies(b, '%s_cookies.json' % USERNAME, 'instagram.com')
  print "Loaded cookies"
  user = instagram.User(USERNAME, b)
  user.maybe_login(PASSWORD)
  utils.save_cookies(b, '%s_cookies.json' % USERNAME)

  profile = instagram.Profile(USERNAME, b)

  try:
    following_usernames = set(profile.following())
    follow_set = set([x.strip() for x in open(argv[1]).readlines()])

    def following():
      return list(follow_set.intersection(following_usernames))

    def not_following():
      return list(follow_set.difference(following_usernames))

    while True:
      print "Following %d out of %d" % (len(following()), len(follow_set))
      if random.random() < 0.6:
        username = random.choice(not_following())
        profile = instagram.Profile(username, b)
        profile.follow()
        following_usernames.add(username)

        if random.random() < 0.05:
          utils.delay(60 * 30)
        else:
          utils.delay(10)

      if len(following()) > len(follow_set) * 0.75 and random.random() < 0.6:
        username = random.choice(following())
        profile = instagram.Profile(username, b)
        profile.unfollow()
        following_usernames.remove(username)

        utils.delay(20)

      print "%s followers: %d" % (USERNAME, instagram.Profile(USERNAME, b).follower_count())

    b.close()
  except Exception,e:
    b.save_screenshot('screenshot.png')



if __name__ == '__main__':
  argv = gflags.FLAGS(sys.argv)
  main(argv)
