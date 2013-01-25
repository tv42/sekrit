import logging

from collections import namedtuple


log = logging.getLogger('sekrit.verify')

from sekrit import (
    decide_recipients,
    extract_recipients,
    keyid_to_fingerprint,
    map_fpr_to_user,
    walk,
    )


VerifyResult = namedtuple(
    'VerifyResult',
    [
        'path',
        'extra',
        'missing',
        'unknown_keys',
        'unknown_fingerprints',
        ],
    )


def verify(cfg, path):
    """
    Generates a list of problems, each item a `VerifyResult`; empty
    list means everything is good.
    """
    for relpath, path in walk.walk(cfg=cfg, path=path):
            log.debug('Verifying file: %s', relpath)
            ok = True
            result = VerifyResult(
                path=relpath,
                extra=set(),
                missing=set(),
                unknown_keys=set(),
                unknown_fingerprints=set(),
                )
            want = decide_recipients.decide_recipients(
                cfg=cfg,
                path=relpath,
                )
            want = set(want)
            log.debug('Expecting recipients: %s', ' '.join(sorted(want)))

            keyids = extract_recipients.extract_recipients(path)
            keyids = set(keyids)
            log.debug('Got recipient keyids: %s', ' '.join(keyids))

            # Keyids can collide; that means a message may (to us)
            # look like it's encrypted to Bob, but in reality it's
            # encrypted to Mallory. This attack requires tricking the
            # person encrypting it to choosing the wrong key; if you
            # use "sekrit set", the recipient will be chosen by
            # fingerprint, and thus this attack is most likely
            # infeasible. Hence, we will just assume the keyids
            # extracted above map simply to our known
            # fingerprints/users.
            fprs = set()
            for keyid in keyids:
                fpr = keyid_to_fingerprint.keyid_to_fingerprint(keyid)
                if fpr is None:
                    log.critical(
                        '%s: Unexpected recipient keyid: %r',
                        relpath,
                        keyid,
                        )
                    result.unknown_keys.add(keyid)
                    ok = False
                else:
                    fprs.add(fpr)
            log.debug('Got recipient fingerprints: %s', ' '.join(fprs))

            got_users = set()
            for fpr in fprs:
                user = map_fpr_to_user.map_fpr_to_user(cfg, fpr)
                if user is None:
                    log.critical(
                        '%s: Unknown recipient fingerprint: %r',
                        relpath,
                        fpr,
                        )
                    result.unknown_fingerprints.add(fpr)
                    ok = False
                else:
                    got_users.add(user)

            log.debug('Got recipients: %s', ' '.join(sorted(got_users)))

            extra = got_users - want
            if extra:
                log.critical(
                    '%s: Unexpected recipients: %s',
                    relpath,
                    ' '.join(sorted(extra)),
                    )
                result.extra.update(extra)
                ok = False

            missing = want - got_users
            if missing:
                log.error(
                    '%s: Missing recipients: %s',
                    relpath,
                    ' '.join(sorted(missing)),
                    )
                result.missing.update(missing)
                ok = False

            if ok:
                log.info('%s: ok: %s', relpath, ' '.join(sorted(got_users)))
            else:
                log.error('%s: bad: %s', relpath)
                yield result
