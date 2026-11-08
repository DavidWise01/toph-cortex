import unittest
from fractions import Fraction
from model import *
class Test036(unittest.TestCase):
    def test_shape(self):self.assertEqual(N,27)
    def test_wave(self):self.assertEqual(len(LEVELS),30)
    def test_wave_symmetry(self):self.assertEqual(LEVELS,LEVELS[::-1])
    def test_six_per_level(self):self.assertTrue(all(LEVELS.count(str(i))==6 for i in range(1,6)))
    def test_ternary(self):self.assertEqual(27+3,30)
    def test_initial_energy(self):self.assertEqual(energy(*initial()),741.3125)
    def test_involution(self):self.assertEqual(exchange(*exchange(*initial())),initial())
    def test_neutral(self):
        a,b=initial();aa,bb=exchange(a,b);self.assertEqual((aa.register[1],bb.register[1]),(a.register[1],b.register[1]))
    def test_identity(self):
        a,b=initial();aa,bb=exchange(a,b);self.assertEqual((aa.identity,bb.identity),(a.identity,b.identity))
    def test_fields(self):
        a,b=initial();aa,bb=exchange(a,b);self.assertEqual((aa.field,bb.field),(a.field,b.field))
    def test_conservation(self):self.assertEqual(energy(*initial()),energy(*exchange(*initial())))
    def test_equal_speeds(self):self.assertEqual(summary(1,1)['first_time'],'27/2')
    def test_equal_midpoint(self):self.assertEqual(summary(1,1)['first_position'],'27/2')
    def test_equal_54(self):self.assertEqual(summary(1,1)['full_closure'],'54')
    def test_equal_one_swap(self):self.assertEqual(summary(1,1)['encounters'],1)
    def test_54_restores(self):self.assertTrue(run(1,1,2)['restored'])
    def test_async_5_4(self):self.assertEqual(summary(5,4)['encounters'],8)
    def test_async_first_vertex(self):self.assertEqual(summary(5,4)['first_position'],'15')
    def test_async_5_4_closes(self):self.assertEqual(summary(5,4)['full_closure'],'135')
    def test_async_5_3_odd(self):self.assertEqual(summary(5,3)['encounters'],7)
    def test_async_5_3_closes_later(self):self.assertEqual(summary(5,3)['full_closure'],'270')
    def test_async_one_loop_not_restored(self):self.assertFalse(run(5,3,1)['restored'])
    def test_async_two_loops_restored(self):self.assertTrue(run(5,3,2)['restored'])
    def test_even_restores_one_loop(self):self.assertTrue(run(5,4,1)['restored'])
    def test_mixed_vertex_edge(self):
        x=summary(5,1);self.assertGreater(x['vertex_meetings'],0);self.assertGreater(x['edge_meetings'],0)
    def test_exact_phase_closure(self):
        for q,r in ((1,1),(5,4),(5,3),(5,2),(7,6),(4,1)):
            period,events=encounter_times(q,r)
            self.assertEqual(period%27,0)
            self.assertEqual((Fraction(r,q)*period)%27,0)
    def test_no_origin_meet_inside_period(self):
        for q,r in ((1,1),(5,4),(5,3),(5,2),(7,6),(4,1)):
            self.assertTrue(all(x!=0 for _,x in encounter_times(q,r)[1]))
    def test_detect_non_midpoint(self):self.assertNotEqual(summary(5,4)['first_position'],'27/2')
    def test_bad_ratio(self):
        for q,r in [(0,1),(1,0),(-1,1),(4,2)]:
            with self.assertRaises(ValueError):parse_ratio(q,r)
    def test_bad_cycles(self):
        with self.assertRaises(ValueError):run(1,1,0)
    def test_event_count_formula(self):
        for q,r in ((1,1),(5,4),(5,3),(5,2),(7,6),(4,1)):
            self.assertEqual(len(encounter_times(q,r)[1]),q+r-1)
    def test_energy_all_events(self):
        self.assertTrue(all(e['conserved'] for e in run(5,3,2)['events']))
    def test_unique_events(self):
        ts=[e['time_exact'] for e in run(5,4,2)['events']];self.assertEqual(len(ts),len(set(ts)))
    def test_closure_seam(self):self.assertEqual(run(1,1)['seam'],'27→27.5→1')
if __name__=='__main__':unittest.main()
