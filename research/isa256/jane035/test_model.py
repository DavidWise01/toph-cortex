import unittest
from dataclasses import replace
from model import *
class Test035(unittest.TestCase):
    def test_vertices(self):self.assertEqual(N,27)
    def test_modes(self):self.assertEqual(MODES,(-1,0,1))
    def test_accounting(self):self.assertEqual(N+len(MODES),30)
    def test_envelope(self):self.assertEqual(len(WAVE),30)
    def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
    def test_balanced_levels(self):self.assertEqual([WAVE.count(str(i)) for i in range(1,6)],[6]*5)
    def test_start(self):self.assertEqual([w.position for w in initial()],[0,0])
    def test_directions(self):self.assertEqual([w.direction for w in initial()],[1,-1])
    def test_exchange_is_involution(self):self.assertEqual(exchange(*exchange(*initial())),initial())
    def test_energy_is_conserved(self):
        r=run();self.assertEqual(r['energy_initial'],r['energy_final'])
    def test_exchanges_one_per_cycle(self):self.assertEqual(run(2)['event_count'],2)
    def test_first_event(self):self.assertEqual(run(1)['events'][0]['midpoint_time'],13.5)
    def test_edge(self):self.assertEqual(run(1)['events'][0]['from_vertices'],[14,15])
    def test_edge_id(self):self.assertEqual(run(1)['events'][0]['edge'],13)
    def test_one_cycle_swaps(self):self.assertNotEqual(run(1)['final_registers'],run(1)['start_registers'])
    def test_two_cycles_recover(self):self.assertTrue(run(2)['restored'])
    def test_full_visit(self):self.assertEqual(run(1)['visited_vertices'],{'minus':27,'plus':27})
    def test_return_positions(self):self.assertEqual(run(1)['positions_final'],[1,1])
    def test_no_untriggered_exchange(self):
        p=initial()
        for _ in range(13):p,e=advance(p)
        self.assertEqual([w.register for w in p],[w.register for w in initial()])
    def test_disable_exchange(self):self.assertTrue(run(1,False)['restored'])
    def test_disable_magnitude(self):self.assertEqual(run(1,False)['energy_final'],run(1,False)['energy_initial'])
    def test_seam_both_directions(self):self.assertEqual(sum(x['seam'] for x in run(1)['trace']),2)
    def test_no_more_than_one_edge_event_per_cycle(self):self.assertEqual(len(run(1)['events']),1)
    def test_no_vertex_created(self):self.assertTrue(all(1<=x['a_vertex']<=27 and 1<=x['b_vertex']<=27 for x in run(2)['trace']))
    def test_field_not_modified(self):
        p=initial()
        for _ in range(54):p,e=advance(p)
        self.assertEqual([w.field for w in p],[w.field for w in initial()])
    def test_bad_cycles(self):
        with self.assertRaises(ValueError):run(0)
if __name__=='__main__':unittest.main()
