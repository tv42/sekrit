import logging
import optparse
import sys

from sekrit import (
    set_secret,
    ordered_config_parser,
    )

def main():
    logging.basicConfig(level=logging.INFO)

    parser = optparse.OptionParser(usage='%prog [OPTIONS] FILE..')
    (options, args) = parser.parse_args()

    cfg = ordered_config_parser.OrderedRawConfigParser()
    with file('sekrit.conf') as f:
        cfg.readfp(f)
    for arg in args:
        set_secret.set_secret(cfg=cfg, path=arg)
