*****************
Synapse Changelog
*****************


v0.1.25 - 2019-09-06
====================
- Add ``$lib.inet.http.put()`` Stormtypes support to allow making HTTP PUT requests.
  (`#1358 <https://github.com/vertexproject/synapse/pull/1358>`_)
- Add ``$llib.base64`` Stormtypes to allow for manipulation of base64 data in Storm.
  (`#1358 <https://github.com/vertexproject/synapse/pull/1358>`_)
- Add healthcheck tooling that can be used to implement heartbeat support for Synapse Cells.
  (`#1344 <https://github.com/vertexproject/synapse/pull/1344>`_)

Features and Enhancements
-------------------------

Bugfixes
--------
- Fix an issue where the ``geo:dist`` was missing comparator support. This was fixed by caussing it to inherit from the
  IntBase type.
  (`#1362 <https://github.com/vertexproject/synapse/pull/1362>`_)


v0.1.24 - 2019-09-03
====================

Features and Enhancements
-------------------------
- Add a granular permission checking helper to the HTTPAPI Handler base.
  (`#1346 <https://github.com/vertexproject/synapse/pull/1346>`_)
- Allow retrieval of data from a LMDB SlabSeqn object by arbitrary index bytes.
  (`#1342 <https://github.com/vertexproject/synapse/pull/1342>`_)
- Add ``synapse.tools.hive.save`` and ``synapse.tools.hive.load`` to save an load arbitrary trees of a Hive.
  (`#1340 <https://github.com/vertexproject/synapse/pull/1340>`_)
- Add support to the Cell to preload hive on **first** boot via a ``hiveboot.yaml`` file containing a serialized Hive
  tree.
  (`#1340 <https://github.com/vertexproject/synapse/pull/1340>`_)
- Add POST support to the ``/api/v1/storm`` and ``/api/v1/storm/nodes`` HTTP APIs.
  (`#1351 <https://github.com/vertexproject/synapse/pull/1351>`_)
- Ensure that a Cortex always has an Axon available.  By default, the Axon will be locally stored on disk in the Cortex
  cell directory.  This can alternatively be configured to point to a Axon URL via the ``axon`` configuration option
  for a Cortex.
  (`#1349 <https://github.com/vertexproject/synapse/pull/1349>`_)
- Add Stormtypes ``$lib.bytes.put()`` to allow storing a Storm variable, representing bytes, in the Axon configured for
  a Cortex.
  (`#1349 <https://github.com/vertexproject/synapse/pull/1349>`_)
- Add support for storing arbitrary key value data on a node.
  (`#1347 <https://github.com/vertexproject/synapse/pull/1347>`_)
- Add ``geo:address`` type to record an arbitrary address string; add ``:address`` property to ``geo:place`` form. Convert
  ``ps:contact:address`` to be type ``geo:address``. This does involve a automatic data migration during Cortex startup.
  (`#1339 <https://github.com/vertexproject/synapse/pull/1339>`_)
- Fix Axon permission handling for remote users to actually enforce permissions.
  (`#1354 <https://github.com/vertexproject/synapse/pull/1354>`_)
- Add a new form, ``inet:url:mirror``, which represents URL content being mirror between two different URLs.
  (`#1360 <https://github.com/vertexproject/synapse/pull/1360>`_)
- Add support for user defined runtime properties.
  (`#1350 <https://github.com/vertexproject/synapse/pull/1350>`_)
- Add support for user defined secondary properties to be attached to a tag.
  (`#1350 <https://github.com/vertexproject/synapse/pull/1350>`_)
- Add support for defererencing a variable value in order to lift by a variable property name.
  (`#1350 <https://github.com/vertexproject/synapse/pull/1350>`_)

Bugfixes
--------
- Fix an issue with the ``kill`` command failing when providing a purely numeric task identifier.
  (`#1343 <https://github.com/vertexproject/synapse/pull/1343>`_)
- Fix an with logging the incorrect user value when terminating a task.
  (`#1343 <https://github.com/vertexproject/synapse/pull/1343>`_)
- Replace ``asyncio.sleep()`` calls with ``self.waitfini()`` calls in loop retry code, to ensure that tasks do not end
  up retrying after the object has been torn down if the ioloop is still running.
  (`#1353 <https://github.com/vertexproject/synapse/pull/1353>`_)
- Remove codecov orb and use the codecov bash uploaded directly.
  (`#1355 <https://github.com/vertexproject/synapse/pull/1355>`_)
  (`#1357 <https://github.com/vertexproject/synapse/pull/1357>`_)
- Make the Storm ``max`` command aware of Ival types, and pull the maximum value based on the right hand side of the
  interval.
  (`#1359 <https://github.com/vertexproject/synapse/pull/1359>`_)


v0.1.23 - 2019-08-14
====================

Features and Enhancements
-------------------------
- Add a new Cortex configuration option, ``layer:lmdb:map_async``, to enable asynchronous fsync calls in LMDB layers.
  (`#1338 <https://github.com/vertexproject/synapse/pull/1338>`_)
- Add ``asyncio.sleep(0)`` calls to Telepath generator loops to enable all Telepath generators to have fair scheduling
  on the server side.
  (`#1341 <https://github.com/vertexproject/synapse/pull/1341>`_)


v0.1.22 - 2019-08-08
====================

Features and Enhancements
-------------------------
- Add ``:loc`` secondary prop to ``tel:mob:telem`` to record geopolitcal location of a mobile telemetry node.
  (`#1337 <https://github.com/vertexproject/synapse/pull/1337>`_)
- Add ``:spec`` secondary prop to ``mat:item`` to record the specification of an instance of an item.
  (`#1337 <https://github.com/vertexproject/synapse/pull/1337>`_)

Bugfixes
--------
- Call seek() after truncating the file descriptor backing an Axon UpLoad context.
  (`#1336 <https://github.com/vertexproject/synapse/pull/1336>`_)


v0.1.21 - 2019-08-08
====================

Features and Enhancements
-------------------------
- All the Axon UpLoad context manager to be re-used after calling ``.save()``
  (`#1333 <https://github.com/vertexproject/synapse/pull/1333>`_)
- Add Stormtypes ``$lib.time.parse()`` to parse an arbitrary date string using datetime.strptime format rules.
  (`#1334 <https://github.com/vertexproject/synapse/pull/1334>`_)
- Make NoSuchProp exceptions more informative about Node form names if that data is relevant.
  (`#1335 <https://github.com/vertexproject/synapse/pull/1335>`_)

Bugfixes
--------
- Allow two Base implementations to be used as mixins together without disrupting their underlying teardown and
  observable behaviors. (`#1332 <https://github.com/vertexproject/synapse/pull/1332>`_)


v0.1.20 - 2019-08-06
====================

Features and Enhancements
-------------------------
- Refactor Axon to allow for easier subclassing. (`#1327 <https://github.com/vertexproject/synapse/pull/1327>`_)
- Miscellaneous Axon improvements. (`#1331 <https://github.com/vertexproject/synapse/pull/1331>`_)


v0.1.19 - 2019-07-25
====================

Features and Enhancements
-------------------------
- Add a new Storm command, ``tee``, that allows for executing multiple storm queries with the input node as the input to
  the queries, and rejoining their output as a new stream of nodes.
  (`#1323 <https://github.com/vertexproject/synapse/pull/1323>`_)

Bugfixes
--------
- Fix a bug in HTTPAPI session handling which created duplicate sessions on the server side.
  (`#1324 <https://github.com/vertexproject/synapse/pull/1324>`_)
- Fix a documentation error in the quickstart guide regarding permissions.
  (`#1326 <https://github.com/vertexproject/synapse/pull/1326>`_)


v0.1.18 - 2019-07-17
====================

Features and Enhancements
-------------------------
- Allow underscores in ``org:alias`` values. (`#1320 <https://github.com/vertexproject/synapse/pull/1320>`_)
- Allow plain variable references in tagnames and tagmatches in Storm. For example: ``+#aka.$var.t42``
  (`#1322 <https://github.com/vertexproject/synapse/pull/1322>`_)


v0.1.17 - 2019-07-12
====================

Features and Enhancements
-------------------------
- Add type base data to show explicit type inheritance for data model types.
  (`#1315 <https://github.com/vertexproject/synapse/pull/1315>`_)

Bugfixes
--------
- Fix rule deletion by the ``synapse.tools.cellauth`` tool.
  (`#1319 <https://github.com/vertexproject/synapse/pull/1319>`_)

Improved Documentation
----------------------
- Add additional Storm documentation edit parenthesis, try statements, and type specific behavior.
  (`#1316 <https://github.com/vertexproject/synapse/pull/1316>`_)


v0.1.16 - 2019-07-11
====================

Features and Enhancements
-------------------------
- In Cmdr, the time when a Storm query is being executed by the Cortex is now emitted to the user.
  (`#1310 <https://github.com/vertexproject/synapse/pull/1310>`_)
- Implement yield keyword.  The keyword "yield" before a subquery causes the output nodes of the subquery to be merged
  into the output stream. (`#1307 <https://github.com/vertexproject/synapse/pull/1307>`_)
- Allow relative and universal properties to be specified from a variable in Storm.
  (`#1305 <https://github.com/vertexproject/synapse/pull/1305>`_)
- Allow parentheses in Storm editblocks. Edit operations in parentheses don't receive incoming nodes from left of the
  parentheses.  (`#1303 <https://github.com/vertexproject/synapse/pull/1303>`_)
- For Cron tasks, expose the Storm query and their iden in the Task data structure.
  (`#1295 <https://github.com/vertexproject/synapse/pull/1295>`_)
- Allow filtering ``inet:fqdn`` properties with ``*`` wildcards, such as ``+inet:fqdn=*.vertex.link``.
  (`#1292 <https://github.com/vertexproject/synapse/pull/1292>`_)
- Add a Bytes object to StormTypes which allows for ``$gzip()``, ``$gunzip()``, ``$bzip()``, ``$bunzip()``
  and ``$json()`` decoding helpers. (`#1291 <https://github.com/vertexproject/synapse/pull/1291>`_)

Bugfixes
--------
- The ``syn:prop`` runtime only nodes did not have ``:univ=1`` set on universal properties which were pushed onto the
  form specific properties.  They now have ``:univ=1`` set on them.  (`#1313 <https://github.com/vertexproject/synapse/pull/1313>`_)
- Fix invalid tool name references for ``synapse.tools.feed`` and ``synapse.tool.pullfile``.
  (`#1311 <https://github.com/vertexproject/synapse/pull/1311>`_)
- Add a missing default share name for the Axon cell. (`#1309 <https://github.com/vertexproject/synapse/pull/1309>`_)
- Fix that non-runtsafe loops didn't yield nodes, they now do.
  (`#1307 <https://github.com/vertexproject/synapse/pull/1307>`_)
- Fix that non-runtsafe loops that ran 0 times yielded the inbound node.  They now yield no nodes.
  (`#1307 <https://github.com/vertexproject/synapse/pull/1307>`_)
- Fix ``synapse.tools.csvtool`` help description. (`#1306 <https://github.com/vertexproject/synapse/pull/1306>`_)
- Fix uses of s_common genfile where opened files weren't being truncated, or in one case, appended to.
  (`#1304 <https://github.com/vertexproject/synapse/pull/1304>`_)

Improved Documentation
----------------------
- Add additional Hive API documentation. (`#1308 <https://github.com/vertexproject/synapse/pull/1308>`_)
- Add additional type specific documentation for Storm. (`#1302 <https://github.com/vertexproject/synapse/pull/1302>`_)
- Add documentation for ``synapse.tools.csvtool``, ``synapse.tools.pushfile``, and ``synapse.tools.pullfile``.
  (`#1312 <https://github.com/vertexproject/synapse/pull/1312>`_)

v0.1.15 - 2019-07-01
====================

Features and Enhancements
-------------------------

- Add ``$lib.user.vars`` and ``$lib.globals`` Storm Types. These allow for persistent variable storage and retrieval inside of Storm across multiple queries.  These use ``.set()``, ``.get()``, ``.pop()`` and ``.list()`` methods on the two new Storm Types. (`#1287 <https://github.com/vertexproject/synapse/pull/1287>`_)
- Add an optional try operator, ``?=``, to the Storm edit mode blocks. This allows for node creation and property setting to fail silently on BadTypeValu and BadPropValu errors.  Example: ``[ inet:ipv4 ?= notAnIpAddress :asn?=NotAnAsn ]``. (`#1288 <https://github.com/vertexproject/synapse/pull/1288>`_)
- Add while loop to Storm.  (`#1290 <https://github.com/vertexproject/synapse/pull/1290>`_)
- Add ``:accuracy`` as a secondary property to the ``tel:mob:telem`` node, so a user can record the accuracy of the ``tel:mob:telem:latlong`` property. (`#1294 <https://github.com/vertexproject/synapse/pull/1294>`_)
- Always interpret numbers in expressions as numbers. (`#1293 <https://github.com/vertexproject/synapse/pull/1293>`_)
- Add a genr argument to ``iterStormQuery()`` to better facilitate nested Storm queries. (`#1297 <https://github.com/vertexproject/synapse/pull/1297>`_)
- Allow headers to be set when using ``$lib.inet.http()`` in Storm. (`#1299 <https://github.com/vertexproject/synapse/pull/1299>`_)
- Allow Storm variables to be used to make tag names in a edit block. (`#1300 <https://github.com/vertexproject/synapse/pull/1300>`_)
- Allow Storm variables with list values to be used to set multiple tags in a edit block, e.g. ``$foo=(tag1,tag2,tag3) [test:str=x +#$foo]``. (`#1300 <https://github.com/vertexproject/synapse/pull/1300>`_)
- Allow quoted strings as variable names and fields. (`#1298 <https://github.com/vertexproject/synapse/pull/1298>`_)

Bugfixes
--------
- Fix runtime safety scoping issue for variables in Storm. (`#1296 <https://github.com/vertexproject/synapse/pull/1296>`_)


v0.1.14 - 2019-06-21
====================

Features and Enhancements
-------------------------

- Add sub-command aliases for the Cmdr ``hive`` and ``cron`` commands, so that similar subcommands like ``list`` and ``ls`` work across both commands. (`#1281 <https://github.com/vertexproject/synapse/pull/1281>`_)
- Simplify adding structured data to the cell Hive via Cmdr. (`#1282 <https://github.com/vertexproject/synapse/pull/1282>`_)

Bugfixes
--------
- Fix an issue in Cmdr for ``hive get`` which could result in failing to properly overwrite files when saving a Hive value to disk. (`#1282 <https://github.com/vertexproject/synapse/pull/1282>`_)

Improved Documentation
----------------------
- Add additional logging for ReadTheDocs documentation builds. (`#1284 <https://github.com/vertexproject/synapse/pull/1284>`_)
- Add additional Hive API docstrings. (`#1285 <https://github.com/vertexproject/synapse/pull/1285>`_)


v0.1.13 - 2019-06-18
====================

Features and Enhancements
-------------------------

- Add ``syn:trigger`` runtime only nodes to the Cortex. These represent triggers which have been configured on a Cortex. (`#1270 <https://github.com/vertexproject/synapse/pull/1270>`_)
- Add a new packed node helper, ``synapse.lib.nodes.tagsnice()``, to get all the leaf tags on a node and any tags which have a time interval associated with them. (`#1271 <https://github.com/vertexproject/synapse/pull/1271>`_)
- Add a ``err?`` column to the output of the ``cron list``.  This includes an ``X`` character in the column if the last execution of that Cron task encountered an error. (`#1272 <https://github.com/vertexproject/synapse/pull/1272>`_)
- Refactor the Boss commands in cmdr to their own file and improve test coverage for the Cortex ``storm`` command in Cmdr. (`#1273 <https://github.com/vertexproject/synapse/pull/1273>`_)
- Add ``$node.globtags()`` method to Storm which accepts a tag glob, and returns a list of the matching glob values. (`#1275 <https://github.com/vertexproject/synapse/pull/1275>`_)
- Add there remote Cortex API ``CoreApi.delNodeProp()`` to allow property deletion from a single node. (`#1279 <https://github.com/vertexproject/synapse/pull/1279>`_)

Bugfixes
--------

- Update CellApi Hive functions to properly check permissions. (`#1274 <https://github.com/vertexproject/synapse/pull/1274>`_)
- Ensure that tearing down a Telepath generator via GeneratorExit from non-async code properly signals the generator to teardown on the ioloop. (`#1278 <https://github.com/vertexproject/synapse/pull/1278>`_)
- Fix an issue where Storm subquery variable assignments were being pushed to the global runtime, but were not properly available to the Path objects associated with inbound nodes. (`#1280 <https://github.com/vertexproject/synapse/pull/1280>`_)

Improved Documentation
----------------------

- Improve inline API help for a few test helper functions. (`#1273 <https://github.com/vertexproject/synapse/pull/1273>`_)
- Update Cmdr reference documentation for trigger and cron updates. (`#1277 <https://github.com/vertexproject/synapse/pull/1277>`_)


v0.1.12 - 2019-06-12
====================

Features and Enhancements
-------------------------

- Centralize the ``allowed()`` and ``_reqUserAllowed()`` function from the CoreApi class to the CellApi, making permission checking easier for CellApi implementers. (`#1268 <https://github.com/vertexproject/synapse/pull/1268>`_)
- Add the ``$path`` built-in Storm variable to the default variables populated in the Storm pipeline. (`#1269 <https://github.com/vertexproject/synapse/pull/1269>`_)
- Add a ``$path.trace()`` method to get a object which traces the pivots from a given Path object.  The path idens can be obtained via ``trace.iden()``. (`#1269 <https://github.com/vertexproject/synapse/pull/1269>`_)
- Add ``$lib.set()`` to Storm Types.  This can be used to get a mutable set object. (`#1269 <https://github.com/vertexproject/synapse/pull/1269>`_)

Bugfixes
--------

- Fix an issue where the Base ``link()`` API required the linking function to be a coroutine. (`#1261 <https://github.com/vertexproject/synapse/pull/1261>`_)

Improved Documentation
----------------------

- Improve inline API help for a few functions. (`#1268 <https://github.com/vertexproject/synapse/pull/1268>`_)


v0.1.11 - 2019-06-06
====================

Features and Enhancements
-------------------------

- Add an optional facility to lmdbslab to prevent its data from being swapped out of memory. Add a Cortex configuration option (in the cell.yaml file) named ``dedicated`` to enable this for the lmdb slabs that store the graph data in a Cortex. This is currently only supported on Linux. (`#1254 <https://github.com/vertexproject/synapse/pull/1254>`_)

Bugfixes
--------

- Fix an issue where the Cmdr color awareness for error highlighting was preventing documentation from building properly. (`#1261 <https://github.com/vertexproject/synapse/pull/1261>`_)
- Fix an issue where the ``synapse.servers.cortex`` ``--mirror`` option was not properly mirroring realtime splices. (`#1264 <https://github.com/vertexproject/synapse/pull/1264>`_)
- Fix a runtsafe variable order bug in Storm. (`#1265 <https://github.com/vertexproject/synapse/pull/1265>`_)
- Work around an issue in prompt-toolkit's ``print_formatted_text`` function. (`#1266 <https://github.com/vertexproject/synapse/pull/1266>`_)
- Fix an issue where color awareness was not available for Cmdr sessions launched via ``synapse.tools.csvtool`` and ``synapse.tools.feed``.  (`#1267 <https://github.com/vertexproject/synapse/pull/1267>`_)

Improved Documentation
----------------------

- Update Storm lift documentation to include lifting by time intervals. (`#1260 <https://github.com/vertexproject/synapse/pull/1260>`_)
- Update ReadTheDocs build configuration to utilize a Docker container, instead of a conda environment. (`#1262 <https://github.com/vertexproject/synapse/pull/1262>`_)


v0.1.10 - 2019-06-04
====================

Features and Enhancements
-------------------------

- Add ``$node.iden()`` method in Storm to expose the iden of a node. (`#1257 <https://github.com/vertexproject/synapse/pull/1257>`_)
- Add ``$lib.text()`` method in Storm Lib to add a mutable string formatting object. (`#1258 <https://github.com/vertexproject/synapse/pull/1258>`_)


v0.1.9 - 2019-05-31
===================

Features and Enhancements
-------------------------

- Add colored error reporting in Cmdr when a BadSyntax exception is sent to the user. (`#1248 <https://github.com/vertexproject/synapse/pull/1248>`_)
- Expose the local Synapse version information in Cmdr via the ``locs`` command. (`#1250 <https://github.com/vertexproject/synapse/pull/1250>`_)
- Add reflected class names to the Telepath shareinfo. Expose this with the ``Proxy._getClasses()`` API. (`#1250 <https://github.com/vertexproject/synapse/pull/1250>`_)
- Add ``--file`` and ``--optsfile`` arguments to the Cmdr ``storm`` command.  These, respectively, allow a user to provide a file containing a raw Storm query and variable arguments as a json file. (`#1252 <https://github.com/vertexproject/synapse/pull/1252>`_)

Bugfixes
--------

- Fix an issue where the Cmdr ``log`` command did not clean up all of its settings. (`#1249 <https://github.com/vertexproject/synapse/pull/1249>`_)
- Fix an issue with the Storm ``switch`` statement handling of non-runtsafe values. (`#1251 <https://github.com/vertexproject/synapse/pull/1251>`_)
- Fix an issue with the Storm ``if`` statement handling of non-runtsafe values. (`#1253 <https://github.com/vertexproject/synapse/pull/1253>`_)
- Fix an issue with when connecting to a Cortex via Telepath for the default remote layer, which previously could have pointed to a layer which was not the correct layer for the default view. (`#1255 <https://github.com/vertexproject/synapse/pull/1255>`_)


v0.1.8 - 2019-05-22
===================

Features and Enhancements
-------------------------

- Add if/elif/else statement.  Add and/or/not inside dollar expressions.  Have expressions always return an int.  (`#1235 <https://github.com/vertexproject/synapse/pull/1235>`_)
- Add variable and expression filters.  Test for and correct all known grammar ambiguities.  Tag filters with a comparison, e.g. ``+#$foo=$bar``, now don't raise an exception (`#1241 <https://github.com/vertexproject/synapse/pull/1235>`_)
- Add ability to enable and disable cron jobs and triggers.  (`#1242 <https://github.com/vertexproject/synapse/pull/1242>`_)

Bugfixes
--------

- Fix a bug where a tag addition could cause a splice to be generated if the tag window being added was inside of the existing tag window. (`#1243 <https://github.com/vertexproject/synapse/pull/1243>`_)
- csvtool now correctly handles print events (`#1245 <https://github.com/vertexproject/synapse/pull/1245>`_)

Improved Documentation
----------------------

- Update release process documentation. (`#1244 <https://github.com/vertexproject/synapse/pull/1244>`_)


v0.1.7 - 2019-05-17
===================

Features and Enhancements
-------------------------

- Add the Synapse version information in the Telepath handshake.  Expose this with the ``Proxy._getSynVers()`` API and in the Cmdr CLI via the ``locs`` command.  (`#1238 <https://github.com/vertexproject/synapse/pull/1238>`_)
- Add a ``--save-nodes`` argument to the Storm command in Cmdr to do a one-shot record of nodes returned by a Storm query.  (`#1239 <https://github.com/vertexproject/synapse/pull/1239>`_)
- Allow ``synapse.tools.cmdr`` to take a second argument and run that argument as a Cmdr command.  (`#1239 <https://github.com/vertexproject/synapse/pull/1239>`_)
- Add ``$node.repr()`` to Storm types.  This allows the user to get the repr of the primary property, or a secondary property, and assign it to a variable in storm.  (`#1222 <https://github.com/vertexproject/synapse/pull/1222>`_)
- Add ``lib.csv.emit()`` to Storm types.  This allows the user to emit a message during a Storm query which can easily be joined into a CSV.  (`#1236 <https://github.com/vertexproject/synapse/pull/1236>`_)
- Add a ``--export`` option to ``synapse.tools.csvtool``.  This allows the user to create a CSV file from a query that uses the ``$lib.csv.emit()`` Storm function.  (`#1236 <https://github.com/vertexproject/synapse/pull/1236>`_)

Bugfixes
--------

- Resolve Storm grammar ambiguity between tag condition filters with value and left join. (`#1237 <https://github.com/vertexproject/synapse/pull/1237>`_)
- Resolve Storm grammar ambiguity to prevent reserved words from being identified as a Storm command. (`#1240 <https://github.com/vertexproject/synapse/pull/1240>`_)


v0.1.6 - 2019-05-15
===================

Bugfixes
--------

- Fix an ambuguity in the Storm grammer regarding quoted command arguments. (`#1234 <https://github.com/vertexproject/synapse/pull/1234>`_)


v0.1.5 - 2019-05-15
===================

Features and Enhancements
-------------------------

- Make Ndef, Edge and TimeEdge repr implementations consistent. (`#1217 <https://github.com/vertexproject/synapse/pull/1217>`_)
- Add jsonl support the ``synapse.tools.feed`` tool. (`#1220 <https://github.com/vertexproject/synapse/pull/1220>`_)
- Add ``/api/v1/model`` API route for the Cortex HTTPAPI to expose the data model for a running Cortex. (`#1221 <https://github.com/vertexproject/synapse/pull/1221>`_)
- Add ``fire()`` function to Storm types to fire ``storm:fire`` messages during Storm command execution. (`#1221 <https://github.com/vertexproject/synapse/pull/1221>`_)
- Add ``$()`` expression syntax to Storm for mathematical operations, along with a new parsing engine built around Lark.  (`#1216 <https://github.com/vertexproject/synapse/pull/1216>`_)
- Add a warning when Synapse is imported if the user is running Python with ``-OO`` optimizations, since that can degrade the library capabilities. (`#1219 <https://github.com/vertexproject/synapse/pull/1219>`_)
- Cleanup some exception chains so that type normalization errors do not result in large tracebacks on the server. (`#1224 <https://github.com/vertexproject/synapse/pull/1224>`_)
- Allow ``$lib.print()`` to accept curly brace ``{}`` formatted strings for using variable substitution when printing values in Storm. (`#1227 <https://github.com/vertexproject/synapse/pull/1227>`_)

Bugfixes
--------

- Fix an issue in Storm with lifting or filtering nodes by tags when the tag value is a variable. (`#1223 <https://github.com/vertexproject/synapse/pull/1223>`_)
- Fix an issue which was preventing a tag variable value reference in Storm from behaving correctly. (`#1228 <https://github.com/vertexproject/synapse/pull/1228>`_)
- Fix a missing await statement which prevented properly setting layers for a Cortex View object. (`#1231 <https://github.com/vertexproject/synapse/pull/1231>`_)

Improved Documentation
----------------------

- Fix some docstrings related to test code helpers. (`#1230 <https://github.com/vertexproject/synapse/pull/1230>`_)


v0.1.4 - 2019-05-01
===================

Features and Enhancements
-------------------------

- Add POST support to the ``/api/v1/model/norm`` HTTP API endpoint. (`#1207 <https://github.com/vertexproject/synapse/pull/1207>`_)
- Add ``getPropNorm()`` and ``getTypeNorm()`` Telepath API endpoints to the Cortex and CoreApi. (`#1207 <https://github.com/vertexproject/synapse/pull/1207>`_)
- Add list ``length()`` and ``index()`` methods to Storm types. (`#1208 <https://github.com/vertexproject/synapse/pull/1208>`_)
- Add helper functions to ``synapse.lib.node`` for extracting repr values from packed nodes. (`#1212 <https://github.com/vertexproject/synapse/pull/1212>`_)
- Add ``--nodes-only`` to the Cmdr ``log`` command to only record raw nodes. (`#1213 <https://github.com/vertexproject/synapse/pull/1213>`_)
- Add ``guid()``, ``min()``, ``max()`` functions to Storm types.  (`#1215 <https://github.com/vertexproject/synapse/pull/1215>`_)
- Add ``getStormEval()`` to the ``synapse.lib.storm.Cmd`` class. This helper can be used by Storm command implementers in resolving variables, full property, and relative property values off of the Storm runtime.  (`#1215 <https://github.com/vertexproject/synapse/pull/1215>`_)
- The Storm ``min`` and ``max`` commands may now accept a relative property path, a full property path, or a variable.  (`#1215 <https://github.com/vertexproject/synapse/pull/1215>`_)
- Add a ``--mirror`` to ``synapse.servers.cortex`` to allow easier mirroring of a backup Cortex from its source Cortex.  (`#1197 <https://github.com/vertexproject/synapse/pull/1197>`_)

Bugfixes
--------

- Fix an error in PropPivotOut and FormPivot where a None object could be yielded in the Storm pipeline. (`#1210 <https://github.com/vertexproject/synapse/pull/1210>`_)
- Shut down HTTP API servers on Cell ``fini()``.  (`#1211 <https://github.com/vertexproject/synapse/pull/1211>`_)

Improved Documentation
----------------------

- Convert developer guide from static RST to Jupyter Notebook.  (`#1209 <https://github.com/vertexproject/synapse/pull/1209>`_)
- Convert HTTP API guide from static RST to Jupyter Notebook.  (`#1211 <https://github.com/vertexproject/synapse/pull/1211>`_)
- Add a note about backing up and restoring a cortex to the quickstart guide.  (`#1214 <https://github.com/vertexproject/synapse/pull/1214>`_)


v0.1.3 - 2019-04-17
===================

Features and Enhancements
-------------------------

- Add the ability to delete a role via HTTP API, as well as being able to mark a user as being archived. Archiving a user will also lock a user. (`#1205 <https://github.com/vertexproject/synapse/pull/1205>`_)
- Add support to archiving for user to the CellApi for use via Telepath. (`#1206 <https://github.com/vertexproject/synapse/pull/1206>`_)

Bugfixes
--------

- Fix remote layer bug injected by previous optimization that would result in missing nodes from lifts when the node
  only resides in the distant layer. (`#1203 <https://github.com/vertexproject/synapse/pull/1203>`_)

Improved Documentation
----------------------

- Fix error in the HTTP API documentation. (`#1204 <https://github.com/vertexproject/synapse/pull/1204>`_)


v0.1.2 - 2019-04-10
===================

Features and Enhancements
-------------------------

- Automatically run unit tests for the master every day. (`#1192 <https://github.com/vertexproject/synapse/pull/1192>`_)
- Add test suite for ``synapse.lib.urlhelp``. (`#1195 <https://github.com/vertexproject/synapse/pull/1195>`_)
- Improve multi-layer and single layer performance. This is a backwards-incompatible API change in that 0.1.2 cortex
  will not interoperate with 0.1.2 remote layers before version 0.1.2. Persistent storage format has not changed.
  (`#1196 <https://github.com/vertexproject/synapse/pull/1196>`_)
- Add skeleton for reverse engineering model. (`#1198 <https://github.com/vertexproject/synapse/pull/1198>`_)

Bugfixes
--------

- When using ``synapse.tools.cmdr``, issuing ctrl-c to cancel a running command in could result in the Telepath Proxy object being fini'd. This has been resolved by adding a signal handler to the ``synapse.lib.cli.Cli`` class which is registered by cmdr. (`#1199 <https://github.com/vertexproject/synapse/pull/1199>`_)
- Fix an issue where deleting a property which has no index failed. (`#1200 <https://github.com/vertexproject/synapse/pull/1200>`_)
- Single letter form and property names were improperly disallowed.  They are now allowed. (`#1201 <https://github.com/vertexproject/synapse/pull/1201>`_)


Improved Documentation
----------------------

- Add some example developer guide documentation. (`#1193 <https://github.com/vertexproject/synapse/pull/1193>`_)


v0.1.1 - 2019-04-03
===================


Features and Enhancements
-------------------------

- Allow ``synapse.servers`` tools to specify a custom Telepath share name. (`#1170 <https://github.com/vertexproject/synapse/pull/1170>`_)
- Add ``$lib.print()``, ``$lib.len()``, ``$lib.min()``, ``$lib.max()``, and ``$lib.dict()`` Storm library functions. (`#1179 <https://github.com/vertexproject/synapse/pull/1179>`_)
- Add ``$lib.str.concat()`` and ``$lib.str.format()`` Storm library functions. (`#1179 <https://github.com/vertexproject/synapse/pull/1179>`_)
- Initial economic model for tracking purchases. (`#1177 <https://github.com/vertexproject/synapse/pull/1177>`_)
- Add progress logging for the ``(0, 1, 0)`` layer migration. (`#1180 <https://github.com/vertexproject/synapse/pull/1180>`_)
- Remove references to ``Cortex.layer`` as a Cortex level attribute. There was no guarantee that this was the correct write layer for a arbitrary view and could lead to incorrect usage. (`#1181 <https://github.com/vertexproject/synapse/pull/1181>`_)
- Optimize the ``snap.getNodesBy()`` API to shortcut true equality lift operations to become pure lifts by buid. (`#1183 <https://github.com/vertexproject/synapse/pull/1183>`_)
- Add a generic Cell server, ``synapse.servers.cell`` that can be used to launch any Cell by python class path and file path.  This can be used to launch custom Cell objects. (`#1182 <https://github.com/vertexproject/synapse/pull/1182>`_)
- Add server side remote event processing to ``.storm()`` API calls. (`#1171 <https://github.com/vertexproject/synapse/pull/1171>`_)
- Add Telepath user proxying. (`#1171 <https://github.com/vertexproject/synapse/pull/1171>`_)
- Migrate Dockerhub docker container builds and pypi packaging and release processes to CircleCI. (`#1185 <https://github.com/vertexproject/synapse/pull/1185>`_)
- Improve performance.  Add a small layer-level cache.  Replace home-grown `synapse.lib.cache.memoize` implementation with standard one.  Make layer microoptimizations. (`#1191 <https://github.com/vertexproject/synapse/pull/1191>`_)

Bugfixes
--------

- Fixes for lmdblab.dropdb and lmdbslab.initdb mapfull safety. (`#1174 <https://github.com/vertexproject/synapse/pull/1174>`_)
- Graceful recovery for pre v0.1.0 database migrations for lmdbslab backed databases. (`#1175 <https://github.com/vertexproject/synapse/pull/1175>`_)
- Syntax parser did not allow for multiple dot hierarchies in universal properties. (`#1178 <https://github.com/vertexproject/synapse/pull/1178>`_)
- Fix for lmdbslab mapfull error during shutdown (`#1184 <https://github.com/vertexproject/synapse/pull/1184>`_)
- ``synapse.lib.reflect.getShareInfo()`` could return incorrect data depending on execution order and object type inheritance. (`#1186 <https://github.com/vertexproject/synapse/pull/1186>`_)
- Add missing test for Str types extracting named regular expression matches as subs. (`#1187 <https://github.com/vertexproject/synapse/pull/1187>`_)

Improved Documentation
----------------------

- Minor documentation updates for permissions. (`#1172 <https://github.com/vertexproject/synapse/pull/1172>`_)
- Added docstring and test for ``synapse.lib.coro.executor()``. (`#1189 <https://github.com/vertexproject/synapse/pull/1189>`_)


v0.1.0 - 2019-03-19
===================

* Synapse version 0.1.0 released.
