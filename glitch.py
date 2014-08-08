#!/usr/bin/env python

"""The Art & Science of Whatever Image Glitch script.

http://www.artofwhatever.com

Based on original script / idea by Cris Cuellar:

* http://blog.art21.org/2011/09/20/how-to-use-python-to-create-a-simple-flickr-photo-glitcher/

"""

import logging
import random
import requests 
from urllib.request import urlretrieve as downloadimage
from PIL import Image
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import configparser
config = configparser.ConfigParser()
config.read('user.config')


__author__ = "Steve Ed Alan > http://www.twitter.com/artofwhatever"
__copyright__ = "Copyright 2013, The Art & Science of Whatever > http://www.artofwhatever.com"
__license__ = "MIT"
__version__ = "1.0"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(name)s [%(levelname)s]: %(message)s')
logger = logging.getLogger("The Art & Science of Whatever::Image Glitch")

API_KEY = config['FLICKR CONFIG']['API_KEY']
FLICKR_API_URL = 'https://api.flickr.com/services/rest/'


class Glitch(object):

    def get_flickr_image(self, keyword):
        """ Find a random image from the public Flickr API:

            * Construct a URL from Flickr's RSS for a keyword.
            * Get a list of images
            * Choose one at random and return it.

        """
        keyword_search_parameters = {
            'method'    : 'flickr.photos.search',
            'api_key'   : API_KEY,
            'text'      : 'keyword',
            'sort'      : 'relevance',
            'format'    : 'rest'
        }

        recent_search_parameters = {
            'method'    : 'flickr.photos.getRecent',
            'api_key'   : API_KEY,
            'format'    : 'rest'
        }

        response = requests.get(FLICKR_API_URL, params=keyword_search_parameters)
        soup = BeautifulSoup(response.text)

        if not soup.findAll('photo'):
            logger.info("No images found for keyword: %s. Getting a recent image instead" % keyword)
            response = requests.get(FLICKR_API_URL, params=recent_search_parameters)
            soup = BeautifulSoup(response.text)

        image_list = []

        for image in soup.findAll('photo'):
            farm_id = dict(image.attrs)['farm']
            server_id = dict(image.attrs)['server']
            photo_id = dict(image.attrs)['id']
            secret = dict(image.attrs)['secret']
            size = 'z'
            image_url = "https://farm%s.staticflickr.com/%s/%s_%s_%s.jpg" % (farm_id, server_id, photo_id, secret, size)
            image_list.append(image_url)

        return random.choice(image_list)

    def download_an_image(self, image_url):
        """ Saves the file to the script directory """
        filename = image_url.split('/')[-1]
        downloadimage(image_url, filename)
        return filename

    def get_random_start_and_end_points_in_file(self, file_data):
        """ Shortcut method for getting random start and end points in a file """
        start_point = random.randint(2500, len(file_data))
        end_point = start_point + random.randint(0, len(file_data) - start_point)

        return start_point, end_point

    def splice_a_chunk_in_a_file(self, file_data):
        """ Splice a chunk in a file.

        * Picks out a random chunk of the file, duplicates it several times, and then inserts that
        chunk at some other random position in the file.

        """
        start_point, end_point = self.get_random_start_and_end_points_in_file(file_data)
        section = file_data[start_point:end_point]
        repeated = b''

        for i in range(1, random.randint(2, 6)):
           repeated += section

        new_start_point, new_end_point = self.get_random_start_and_end_points_in_file(file_data)
        file_data = file_data[:new_start_point] + repeated + file_data[new_end_point:]
        return file_data

    # def additional_image_processing(self, imgfile):
    #     """ Some further pre-processing / manuipulation with PIL """
    #     logger.info("Enhancing....")
    #     img = Image.open(imgfile)
    #     img.save(imgfile, "jpeg")
    #     r, g, b = img.split()
    #     img = Image.merge('RGB',(g,r,b))
    #     img.save(imgfile, "jpeg")
    #     return imgfile

    def glitch_an_image(self, local_image):
        """ Glitch!

        * Opens the original image file, reads its contents and stores them as 'file_data'
        * Calls 'splice_a_chunk_in_a_file()' method on the data a random number of times between 1 and 5
        * Writes the new glitched image out to a file

        """

        #Image pre-processing via PIL # TODO
        #local_image = self.additional_image_processing(local_image)

        with open(local_image, 'rb') as original_file_handler:
            file_data = original_file_handler.read()

        for i in range(1, random.randint(2, 6)):
            file_data = self.splice_a_chunk_in_a_file(file_data)

        with open(self.append_random_number_to_filename(local_image), 'wb') as glitch_file_handler:
            glitch_file_handler.write(file_data)

        return local_image

    def append_random_number_to_filename(self, local_img_file):
        """ Prevent overwriting of original file """
        return "%s-%s-glitched.%s" % (local_img_file.split(".")[0], random.randint(100, 999), local_img_file.split(".")[1])

    def trigger(self, local_img_file, keyword):
        """ Main trigger function """
        if not local_img_file:
            image_url = self.get_flickr_image(keyword)
            local_img_file = self.download_an_image(image_url)
        image_glitch_file = self.glitch_an_image(local_img_file)
        logger.info("Finished glitching %s" % image_glitch_file)


def main():
    # Handle args
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-f", "--file",
        dest="local_img_file",
        help="A local file to glitch.",
        metavar="local_file",
    )
    parser.add_argument(
        "-k", "--keyword",
        dest="keyword",
        help="Keyword to use when fetching image via Flickr. Default = 'random'.",
        default="random",
        metavar="keyword",
    )

    args = parser.parse_args()

    # Start the glitch script
    glitch = Glitch()
    glitch.trigger(args.local_img_file, args.keyword)

if __name__ == '__main__':
    main()
