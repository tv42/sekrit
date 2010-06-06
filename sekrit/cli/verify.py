import logging
import optparse

from sekrit import (
    verify,
    ordered_config_parser,
    )

def main():
    logging.basicConfig(level=logging.INFO)

    parser = optparse.OptionParser(usage='%prog')
    (options, args) = parser.parse_args()

    if args:
        parser.error('Got unexpected arguments')

    cfg = ordered_config_parser.OrderedRawConfigParser()
    with file('sekrit.conf') as f:
        cfg.readfp(f)
    ok = verify.verify(cfg=cfg, path='.')
    if ok:
        print 'ok'
    else:
        print 'BAD'
