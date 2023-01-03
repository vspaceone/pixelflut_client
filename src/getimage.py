import sys
sys.path.append('.')

import cv2
import socket
import numpy as np
import tqdm
import logging
import argparse
import pathlib
from matplotlib import pyplot

from pixelflutapi.helper import hex_to_floats
from pixelflutapi.api import get_pixel, get_size

def get_image():
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('pixelflut_client')

    parser = argparse.ArgumentParser(description='This is a Pixelflut Client')
    parser.add_argument(    'server',
                            type=str,
                            help='''The server running Pixelflut''')
    parser.add_argument(    'port',
                            type=int,
                            help='''The port of the Pixelflut server''')
    parser.add_argument(    'imagefile',
                            type=str,
                            help='''The path to the file to send. Relative or Absolute.
                            Use transparent pixels for pixel that should not be send to the server.''')
    parser.add_argument(    '--mode',
                            metavar='m',
                            required=False,
                            type=str,
                            choices=['random','ordered'],
                            default='ordered',
                            help='''Mode in which the image is send. Use 'random' or 'ordered'.''')
    parser.add_argument(    '--debug',
                            dest='debug', 
                            action='store_true',
                            default=False,
                            help='''Set the logging to debug''')                    
        
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.DEBUG)

    imagefile = pathlib.Path(args.imagefile)
    server = str(args.server)
    port = int(args.port)

    logger.info(f"Exporting '{imagefile}' from {server}:{port}")

    logger.debug("Connecting to server...")
    s = socket.create_connection((server,port))
    logger.debug("Connection established.")
    
    (W,H) = get_size(s)
    logger.info(f"The screensize is {W}x{H}")

    image = np.zeros((H,W,3), np.uint8)

    if args.mode == "ordered":
        for x in tqdm.tqdm(range(0,H,1)):
            for y in range(0,W,1):
                image[x,y] = hex_to_floats(f"#{get_pixel(s,y,x)}")
                #pyplot.imshow(image)
                #pyplot.show()
                cv2.imwrite(str(imagefile), image)
    elif args.mode == "random":
        for x in tqdm.tqdm(range(0,H,1)):
            for y in range(0,W,1):
                image[x,y] = hex_to_floats(f"#{get_pixel(s,y,x)}")
                #pyplot.imshow(image)
                #pyplot.show()
                cv2.imwrite(str(imagefile), image)
    else:
        raise Exception(f"Unkown mode!")


    cv2.imwrite(str(imagefile), image)


if __name__ == "__main__":
    get_image()
else:
    raise Exception("Run this program as main!")