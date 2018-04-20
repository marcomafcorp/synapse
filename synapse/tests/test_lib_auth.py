import lmdb
from synapse.tests.common import *

import synapse.lib.auth as s_auth

class TstAthMxn(s_auth.AuthMixin):
    def __init__(self, dirn, root='root'):
        auth = s_auth.Auth(dirn)
        s_auth.AuthMixin.__init__(self, auth)
        try:
            root = auth.addUser(root)
        except s_exc.DupUserName:
            root = auth.reqUser(root)
        finally:
            root.setAdmin(True)

class AuthTest(SynTest):

    def test_auth_rules(self):

        rules = (
            (True, ('foo:bar', {'baz': 'faz'})),
            (False, ('foo:bar', {'baz': 'woot*'})),

            (True, ('hehe:*', {})),
        )

        rulz = s_auth.Rules(rules)

        self.true(rulz.allow(('hehe:ha', {})))
        self.true(rulz.allow(('foo:bar', {'baz': 'faz'})))
        self.false(rulz.allow(('foo:bar', {'gigles': 'clown'})))

        self.false(rulz.allow(('foo:bar', {'baz': 'wootwoot'})))
        self.false(rulz.allow(('newp:newp', {})))

    def test_auth_runas(self):
        self.eq(s_auth.whoami(), 'root@localhost')
        with s_auth.runas('visi@vertex.link'):
            self.eq(s_auth.whoami(), 'visi@vertex.link')
        self.eq(s_auth.whoami(), 'root@localhost')

    def test_auth_tagtree(self):

        tree = s_auth.TagTree()

        tree.add('foo.bar.baz')

        self.false(tree.get('foo'))
        self.false(tree.get('foo.bar'))

        self.true(tree.get('foo.bar.baz'))
        self.true(tree.get('foo.bar.baz.faz'))

        tree.add('foo')

        self.true(tree.get('foo'))
        self.true(tree.get('foo.bar'))

    def test_auth_rbac(self):

        with self.getTestDir() as dirn:

            with s_auth.Auth(dirn) as auth:

                # Ensure our default lmdb size is correct
                self.eq(auth.getConfOpt('lmdb:mapsize'),
                        s_const.gigabyte)

                self.none(auth.users.get('visi@vertex.link'))
                self.none(auth.roles.get('ninjas'))

                self.nn(auth.addUser('root@vertex.link'))
                self.nn(auth.addUser('visi@vertex.link'))
                self.nn(auth.addRole('ninjas'))

                self.true(auth.addUser('delme@vertex.link'))
                self.true(auth.addRole('delmes'))

                udel = auth.users.get('delme@vertex.link')  # type: s_auth.User
                rdel = auth.roles.get('delmes')  # type: s_auth.Role

                self.true(udel.addRole('delmes'))
                self.nn(udel.roles.get('delmes'))

                self.true(udel.delRole('delmes'))
                self.none(udel.roles.get('delmes'))

                self.true(udel.addRole('delmes'))
                self.nn(udel.roles.get('delmes'))

                self.true(auth.delRole('delmes'))
                self.none(udel.roles.get('delmes'))
                self.raises(NoSuchRole, auth.delRole, 'delmes')

                self.true(auth.delUser('delme@vertex.link'))

                self.raises(s_exc.NoSuchUser, auth.delUser, 'delme@vertex.link')
                self.raises(s_exc.DupUserName, auth.addUser, 'visi@vertex.link')
                self.raises(s_exc.DupRoleName, auth.addRole, 'ninjas')

                root = auth.users.get('root@vertex.link')  # type: s_auth.User
                self.nn(root)

                visi = auth.users.get('visi@vertex.link')  # type: s_auth.User
                self.nn(visi)

                ninj = auth.roles.get('ninjas')  # type: s_auth.Role
                self.nn(ninj)

                self.false(visi.allowed(('node:add', {'form': 'inet:ipv4'})))
                self.false(visi.allowed(('node:del', {'form': 'inet:ipv4'})))
                self.false(visi.allowed(('node:prop:set', {'form': 'inet:ipv4', 'prop': 'cc'})))

                self.false(visi.allowed(('node:tag:add', {'tag': 'hehe.haha'})))
                self.false(visi.allowed(('node:tag:del', {'tag': 'hehe.haha'})))

                self.true(visi.addRule(('node:add', {'form': 'inet:ipv4'})))
                visi.addRule(('node:del', {'form': 'inet:ipv4'}))
                visi.addRule(('node:prop:set', {'form': 'inet:ipv4', 'prop': 'cc'}))
                visi.addRule(('node:tag:add', {'tag': 'foo.bar'}))
                visi.addRule(('node:tag:del', {'tag': 'baz.faz'}))
                self.true(visi.allowed(('node:del', {'form': 'inet:ipv4'})))
                self.true(visi.allowed(('node:prop:set', {'form': 'inet:ipv4', 'prop': 'cc'})))

                root.setAdmin(True)
                self.true(root.allowed(('node:add', {'form': 'inet:ipv4'})))
                self.false(root.allowed(('node:add', {'form': 'inet:ipv4'}), elev=False))
                # Setting the admin flag to the same value is a no-op
                root.setAdmin(True)
                # We can twiddle the admin privs
                root.setAdmin(False)
                self.false(root.admin)
                self.false(root.allowed(('node:add', {'form': 'inet:ipv4'})))
                self.false(root.allowed(('node:add', {'form': 'inet:ipv4'}), elev=False))
                # And setting back to true restores the previous behavior.
                root.setAdmin(True)
                self.true(root.allowed(('node:add', {'form': 'inet:ipv4'})))
                self.false(root.allowed(('node:add', {'form': 'inet:ipv4'}), elev=False))

                self.true(root.admin)
                self.false(visi.admin)

                ninj.addRule(('node:add', {'form': 'inet:fqdn'}))

                self.true(visi.allowed(('node:tag:add', {'tag': 'foo.bar'})))

                self.true(visi.allowed(('node:tag:add', {'tag': 'foo.bar'})))
                self.true(visi.allowed(('node:tag:del', {'tag': 'baz.faz'})))

                self.true(visi.allowed(('node:tag:add', {'tag': 'foo.bar.yep'})))
                self.true(visi.allowed(('node:tag:del', {'tag': 'baz.faz.yep'})))

                self.false(visi.allowed(('node:tag:add', {'tag': 'hehe.haha'})))
                self.false(visi.allowed(('node:tag:del', {'tag': 'hehe.haha'})))

                self.true(visi.allowed(('node:add', {'form': 'inet:ipv4'})))
                self.false(ninj.allowed(('node:add', {'form': 'inet:ipv4'})))

                self.true(ninj.allowed(('node:add', {'form': 'inet:fqdn'})))
                self.false(visi.allowed(('node:add', {'form': 'inet:fqdn'})))

                self.true(visi.addRole('ninjas'))
                self.true(visi.allowed(('node:add', {'form': 'inet:fqdn'})))
                self.raises(NoSuchRole, visi.addRole, 'bladerunner')

                self.true(visi.delRole('ninjas'))
                self.false(visi.allowed(('node:add', {'form': 'inet:fqdn'})))
                self.false(visi.delRole('ninjas'))

                # star perm testing
                na_star = ('node:add', {'form': '*'})
                self.false(visi.allowed(('node:add', {'form': 'strform'})))
                self.true(visi.addRule(na_star))
                self.true(visi.allowed(('node:add', {'form': 'strform'})))
                self.true(visi.delRule(na_star))
                self.false(visi.allowed(('node:add', {'form': 'strform'})))

                nd_star = ('node:del', {'form': '*', })
                self.false(visi.allowed(('node:del', {'form': 'strform'})))
                self.true(visi.addRule(nd_star))
                self.true(visi.allowed(('node:del', {'form': 'strform'})))
                self.true(visi.delRule(nd_star))
                self.false(visi.allowed(('node:del', {'form': 'strform'})))

                ns_star = ('node:prop:set', {'form': 'strform', 'prop': '*'})
                self.false(visi.allowed(('node:prop:set', {'form': 'strform'})))
                self.true(visi.addRule(ns_star))
                self.true(visi.allowed(('node:prop:set', {'form': 'strform'})))
                self.true(visi.delRule(ns_star))
                self.false(visi.allowed(('node:set', {'form': 'strform'})))

                visi.addRole('ninjas')

                # Sad path testing
                brules = [
                    ('node:add', ['this', 'will', 'fail']),
                    ('node:add', {}),
                    ('node:add', {'hehe': 'haha'}),
                    ('node:del', ['this', 'will', 'fail']),
                    ('node:del', {}),
                    ('node:del', {'hehe': 'haha'}),
                    ('node:prop:set', ['this', 'will', 'fail']),
                    ('node:prop:set', {}),
                    ('node:prop:set', {'hehe': 'haha'}),
                    ('node:prop:set', {'form': 'haha'}),
                    ('node:prop:set', {'prop': 'haha'}),
                    ('node:tag:add', ['this:will:fail']),
                    ('node:tag:add', {}),
                    ('node:tag:add', {'hehe:haha'}),
                    ('node:tag:del', ['this:will:fail']),
                    ('node:tag:del', {}),
                    ('node:tag:del', {'hehe:haha'}),
                ]
                for rule in brules:
                    with self.getLoggerStream('synapse.lib.auth', 'rule function error') as stream:
                        self.false(visi.addRule(rule))
                        self.true(stream.wait(1))

                with self.getLoggerStream('synapse.lib.auth', 'no such rule func') as stream:
                    self.false(visi.addRule(('node:nonexistent', {'form': 'lulz'})))
                    self.true(stream.wait(1))

                with self.getLoggerStream('synapse.lib.auth', 'unknown perm') as stream:
                    self.false(visi.allowed(('node:nonexistent', {'form': 'inet:fqdn'})))
                    self.true(stream.wait(1))

                with self.getLoggerStream('synapse.lib.auth', 'AuthBase "may" func error') as stream:
                    self.false(visi.allowed(('node:add', ['this', 'will', 'fail'])))
                    self.true(stream.wait(1))
                self.raises(s_exc.NoSuchRole, auth.reqRole, 'lolnewp')

            # Ensure persistence of the auth data
            with s_auth.Auth(dirn) as auth:  # type: s_auth.Auth

                self.none(auth.users.get('delme@vertex.link'))
                self.none(auth.roles.get('delmes'))

                visi = auth.users.get('visi@vertex.link')  # type: s_auth.User
                self.true(visi.allowed(('node:add', {'form': 'inet:ipv4'})))

                self.nn(visi.roles.get('ninjas'))
                self.true(visi.allowed(('node:add', {'form': 'inet:fqdn'})))

                root = auth.users.get('root@vertex.link')  # type: s_auth.User
                self.true(root.admin)

                # These are destructive tests
                erule = ('node:add', {'form': 'inet:ipv4'})
                visi.delRule(erule)
                self.false(visi.allowed(('node:add', {'form': 'inet:ipv4'})))
                self.raises(s_exc.NoSuchRule, visi.delRule, erule)

    def test_auth_mixin(self):
        rname = 'pennywise'
        uname = 'bob'
        nrole = 'ninja'
        rule1 = ('node:add', {'form': 'strform'})
        with self.getTestDir() as dirn:
            foo = TstAthMxn(dirn, root=rname)
            # Test decorators
            self.raises(s_exc.NoSuchUser, foo.authGetUsers)
            with s_scope.enter('syn:user', uname):
                self.raises(s_exc.NoSuchUser, foo.authGetUsers)

            with s_scope.enter({'syn:user': rname}):
                self.isin(rname, foo.authGetUsers())
                self.eq(foo.authGetRoles(), [])
                root = foo.authReqUser(rname)
                self.istufo(root)
                role = foo.authAddRole(nrole)
                self.istufo(role)
                self.eq(foo.authGetRoles(), [nrole])
                role = foo.authAddRoleRule(nrole, rule1)
                self.len(1, role[1].get('rules'))
                root = foo.authAddUserRole(rname, nrole)
                self.isin(nrole, root[1].get('roles'))
                role = foo.authReqRole(nrole)

                user = foo.authAddUser(uname)
                user = foo.authAddUserRule(uname, rule1)
                user = foo.authAddUserRole(uname, nrole)

                user = foo.authAddUser('hatguy')
                user = foo.authAddAdmin('hatguy')
                self.true(user[1].get('admin'))
                user = foo.authDelAdmin('hatguy')
                self.false(user[1].get('admin'))

                self.true(foo.authDelRoleRule(nrole, rule1))

            # Now that we have the uname user we'll fail in a different way
            with s_scope.enter('syn:user', uname):
                self.raises(s_exc.AuthDeny, foo.authGetUsers)

            with s_scope.enter('syn:user', rname):
                self.true(foo.authDelUserRule(uname, rule1))
                self.true(foo.authDelUserRole(uname, nrole))
                self.true(foo.authDelUser(uname))
                self.true(foo.authDelRole(nrole))
                root = foo.authReqUser(rname)
                self.eq(root[1].get('roles'), [])

        class Broken(s_auth.AuthMixin):
            def __init__(self):
                pass

        broke = Broken()
        self.raises(s_exc.ReqConfOpt, broke.authGetUsers)
