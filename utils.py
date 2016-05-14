#!/usr/bin/env python3
from __future__ import print_function
from urllib.parse import urlparse
import logging

import praw
import requests
import weasyprint
from bs4 import BeautifulSoup
from imgurpython import ImgurClient

import config


def save_as_image(html, filename):
    '''Uses Weasyprint to convert HTML to Image.'''
    logging.info("reading html file... {}".format(html))
    wp = weasyprint.HTML(string=html)

    logging.info("generating png...")
    wp.write_png(filename)
    logging.info("generated.")


def readability_response(url):
    req_url = config.READABILITY_API_URL.format(url)
    response = requests.get(req_url).json()
    error = response.get('error', None)
    if error:
        logging.warning("Error reason: ".format(error))
        return None
    return response


def parse_snippet(domain, body):
    soup = BeautifulSoup(body, 'html.parser')


    def search_for_text(class_name):
        content = soup.find('div', {'class': class_name})
        logging.info("got content {}".format(content))
        if content:
            return ['\n\n*' + snippet.text.replace('\n', '').strip() + '*\n'
                    for snippet in content.find_all('p')[:2]]


    if 'folha' in domain:
        return search_for_text('content')
    elif 'oglobo' in domain:
        return search_for_text('corpo')


def upload_image(imgur, filename):
    return imgur.upload_from_path(filename)['link']


def reddit_login():
    reddit = praw.Reddit(user_agent="u-folha-de-sp-by-u-epseh")
    reddit.login(
        config.REDDIT_USERNAME, config.REDDIT_PASSWORD, disable_warning=True
    )
    logging.info("logged into reddit")
    return reddit


def imgur_login():
    logging.info("logging into imgur")
    return ImgurClient(config.IMGUR_API_CLIENT, config.IMGUR_API_SECRET)


def parse_url(news_url):
    logging.info("news url: {}".format(news_url))
    url = None
    if 'folha' in news_url:
        if 'tools' in news_url:
            return url
        elif '?mobile' in news_url:
            url = news_url.replace('?mobile', '')
            url = url.replace('/m.folha', '/www1.folha')
        elif "web.archive" in news_url:
            url = news_url.replace('https://web.archive.org/save/', '')
        elif "http://f5" in news_url:
            # try http and https
            url = news_url.replace('http://f5', 'http://').replace('https://f5', 'https://')
        else:
            url = urlparse(news_url)
            url = url.scheme + '://' + url.netloc + url.path
        url = print_folha_url(url)
        logging.info("formatted Folha url: {}".format(url))
    elif 'oglobo' in news_url:
        # we cannot parse blog posts, so ignore them.
        if not 'blogs' in news_url:
            url = urlparse(news_url)
            url = url.scheme + '://' + url.netloc + url.path
    return url


def print_folha_url(url):
    return 'http://tools.folha.com.br/print?site=emcimadahora&url={}'.format(url)
    

def subreddits_posts(conn):
    submissions = []

    def get_submissions_from_subreddits(subs):
        for sub in subs:
            for submission in conn.get_subreddit(sub).get_hot():
                submissions.append(submission)
            for submission in conn.get_subreddit(sub).get_new():
                submissions.append(submission)

    get_submissions_from_subreddits(['brasil', 'BrasildoB'])
    for submission in submissions:
        if 'folha.uol' in submission.url or 'oglobo' in submission.url:
            yield submission


def html_beautify(title, body):
    soup = BeautifulSoup(body, 'html.parser')
    return '''<html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style type="text/css">
                body {
                    margin:40px auto;
                    max-width:650px;
                    line-height:1.6;
                    font-size:18px;
                    color:#444;
                    padding:0 10px;
                    background: white;
                }
                h1,h2,h3 {
                    line-height:1.2
                }
            </style>
        </head>
        <body>
        <h1>
            %s
        </h1>
            %s
        </body>
    </html>
    ''' % (title, soup.prettify())
