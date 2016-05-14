#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
import os
import time
import logging

import utils
import config


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def main():
    reddit_conn = utils.reddit_login()
    imgur_conn = utils.imgur_login()
    while True:
        try:
            for post in utils.subreddits_posts(reddit_conn):
                if post.id not in posts:
                    logging.info('New post: {}'.format(post.id))
                    url = utils.parse_url(post.url)
                    logging.info("parsed url: {}, post: {}".format(url, post))
                    if not url:
                        # tools.folha url or blogs post in case of oglobo. do not post. however, put it in post list so it doesn't keep getting processed
                        posts.append(post.id)
                        continue

                    response = utils.readability_response(url)
                    if not response:
                        # do not retry it.
                        posts.append(post.id)
                        logging.warning('something went wrong with readability {}'.format(response))
                        continue

                    title, body, domain = response['title'], response['content'], response['domain']

                    snippet = utils.parse_snippet(domain, body)
                    if not snippet:
                        posts.append(post.id)
                        logging.warning('something went wrong parsing {}'.format(response))
                        continue

                    formatted_html = utils.html_beautify(title, body)
                    utils.save_as_image(
                        html=formatted_html,
                        filename=config.DOWNLOAD_FILENAME
                    )
                    img_link = utils.upload_image(imgur_conn, config.DOWNLOAD_FILENAME).replace("http://", "https://")
                    logging.info("img link generated: {}".format(img_link))
                    post.add_comment(
                        '''Eu sou um bot e fiz o upload desta página como imagem para vocês!
                        A imagem pode ser acessada por este [link]({}).
                        Você pode acessar o link para ler por [este]({}).
                        Você pode ler um pouco da matéria abaixo: {} {}
                        '''.format(img_link, url, *snippet)
                    )
                    os.remove(config.DOWNLOAD_FILENAME)
                    posts.append(post.id)

            logging.info("waiting...")
            time.sleep(900)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.warning("error occurred {}".format(e))
            pass  # do not die


if __name__ == '__main__':
    main()
