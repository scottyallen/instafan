import re
import time
import utils

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import selenium.common.exceptions

class Profile(object):

  def __init__(self, username, browser):
    self.username = username
    self.browser = browser

  def following(self):
    print "Getting following list..."
    utils.get(self.browser, 'https://www.instagram.com/%s/' % self.username)
    self.browser.find_element_by_partial_link_text(' following').click()
    last_count = 0
    while True:
      for i in xrange(5):
        self.browser.execute_script(
        '''function getElementByXpath(path) {
             return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
           }
           ul = getElementByXpath("//div[@role=\'dialog\']//ul");
           ul.children[ul.childElementCount - 1].scrollIntoView()
        ''')
        time.sleep(.2);
      xpath = '//div[@role="dialog"]//ul/li//a[text()!=""]'
      urls = [e.get_attribute('href') for e in self.browser.find_elements_by_xpath(xpath)]
      if last_count == len(urls):
        break
      last_count = len(urls)

    return [utils.extract_username(url) for url in urls]

  def follow(self):
    utils.get(self.browser, 'https://www.instagram.com/%s/' % self.username)
    try:
      self.browser.find_element_by_xpath('//button[text()="Follow"]').click()
    except selenium.common.exceptions.NoSuchElementException:
      print "Already following %s" % self.username
      return []
    print "Followed %s" % self.username
    suggested = [e.get_attribute('href') for e in self.browser.find_elements_by_xpath('//ul/li/div/div/a')]
    suggested = [utils.extract_username(url) for url in suggested]
    return suggested

  def unfollow(self):
    utils.get(self.browser, 'https://www.instagram.com/%s/' % self.username)
    try:
      self.browser.find_element_by_xpath('//button[text()="Following"]').click()
    except selenium.common.exceptions.NoSuchElementException:
      print "Not following %s" % self.username
      return
    print "Unfollowed %s" % self.username

  def suggested(self):
    utils.get(self.browser, 'https://www.instagram.com/%s/' % self.username)
    e = (self.browser.find_elements_by_class_name('coreSpriteDropdownArrowBlue5') +
         self.browser.find_elements_by_class_name('coreSpriteDropdownArrowWhite'))
    e[0].click()
    suggested = [e.get_attribute('href') for e in self.browser.find_elements_by_xpath('//ul/li/div/div/a')]
    suggested = [utils.extract_username(url) for url in suggested]
    return suggested

  def follower_count(self):
    utils.get(self.browser, 'https://www.instagram.com/%s/' % self.username)
    span = self.browser.find_element_by_partial_link_text(' followers').find_element_by_tag_name('span')
    return int(span.get_attribute('title').replace(',', ''))

class User(object):

  def __init__(self, username, browser):
    self.username = username
    self.browser = browser

  def is_logged_in(self):
    utils.get(self.browser, 'https://www.instagram.com/', force=True)
    e = self.browser.find_elements_by_link_text('Profile')
    return len(e) > 0

  def current_user(self):
    utils.get(self.browser, 'https://www.instagram.com/')
    e = self.browser.find_elements_by_link_text('Profile')
    if not e:
      return
    return utils.extract_username(e[0].get_attribute('href'))

  def login(self, password):
    print 'Logging in...'
    utils.get(self.browser, 'https://www.instagram.com/accounts/login/')

    self.browser.find_element_by_name('username').send_keys(self.username)
    self.browser.find_element_by_name('password').send_keys(password)
    self.browser.find_element_by_tag_name('button').click()

    element = WebDriverWait(self.browser, 10).until(
        expected_conditions.title_is('Instagram')
    )

  def logout(self):
    print "Logging out..."
    self.browser.delete_all_cookies()

  def maybe_login(self, password):
    if not self.is_logged_in() or self.current_user() != self.username:
      print "Current user: %s" % self.current_user()
      if self.current_user != self.username:
        self.logout()
      self.login(password)
      if self.is_logged_in():
        print 'Successfully logged in'
      else:
        print 'Failed to login'
    else:
      print 'Already logged in'
