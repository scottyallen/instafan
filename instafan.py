import random
import sys

from selenium import webdriver

import instagram
import utils
import gflags

gflags.DEFINE_string('credentials', None,
                     'Login credentials.  Filename for file with USERNAME= and PASSWORD= on separate lines')
FLAGS = gflags.FLAGS

def main(argv):

  USERNAME, PASSWORD = utils.load_credentials(FLAGS.credentials)

  b = webdriver.Chrome()
  b.implicitly_wait(5)

  utils.get(b, 'https://www.instagram.com/')
  utils.load_cookies(b, 'cookies.json', 'instagram.com')
  user = instagram.User(USERNAME, b)
  user.maybe_login(PASSWORD)

  profile = instagram.Profile(USERNAME, b)

  following_usernames = profile.following()
  suggested_usernames = instagram.Profile('lonelyplanet', b).suggested()
  print suggested_usernames
  while True:
    if random.random() < 0.6:
      username = random.choice(suggested_usernames)
      profile = instagram.Profile(username, b)
      suggested_usernames.extend(profile.follow())
      suggested_usernames.remove(username)
      following_usernames.append(username)

      if random.random() < 0.05:
        utils.delay(60 * 30)
      else:
        utils.delay(30)

    if random.random() < 0.6:
      username = random.choice(following_usernames)
      profile = instagram.Profile(username, b)
      profile.unfollow()
      following_usernames.remove(username)

      utils.delay(15)

  utils.save_cookies(b, 'cookies.json')
  b.close()

if __name__ == '__main__':
  argv = gflags.FLAGS(sys.argv)
  main(argv)
