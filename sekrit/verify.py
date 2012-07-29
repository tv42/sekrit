import logging


log = logging.getLogger('sekrit.verify')

from sekrit import (
    decide_recipients,
    extract_recipients,
    keyid_to_fingerprint,
    map_fpr_to_user,
    walk,
    )


def verify(cfg, path):
    ok = True
    for relpath, path in walk.walk(cfg=cfg, path=path):
            log.debug('Verifying file: %s', relpath)
            want = decide_recipients.decide_recipients(
                cfg=cfg,
                path=relpath,
                )
            want = set(want)
            log.debug('Expecting recipients: %s', ' '.join(sorted(want)))

            got = extract_recipients.extract_recipients(path)
            got = set(got)
            log.debug('Got recipient keyids: %s', ' '.join(got))

            # Keyids can collide; that means a message may (to us)
            # look like it's encrypted to Bob, but in reality it's
            # encrypted to Mallory. This attack requires tricking the
            # person encrypting it to choosing the wrong key; if you
            # use "sekrit set", the recipient will be chosen by
            # fingerprint, and thus this attack is most likely
            # infeasible. Hence, we will just assume the keyids
            # extracted above map simply to our known
            # fingerprints/users.
            def keyids_to_fprs(keyids):
                for keyid in keyids:
                    fpr = keyid_to_fingerprint.keyid_to_fingerprint(keyid)
                    if fpr is None:
                        log.critical(
                            '%s: Unexpected recipient keyid: %r',
                            relpath,
                            keyid,
                            )
                        ok = False
                    else:
                        yield fpr
            got = keyids_to_fprs(got)
            got = set(got)
            log.debug('Got recipient fingerprints: %s', ' '.join(got))

            got_users = set()
            for fpr in got:
                user = map_fpr_to_user.map_fpr_to_user(cfg, fpr)
                if user is None:
                    log.critical(
                        '%s: Unknown recipient fingerprint: %r',
                        relpath,
                        fpr,
                        )
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
                ok = False

            missing = want - got_users
            if missing:
                log.error(
                    '%s: Missing recipients: %s',
                    relpath,
                    ' '.join(sorted(missing)),
                    )
                ok = False

            if ok:
                log.debug('%s: ok: %s', relpath, ' '.join(sorted(got_users)))

    return ok
