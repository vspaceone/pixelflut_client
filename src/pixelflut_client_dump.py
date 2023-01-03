import sys
sys.path.append('.')
import errno
import cv2
import socket
import tqdm
import argparse
import pathlib
import logging
import random

from pixelflutapi.api import set_pixel_packet

def pixelflut_client_dump():
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('pixelflut_client')

    parser = argparse.ArgumentParser(description='This is a Pixelflut Client')
    parser.add_argument(    'imagefile',
                            type=str,
                            help='''The path to the file to send. Relative or Absolute.
                            Use transparent pixels for pixel that should not be send to the server.''')
    parser.add_argument(    'server',
                            type=str,
                            help='''The server running Pixelflut''')
    parser.add_argument(    'port',
                            type=int,
                            help='''The port of the Pixelflut server''')
    parser.add_argument(    '--mode',
                            metavar='m',
                            required=False,
                            type=str,
                            choices=['random','ordered'],
                            default='random',
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

    if not imagefile.exists():
        raise FileNotFoundError(f"{imagefile} not found!")

    logger.info(f"Running on '{imagefile}' against {server}:{port}")

    logger.debug("Loading image...")
    image = cv2.imread(str(imagefile), cv2.IMREAD_UNCHANGED)
    W,H,C = image.shape
    assert( C in [3,4])
    has_alpha = (C == 4)
    logger.debug(f"Successfully loaded '{imagefile}' with shape {image.shape}")

    logger.debug("Connecting to server...")
    s = socket.create_connection((server,port))
    logger.debug("Connection established.")

    packet = b''
    if args.mode == 'ordered':
        logger.debug("Setup up packet ordered...")
        for x in tqdm.tqdm(range(0,W)):
            for y in range(0,H):
                if has_alpha:
                    r,g,b,a = image[x,y]
                    if a != 0:
                        packet += set_pixel_packet(y,x, '%02x%02x%02x' % (r, g, b))
                else:
                    r,g,b = image[x,y]
                    packet += set_pixel_packet(y,x, '%02x%02x%02x' % (r, g, b))
    elif args.mode == 'random':
        logger.debug("Setup up packet randomly...")
        pixels = []
        for x in tqdm.tqdm(range(0,W)):
            for y in range(0,H):
                if has_alpha:
                    r,g,b,a = image[x,y]
                    if a != 0:
                        pixels.append((x,y,r,g,b))
                else:
                    r,g,b = image[x,y]
                    pixels.append((x,y,r,g,b))
        
        random.shuffle(pixels)
        for (x,y,r,g,b) in pixels:
            packet += set_pixel_packet(y,x, '%02x%02x%02x' % (r, g, b))

    logger.info(f'Packetsize {len(packet)} bytes')
    logger.info("Sending to server... (endless)")
    logger.info("Strg-C to cancel")
    while True:
        try:
            s.send(packet)
        except IOError as e:
            if e.errno == errno.EPIPE: 
                logger.info("Seems like we got a broken pipe. Try ...")
                raise e
        except KeyboardInterrupt:
            print("\n")
            logger.info("Closing connection...")
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            s = None
            logger.info("Connection closed. Quit.")
            exit(0)

if __name__ == "__main__":
    pixelflut_client_dump()
else:
    raise Exception("Run this program as main!")