import synapse.exc as s_exc
import synapse.common as s_common

import synapse.tests.utils as s_t_utils
from synapse.tests.utils import alist

import synapse.lib.module as s_module

geotestmodel = {

    'ctors': (),

    'types': (
        ('test:latlong', ('geo:latlong', {}), {}),
    ),

    'forms': (

        ('test:latlong', {}, (
            ('lat', ('geo:latitude', {}), {}),
            ('long', ('geo:longitude', {}), {}),
            ('dist', ('geo:dist', {}), {}),
        )),
    ),
}

class GeoTstModule(s_module.CoreModule):
    def getModelDefs(self):
        return (
            ('geo:test', geotestmodel),
        )


class GeoTest(s_t_utils.SynTest):

    async def test_types_forms(self):
        formlat = 'geo:latitude'
        formlon = 'geo:longitude'
        formlatlon = 'geo:latlong'

        async with self.getTestCore() as core:

            # Latitude Type Tests =====================================================================================
            t = core.model.type(formlat)
            self.raises(s_exc.BadTypeValu, t.norm, '-90.1')
            self.eq(t.norm('-90')[0], -90.0)
            self.eq(t.norm('-12.345678901234567890')[0], -12.3456789)
            self.eq(t.norm('-0')[0], 0.0)
            self.eq(t.norm('0')[0], 0.0)
            self.eq(t.norm('12.345678901234567890')[0], 12.3456789)
            self.eq(t.norm('90')[0], 90.0)
            self.raises(s_exc.BadTypeValu, t.norm, '90.1')
            self.raises(s_exc.BadTypeValu, t.norm, 'newp')

            self.eq(t.indx(-90), b'\x00\x00\x00\x00\x00')  # index starts at 0 and goes to 9000000000
            self.eq(t.indx(-12.34567890123456789), b'\x01\xce\xdb\x17-')
            self.eq(t.indx(0), b'\x02\x18q\x1a\x00')
            self.eq(t.indx(12.34567890123456789), b'\x02b\x07\x1c\xd2')
            self.eq(t.indx(90), b'\x040\xe24\x00')

            # Longitude Type Tests =====================================================================================
            t = core.model.type(formlon)
            self.raises(s_exc.BadTypeValu, t.norm, '-180.1')
            self.eq(t.norm('-180')[0], -180.0)
            self.eq(t.norm('-12.345678901234567890')[0], -12.3456789)
            self.eq(t.norm('-0')[0], 0.0)
            self.eq(t.norm('0')[0], 0.0)
            self.eq(t.norm('12.345678901234567890')[0], 12.3456789)
            self.eq(t.norm('180')[0], 180.0)
            self.raises(s_exc.BadTypeValu, t.norm, '180.1')
            self.raises(s_exc.BadTypeValu, t.norm, 'newp')

            self.eq(t.indx(-180), b'\x00\x00\x00\x00\x00')  # index starts at 0 and goes to 18000000000
            self.eq(t.indx(-12.34567890123456789), b'\x03\xe7L1-')
            self.eq(t.indx(0), b'\x040\xe24\x00')
            self.eq(t.indx(12.34567890123456789), b'\x04zx6\xd2')
            self.eq(t.indx(180), b'\x08a\xc4h\x00')

            # Latlong Type Tests =====================================================================================
            t = core.model.type(formlatlon)
            self.eq(t.norm('0,-0'), ((0.0, 0.0), {'subs': {'lat': 0.0, 'lon': 0.0}}))
            self.eq(t.norm('89.999,179.999'), ((89.999, 179.999), {'subs': {'lat': 89.999, 'lon': 179.999}}))
            self.eq(t.norm('-89.999,-179.999'), ((-89.999, -179.999), {'subs': {'lat': -89.999, 'lon': -179.999}}))

            self.eq(t.norm([89.999, 179.999]), ((89.999, 179.999), {'subs': {'lat': 89.999, 'lon': 179.999}}))
            self.eq(t.norm((89.999, 179.999)), ((89.999, 179.999), {'subs': {'lat': 89.999, 'lon': 179.999}}))

            self.raises(s_exc.BadTypeValu, t.norm, '-91,0')
            self.raises(s_exc.BadTypeValu, t.norm, '91,0')
            self.raises(s_exc.BadTypeValu, t.norm, '0,-181')
            self.raises(s_exc.BadTypeValu, t.norm, '0,181')
            self.raises(s_exc.BadTypeValu, t.norm, ('newp', 'newp', 'still newp'))

            # Demonstrate precision
            self.eq(t.norm('12.345678,-12.345678'),
                ((12.345678, -12.345678), {'subs': {'lat': 12.345678, 'lon': -12.345678}}))
            self.eq(t.norm('12.3456789,-12.3456789'),
                ((12.3456789, -12.3456789), {'subs': {'lat': 12.3456789, 'lon': -12.3456789}}))
            self.eq(t.norm('12.34567890,-12.34567890'),
                ((12.3456789, -12.3456789), {'subs': {'lat': 12.3456789, 'lon': -12.3456789}}))

            self.eq(t.indx((-90, -180)), b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            self.eq(t.indx((90, 180)), b'\x040\xe24\x00\x08a\xc4h\x00')

            self.eq(t.indx((0, 0)), b'\x02\x18q\x1a\x00\x040\xe24\x00')
            self.eq(t.indx((0, -0)), b'\x02\x18q\x1a\x00\x040\xe24\x00')
            self.eq(t.indx((0, 1)), b'\x02\x18q\x1a\x00\x046\xd8\x15\x00')
            self.eq(t.indx((0, -1)), b'\x02\x18q\x1a\x00\x04*\xecS\x00')
            self.eq(t.indx((-90, 180)), b'\x00\x00\x00\x00\x00\x08a\xc4h\x00')
            self.eq(t.indx((90, -180)), b'\x040\xe24\x00\x00\x00\x00\x00\x00')
            self.eq(t.indx((12.3456789, -12.3456789)), b'\x02b\x07\x1c\xd2\x03\xe7L1.')
            self.eq(t.indx((12.34567890, -12.34567890)), b'\x02b\x07\x1c\xd2\x03\xe7L1.')

            self.eq(t.repr((0, 0)), '0,0')
            self.eq(t.repr((0, -0)), '0,0')
            self.eq(t.repr((12.345678, -12.345678)), '12.345678,-12.345678')

            # Geo-dist tests
            formname = 'geo:dist'
            t = core.model.type(formname)

            self.eq(t.norm('100km')[0], 100000000)
            self.eq(t.norm('100     km')[0], 100000000)
            self.eq(t.norm('837.33 m')[0], 837330)
            self.eq(t.norm('11.2 km'), (11200000, {}))
            self.eq(t.norm(11200000), (11200000, {}))

            self.eq(t.repr(5), '5 mm')
            self.eq(t.repr(500), '50.0 cm')
            self.eq(t.repr(1000), '1.0 m')
            self.eq(t.repr(10000), '10.0 m')
            self.eq(t.repr(1000000), '1.0 km')

            self.raises(s_exc.BadTypeValu, t.norm, '1.3 pc')

            # geo:nloc
            formname = 'geo:nloc'
            t = core.model.type(formname)

            ndef = ('inet:ipv4', '0.0.0.0')
            latlong = ('0.000000000', '0')
            stamp = -0

            async with await core.snap() as snap:
                node = await snap.addNode('geo:nloc', (ndef, latlong, stamp))
                self.eq(node.ndef[1], (('inet:ipv4', 0), (0.0, 0.0), stamp))
                self.eq(node.get('ndef'), ('inet:ipv4', 0))
                self.eq(node.get('ndef:form'), 'inet:ipv4')
                self.eq(node.get('latlong'), (0.0, 0.0))
                self.eq(node.get('time'), 0)
                self.nn(await snap.getNodeByNdef(('inet:ipv4', 0)))

            # geo:place

            # test inline tuple/float with negative syntax...
            node = (await alist(core.eval('[ geo:place="*" :latlong=(-30.0,20.22) ]')))[0]
            self.eq(node.get('latlong'), (-30.0, 20.22))

            async with await core.snap() as snap:
                guid = s_common.guid()
                props = {'name': 'Vertex  HQ',
                         'desc': 'The place where Vertex Project hangs out at!',
                         'address': '208 Datong Road, Pudong District, Shanghai, China',
                         'loc': 'us.hehe.haha',
                         'latlong': '34.1341, -118.3215',
                         'radius': '1.337km'}
                node = await snap.addNode('geo:place', guid, props)
                self.eq(node.ndef[1], guid)
                self.eq(node.get('name'), 'vertex hq')
                self.eq(node.get('loc'), 'us.hehe.haha')
                self.eq(node.get('latlong'), (34.13409999, -118.3215))
                self.eq(node.get('radius'), 1337000)
                self.eq(node.get('desc'), 'The place where Vertex Project hangs out at!')
                self.eq(node.get('address'), '208 datong road, pudong district, shanghai, china')

    async def test_near(self):
        async with self.getTestCore() as core:
            async with await core.snap() as snap:
                # These two nodes are 2,605m apart
                guid0 = s_common.guid()
                props = {'name': 'Vertex  HQ',
                         'latlong': '34.1341, -118.3215',  # hollywood sign
                         'radius': '1.337km'}
                node = await snap.addNode('geo:place', guid0, props)
                self.nn(node)

                guid1 = s_common.guid()
                props = {'name': 'Griffith Observatory',
                         'latlong': '34.118560, -118.300370',
                         'radius': '75m'}
                node = await snap.addNode('geo:place', guid1, props)
                self.nn(node)

                guid2 = s_common.guid()
                props = {'name': 'unknown location'}
                node = await snap.addNode('geo:place', guid2, props)
                self.nn(node)

                # A telemetry node for example by the observatory
                guid3 = s_common.guid()
                props = {'latlong': '34.118660, -118.300470'}
                node = await snap.addNode('tel:mob:telem', guid3, props)
                self.nn(node)

                # A telemetry node for example by the HQ
                guid4 = s_common.guid()
                props = {'latlong': '34.13412, -118.32153'}
                node = await snap.addNode('tel:mob:telem', guid4, props)
                self.nn(node)

            # Node filtering behavior
            nodes = await alist(core.eval('geo:place +:latlong*near=((34.1, -118.3), 10km)'))
            self.len(2, nodes)
            nodes = await alist(core.eval('geo:place +geo:place:latlong*near=((34.1, -118.3), 10km)'))
            self.len(2, nodes)

            nodes = await alist(core.eval('geo:place +:latlong*near=((34.1, -118.3), 50m)'))
            self.len(0, nodes)

            # +1's come from the unknown loc without a latlong prop
            nodes = await alist(core.eval('geo:place -:latlong*near=((34.1, -118.3), 10km)'))
            self.len(0 + 1, nodes)
            nodes = await alist(core.eval('geo:place -:latlong*near=((34.1, -118.3), 50m)'))
            self.len(2 + 1, nodes)

            # Storm variable use to filter nodes based on a given location.
            q = f'geo:place={guid0} $latlong=:latlong $radius=:radius | spin | geo:place +:latlong*near=($latlong, ' \
                f'$radius)'
            nodes = await alist(core.eval(q))
            self.len(1, nodes)

            q = f'geo:place={guid0} $latlong=:latlong $radius=:radius | spin | geo:place +:latlong*near=($latlong, 5km)'
            nodes = await alist(core.eval(q))
            self.len(2, nodes)

            # Lifting nodes by *near=((latlong), radius)
            nodes = await alist(core.eval('geo:place:latlong*near=((34.1, -118.3), 10km)'))
            self.len(2, nodes)

            nodes = await alist(core.eval('geo:place:latlong*near=(("34.118560", "-118.300370"), 50m)'))
            self.len(1, nodes)

            nodes = await alist(core.eval('geo:place:latlong*near=((0, 0), 50m)'))
            self.len(0, nodes)

            # Use a radius to lift nodes which will be inside the bounding box,
            # but outside the cmpr implemented using haversine filtering.
            nodes = await alist(core.eval('geo:place:latlong*near=(("34.118560", "-118.300370"), 2600m)'))
            self.len(1, nodes)

            # Storm variable use to lift nodes based on a given location.
            q = f'geo:place={guid1} $latlong=:latlong $radius=:radius ' \
                f'tel:mob:telem:latlong*near=($latlong, 3km) +tel:mob:telem'
            nodes = await alist(core.eval(q))
            self.len(2, nodes)

            q = f'geo:place={guid1} $latlong=:latlong $radius=:radius ' \
                f'tel:mob:telem:latlong*near=($latlong, $radius) +tel:mob:telem'
            nodes = await alist(core.eval(q))
            self.len(1, nodes)

        async with self.getTestCore() as core:
            await core.loadCoreModule('synapse.tests.test_model_geospace.GeoTstModule')
            # Lift behavior for a node whose has a latlong as their primary property
            nodes = await core.eval('[(test:latlong=(10, 10) :dist=10m) '
                                    '(test:latlong=(10.1, 10.1) :dist=20m) '
                                    '(test:latlong=(3, 3) :dist=5m)]').list()
            self.len(3, nodes)

            nodes = await core.eval('test:latlong*near=((10, 10), 5km)').list()
            self.len(1, nodes)
            nodes = await core.eval('test:latlong*near=((10, 10), 30km)').list()
            self.len(2, nodes)

            # Ensure geo:dist inherits from IntBase correctly
            nodes = await core.nodes('test:latlong +:dist>5m')
            self.len(2, nodes)
            nodes = await core.nodes('test:latlong +:dist>=5m')
            self.len(3, nodes)
            nodes = await core.nodes('test:latlong +:dist<5m')
            self.len(0, nodes)
            nodes = await core.nodes('test:latlong +:dist<=5m')
            self.len(1, nodes)
            nodes = await core.nodes('test:latlong:dist>5m')
            self.len(2, nodes)
            nodes = await core.nodes('test:latlong:dist>=5m')
            self.len(3, nodes)
            nodes = await core.nodes('test:latlong:dist<5m')
            self.len(0, nodes)
            nodes = await core.nodes('test:latlong:dist<=5m')
            self.len(1, nodes)

            nodes = await core.nodes('test:latlong +:dist*range=(8m, 10m)')
            self.len(1, nodes)
            nodes = await core.nodes('test:latlong:dist*range=(8m, 10m)')
            self.len(1, nodes)
