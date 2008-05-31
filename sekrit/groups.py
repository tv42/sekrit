def expand_groups(cfg, users):
    users = list(users)
    seen = set()

    while users:
        user = users.pop(0)

        if not user.startswith('@'):
            yield user
            continue

        if user in seen:
            continue
        seen.add(user)

        members = cfg.get(
            section='group %s' % user[1:],
            option='users',
            )
        members = members.split(None)
        for member in members:
            users.append(member)
