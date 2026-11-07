import unittest
from dataclasses import replace
from model import *
class TestJANE034(unittest.TestCase):
    def test_27_positions(self):self.assertEqual(N,27)
    def test_three_ternary_labels(self):self.assertEqual(MODES,(-1,0,1))
    def test_thirty_counted_components(self):self.assertEqual(N+len(MODES),30)
    def test_wave_length(self):self.assertEqual(len(WAVE),30)
    def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
    def test_six_each(self):self.assertEqual({WAVE.count(str(i)) for i in range(1,6)},{6})
    def test_plateau(self):self.assertEqual(WAVE[12:18],"555555")
    def test_meeting(self):self.assertTrue(meeting())
    def test_no_intermediate_vertex_overlap(self):self.assertFalse(any(position(t,1)==position(t,-1) for t in range(1,27)))
    def test_seam(self):self.assertEqual(seam(),(27,27.5,1))
    def test_involution(self):
        a,b=make_waldos();self.assertEqual(exchange(*exchange(a,b)),(a,b))
    def test_negative_exchange(self):
        a,b=make_waldos();x,y=exchange(a,b)
        self.assertEqual((x.register[0],y.register[2]),(b.register[2],a.register[0]))
    def test_positive_exchange(self):
        a,b=make_waldos();x,y=exchange(a,b)
        self.assertEqual((x.register[2],y.register[0]),(b.register[0],a.register[2]))
    def test_neutral_local(self):
        a,b=make_waldos();x,y=exchange(a,b)
        self.assertEqual((x.register[1],y.register[1]),(a.register[1],b.register[1]))
    def test_identity(self):
        a,b=make_waldos();x,y=exchange(a,b);self.assertEqual((x.identity,y.identity),(a.identity,b.identity))
    def test_spatial_paths(self):
        a,b=make_waldos();x,y=exchange(a,b);self.assertEqual((x.path,y.path),(a.path,b.path))
    def test_energy(self):
        a,b=make_waldos();self.assertEqual(energy(a,b),energy(*exchange(a,b)))
    def test_arbitrary_payloads(self):
        a,b=make_waldos();a=replace(a,register=(-100.1,0,3.7));b=replace(b,register=(9,1e-6,2.4))
        self.assertEqual(exchange(*exchange(a,b)),(a,b))
    def test_zero_neutrals(self):
        a,b=make_waldos();a=replace(a,register=(1,0,2));b=replace(b,register=(2,0,1))
        self.assertEqual(energy(a,b),energy(*exchange(a,b)))
    def test_report(self):
        r=experiment();self.assertTrue(r["reversible"] and r["identity_preserved"])
if __name__=="__main__":unittest.main()
