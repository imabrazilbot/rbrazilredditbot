#!/usr/bin/env python3
import os


REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
IMGUR_API_CLIENT = os.getenv("IMGUR_API_CLIENT")
IMGUR_API_SECRET = os.getenv("IMGUR_API_SECRET")
READABILITY_TOKEN = os.getenv("READABILITY_TOKEN")
READABILITY_API_URL = 'http://www.readability.com/api/content/v1/parser?url={}&token=%s' % READABILITY_TOKEN

HTML_FILENAME = 'readme.html'
DOWNLOAD_FILENAME = 'download.png'
