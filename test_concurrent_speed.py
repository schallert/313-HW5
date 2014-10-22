#!/usr/bin/env python

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#### PHASE 1 - Fire up the main browser that will be
#### entering information
display_main = Display(visible=0, size=(800, 600))
display_main.start()
browser_main = webdriver.Firefox()

browser_main.get('http://localhost:9001')
button = browser_main.find_element_by_id('button')
button.click()

# Wait until a pad is loaded
element = WebDriverWait(browser_main, 10).until(
    EC.title_contains("|")
)

main_url = browser_main.current_url
print main_url

viewers = []
#### PHASE 2 - Fire up a bunch of viewers that
#### will be monitoring the document
#### NOTE: due to memory constraints this is set to 3
####       but increasing it on a more powerful machine
####       would be helpful as well
for i in range(0,3):
  print "loading" + str(i)
  display = Display(visible=0, size=(800, 600))
  display.start()
  browser = webdriver.Firefox()

  browser.get(main_url)
  viewers.append(browser)
  print "loaded" + str(i)

# Wait until the last viewer has loaded the page
last = viewers[-1]
WebDriverWait(last, 10).until(EC.title_contains("|"))

#### PHASE 3 - Tell the main browser to send some messages
browser_main.switch_to_frame("ace_outer")
browser_main.switch_to_frame("ace_inner")
elem = browser_main.find_element_by_id('innerdocbody')
elem.send_keys("MY_TEST_MESSAGE")

# Record time message was sent in Unix epoch time
time_sent = time.time()

passed = True

#### Check that viewers all see the message
for viewer in viewers:
  viewer.switch_to_frame("ace_outer")
  viewer.switch_to_frame("ace_inner")
  elem = viewer.find_element_by_id('innerdocbody')
  WebDriverWait(viewer, 10).until(EC.text_to_be_present_in_element((By.ID, "innerdocbody"), "MY_TEST_MESSAGE"))

  # If more than 2 seconds between time sent and time seen in viewers,
  # this does not meet our standard
  if time.time() - time_sent > 2:
    passed = False
    print "FAILURE: More than 2 seconds elapsed between message sent and seen on viewers"

if passed:
  print "TEST PASSED"
