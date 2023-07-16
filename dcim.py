import argparse
import logging
import os

from PIL import Image
from pillow_heif import register_heif_opener
from wrenchbox.logging import setup_log

register_heif_opener()


class DCIM:
    def __init__(self, dir):
        self.dir = dir

    def run(self):
        for f in os.listdir(self.dir):
            ff = os.path.join(self.dir, f)
            if os.path.isfile(ff):
                try:
                    img = Image.open(ff)
                    exif_data = img.getexif()
                except:
                    logging.warning('Skipping: %s', ff)
                else:
                    if 306 in exif_data:
                        i = 0
                        ss = None
                        while ss != ff and (i == 0 or os.path.isfile(ss)):
                            s = 'IMG_' + exif_data[306].replace(':', '').replace(' ', '_')
                            if i > 0:
                                s += '_{}'.format(i)
                            ss = os.path.join(self.dir, s + os.path.splitext(ff)[1].lower())
                            i += 1
                        if ss != ff:
                            logging.info('%s %s %s', ff, '=>', ss)
                            os.rename(ff, ss)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='show debug information')
    parser.add_argument('dir', type=str, help='directory contains photos')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    DCIM(args.dir).run()
