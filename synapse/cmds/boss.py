import shlex
import synapse.exc as s_exc

import synapse.lib.cmd as s_cmd
import synapse.lib.cli as s_cli
import synapse.lib.time as s_time

class PsCmd(s_cli.Cmd):

    '''
    List running tasks in the cortex.
    '''

    _cmd_name = 'ps'
    _cmd_syntax = ()

    async def runCmdOpts(self, opts):

        core = self.getCmdItem()
        tasks = await core.ps()

        for task in tasks:

            self.printf('task iden: %s' % (task.get('iden'),))
            self.printf('    name: %s' % (task.get('name'),))
            self.printf('    user: %r' % (task.get('user'),))
            self.printf('    status: %r' % (task.get('status'),))
            self.printf('    metadata: %r' % (task.get('info'),))
            self.printf('    start time: %s' % (s_time.repr(task.get('tick', 0)),))

        self.printf('%d tasks found.' % (len(tasks,)))

class KillCmd(s_cli.Cmd):
    '''
    Kill a running task/query within the cortex.

    Syntax:
        kill <iden>

    Users may specify a partial iden GUID in order to kill
    exactly one matching process based on the partial guid.
    '''
    _cmd_name = 'kill'
    _cmd_syntax = (
        ('line', {'type': 'glob'}),
    )

    def _make_argparser(self):
        parser = s_cmd.Parser(prog='kill', outp=self, description=self.__doc__)
        parser.add_argument('iden', help='Task iden to kill.', type=str)
        return parser

    async def runCmdOpts(self, opts):

        line = opts.get('line')
        if line is None:
            self.printf(self.__doc__)
            return

        try:
            opts = self._make_argparser().parse_args(shlex.split(line))
        except s_exc.ParserExit:
            return

        core = self.getCmdItem()

        match = opts.iden
        idens = []
        for task in await core.ps():
            iden = task.get('iden')
            if iden.startswith(match):
                idens.append(iden)

        if len(idens) == 0:
            self.printf('no matching process found.')
            return

        if len(idens) > 1:  # pragma: no cover
            # this is a non-trivial situation to test since the
            # boss idens are random guids
            self.printf('multiple matching process found. aborting.')
            return

        kild = await core.kill(idens[0])
        self.printf('kill status: %r' % (kild,))
