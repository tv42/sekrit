import logging
import optparse
import sys

from sekrit import (
    get_secret,
    ordered_config_parser,
    )

def main():
    logging.basicConfig(level=logging.INFO)

    parser = optparse.OptionParser(usage='%prog [OPTIONS] FILE..')
    (options, args) = parser.parse_args()

    if not args:
        parser.error('Need atleast one filename')

    cfg = ordered_config_parser.OrderedRawConfigParser()
    with file('sekrit.conf') as f:
        cfg.readfp(f)
    for arg in args:
        secret = get_secret.get_secret(cfg=cfg, path=arg)
        sys.stdout.write(secret)
        del secret
