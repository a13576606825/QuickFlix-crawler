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

        # Commented out for now to prevent duplicate storage of the variety.com review
        #print('Storing a review of ' + movie_title)
        #store.store.insert_into_db('crawler', review)

        # Check that stored review can be retrieved
        print('Finding reviews...')
        reviews_in_db = store.store.read_from_db('crawler', movie_title)
        if reviews_in_db == 0:
            print('No reviews found for ' + movie_title)
        else:
            for rev in reviews_in_db:
                print('Found a review by ' + rev['author'][0]['name'])

    # parse_urls
    urls = remote.crawler.parse_urls(html)
    if len(urls) == 0: print('No urls found')
    for url in urls:
        i=1
        #print(url)
