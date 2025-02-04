import types
import asyncio
import logging

logger = logging.getLogger(__name__)

import synapse.exc as s_exc
import synapse.common as s_common
import synapse.telepath as s_telepath

import synapse.lib.base as s_base
import synapse.lib.coro as s_coro
import synapse.lib.link as s_link
import synapse.lib.scope as s_scope
import synapse.lib.share as s_share
import synapse.lib.certdir as s_certdir
import synapse.lib.urlhelp as s_urlhelp
import synapse.lib.reflect as s_reflect

class Sess(s_base.Base):

    async def __anit__(self):

        await s_base.Base.__anit__(self)

        self.items = {}
        self.iden = s_common.guid()
        self.user = None

    def getSessItem(self, name):
        return self.items.get(name)

    def setSessItem(self, name, item):
        self.items[name] = item

    def popSessItem(self, name):
        return self.items.pop(name, None)

class Genr(s_share.Share):

    typename = 'genr'

    async def _runShareLoop(self):

        try:

            for item in self.item:

                if self.isfini:
                    break

                retn = (True, item)
                mesg = ('share:data', {'share': self.iden, 'data': retn})

                await self.link.tx(mesg)

                # purposely yield for fair scheduling
                await asyncio.sleep(0)

        except Exception as e:

            retn = s_common.retnexc(e)
            mesg = ('share:data', {'share': self.iden, 'data': retn})
            await self.link.tx(mesg)

        finally:

            mesg = ('share:data', {'share': self.iden, 'data': None})
            await self.link.tx(mesg)
            await self.fini()


class AsyncGenr(s_share.Share):

    typename = 'genr'

    async def _runShareLoop(self):

        try:

            async for item in self.item:

                if self.isfini:
                    break

                retn = (True, item)
                mesg = ('share:data', {'share': self.iden, 'data': retn})

                await self.link.tx(mesg)

                # purposely yield for fair scheduling
                await asyncio.sleep(0)

        except Exception as e:
            retn = s_common.retnexc(e)
            mesg = ('share:data', {'share': self.iden, 'data': retn})
            await self.link.tx(mesg)

        finally:

            mesg = ('share:data', {'share': self.iden, 'data': None})
            await self.link.tx(mesg)
            await self.fini()

dmonwrap = (
    (s_coro.GenrHelp, AsyncGenr),
    (types.AsyncGeneratorType, AsyncGenr),
    (types.GeneratorType, Genr),
)

class Daemon(s_base.Base):

    async def __anit__(self, certdir=None):

        await s_base.Base.__anit__(self)

        self._shareLoopTasks = set()

        self.certdir = s_certdir.CertDir(path=certdir)

        self.televers = s_telepath.televers

        self.addr = None    # our main listen address
        self.cells = {}     # all cells are shared.  not all shared are cells.
        self.shared = {}    # objects provided by daemon
        self.listenservers = [] # the sockets we're listening on
        self.connectedlinks = [] # the links we're currently connected on

        self.sessions = {}

        self.mesgfuncs = {
            'tele:syn': self._onTeleSyn,
            'task:init': self._onTaskInit,
            'share:fini': self._onShareFini,

            # task version 2 API
            't2:init': self._onTaskV2Init,
        }

        self.onfini(self._onDmonFini)

    async def listen(self, url, **opts):
        '''
        Bind and listen on the given host/port with possible SSL.

        Args:
            host (str): A hostname or IP address.
            port (int): The TCP port to bind.
        '''
        info = s_urlhelp.chopurl(url, **opts)
        info.update(opts)

        scheme = info.get('scheme')

        if scheme == 'unix':
            path = info.get('path')
            try:
                server = await s_link.unixlisten(path, self._onLinkInit)
            except Exception as e:
                if 'path too long' in str(e):
                    logger.error(f'unix:// exceeds OS supported UNIX socket path length: {path}')
                raise

        else:

            host = info.get('host')
            port = info.get('port')

            sslctx = None
            if scheme == 'ssl':
                sslctx = self.certdir.getServerSSLContext(hostname=host)

            server = await s_link.listen(host, port, self._onLinkInit, ssl=sslctx)

        self.listenservers.append(server)
        ret = server.sockets[0].getsockname()

        if self.addr is None:
            self.addr = ret

        return ret

    def share(self, name, item):
        '''
        Share an object via the telepath protocol.

        Args:
            name (str): Name of the shared object
            item (object): The object to share over telepath.
        '''

        try:

            if isinstance(item, s_telepath.Aware):
                item.onTeleShare(self, name)

            self.shared[name] = item

        except Exception:
            logger.exception(f'onTeleShare() error for: {name}')

    async def _onDmonFini(self):
        for s in self.listenservers:
            try:
                s.close()
            except Exception as e:  # pragma: no cover
                logger.warning('Error during socket server close()', exc_info=e)

        for name, share in self.shared.items():
            if isinstance(share, s_base.Base):
                await share.fini()

        finis = [sess.fini() for sess in self.sessions.values()]
        if finis:
            await asyncio.wait(finis)

        finis = [link.fini() for link in self.connectedlinks]
        if finis:
            await asyncio.wait(finis)

    async def _onLinkInit(self, link):

        async def rxloop():

            while not link.isfini:

                mesg = await link.rx()
                if mesg is None:
                    return

                coro = self._onLinkMesg(link, mesg)
                self.schedCoro(coro)

        self.schedCoro(rxloop())

    async def _onLinkMesg(self, link, mesg):

        try:
            func = self.mesgfuncs.get(mesg[0])
            if func is None:
                logger.exception('Dmon.onLinkMesg Invalid: %.80r' % (mesg,))
                return

            await func(link, mesg)

        except Exception:
            logger.exception('Dmon.onLinkMesg Handler: %.80r' % (mesg,))

    async def _onShareFini(self, link, mesg):

        sess = link.get('sess')
        if sess is None:
            return

        name = mesg[1].get('share')

        item = sess.popSessItem(name)
        if item is None:
            return

        await item.fini()

    async def _onTeleSyn(self, link, mesg):

        reply = ('tele:syn', {
            'vers': self.televers,
            'retn': (True, None),
        })

        try:

            vers = mesg[1].get('vers')

            if vers[0] != s_telepath.televers[0]:
                raise s_exc.BadMesgVers(vers=vers, myvers=s_telepath.televers)

            path = ()

            name = mesg[1].get('name')
            if not name:
                name = '*'

            if '/' in name:
                name, rest = name.split('/', 1)
                if rest:
                    path = rest.split('/')

            item = self.shared.get(name)

            if item is None:
                raise s_exc.NoSuchName(name=name)

            sess = await Sess.anit()
            async def sessfini():
                self.sessions.pop(sess.iden, None)

            sess.onfini(sessfini)
            link.onfini(sess.fini)

            self.sessions[sess.iden] = sess

            link.set('sess', sess)

            if isinstance(item, s_telepath.Aware):
                item = await s_coro.ornot(item.getTeleApi, link, mesg, path)
                if isinstance(item, s_base.Base):
                    link.onfini(item.fini)

            reply[1]['sharinfo'] = s_reflect.getShareInfo(item)

            sess.setSessItem(None, item)
            reply[1]['sess'] = sess.iden

        except Exception as e:
            logger.exception('tele:syn error')
            reply[1]['retn'] = s_common.retnexc(e)

        await link.tx(reply)

    async def _runTodoMeth(self, link, meth, args, kwargs):

        valu = meth(*args, **kwargs)

        for wraptype, wrapctor in dmonwrap:
            if isinstance(valu, wraptype):
                return await wrapctor.anit(link, valu)

        if s_coro.iscoro(valu):
            valu = await valu

        return valu

    def _getTaskFiniMesg(self, task, valu):

        if not isinstance(valu, s_share.Share):
            retn = (True, valu)
            return ('task:fini', {'task': task, 'retn': retn})

        retn = (True, valu.iden)
        typename = valu.typename
        return ('task:fini', {'task': task, 'retn': retn, 'type': typename})

    async def _onTaskV2Init(self, link, mesg):

        # t2:init is used by the pool sockets on the client

        name = mesg[1].get('name')
        sidn = mesg[1].get('sess')
        todo = mesg[1].get('todo')

        try:

            if sidn is None or todo is None:
                raise s_exc.NoSuchObj(name=name)

            sess = self.sessions.get(sidn)
            if sess is None:
                raise s_exc.NoSuchObj(name=name)

            item = sess.getSessItem(name)
            if item is None:
                raise s_exc.NoSuchObj(name=name)

            s_scope.set('sess', sess)
            # TODO set user....

            methname, args, kwargs = todo

            if methname[0] == '_':
                raise s_exc.NoSuchMeth(name=methname)

            meth = getattr(item, methname, None)
            if meth is None:
                logger.warning(f'{item!r} has no method: {methname}')
                raise s_exc.NoSuchMeth(name=methname)

            valu = meth(*args, **kwargs)

            if s_coro.iscoro(valu):
                valu = await valu

            try:
                if isinstance(valu, types.AsyncGeneratorType):
                    desc = 'async generator'

                    await link.tx(('t2:genr', {}))

                    async for item in valu:
                        await link.tx(('t2:yield', {'retn': (True, item)}))

                    await link.tx(('t2:yield', {'retn': None}))
                    return

                elif isinstance(valu, types.GeneratorType):
                    desc = 'generator'

                    await link.tx(('t2:genr', {}))

                    for item in valu:
                        await link.tx(('t2:yield', {'retn': (True, item)}))

                    await link.tx(('t2:yield', {'retn': None}))
                    return

            except Exception as e:
                logger.exception(f'error during {desc} task: {methname}')
                if not link.isfini:
                    retn = s_common.retnexc(e)
                    await link.tx(('t2:yield', {'retn': retn}))

                return

            if isinstance(valu, s_share.Share):
                sess.onfini(valu)
                info = s_reflect.getShareInfo(valu)
                await link.tx(('t2:share', {'iden': valu.iden, 'sharinfo': info}))
                return

            await link.tx(('t2:fini', {'retn': (True, valu)}))

        except Exception as e:

            logger.exception('on t2:init: %r' % (mesg,))

            if not link.isfini:
                retn = s_common.retnexc(e)
                await link.tx(('t2:fini', {'retn': retn}))

    async def _onTaskInit(self, link, mesg):

        task = mesg[1].get('task')
        name = mesg[1].get('name')

        sess = link.get('sess')
        if sess is None:
            raise s_exc.NoSuchObj(name=name)

        item = sess.getSessItem(name)
        if item is None:
            raise s_exc.NoSuchObj(name=name)

        try:

            methname, args, kwargs = mesg[1].get('todo')

            if methname[0] == '_':
                raise s_exc.NoSuchMeth(name=methname)

            meth = getattr(item, methname, None)
            if meth is None:
                logger.warning(f'{item!r} has no method: {methname}')
                raise s_exc.NoSuchMeth(name=methname)

            valu = await self._runTodoMeth(link, meth, args, kwargs)

            mesg = self._getTaskFiniMesg(task, valu)

            await link.tx(mesg)

            # if it's a Share(), spin off the share loop
            if isinstance(valu, s_share.Share):

                if isinstance(item, s_base.Base):
                    item.onfini(valu)

                async def spinshareloop():
                    try:
                        await valu._runShareLoop()
                    except asyncio.CancelledError:
                        pass
                    except Exception:
                        logger.exception('Error running %r', valu)
                    finally:
                        await valu.fini()

                self.schedCoro(spinshareloop())

        except Exception as e:

            logger.exception('on task:init: %r' % (mesg,))

            retn = s_common.retnexc(e)

            await link.tx(
                ('task:fini', {'task': task, 'retn': retn})
            )
