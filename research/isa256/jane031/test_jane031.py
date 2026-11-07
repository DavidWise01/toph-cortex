import unittest, json
from jane031 import Primitive, Message, run, RULES, pack_record

class Tests(unittest.TestCase):
    def test_shape(self):self.assertEqual([len(c) for c in Primitive(0).cells],[72,72])
    def test_empty(self):self.assertEqual(Primitive(0).decode(),{})
    def test_pack(self):self.assertEqual(len(pack_record(511,0)),19)
    def test_local_threshold(self):
        p=Primitive(0);p.observe(17,68);self.assertIsNone(p.predict(17))
        p.observe(17,68);self.assertIsNone(p.predict(17))
        p.observe(17,68);self.assertEqual(p.predict(17),68)
    def test_candidate_not_learning(self):
        p=Primitive(1);p.receive(Message.make(0,1,1,17,68,100));self.assertIsNone(p.predict(17))
    def test_local_corroboration(self):
        p=Primitive(1);p.observe(17,68)
        p.receive(Message.make(0,1,1,17,68,4))
        self.assertEqual(p.predict(17),68)
    def test_wrong_neighbor(self):
        p=Primitive(1);p.observe(17,68)
        self.assertEqual(p.receive(Message.make(0,1,1,17,69,4)),"CONFLICT")
        self.assertIsNone(p.predict(17))
    def test_corruption(self):
        p=Primitive(1);m=Message.make(0,1,1,17,68,4)
        bad=Message(m.src,m.to,m.seq,m.key,69,m.samples,m.digest)
        self.assertEqual(p.receive(bad),"CORRUPT")
    def test_replay(self):
        p=Primitive(1);m=Message.make(0,1,1,17,68,4)
        self.assertEqual(p.receive(m),"CANDIDATE")
        self.assertEqual(p.receive(m),"REPLAY")
    def test_wrong_dest(self):
        self.assertEqual(Primitive(1).receive(Message.make(0,2,1,17,68,4)),"WRONG_DEST")
    def test_restart(self):
        p=Primitive(0)
        for _ in range(3):p.observe(17,68)
        q=Primitive.restore(json.loads(json.dumps(p.export())))
        self.assertEqual(q.predict(17),68)
    def test_all_three(self):
        p=Primitive(0)
        for k,v in RULES:
            for _ in range(3):p.observe(k,v)
        self.assertEqual(p.decode(),dict(RULES))
    def test_capacity(self):
        p=Primitive(0)
        for k in range(4):
            for _ in range(3):p.observe(k,k+1)
        self.assertEqual(len(p.decode()),3)
    def test_no_loss_transfer(self):
        r=run(loss=0)
        self.assertEqual((r["learned"],r["isolated"],r["source"]),(3,0,3))
    def test_all_loss(self):
        r=run(loss=1)
        self.assertEqual((r["learned"],r["isolated"]),(0,0))
    def test_reproducible(self):
        self.assertEqual(run(seed=44,loss=.3)["recipient_memory"],run(seed=44,loss=.3)["recipient_memory"])
    def test_conflict(self):
        self.assertGreaterEqual(run(loss=0,contradiction=True)["conflicts"],1)
    def test_not_trusted_source_truth(self):
        p=Primitive(1);p.receive(Message.make(0,1,1,17,69,10))
        self.assertIsNone(p.predict(17))
    def test_sensor_really_learns(self):
        p=Primitive(0);p.observe(17,68)
        self.assertEqual(p.decode(),{})
        for _ in range(2):p.observe(17,68)
        self.assertEqual(p.decode(),{17:68})

if __name__=="__main__":unittest.main()
