import logging
import optparse

from sekrit import (
    verify,
    ordered_config_parser,
    )

def main():
    logging.basicConfig(level=logging.WARNING)

    parser = optparse.OptionParser(usage='%prog')
    (options, args) = parser.parse_args()

    if args:
        parser.error('Got unexpected arguments')

    cfg = ordered_config_parser.OrderedRawConfigParser()
    with file('sekrit.conf') as f:
        cfg.readfp(f)
    ok = True
    problems = verify.verify(cfg=cfg, path='.')
    for result in problems:
        ok = False

        if result.extra:
            print '{result.path} has extra recipients: {l}'.format(
                result=result,
                l=' '.join(result.extra),
                )

        if result.missing:
            print '{result.path} has missing recipients: {l}'.format(
                result=result,
                l=' '.join(result.missing),
                )

        if result.unknown_keys:
            print '{result.path} has unknown keys: {l}'.format(
                result=result,
                l=' '.join(result.unknown_keys),
                )

        if result.unknown_fingerprints:
            print '{result.path} has unknown fingerprints: {l}'.format(
                result=result,
                l=' '.join(result.unknown_fingerprints),
                )

    if ok:
        print 'ok'
    else:
        print 'BAD'
