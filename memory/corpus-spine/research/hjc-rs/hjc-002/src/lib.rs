//! HJC-002-RS / .dlw — structured conservation, not natural-language proof.
use sha2::{Digest, Sha256};
pub type Hash = [u8; 32];
pub const SEQUENCE: [u8; 12] = [0,1,2,1,2,0,2,0,1,0,1,2];
pub const PERIOD: u64 = 108;
const GENESIS: Hash = [0;32];

fn hash(domain: &[u8], fields: &[&[u8]]) -> Hash {
    let mut h = Sha256::new();
    for field in std::iter::once(domain).chain(fields.iter().copied()) {
        h.update((field.len() as u64).to_be_bytes());
        h.update(field);
    }
    h.finalize().into()
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Action { Preserve, Remove }
impl Action {
    fn tag(&self) -> &'static [u8] {
        match self { Self::Preserve => b"preserve", Self::Remove => b"remove" }
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Constraint {
    pub action: Action,
    pub object: String,
    pub source: String,
}
impl Constraint {
    fn digest(&self) -> Hash {
        hash(b"HJC/constraint/v1", &[self.action.tag(), self.object.as_bytes(), self.source.as_bytes()])
    }
    fn valid(&self) -> bool { !self.object.trim().is_empty() && !self.source.trim().is_empty() }
}
#[derive(Clone, Debug)]
pub struct Intent {
    original: String,
    constraint: Constraint,
    digest: Hash,
}
impl Intent {
    pub fn new(original: String, constraint: Constraint) -> Result<Self, &'static str> {
        if !constraint.valid() || !original.contains(&constraint.object) || !original.contains(&constraint.source) {
            return Err("unbound original or constraint");
        }
        let digest = hash(b"HJC/intent/v1", &[original.as_bytes(), &constraint.digest()]);
        Ok(Self { original, constraint, digest })
    }
    pub fn original(&self) -> &str { &self.original }
    pub fn digest(&self) -> Hash { self.digest }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Candidate {
    pub text: String,
    // Explicit structured assertion, not extracted or authenticated natural language.
    pub declared: Constraint,
}
impl Candidate {
    fn digest(&self) -> Hash {
        hash(b"HJC/candidate/v1", &[self.text.as_bytes(), &self.declared.digest()])
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum Outcome { StructuredMatch = 1, Conflict = 2, Unresolved = 3, Refused = 4 }
pub fn compare(i: &Intent, c: &Candidate) -> Outcome {
    if !c.declared.valid() || !c.text.contains(&i.constraint.object) || !c.text.contains(&i.constraint.source) {
        return Outcome::Unresolved;
    }
    if c.declared != i.constraint { return Outcome::Conflict; }
    // Even an equal declaration can contradict the accompanying text.
    Outcome::StructuredMatch
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Event {
    pub tick: u64,
    pub position: u64,
    pub body: u8,
    pub intent: Hash,
    pub candidate: Hash,
    pub outcome: Outcome,
    pub reason: String,
    pub previous: Hash,
    pub seal: Hash,
}
impl Event {
    fn digest(&self) -> Hash {
        hash(b"HJC/event/v1", &[&self.tick.to_be_bytes(), &self.position.to_be_bytes(), &[self.body], &self.intent, &self.candidate, &[self.outcome as u8], self.reason.as_bytes(), &self.previous])
    }
}
#[derive(Default)]
pub struct Hotel { events: Vec<Event> }
impl Hotel {
    pub fn referent(&self) -> (i8,u8) { (0,1) }
    pub fn events(&self) -> &[Event] { &self.events }
    fn append(&mut self, i: &Intent, c: Hash, outcome: Outcome, reason: String) -> Result<&Event,&'static str> {
        let tick = u64::try_from(self.events.len()).map_err(|_| "tick exhausted")?;
        let position = tick % PERIOD;
        let mut e = Event { tick, position, body: SEQUENCE[(position%12) as usize], intent:i.digest(), candidate:c, outcome, reason, previous:self.events.last().map_or(GENESIS, |e|e.seal), seal:GENESIS };
        e.seal=e.digest();
        self.events.push(e);
        Ok(self.events.last().expect("just appended"))
    }
    pub fn observe(&mut self, i: &Intent, c: &Candidate) -> Result<&Event,&'static str> {
        self.append(i,c.digest(),compare(i,c),String::new())
    }
    pub fn refuse(&mut self, i: &Intent, reason: String) -> Result<&Event,&'static str> {
        if reason.trim().is_empty() { return Err("reason required"); }
        self.append(i,GENESIS,Outcome::Refused,reason)
    }
}
// An expected head and length must be obtained from trusted external custody
// to detect truncation or complete resealing. This does not verify semantics.
pub fn verify_chain(events: &[Event], expected_len: usize, expected_head: Hash) -> bool {
    if events.len()!=expected_len { return false; }
    let mut previous=GENESIS;
    for (n,e) in events.iter().enumerate() {
        let tick=match u64::try_from(n) { Ok(v)=>v, Err(_)=>return false };
        if e.tick!=tick || e.position!=tick%PERIOD || e.body!=SEQUENCE[(tick%12) as usize] ||
            e.previous!=previous || e.seal!=e.digest() { return false; }
        previous=e.seal;
    }
    previous==expected_head
}
#[cfg(test)]
mod tests {
    use super::*;
    fn constraint(action: Action) -> Constraint { Constraint { action, object:"cinnamon".into(), source:"source-42".into() } }
    fn intent() -> Intent { Intent::new("Preserve cinnamon source-42".into(),constraint(Action::Preserve)).unwrap() }
    fn candidate(action: Action, text: &str) -> Candidate { Candidate {text:text.into(),declared:constraint(action)} }
    #[test] fn exact_structure() { assert_eq!(compare(&intent(),&candidate(Action::Preserve,"Keep cinnamon source-42")),Outcome::StructuredMatch); }
    #[test] fn opposite_action() { assert_eq!(compare(&intent(),&candidate(Action::Remove,"Remove cinnamon source-42")),Outcome::Conflict); }
    #[test] fn missing_object() { assert_eq!(compare(&intent(),&candidate(Action::Preserve,"Keep spice source-42")),Outcome::Unresolved); }
    #[test] fn missing_source() { assert_eq!(compare(&intent(),&candidate(Action::Preserve,"Keep cinnamon")),Outcome::Unresolved); }
    #[test] fn forged_declaration_not_semantic_proof() { assert_eq!(compare(&intent(),&candidate(Action::Preserve,"Remove cinnamon source-42")),Outcome::StructuredMatch); }
    #[test] fn field_boundaries() { assert_ne!(hash(b"x",&[b"ab",b"c"]),hash(b"x",&[b"a",b"bc"])); }
    #[test] fn source_bound() { let a=intent(); let b=Intent::new("Preserve cinnamon source-43".into(),Constraint{source:"source-43".into(),..constraint(Action::Preserve)}).unwrap(); assert_ne!(a.digest(),b.digest()); }
    #[test] fn candidate_bound() { assert_ne!(candidate(Action::Preserve,"Keep cinnamon source-42").digest(),candidate(Action::Preserve,"Remove cinnamon source-42").digest()); }
    #[test] fn chain_and_tamper() {
        let mut h=Hotel::default(); let i=intent();
        h.observe(&i,&candidate(Action::Preserve,"Keep cinnamon source-42")).unwrap();
        h.refuse(&i,"unverified meaning".into()).unwrap();
        let head=h.events()[1].seal;
        assert!(verify_chain(h.events(),2,head));
        let mut copy=h.events().to_vec(); copy[0].outcome=Outcome::Conflict;
        assert!(!verify_chain(&copy,2,head));
        assert!(!verify_chain(&h.events()[..1],2,head));
        copy=h.events().to_vec(); copy.swap(0,1); assert!(!verify_chain(&copy,2,head));
    }
    #[test] fn singular_cycle() {
        let mut h=Hotel::default(); let i=intent(); let mut counts=[0;3]; let mut transitions=[[0;3];3];
        for n in 0..108 { let e=h.refuse(&i,"test".into()).unwrap(); counts[e.body as usize]+=1; transitions[e.body as usize][SEQUENCE[(n+1)%12] as usize]+=1; assert_eq!(e.position,n as u64); }
        assert_eq!(counts,[36;3]); assert_eq!(transitions,[[0,27,9],[9,0,27],[27,9,0]]);
        assert_eq!(h.referent(),(0,1)); assert_eq!(h.refuse(&i,"test".into()).unwrap().position,0);
    }
    #[test] fn refusal_requires_reason() { let mut h=Hotel::default(); assert!(h.refuse(&intent()," ".into()).is_err()); assert!(h.events().is_empty()); }
}
