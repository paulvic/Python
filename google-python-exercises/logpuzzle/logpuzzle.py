#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import codecs

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def url_sorter(url):
  match = re.search(r'-(\w+)-(\w+)\.\w+', url)
  if match:
    return match.group(2)
  else:
    return url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  match = re.search(r'.+_(.+)', filename)
  host = ""
  if match:
    host = "http://" + match.group(1)
  else:
    print filename + " name is not in the correct format (name_www.example.com)"
    sys.exit(1)

  urls = {}
  with codecs.open(filename, 'rU', 'utf-8') as f:
    for line in f:
      match = re.search(r'GET (\S+/puzzle/\S+)', line)

      if match:
        url = host + match.group(1)
        urls[url] = 1
  
  return sorted(urls.keys(), key=url_sorter)
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  dest_dir = os.path.abspath(dest_dir)
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  index_file = os.path.join(dest_dir, "index.html")
  with codecs.open(index_file, 'wU', 'utf-8') as f:
    f.write("<html><body>\n")
    i = 0
    for img in img_urls:
      extension = img[img.rindex('.'):]
      filename = "img" + str(i) + extension
      destination = os.path.join(dest_dir, filename)
      print img + " >> " + destination
      urllib.urlretrieve(img, destination)
      i += 1
      f.write("<img src='" + filename + "'>")
    f.write("\n</body></html>\n")

  os.system(index_file)
    
    

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
