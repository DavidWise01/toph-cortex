import unittest, tempfile, json, random
from pathlib import Path
from model import *

class ProofCarrying(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.p=Pair(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def complete(self):
        self.p.drive(loss=0)
        return self.p
    def test_positions(self):self.assertEqual(POSITIONS,27)
    def test_modes(self):self.assertEqual(TERNARY,(-1,0,1))
    def test_accounting_30(self):self.assertEqual(POSITIONS+len(TERNARY),30)
    def test_wave_length(self):self.assertEqual(len(WAVE),30)
    def test_wave_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
    def test_wave_six(self):self.assertEqual({WAVE.count(str(i)) for i in range(1,6)},{6})
    def test_baseline(self):self.assertEqual(BASELINE,741.3125)
    def test_four_payloads(self):self.assertEqual(len(PAYLOADS),4)
    def test_initial(self):self.assertEqual(self.p.accounting()['total'],BASELINE)
    def test_zero_records(self):self.assertEqual(len(self.p.logs['A'].body()),0)
    def test_stage_once(self):
        self.p.stage('A_MINUS');self.p.stage('A_MINUS')
        self.assertEqual(len(self.p.logs['A'].body()),1)
    def test_accept_requires_stage(self):self.assertIsNone(self.p.accept('A_MINUS'))
    def test_release_requires_receipt(self):
        self.p.stage('A_MINUS');self.assertIsNone(self.p.release('A_MINUS'))
    def test_finalize_requires_release(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS')
        self.assertIsNone(self.p.finalize('A_MINUS'))
    def test_provisional_not_owned(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS')
        self.assertEqual(self.p.trace('A_MINUS'),'PROVISIONAL')
        self.assertEqual(self.p.accounting()['buckets']['sender'],87.0)
    def test_release_in_flight(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS');self.p.release('A_MINUS')
        self.assertEqual(self.p.trace('A_MINUS'),'IN_FLIGHT')
        self.assertEqual(self.p.accounting()['buckets']['gap'],9.0)
    def test_finalize_ownership(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS');self.p.release('A_MINUS');self.p.finalize('A_MINUS')
        self.assertEqual(self.p.trace('A_MINUS'),'RECEIVED')
        self.assertEqual(self.p.accounting()['buckets']['receiver'],9.)
    def test_conservation_each_state(self):
        for op in (self.p.stage,self.p.accept,self.p.release,self.p.finalize):
            op('A_MINUS');self.assertEqual(self.p.accounting()['total'],BASELINE)
    def test_full_completion(self):self.assertTrue(self.complete().accounting()['closed'])
    def test_full_provenance(self):self.assertTrue(self.complete().accounting()['all_proven'])
    def test_double_drive_idempotent(self):
        self.complete(); lengths=[len(self.p.logs[k].body()) for k in ('A','B')]
        self.p.drive();self.assertEqual(lengths,[len(self.p.logs[k].body()) for k in ('A','B')])
    def test_restart(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS');self.p=self.p.restart();self.p.release('A_MINUS');self.p.finalize('A_MINUS')
        self.assertEqual(self.p.trace('A_MINUS'),'RECEIVED')
    def test_full_loss(self):self.assertFalse(self.p.drive(loss=1)['closed'])
    def test_zero_loss(self):self.assertTrue(self.p.drive(loss=0)['closed'])
    def test_40_loss(self):self.assertTrue(experiment(seed=4,loss=.4)['closed'])
    def test_determinism(self):self.assertEqual(experiment(41,.4),experiment(41,.4))
    def test_invalid_json(self):
        self.p.stage('A_MINUS')
        with self.p.logs['A'].path.open('ab') as f:f.write(b'garbage\n')
        self.assertEqual(self.p.logs['A'].audit().reason,'INVALID_JSON')
    def test_truncated_tail(self):
        self.p.stage('A_MINUS')
        data=self.p.logs['A'].path.read_bytes();self.p.logs['A'].path.write_bytes(data[:-1])
        self.assertEqual(self.p.logs['A'].audit().reason,'TRUNCATED_TAIL')
    def test_hash_mismatch(self):
        self.p.stage('A_MINUS');s=self.p.logs['A'].path.read_text().replace('A_MINUS','B_PLUS')
        self.p.logs['A'].path.write_text(s)
        self.assertEqual(self.p.logs['A'].audit().reason,'HASH_MISMATCH')
    def test_chain_broken(self):
        self.p.stage('A_MINUS');self.p.stage('A_PLUS')
        lines=self.p.logs['A'].path.read_text().splitlines();self.p.logs['A'].path.write_text(lines[1]+'\n')
        self.assertEqual(self.p.logs['A'].audit().reason,'BROKEN_CHAIN')
    def test_append_refuses_corruption(self):
        self.p.stage('A_MINUS');self.p.logs['A'].path.write_text('x')
        with self.assertRaises(AuditError):self.p.stage('A_PLUS')
    def test_receiver_journal_deletion_caught(self):
        self.complete();self.p.logs['B'].path.write_text('')
        a=self.p.accounting();self.assertFalse(a['valid'])
    def test_sender_journal_deletion_caught(self):
        self.complete();self.p.logs['A'].path.write_text('')
        self.assertFalse(self.p.accounting()['valid'])
    def test_all_logs_loss_not_detectable(self):
        self.complete()
        for l in self.p.logs.values():l.path.write_text('')
        self.assertTrue(self.p.accounting()['valid'])
        self.assertFalse(self.p.accounting()['closed'])
    def test_forgery_limitation(self):
        self.p.stage('A_MINUS')
        doc=json.loads(self.p.logs['A'].path.read_text());doc['body']['value']=999
        doc['hash']=digest({'seq':doc['seq'],'prev':doc['prev'],'body':doc['body']})
        self.p.logs['A'].path.write_text(canonical(doc)+'\n')
        self.assertTrue(self.p.logs['A'].audit().valid)
    def test_no_28th_vertex(self):self.assertEqual(POSITIONS,27)
    def test_stage_record_link(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS');a=self.p._find('B','ACCEPT','A_MINUS')[0]
        self.assertEqual(a['stage_hash'],digest(self.p._find('A','STAGE','A_MINUS')[0]))
    def test_receipt_link(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS');self.p.release('A_MINUS')
        self.assertEqual(self.p._find('A','RELEASE','A_MINUS')[0]['receipt_hash'],digest(self.p._find('B','ACCEPT','A_MINUS')[0]))
    def test_provenance_order(self):
        self.p.stage('A_MINUS');self.p.accept('A_MINUS');self.p.release('A_MINUS');self.p.finalize('A_MINUS')
        self.assertEqual(self.p.trace('A_MINUS'),'RECEIVED')
    def test_journal_sequence(self):
        self.complete()
        for who in ('A','B'):
            rows=self.p.logs[who].audit().records
            self.assertEqual([x['seq'] for x in rows],list(range(len(rows))))
    def test_100_seed_total(self):
        for r in trial_table(10):self.assertEqual(r['valid'],10)

if __name__=='__main__':unittest.main()
