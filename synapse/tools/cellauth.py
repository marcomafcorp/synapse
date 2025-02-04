import sys
import logging
import functools
import traceback
import synapse.exc as s_exc
import synapse.common as s_common

import synapse.glob as s_glob
import synapse.telepath as s_telepath

import synapse.lib.cmd as s_cmd
import synapse.lib.output as s_output

logger = logging.getLogger(__name__)

desc = '''
Admin users in a remote cell.
'''
outp = None

denyallow = ['deny', 'allow']
def reprrule(rule):
    head = denyallow[rule[0]]
    text = '.'.join(rule[1])
    return f'{head}: {text}'

def printuser(user):

    admin = user[1].get('admin')
    authtype = user[1].get('type')

    outp.printf(f'{user[0]}')
    outp.printf(f'type: {authtype}')
    outp.printf(f'admin: {admin}')

    if authtype == 'user':
        locked = user[1].get('locked')
        outp.printf(f'locked: {locked}')

    outp.printf('rules:')

    for i, rule in enumerate(user[1].get('rules')):
        rrep = reprrule(rule)
        outp.printf(f'    {i} {rrep}')

    outp.printf('')

    if authtype == 'user':

        outp.printf('roles:')
        for rolename in sorted(user[1].get('roles')):
            outp.printf(f'    role: {rolename}')

async def handleModify(opts):
    try:
        async with await s_telepath.openurl(opts.cellurl) as cell:

            if opts.adduser:
                outp.printf(f'adding user: {opts.name}')
                user = await cell.addAuthUser(opts.name)

            if opts.deluser:
                outp.printf(f'deleting user: {opts.name}')
                user = await cell.delAuthUser(opts.name)

            if opts.addrole:
                outp.printf(f'adding role: {opts.name}')
                user = await cell.addAuthRole(opts.name)

            if opts.delrole:
                outp.printf(f'deleting role: {opts.name}')
                user = await cell.delAuthRole(opts.name)

            if opts.passwd:
                outp.printf(f'setting passwd for: {opts.name}')
                await cell.setUserPasswd(opts.name, opts.passwd)

            if opts.grant:
                outp.printf(f'granting {opts.grant} to: {opts.name}')
                await cell.addUserRole(opts.name, opts.grant)

            if opts.revoke:
                outp.printf(f'revoking {opts.revoke} from: {opts.name}')
                await cell.delUserRole(opts.name, opts.revoke)

            if opts.admin:
                outp.printf(f'granting admin status: {opts.name}')
                await cell.setAuthAdmin(opts.name, True)

            if opts.noadmin:
                outp.printf(f'revoking admin status: {opts.name}')
                await cell.setAuthAdmin(opts.name, False)

            if opts.lock:
                outp.printf(f'locking user: {opts.name}')
                await cell.setUserLocked(opts.name, True)

            if opts.unlock:
                outp.printf(f'unlocking user: {opts.name}')
                await cell.setUserLocked(opts.name, False)

            if opts.addrule:

                text = opts.addrule

                # TODO: syntax for index...
                allow = True
                if text.startswith('!'):
                    allow = False
                    text = text[1:]

                rule = (allow, text.split('.'))

                outp.printf(f'adding rule to {opts.name}: {rule!r}')
                await cell.addAuthRule(opts.name, rule, indx=None)

            if opts.delrule is not None:
                outp.printf(f'deleting rule index: {opts.delrule}')
                await cell.delAuthRuleIndx(opts.name, opts.delrule)

            try:
                user = await cell.getAuthInfo(opts.name)
            except s_exc.NoSuchName as e:
                outp.printf(f'no such user: {opts.name}')
                return 1

            printuser(user)

    except Exception as e:  # pragma: no cover

        if opts.debug:
            traceback.print_exc()

        outp.printf(str(e))
        return 1

    else:
        return 0

async def handleList(opts):
    try:
        async with await s_telepath.openurl(opts.cellurl) as cell:

            if opts.name:
                for name in opts.name:
                    user = await cell.getAuthInfo(name)
                    if user is None:
                        outp.printf(f'no such user: {opts.name}')
                        return 1

                    printuser(user)
                return 0

            outp.printf(f'getting users and roles')

            outp.printf('users:')
            for user in await cell.getAuthUsers():
                outp.printf(f'    {user}')

            outp.printf('roles:')
            for role in await cell.getAuthRoles():
                outp.printf(f'    {role}')

    except Exception as e:  # pragma: no cover

        if opts.debug:
            traceback.print_exc()

        outp.printf(str(e))
        return 1

    else:
        return 0

async def main(argv, outprint=None):
    if outprint is None:   # pragma: no cover
        outprint = s_output.OutPut()
    global outp
    outp = outprint

    pars = makeargparser()
    try:
        opts = pars.parse_args(argv)
    except s_exc.ParserExit:
        return -1

    return await opts.func(opts)

def makeargparser():
    global outp
    pars = s_cmd.Parser('synapse.tools.cellauth', outp=outp, description=desc)

    pars.add_argument('--debug', action='store_true', help='Show debug traceback on error.')
    pars.add_argument('cellurl', help='The telepath URL to connect to a cell.')

    subpars = pars.add_subparsers(required=True,
                                  title='subcommands',
                                  dest='cmd',
                                  parser_class=functools.partial(s_cmd.Parser, outp=outp))

    # list
    pars_list = subpars.add_parser('list', help='List users/roles')
    pars_list.add_argument('name', nargs='*', default=None, help='The name of the user/role to list')
    pars_list.set_defaults(func=handleList)

    # create / modify / delete
    pars_mod = subpars.add_parser('modify', help='Create, modify, delete the names user/role')
    muxp = pars_mod.add_mutually_exclusive_group()
    muxp.add_argument('--adduser', action='store_true', help='Add the named user to the cortex.')
    muxp.add_argument('--addrole', action='store_true', help='Add the named role to the cortex.')

    muxp.add_argument('--deluser', action='store_true', help='Delete the named user to the cortex.')
    muxp.add_argument('--delrole', action='store_true', help='Delete the named role to the cortex.')

    muxp.add_argument('--admin', action='store_true', help='Grant admin powers to the user/role.')
    muxp.add_argument('--noadmin', action='store_true', help='Revoke admin powers from the user/role.')

    muxp.add_argument('--lock', action='store_true', help='Lock the user account.')
    muxp.add_argument('--unlock', action='store_true', help='Unlock the user account.')

    muxp.add_argument('--passwd', help='Set the user password.')

    muxp.add_argument('--grant', help='Grant the specified role to the user.')
    muxp.add_argument('--revoke', help='Grant the specified role to the user.')

    muxp.add_argument('--addrule', help='Add the given rule to the user/role.')
    muxp.add_argument('--delrule', type=int, help='Delete the given rule number from the user/role.')

    pars_mod.add_argument('name', help='The user/role to modify.')
    pars_mod.set_defaults(func=handleModify)
    return pars

async def _main():  # pragma: no cover
    s_common.setlogging(logger, 'DEBUG')
    return await main(sys.argv[1:])

if __name__ == '__main__':  # pragma: no cover
    sys.exit(s_glob.sync(_main()))
