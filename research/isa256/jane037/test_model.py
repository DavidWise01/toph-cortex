import unittest
from model import *
class Test037(unittest.TestCase):
    def test_geometry(self):self.assertEqual(N,27)
    def test_wave_length(self):self.assertEqual(len(WAVE),30)
    def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
    def test_sixfold(self):self.assertTrue(all(WAVE.count(str(i))==6 for i in range(1,6)))
    def test_fields(self):self.assertEqual((len(F0),len(F1)),(27,27))
    def test_center(self):self.assertEqual(WAVE[12:18],"555555")
    def test_norm(self):self.assertEqual(norm(list(A0),list(B0)),741.3125)
    def test_swap_involution(self):
        a,b=list(A0),list(B0);swap(a,b);swap(a,b);self.assertEqual((tuple(a),tuple(b)),(A0,B0))
    def test_neutral(self):
        a,b=list(A0),list(B0);swap(a,b);self.assertEqual((a[1],b[1]),(.5,-.25))
    def test_cyclic_distance(self):self.assertAlmostEqual(dist(0,26.8),.2)
    def test_no_distance(self):self.assertEqual(dist(3,3),0)
    def test_true_encounters(self):self.assertEqual(run()['true_crossings'],3)
    def test_raw_duplicate(self):self.assertGreater(run(method="raw")["triggered_exchanges"],20)
    def test_clean_latch(self):self.assertEqual(run(method="latch")["triggered_exchanges"],3)
    def test_clean_debounce(self):self.assertEqual(run()["triggered_exchanges"],3)
    def test_jitter(self):self.assertEqual(run(jitter=.12)["triggered_exchanges"],3)
    def test_latch_noise(self):self.assertNotEqual(run(jitter=.12,sensor_error=.01,method="latch")["triggered_exchanges"],3)
    def test_debounce_noise(self):self.assertEqual(run(jitter=.12,sensor_error=.01)["triggered_exchanges"],3)
    def test_loss_all(self):self.assertEqual(run(drop_rate=1)["triggered_exchanges"],0)
    def test_loss_none(self):self.assertEqual(run(drop_rate=0)["triggered_exchanges"],3)
    def test_energy_raw(self):self.assertEqual(run(method="raw")["energy_start"],run(method="raw")["energy_end"])
    def test_energy_latch(self):self.assertEqual(run(method="latch")["energy_start"],run(method="latch")["energy_end"])
    def test_energy_debounce(self):self.assertEqual(run()["energy_start"],run()["energy_end"])
    def test_energy_oracle(self):self.assertEqual(run(method="oracle")["energy_start"],run(method="oracle")["energy_end"])
    def test_repeat(self):self.assertEqual(run(seed=91)["records"],run(seed=91)["records"])
    def test_invalid_method(self):
        with self.assertRaises(ValueError):run(method="unknown")
    def test_invalid_jitter(self):
        with self.assertRaises(ValueError):run(jitter=1)
    def test_invalid_width(self):
        with self.assertRaises(ValueError):run(width=0)
    def test_invalid_dt(self):
        with self.assertRaises(ValueError):run(dt=.2)
    def test_counts(self):self.assertEqual(len(sweep(trials=2)),48)
if __name__=="__main__":unittest.main()
