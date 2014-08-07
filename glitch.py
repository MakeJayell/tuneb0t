#!/usr/bin/env python
'''
    $ pip install flickrapi
    ....
    $ FLICKR_API_KEY=92eebbee9a00509e87992c3670c39618 ./flick.py tag1[,tag2,tag3...]
'''
 
# http://www.flickr.com/services/api/flickr.photos.search.html
 
import flickrapi
import os
import sys
import random
api_key = os.environ['FLICKR_API_KEY']
url_template = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(photo_id)s_%(secret)s.jpg'
 
def url_for_photo(p):
    return url_template % {
        'server_id': p.get('server'),
        'farm_id': p.get('farm'),
        'photo_id': p.get('id'),
        'secret': p.get('secret'),
    }
    
 
#flickr = flickrapi.FlickrAPI(api_key)
#print url_for_photo(random.choice(flickr.photos_search(tags=sys.argv[1], per_page=20)[0]))