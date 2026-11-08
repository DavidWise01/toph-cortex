import unittest
from model import *
class Tests(unittest.TestCase):
    def test_agent(self):self.assertEqual(AGENT,'{{j}}')
    def test_root(self):self.assertEqual(ROOT,'{{i}}')
    def test_space(self):self.assertEqual(SPACE_COUNT,216)
    def test_transport(self):self.assertEqual(TRANSPORT_COUNT,16)
    def test_have(self):self.assertEqual(HAVE_COUNT,4)
    def test_capacity(self):self.assertEqual(CAPACITY,13824)
    def test_first(self):self.assertEqual(encode((0,0,0),(0,0),(0,0)),0)
    def test_last(self):self.assertEqual(encode((5,5,5),(3,3),(1,1)),13823)
    def test_roundtrip(self):
        for i in range(CAPACITY):self.assertEqual(encode(*decode(i)),i)
    def test_bad_address(self):
        with self.assertRaises(ValueError):decode(CAPACITY)
    def test_negative_address(self):
        with self.assertRaises(ValueError):decode(-1)
    def test_boolean_address(self):
        with self.assertRaises(ValueError):decode(True)
    def test_bad_shape(self):
        with self.assertRaises(ValueError):encode((1,1),(0,0),(0,0))
    def test_bad_dimension(self):
        with self.assertRaises(ValueError):encode((6,0,0),(0,0),(0,0))
    def test_required(self):
        with self.assertRaises(ValueError):JaneHive(required=0)
    def test_accumulate(self):self.assertEqual(JaneHive().add('first')['status'],'ACCUMULATING')
    def test_two(self):
        h=JaneHive();h.add('a');self.assertEqual(h.add('b')['filled'],2)
    def test_complete(self):
        h=JaneHive();[h.add(i,key=str(i)) for i in range(3)]
        self.assertEqual(h.summary()['releases'],1)
    def test_full(self):
        h=JaneHive(required=8);ans=[h.add(i,key=str(i)) for i in range(4)]
        self.assertEqual(ans[-1]['record']['reason'],'CAPACITY_FULL')
    def test_purpose_change(self):
        h=JaneHive();h.add('a',purpose='one')
        with self.assertRaises(ValueError):h.add('b',purpose='two')
    def test_after_release_new_purpose(self):
        h=JaneHive(required=1);h.add('a',purpose='one');h.add('b',purpose='two')
        self.assertEqual(h.generation,2)
    def test_idempotence(self):
        h=JaneHive();h.add('a',key='a');self.assertEqual(h.add('a',key='a')['status'],'DUPLICATE')
    def test_packet_hash(self):
        h=JaneHive(required=1);h.add('a');p=h.fetch(0)
        self.assertEqual(p['payload_hash'],digest(p['payload']))
    def test_packet_tamper(self):
        h=JaneHive(required=1);h.add('a');h.distributed[0]['payload']['content']='changed'
        with self.assertRaises(ValueError):h.fetch(0)
    def test_tamper_detected(self):
        h=JaneHive(required=1);h.add('a');h.distributed[0]['payload']['content']='changed'
        self.assertFalse(h.verify())
    def test_history_chain(self):
        h=JaneHive(required=1);h.add('a');self.assertTrue(h.verify())
    def test_history_tamper(self):
        h=JaneHive(required=1);h.add('a');h.events[0]=Event(0,'ALTERED',0,'x','x','GENESIS','x')
        self.assertFalse(h.verify())
    def test_empty_release(self):
        with self.assertRaises(ValueError):JaneHive().release()
    def test_invalid_release(self):
        h=JaneHive();h.add('a')
        with self.assertRaises(ValueError):h.release('OTHER')
    def test_distinct_generations(self):
        h=JaneHive(required=1);h.add('a',key='a');h.add('b',key='b')
        self.assertNotEqual(h.release_history[0]['addresses'],h.release_history[1]['addresses'])
    def test_events_order(self):
        h=JaneHive(required=1);h.add('a')
        self.assertEqual([e.phase for e in h.events],['FORWARD','BACKWARD','FORWARD','REPLACE'])
    def test_stable_content(self):
        h=JaneHive(required=1);h.add({'x':[1,2]},key='a');self.assertEqual(h.fetch(0)['payload']['content'],{'x':[1,2]})
    def test_no_overwrite(self):
        h=JaneHive(required=1);h.add('a',key='a')
        h.generation=SPACE_COUNT*TRANSPORT_COUNT
        with self.assertRaises(ValueError):h.add('b',key='b')
        self.assertEqual(h.fetch(0)['payload']['content'],'a')
    def test_summary(self):self.assertIn('13824',str(JaneHive().summary()['address_capacity_per_epoch']))
    def test_demo(self):self.assertEqual(demonstration()['summary']['releases'],2)
    def test_three_scales_not_three_cells(self):self.assertEqual(len(decode(13)),3)
    def test_hash_deterministic(self):self.assertEqual(digest({'a':1}),digest({'a':1}))
    def test_empty_purpose(self):
        with self.assertRaises(ValueError):JaneHive().add('x',purpose='')
    def test_gated_completion(self):
        h=JaneHive(required=3);h.add('a');h.add('b');self.assertEqual(h.generation,0)
    def test_replacement_preserves(self):
        h=JaneHive(required=1);h.add('a',key='a');old=h.fetch(0).copy();h.add('b',key='b');self.assertEqual(h.fetch(0),old)
    def test_global_epoch_coverage(self):
        addresses=set();h=JaneHive(required=1)
        for g in range(SPACE_COUNT*TRANSPORT_COUNT):
            h.generation=g
            space,transport=h.work_address
            addresses.update(encode(space,transport,(s//2,s%2)) for s in range(4))
        self.assertEqual(len(addresses),CAPACITY)
    def test_max_address(self):self.assertEqual(decode(13823),((5,5,5),(3,3),(1,1)))
if __name__=='__main__':unittest.main()
