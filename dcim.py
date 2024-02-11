import argparse
import logging
import os

import exiftool
from pillow_heif import register_heif_opener
from wrenchbox.logging import setup_log

register_heif_opener()


class DCIM:
    keywords = ('QuickTime:CreationDate', 'EXIF:DateTimeOriginal')

    def __init__(self, dir):
        self.dir = dir
        self.e = exiftool.ExifToolHelper()

    def run(self):
        for f in os.listdir(self.dir):
            ff = os.path.join(self.dir, f)
            if os.path.isfile(ff):
                try:
                    e = self.e.get_metadata(ff)
                except:
                    logging.error('Skipping: %s', ff)
                else:
                    t = None
                    for k in self.keywords:
                        if k in e[0]:
                            t = e[0][k]
                    if t is not None:
                        t = t[:19].replace(':', '').replace(' ', '_')
                        i = 0
                        ss = None
                        while ss != ff and (i == 0 or os.path.isfile(ss)):
                            s = 'IMG_' + t
                            if i > 0:
                                s += '_{}'.format(i)
                            ss = os.path.join(self.dir, s + os.path.splitext(ff)[1].lower())
                            i += 1
                        if ss != ff:
                            logging.info('%s %s %s', ff, '=>', ss)
                            os.rename(ff, ss)
                    else:
                        logging.warning('Skipping: %s', ff)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='show debug information')
    parser.add_argument('dir', type=str, help='directory contains photos and videos')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    DCIM(args.dir).run()
