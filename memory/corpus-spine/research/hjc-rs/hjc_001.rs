//! HJC-001-RS — ROOT0 / .dlw
//! Exact literal preservation gate, not a semantic equivalence oracle.
pub const SEQUENCE: [u8; 12] = [0,1,2,1,2,0,2,0,1,0,1,2];
pub const PERIOD: usize = 108;

#[derive(Debug, PartialEq, Eq)]
pub struct Intent {
    original: String,
    source_id: String,
    protected: Vec<String>,
}

impl Intent {
    pub fn new(original: String, source_id: String, protected: Vec<String>) -> Result<Self, &'static str> {
        if original.trim().is_empty() || source_id.trim().is_empty() {
            return Err("missing intent or source identifier");
        }
        if protected.is_empty() || protected.iter().any(|p| p.trim().is_empty() || !original.contains(p)) {
            return Err("invalid protected literals");
        }
        Ok(Self { original, source_id, protected })
    }
    pub fn original(&self) -> &str { &self.original }
    pub fn source_id(&self) -> &str { &self.source_id }
}

#[derive(Debug, PartialEq, Eq)]
pub enum Decision {
    LiteralCandidate { index: usize },
    NoRoomWithinSuppliedCandidates,
    UnknownBudget,
    Refused { reason: &'static str },
}

#[derive(Debug, PartialEq, Eq)]
pub struct Observation {
    pub tick: u64,
    pub position: usize,
    pub body: u8,
    pub source_id: String,
    pub examined: usize,
    pub decision: Decision,
}

#[derive(Default)]
pub struct Hotel {
    ledger: Vec<Observation>,
    tick: u64,
}

impl Hotel {
    pub fn referent(&self) -> (i8, u8) { (0, 1) }
    pub fn ledger(&self) -> &[Observation] { &self.ledger }
    pub fn search(&mut self, intent: &Intent, candidates: &[String], budget: usize) -> Result<&Observation, &'static str> {
        let next = self.tick.checked_add(1).ok_or("tick exhausted")?;
        let mut examined = 0;
        let mut decision = Decision::NoRoomWithinSuppliedCandidates;
        for (index, candidate) in candidates.iter().enumerate() {
            if examined == budget {
                decision = Decision::UnknownBudget;
                break;
            }
            examined += 1;
            if intent.protected.iter().all(|p| candidate.contains(p)) {
                decision = Decision::LiteralCandidate { index };
                break;
            }
        }
        let position = (self.tick % PERIOD as u64) as usize;
        self.ledger.push(Observation {
            tick: self.tick, position, body: SEQUENCE[position % SEQUENCE.len()],
            source_id: intent.source_id.clone(), examined, decision,
        });
        self.tick = next;
        Ok(self.ledger.last().expect("just appended"))
    }
    pub fn refuse(&mut self, intent: &Intent, reason: &'static str) -> Result<&Observation, &'static str> {
        if reason.trim().is_empty() { return Err("reason required"); }
        let next = self.tick.checked_add(1).ok_or("tick exhausted")?;
        let position = (self.tick % PERIOD as u64) as usize;
        self.ledger.push(Observation {
            tick: self.tick, position, body: SEQUENCE[position % SEQUENCE.len()],
            source_id: intent.source_id.clone(), examined: 0,
            decision: Decision::Refused { reason },
        });
        self.tick = next;
        Ok(self.ledger.last().expect("just appended"))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn intent() -> Intent {
        Intent::new("Keep cinnamon and source-42".into(), "source-42".into(), vec!["cinnamon".into(), "source-42".into()]).unwrap()
    }
    #[test] fn rejects_flattening() {
        let mut h = Hotel::default();
        assert_eq!(h.search(&intent(), &["Keep spice and source-42".into()], 1).unwrap().decision, Decision::NoRoomWithinSuppliedCandidates);
    }
    #[test] fn finds_literal_candidate() {
        let mut h = Hotel::default();
        assert_eq!(h.search(&intent(), &["spice".into(), "cinnamon source-42".into()], 2).unwrap().decision, Decision::LiteralCandidate { index: 1 });
    }
    #[test] fn rejects_lost_identifier() {
        let mut h = Hotel::default();
        assert_eq!(h.search(&intent(), &["cinnamon".into()], 1).unwrap().decision, Decision::NoRoomWithinSuppliedCandidates);
    }
    #[test] fn budget_is_not_exhaustive_failure() {
        let mut h = Hotel::default();
        assert_eq!(h.search(&intent(), &["spice".into(), "cinnamon source-42".into()], 1).unwrap().decision, Decision::UnknownBudget);
    }
    #[test] fn empty_scope_is_exhaustive() {
        let mut h = Hotel::default();
        assert_eq!(h.search(&intent(), &[], 0).unwrap().decision, Decision::NoRoomWithinSuppliedCandidates);
    }
    #[test] fn zero_budget_nonempty_is_unknown() {
        let mut h = Hotel::default();
        assert_eq!(h.search(&intent(), &["cinnamon source-42".into()], 0).unwrap().decision, Decision::UnknownBudget);
    }
    #[test] fn rejects_empty_or_invented_protected_terms() {
        for p in [vec![], vec!["".into()], vec!["spice".into()]] {
            assert!(Intent::new("cinnamon".into(), "s".into(), p).is_err());
        }
    }
    #[test] fn immutable_input_and_append_only_history() {
        let i = intent();
        let mut h = Hotel::default();
        h.search(&i, &["spice".into()], 1).unwrap();
        h.refuse(&i, "uncertain").unwrap();
        assert_eq!(i.original(), "Keep cinnamon and source-42");
        assert_eq!(h.ledger().len(), 2);
        assert_eq!(h.ledger()[0].decision, Decision::NoRoomWithinSuppliedCandidates);
        assert_eq!(h.ledger()[1].tick, 1);
        assert_eq!(h.ledger()[1].source_id, "source-42");
    }
    #[test] fn cycle_balance_and_singlet() {
        let mut h = Hotel::default();
        let i = intent();
        let mut counts = [0;3];
        let mut transitions = [[0;3];3];
        for t in 0..PERIOD {
            let o = h.search(&i, &[], 0).unwrap();
            counts[o.body as usize] += 1;
            transitions[o.body as usize][SEQUENCE[(t+1)%12] as usize] += 1;
            assert_eq!(o.position, t);
            assert_eq!(h.referent(), (0,1));
        }
        assert_eq!(counts, [36;3]);
        assert_eq!(transitions, [[0,18,18],[18,0,18],[18,18,0]]);
        let o = h.search(&i, &[], 0).unwrap();
        assert_eq!((o.tick,o.position),(108,0));
    }
    #[test] fn literal_match_is_not_semantic_acceptance() {
        let mut h = Hotel::default();
        assert_eq!(h.search(&intent(), &["Remove cinnamon and source-42".into()], 1).unwrap().decision, Decision::LiteralCandidate { index: 0 });
    }
}
