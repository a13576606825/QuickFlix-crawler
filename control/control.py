'''
Master control class
--------------------------------------------
'''

import logging

import config
import remote
import store

log = logging.getLogger(__name__)


''' Top Level Method'''
def start():
    # fetch_html
    url = 'http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/'
    html = remote.crawler.fetch_html(url) # TODO catch exception
    print('==============')

    # parse_review
    review = remote.crawler.parse_review(html)
    if review is None:
        print('Page does not contain a movie review json')
    else:
        movie_title = review['itemReviewed']['name']
        print(movie_title)

        # My DB already contains the json so I'm commenting this part out
        #store.store.insert_into_db('crawler', review)

        # (TO FIX) Check that stored review can be retrieved
        reviews_in_db = store.store.read_from_db('crawler', movie_title)
        if reviews_in_db == 0:
            print('No reviews for this movie')
        else:
            for rev in reviews_in_db:
                print('Found a review by ' + review['author'][0]['name'])

    # parse_urls
    urls = remote.crawler.parse_urls(html)
    if len(urls) == 0: print('No urls found')
    for url in urls:
        i=1
        #print(url)
