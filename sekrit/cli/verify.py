import itertools
import logging
import optparse

from sekrit import (
    verify,
    ordered_config_parser,
    )

def main():
    logging.basicConfig(level=logging.WARNING)

    parser = optparse.OptionParser(usage='%prog [PATH..]')
    (options, args) = parser.parse_args()

    if not args:
        args = ['.']

    cfg = ordered_config_parser.OrderedRawConfigParser()
    with file('sekrit.conf') as f:
        cfg.readfp(f)
    ok = True
    problems = itertools.chain.from_iterable(
        verify.verify(cfg=cfg, path=path)
        for path in args
        )
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
