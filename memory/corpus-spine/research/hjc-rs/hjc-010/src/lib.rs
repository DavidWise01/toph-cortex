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

// HJC-003: authenticated observation, not proof of independent cognition.
pub mod witness {
    use super::*;
    use ed25519_dalek::{Signature, VerifyingKey};
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    #[repr(u8)]
    pub enum Verdict { Preserve=1, Conflict=2, Unknown=3 }
    #[derive(Clone)]
    pub struct Root { pub key: VerifyingKey, pub ancestry: Hash }
    pub struct Policy { proposer: Root, witness: Root, context: Hash }
    #[derive(Clone)]
    pub struct Receipt {
        pub intent: Hash, pub candidate: Hash, pub context: Hash,
        pub tick: u64, pub previous: Hash, pub verdict: Verdict,
        pub signature: Signature,
    }
    impl Receipt {
        pub fn message(&self) -> Hash {
            hash(b"HJC/witness/v1",&[&self.intent,&self.candidate,&self.context,
                &self.tick.to_be_bytes(),&self.previous,&[self.verdict as u8]])
        }
    }
    #[derive(Debug,PartialEq,Eq)]
    pub enum Gate { WitnessedCandidate, Conflict, Hold }
    impl Policy {
        pub fn new(proposer: Root,witness: Root,session: Hash)->Result<Self,&'static str>{
            if proposer.key==witness.key || proposer.ancestry==witness.ancestry ||
                proposer.ancestry==[0;32] || witness.ancestry==[0;32] || session==[0;32] {
                return Err("distinct registered roots and session required");
            }
            let context=hash(b"HJC/policy/v1",&[proposer.key.as_bytes(),&proposer.ancestry,
                witness.key.as_bytes(),&witness.ancestry,&session]);
            Ok(Self{proposer,witness,context})
        }
        pub fn context(&self)->Hash {self.context}
        pub fn proposal_message(&self,i:&Intent,c:&Candidate,tick:u64,previous:Hash)->Hash{
            hash(b"HJC/proposal/v1",&[&self.context,&i.digest(),&c.digest(),&tick.to_be_bytes(),&previous])
        }
        pub fn gate(&self,i:&Intent,c:&Candidate,tick:u64,previous:Hash,
            proposal:&Signature,r:&Receipt)->Gate {
            if self.proposer.key.verify_strict(&self.proposal_message(i,c,tick,previous),proposal).is_err()
                || r.intent!=i.digest() || r.candidate!=c.digest() || r.context!=self.context
                || r.tick!=tick || r.previous!=previous
                || self.witness.key.verify_strict(&r.message(),&r.signature).is_err() {
                return Gate::Hold;
            }
            match (compare(i,c),r.verdict) {
                (Outcome::Conflict,_)|(_,Verdict::Conflict)=>Gate::Conflict,
                (Outcome::StructuredMatch,Verdict::Preserve)=>Gate::WitnessedCandidate,
                _=>Gate::Hold,
            }
        }
    }
    #[cfg(test)]
    mod tests {
        use super::*;
        use ed25519_dalek::{Signer,SigningKey};
        fn fixture()->(SigningKey,SigningKey,Policy,Intent,Candidate) {
            let a=SigningKey::from_bytes(&[1;32]);let b=SigningKey::from_bytes(&[2;32]);
            let p=Policy::new(Root{key:a.verifying_key(),ancestry:[3;32]},
                Root{key:b.verifying_key(),ancestry:[4;32]},[5;32]).unwrap();
            let c=Constraint{action:Action::Preserve,object:"cinnamon".into(),source:"source-42".into()};
            let i=Intent::new("Preserve cinnamon source-42".into(),c.clone()).unwrap();
            (a,b,p,i,Candidate{text:"Keep cinnamon source-42".into(),declared:c})
        }
        fn receipt(p:&Policy,i:&Intent,c:&Candidate,b:&SigningKey,v:Verdict)->Receipt {
            let mut r=Receipt{intent:i.digest(),candidate:c.digest(),context:p.context(),
                tick:0,previous:[0;32],verdict:v,signature:b.sign(b"placeholder")};
            r.signature=b.sign(&r.message());r
        }
        #[test] fn valid_receipt(){
            let(a,b,p,i,c)=fixture();let r=receipt(&p,&i,&c,&b,Verdict::Preserve);
            assert_eq!(p.gate(&i,&c,0,[0;32],&a.sign(&p.proposal_message(&i,&c,0,[0;32])),&r),Gate::WitnessedCandidate);
        }
        #[test] fn self_certification_rejected(){
            let(a,_,_,_,_)=fixture();assert!(Policy::new(Root{key:a.verifying_key(),ancestry:[3;32]},Root{key:a.verifying_key(),ancestry:[4;32]},[5;32]).is_err());
        }
        #[test] fn shared_ancestry_rejected(){
            let(a,b,_,_,_)=fixture();assert!(Policy::new(Root{key:a.verifying_key(),ancestry:[3;32]},Root{key:b.verifying_key(),ancestry:[3;32]},[5;32]).is_err());
        }
        #[test] fn negative_and_unknown(){
            let(a,b,p,i,c)=fixture();let s=a.sign(&p.proposal_message(&i,&c,0,[0;32]));
            for(v,g)in [(Verdict::Conflict,Gate::Conflict),(Verdict::Unknown,Gate::Hold)]{
                assert_eq!(p.gate(&i,&c,0,[0;32],&s,&receipt(&p,&i,&c,&b,v)),g);
            }
        }
        #[test] fn wrong_signer_and_mutation(){
            let(a,b,p,i,mut c)=fixture();let s=a.sign(&p.proposal_message(&i,&c,0,[0;32]));
            assert_eq!(p.gate(&i,&c,0,[0;32],&s,&receipt(&p,&i,&c,&a,Verdict::Preserve)),Gate::Hold);
            let r=receipt(&p,&i,&c,&b,Verdict::Preserve);c.text.push('!');
            assert_eq!(p.gate(&i,&c,0,[0;32],&s,&r),Gate::Hold);
        }
        #[test] fn stale_position(){
            let(a,b,p,i,c)=fixture();let r=receipt(&p,&i,&c,&b,Verdict::Preserve);
            let s=a.sign(&p.proposal_message(&i,&c,1,[7;32]));
            assert_eq!(p.gate(&i,&c,1,[7;32],&s,&r),Gate::Hold);
        }
        #[test] fn signature_not_truth(){
            let(a,b,p,i,mut c)=fixture();c.text="Remove cinnamon source-42".into();
            let r=receipt(&p,&i,&c,&b,Verdict::Preserve);
            assert_eq!(p.gate(&i,&c,0,[0;32],&a.sign(&p.proposal_message(&i,&c,0,[0;32])),&r),Gate::WitnessedCandidate);
        }
    }
}

// HJC-004: one checkpoint, three separately registered observation slots.
pub mod triad {
    use super::*;
    use super::witness::{Root,Verdict};
    use ed25519_dalek::Signature;
    #[derive(Clone)]
    pub struct Receipt { pub slot:u8, pub message:Hash, pub verdict:Verdict, pub signature:Signature }
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub enum Status { Missing, Invalid, Preserve, Conflict, Unknown, Duplicate }
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub enum ResultGate { Hold, Conflict, WitnessedCandidate }
    #[derive(Clone)]
    pub struct Record {
        pub tick:u64, pub previous:Hash, pub intent:Hash, pub candidate:Hash,
        pub proposal:Signature, pub receipts:Vec<Receipt>, pub slots:[Status;3],
        pub gate:ResultGate, pub seal:Hash,
    }
    pub struct Triad {
        proposer:Root, roots:[Root;3], context:Hash, records:Vec<Record>,
    }
    impl Triad {
        pub fn new(proposer:Root, roots:[Root;3], session:Hash)->Result<Self,&'static str>{
            let all=[&proposer,&roots[0],&roots[1],&roots[2]];
            if session==[0;32] {return Err("zero session");}
            for (i,a) in all.iter().enumerate(){
                if a.ancestry==[0;32] {return Err("zero ancestry");}
                for b in &all[..i] {
                    if a.key==b.key || a.ancestry==b.ancestry {return Err("shared registered root");}
                }
            }
            let context=hash(b"HJC/triad/policy/v1",&[&session,proposer.key.as_bytes(),&proposer.ancestry,
                roots[0].key.as_bytes(),&roots[0].ancestry,roots[1].key.as_bytes(),&roots[1].ancestry,
                roots[2].key.as_bytes(),&roots[2].ancestry]);
            Ok(Self{proposer,roots,context,records:Vec::new()})
        }
        pub fn records(&self)->&[Record]{&self.records}
        pub fn referent(&self)->(i8,u8){(0,1)}
        pub fn checkpoint(&self)->(u64,Hash){
            (self.records.len() as u64,self.records.last().map_or([0;32],|r|r.seal))
        }
        pub fn proposal_message(&self,i:&Intent,c:&Candidate)->Hash{
            let(t,p)=self.checkpoint();
            hash(b"HJC/triad/proposal/v1",&[&self.context,&t.to_be_bytes(),&p,&i.digest(),&c.digest()])
        }
        pub fn witness_message(proposal:Hash,slot:u8,v:Verdict)->Hash{
            hash(b"HJC/triad/receipt/v1",&[&proposal,&[slot],&[v as u8]])
        }
        pub fn observe(&mut self,i:&Intent,c:&Candidate,proposal:Signature,receipts:Vec<Receipt>)->Result<&Record,&'static str>{
            if receipts.len()>12 {return Err("receipt envelope exceeds bound");}
            let(tick,previous)=self.checkpoint();
            tick.checked_add(1).ok_or("tick exhausted")?;
            let msg=self.proposal_message(i,c);
            let authenticated=self.proposer.key.verify_strict(&msg,&proposal).is_ok();
            let mut slots=[Status::Missing;3];
            let mut counts=[0u8;3];
            let mut conflict=false;
            let mut malformed=false;
            for r in &receipts {
                let k=r.slot as usize;
                if k>=3 {malformed=true;continue;}
                counts[k]+=1;
                let valid=r.message==Self::witness_message(msg,r.slot,r.verdict)
                    && self.roots[k].key.verify_strict(&r.message,&r.signature).is_ok();
                if valid && r.verdict==Verdict::Conflict {conflict=true;}
                slots[k]=if counts[k]>1 {Status::Duplicate} else if !valid {Status::Invalid}
                    else {match r.verdict {Verdict::Preserve=>Status::Preserve,Verdict::Conflict=>Status::Conflict,Verdict::Unknown=>Status::Unknown}};
            }
            let gate=if !authenticated {ResultGate::Hold}
                else if conflict || compare(i,c)==Outcome::Conflict {ResultGate::Conflict}
                else if !malformed && slots==[Status::Preserve;3] && compare(i,c)==Outcome::StructuredMatch {ResultGate::WitnessedCandidate}
                else {ResultGate::Hold};
            let mut bytes=Vec::new();
            for r in &receipts {bytes.push(r.slot);bytes.extend(r.message);bytes.push(r.verdict as u8);bytes.extend(r.signature.to_bytes());}
            let tags=slots.map(|s|match s{Status::Missing=>0,Status::Invalid=>1,Status::Preserve=>2,Status::Conflict=>3,Status::Unknown=>4,Status::Duplicate=>5});
            let g=match gate{ResultGate::Hold=>0,ResultGate::Conflict=>1,ResultGate::WitnessedCandidate=>2};
            let seal=hash(b"HJC/triad/event/v1",&[&msg,&proposal.to_bytes(),&bytes,&tags,&[g]]);
            self.records.push(Record{tick,previous,intent:i.digest(),candidate:c.digest(),proposal,receipts,slots,gate,seal});
            Ok(self.records.last().unwrap())
        }
    }
    #[cfg(test)]
    mod tests{
        use super::*;
        use ed25519_dalek::{Signer,SigningKey};
        fn fixture()->(Triad,[SigningKey;4],Intent,Candidate){
            let keys=[1,2,3,4].map(|v|SigningKey::from_bytes(&[v;32]));
            let root=|k:usize|Root{key:keys[k].verifying_key(),ancestry:[(k+10) as u8;32]};
            let h=Triad::new(root(0),[root(1),root(2),root(3)],[9;32]).unwrap();
            let d=Constraint{action:Action::Preserve,object:"cinnamon".into(),source:"source-42".into()};
            let i=Intent::new("Preserve cinnamon source-42".into(),d.clone()).unwrap();
            (h,keys,i,Candidate{text:"Keep cinnamon source-42".into(),declared:d})
        }
        fn batch(h:&Triad,k:&[SigningKey;4],i:&Intent,c:&Candidate,v:[Verdict;3])->(Signature,Vec<Receipt>){
            let p=h.proposal_message(i,c);
            (k[0].sign(&p),(0..3).map(|s|{let m=Triad::witness_message(p,s as u8,v[s]);Receipt{slot:s as u8,message:m,verdict:v[s],signature:k[s+1].sign(&m)}}).collect())
        }
        #[test] fn all_27_verdict_combinations(){
            for a in [Verdict::Preserve,Verdict::Conflict,Verdict::Unknown]{
                for b in [Verdict::Preserve,Verdict::Conflict,Verdict::Unknown]{
                    for c in [Verdict::Preserve,Verdict::Conflict,Verdict::Unknown]{
                        let(mut h,k,i,p)=fixture();let v=[a,b,c];let(s,r)=batch(&h,&k,&i,&p,v);
                        let expected=if v.contains(&Verdict::Conflict){ResultGate::Conflict}else if v==[Verdict::Preserve;3]{ResultGate::WitnessedCandidate}else{ResultGate::Hold};
                        assert_eq!(h.observe(&i,&p,s,r).unwrap().gate,expected);
                    }
                }
            }
        }
        #[test] fn missing_is_not_quorum(){let(mut h,k,i,c)=fixture();let(s,mut r)=batch(&h,&k,&i,&c,[Verdict::Preserve;3]);r.pop();assert_eq!(h.observe(&i,&c,s,r).unwrap().gate,ResultGate::Hold);}
        #[test] fn duplicate_is_not_witness(){let(mut h,k,i,c)=fixture();let(s,mut r)=batch(&h,&k,&i,&c,[Verdict::Preserve;3]);r.push(r[0].clone());assert_eq!(h.observe(&i,&c,s,r).unwrap().gate,ResultGate::Hold);}
        #[test] fn replay_moves_checkpoint(){let(mut h,k,i,c)=fixture();let(s,r)=batch(&h,&k,&i,&c,[Verdict::Preserve;3]);let first=h.observe(&i,&c,s,r.clone()).unwrap().seal;let e=h.observe(&i,&c,s,r).unwrap();assert_eq!(e.previous,first);assert_eq!(e.gate,ResultGate::Hold);assert_eq!(h.referent(),(0,1));}
        #[test] fn wrong_signer(){let(mut h,k,i,c)=fixture();let(s,mut r)=batch(&h,&k,&i,&c,[Verdict::Preserve;3]);r[0].signature=k[0].sign(&r[0].message);assert_eq!(h.observe(&i,&c,s,r).unwrap().gate,ResultGate::Hold);}
        #[test] fn duplicate_root(){let(_,k,_,_)=fixture();let a=Root{key:k[0].verifying_key(),ancestry:[1;32]};assert!(Triad::new(a.clone(),[a.clone(),a.clone(),a],[9;32]).is_err());}
    }
}

// HJC-005: finite deterministic room discovery. No semantic authorization.
pub mod rooms {
    use super::*;
    pub const MAX_INPUT_BYTES:usize=65536;
    pub const MAX_ROOMS:usize=9;
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub enum Room { N,S,E,W,Ne,Nw,Se,Sw,Singlet }
    pub const ROOMS:[Room;9]=[Room::N,Room::S,Room::E,Room::W,Room::Ne,Room::Nw,Room::Se,Room::Sw,Room::Singlet];
    impl Room {
        fn label(self)->&'static str {
            match self {Self::N=>"N",Self::S=>"S",Self::E=>"E",Self::W=>"W",Self::Ne=>"NE",Self::Nw=>"NW",Self::Se=>"SE",Self::Sw=>"SW",Self::Singlet=>"SINGLET"}
        }
    }
    #[derive(Clone,Debug)]
    pub struct Found { pub room:Room,pub candidate:Candidate,pub digest:Hash }
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub enum SearchState { CandidatesFound, NoRoomInDeclaredScope, BudgetExhausted, InputLimit }
    #[derive(Clone,Debug)]
    pub struct Report {
        pub intent:Hash,pub examined:usize,pub complete:bool,pub state:SearchState,
        pub candidates:Vec<Found>,pub trace:Vec<(Room,Hash,bool)>,
    }
    // Wrappers preserve the original byte sequence, rather than paraphrasing it.
    // No candidate is interpreted as an instruction or executed by this module.
    fn generate(i:&Intent,room:Room)->Candidate {
        let original=i.original();
        let text=match room {
            Room::Singlet=>original.to_owned(),
            _=>format!("HJC room {}\nOriginal intent ({} bytes):\n{}",room.label(),original.len(),original),
        };
        Candidate{text,declared:i.constraint.clone()}
    }
    pub fn discover(i:&Intent,budget:usize,max_room_bytes:usize)->Report {
        let mut r=Report{intent:i.digest(),examined:0,complete:false,state:SearchState::BudgetExhausted,candidates:Vec::new(),trace:Vec::new()};
        if i.original().len()>MAX_INPUT_BYTES || i.constraint.object.len()>MAX_INPUT_BYTES || i.constraint.source.len()>MAX_INPUT_BYTES {
            r.state=SearchState::InputLimit;return r;
        }
        for room in ROOMS.iter().copied().take(budget.min(MAX_ROOMS)) {
            let c=generate(i,room);
            let fits=c.text.len()<=max_room_bytes && c.text.ends_with(i.original())
                && compare(i,&c)==Outcome::StructuredMatch;
            let digest=c.digest();
            r.examined+=1;
            r.trace.push((room,digest,fits));
            if fits {r.candidates.push(Found{room,candidate:c,digest});}
        }
        r.complete=r.examined==MAX_ROOMS;
        r.state=if !r.candidates.is_empty(){SearchState::CandidatesFound}
            else if r.complete{SearchState::NoRoomInDeclaredScope}
            else{SearchState::BudgetExhausted};
        r
    }
    #[cfg(test)]
    mod tests {
        use super::*;
        fn intent()->Intent {
            Intent::new("Preserve cinnamon source-42".into(),Constraint{action:Action::Preserve,object:"cinnamon".into(),source:"source-42".into()}).unwrap()
        }
        #[test] fn all_nine_rooms() {
            let i=intent();let r=discover(&i,9,1000);
            assert_eq!(r.examined,9);assert!(r.complete);assert_eq!(r.candidates.len(),9);
            assert_eq!(r.state,SearchState::CandidatesFound);
            for c in r.candidates {assert!(c.candidate.text.ends_with(i.original()));assert_eq!(c.digest,c.candidate.digest());}
        }
        #[test] fn hidden_room_exact_fit() {
            let i=intent();let r=discover(&i,9,i.original().len());
            assert_eq!(r.candidates.len(),1);assert_eq!(r.candidates[0].room,Room::Singlet);
            assert_eq!(r.candidates[0].candidate.text,i.original());
        }
        #[test] fn budget_cannot_claim_impossibility() {
            let i=intent();let r=discover(&i,8,i.original().len());
            assert_eq!(r.state,SearchState::BudgetExhausted);assert!(!r.complete);
        }
        #[test] fn exhausted_scope() {
            let i=intent();let r=discover(&i,9,i.original().len()-1);
            assert_eq!(r.state,SearchState::NoRoomInDeclaredScope);assert!(r.complete);
        }
        #[test] fn zero_budget() {
            let r=discover(&intent(),0,1000);assert_eq!(r.examined,0);assert_eq!(r.state,SearchState::BudgetExhausted);
        }
        #[test] fn deterministic_trace() {
            let i=intent();assert_eq!(discover(&i,9,1000).trace,discover(&i,usize::MAX,1000).trace);
        }
        #[test] fn immutable_intent() {
            let i=intent();let d=i.digest();let _=discover(&i,9,1000);assert_eq!(i.digest(),d);assert_eq!(i.original(),"Preserve cinnamon source-42");
        }
        #[test] fn input_limit() {
            let mut s="cinnamon source-42 ".to_owned();s.push_str(&"x".repeat(MAX_INPUT_BYTES));
            let i=Intent::new(s,Constraint{action:Action::Preserve,object:"cinnamon".into(),source:"source-42".into()}).unwrap();
            let r=discover(&i,9,usize::MAX);assert_eq!(r.state,SearchState::InputLimit);assert_eq!(r.examined,0);
        }
        #[test] fn partial_success_not_complete() {
            let r=discover(&intent(),1,1000);assert_eq!(r.state,SearchState::CandidatesFound);assert!(!r.complete);
        }
    }
}

// HJC-006: finite occupancy; relocation changes slots, never customer identity.
pub mod occupancy {
    use super::*;
    pub const N:usize=9;
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub struct Customer { id:Hash, allowed:u16 }
    impl Customer {
        pub fn new(i:&Intent,allowed:u16)->Result<Self,&'static str>{
            if allowed==0 || allowed & !0x1ff !=0{return Err("invalid room mask");}
            Ok(Self{id:i.digest(),allowed})
        }
        pub fn id(&self)->Hash{self.id}
        fn fits(&self,k:usize)->bool{self.allowed & (1u16<<k)!=0}
    }
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub enum Admission { Admitted, Duplicate, Full, NoCompatiblePath, BudgetExhausted }
    #[derive(Clone,Debug)]
    pub struct Record {
        pub tick:u64,pub position:u64,pub body:u8,pub incoming:Hash,pub allowed:u16,
        pub budget:usize,pub examined:usize,pub result:Admission,
        pub before:Hash,pub after:Hash,pub previous:Hash,pub seal:Hash,
    }
    #[derive(Default)]
    pub struct Hotel { slots:[Option<Customer>;N], history:Vec<Record> }
    fn snapshot(slots:&[Option<Customer>;N])->Hash{
        let mut b=Vec::new();
        for slot in slots {
            match slot {None=>b.push(0),Some(c)=>{b.push(1);b.extend(c.id);b.extend(c.allowed.to_be_bytes());}}
        }
        hash(b"HJC/occupancy/snapshot/v1",&[&b])
    }
    // Deterministic augmenting path through distinct rooms. Mutate only on success.
    fn place(c:Customer,slots:&mut [Option<Customer>;N],seen:&mut [bool;N],remaining:&mut usize)->Result<bool,()>{
        for k in 0..N {
            if seen[k] || !c.fits(k){continue;}
            if *remaining==0{return Err(());}
            *remaining-=1;seen[k]=true;
            let success=match slots[k]{None=>true,Some(old)=>place(old,slots,seen,remaining)?};
            if success {slots[k]=Some(c);return Ok(true);}
        }
        Ok(false)
    }
    impl Hotel {
        pub fn slots(&self)->&[Option<Customer>;N]{&self.slots}
        pub fn history(&self)->&[Record]{&self.history}
        pub fn referent(&self)->(i8,u8){(0,1)}
        pub fn admit(&mut self,c:Customer,budget:usize)->Result<&Record,&'static str>{
            let tick=u64::try_from(self.history.len()).map_err(|_|"tick exhausted")?;
            tick.checked_add(1).ok_or("tick exhausted")?;
            let before=snapshot(&self.slots);let mut trial=self.slots;
            let limit=budget.min(N);let mut remaining=limit;
            let result=if self.slots.iter().flatten().any(|x|x.id==c.id){Admission::Duplicate}
                else if self.slots.iter().all(Option::is_some){Admission::Full}
                else{match place(c,&mut trial,&mut [false;N],&mut remaining){
                    Ok(true)=>{self.slots=trial;Admission::Admitted},
                    Ok(false)=>Admission::NoCompatiblePath,
                    Err(())=>Admission::BudgetExhausted,
                }};
            let after=snapshot(&self.slots);
            let previous=self.history.last().map_or([0;32],|r|r.seal);
            let tag=match result{Admission::Admitted=>1,Admission::Duplicate=>2,Admission::Full=>3,Admission::NoCompatiblePath=>4,Admission::BudgetExhausted=>5};
            let examined=limit-remaining;
            let seal=hash(b"HJC/occupancy/event/v1",&[&tick.to_be_bytes(),&c.id,&c.allowed.to_be_bytes(),
                &(limit as u64).to_be_bytes(),&(examined as u64).to_be_bytes(),&[tag],&before,&after,&previous]);
            self.history.push(Record{tick,position:tick%PERIOD,body:SEQUENCE[(tick%12) as usize],incoming:c.id,
                allowed:c.allowed,budget:limit,examined,result,before,after,previous,seal});
            Ok(self.history.last().unwrap())
        }
    }
    #[cfg(test)]
    mod tests{
        use super::*;
        fn customer(n:usize,mask:u16)->Customer{
            let s=format!("Preserve cinnamon source-{n}");
            let i=Intent::new(s,Constraint{action:Action::Preserve,object:"cinnamon".into(),source:format!("source-{n}")}).unwrap();
            Customer::new(&i,mask).unwrap()
        }
        #[test] fn relocation_preserves_customer(){
            let mut h=Hotel::default();let a=customer(1,3);let b=customer(2,1);
            h.admit(a,9).unwrap();assert_eq!(h.admit(b,9).unwrap().result,Admission::Admitted);
            assert_eq!(h.slots()[0],Some(b));assert_eq!(h.slots()[1],Some(a));
        }
        #[test] fn budget_failure_atomic(){
            let mut h=Hotel::default();h.admit(customer(1,3),9).unwrap();let prior=*h.slots();
            let r=h.admit(customer(2,1),1).unwrap();assert_eq!(r.result,Admission::BudgetExhausted);assert_eq!(r.before,r.after);
            assert_eq!(*h.slots(),prior);
        }
        #[test] fn incompatible_atomic(){
            let mut h=Hotel::default();h.admit(customer(1,1),9).unwrap();let prior=*h.slots();
            assert_eq!(h.admit(customer(2,1),9).unwrap().result,Admission::NoCompatiblePath);assert_eq!(*h.slots(),prior);
        }
        #[test] fn full_hotel(){
            let mut h=Hotel::default();for n in 0..9{assert_eq!(h.admit(customer(n,0x1ff),9).unwrap().result,Admission::Admitted);}
            let prior=*h.slots();assert_eq!(h.admit(customer(9,0x1ff),9).unwrap().result,Admission::Full);assert_eq!(*h.slots(),prior);
        }
        #[test] fn duplicate_rejected(){
            let mut h=Hotel::default();let c=customer(1,3);h.admit(c,9).unwrap();
            assert_eq!(h.admit(c,9).unwrap().result,Admission::Duplicate);
        }
        #[test] fn chain_of_relocations(){
            let mut h=Hotel::default();
            for n in 0..8{h.admit(customer(n,3u16<<n),9).unwrap();}
            assert_eq!(h.admit(customer(8,1),9).unwrap().result,Admission::Admitted);
            for (k,c) in h.slots().iter().enumerate(){assert!(c.unwrap().fits(k));}
            for n in 0..8{assert_eq!(h.slots()[n+1],Some(customer(n,3u16<<n)));}
        }
        #[test] fn zero_budget(){
            let mut h=Hotel::default();assert_eq!(h.admit(customer(0,1),0).unwrap().result,Admission::BudgetExhausted);
            assert!(h.slots().iter().all(Option::is_none));
        }
        #[test] fn history_advances_without_mutating_reference(){
            let mut h=Hotel::default();let c=customer(0,1);
            for n in 0..109 {let r=h.admit(c,9).unwrap();assert_eq!(r.tick,n);assert_eq!(r.position,n%108);}
            assert_eq!(h.referent(),(0,1));
            for pair in h.history().windows(2){assert_eq!(pair[1].previous,pair[0].seal);}
        }
    }
}

// HJC-007: bounded nested accommodation; one global referent, no execution authority.
pub mod nested {
    use super::*;
    pub const HOTELS:usize=3;
    pub const ROOMS:usize=9;
    pub const CAPACITY:usize=HOTELS*ROOMS;
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub struct Customer { id:Hash, allowed:u32 }
    impl Customer {
        pub fn new(i:&Intent,allowed:u32)->Result<Self,&'static str>{
            if allowed==0 || allowed & !((1u32<<CAPACITY)-1)!=0{return Err("invalid global compatibility mask");}
            Ok(Self{id:i.digest(),allowed})
        }
        pub fn id(&self)->Hash{self.id}
        fn fits(&self,k:usize)->bool{self.allowed & (1u32<<k)!=0}
    }
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    #[repr(u8)]
    pub enum Decision { Admitted=1, Duplicate=2, Full=3, NoPathInScope=4, BudgetExhausted=5 }
    #[derive(Clone,Debug)]
    pub struct Record {
        pub tick:u64,pub position:u64,pub incoming:Hash,pub allowed:u32,
        pub depth:usize,pub budget:usize,pub examined:usize,pub decision:Decision,
        pub before:Hash,pub after:Hash,pub previous:Hash,pub seal:Hash,
    }
    pub struct Hotel { slots:[Option<Customer>;CAPACITY], history:Vec<Record> }
    impl Default for Hotel {fn default()->Self{Self{slots:[None;CAPACITY],history:Vec::new()}}}
    fn snapshot(s:&[Option<Customer>;CAPACITY])->Hash{
        let mut b=Vec::new();
        for x in s {match x{None=>b.push(0),Some(c)=>{b.push(1);b.extend(c.id);b.extend(c.allowed.to_be_bytes());}}}
        hash(b"HJC/nested/snapshot/v1",&[&b])
    }
    // Linear ancestry: root -> child -> grandchild. Scope is a depth prefix.
    // Search marks each room once; staged moves are published only on success.
    fn place(c:Customer,s:&mut [Option<Customer>;CAPACITY],seen:&mut [bool;CAPACITY],remaining:&mut usize,scope:usize)->Result<bool,()>{
        for k in 0..scope{
            if seen[k] || !c.fits(k){continue;}
            if *remaining==0{return Err(());}
            *remaining-=1;seen[k]=true;
            let ok=match s[k]{None=>true,Some(old)=>place(old,s,seen,remaining,scope)?};
            if ok{s[k]=Some(c);return Ok(true);}
        }
        Ok(false)
    }
    impl Hotel {
        pub fn slots(&self)->&[Option<Customer>;CAPACITY]{&self.slots}
        pub fn history(&self)->&[Record]{&self.history}
        pub fn referent(&self)->(i8,u8){(0,1)}
        pub fn admit(&mut self,c:Customer,depth:usize,budget:usize)->Result<&Record,&'static str>{
            if depth>=HOTELS{return Err("depth outside topology");}
            let tick=u64::try_from(self.history.len()).map_err(|_|"tick exhausted")?;
            tick.checked_add(1).ok_or("tick exhausted")?;
            let scope=(depth+1)*ROOMS;let limit=budget.min(scope);let mut remaining=limit;
            let before=snapshot(&self.slots);let mut trial=self.slots;
            let decision=if self.slots.iter().flatten().any(|x|x.id==c.id){Decision::Duplicate}
                else if self.slots.iter().all(Option::is_some){Decision::Full}
                else{match place(c,&mut trial,&mut [false;CAPACITY],&mut remaining,scope){
                    Ok(true)=>{self.slots=trial;Decision::Admitted},
                    Ok(false)=>Decision::NoPathInScope,
                    Err(())=>Decision::BudgetExhausted,
                }};
            let after=snapshot(&self.slots);let previous=self.history.last().map_or([0;32],|r|r.seal);
            let examined=limit-remaining;
            let seal=hash(b"HJC/nested/event/v1",&[&tick.to_be_bytes(),&c.id,&c.allowed.to_be_bytes(),
                &(depth as u64).to_be_bytes(),&(limit as u64).to_be_bytes(),&(examined as u64).to_be_bytes(),
                &[decision as u8],&before,&after,&previous]);
            self.history.push(Record{tick,position:tick%PERIOD,incoming:c.id,allowed:c.allowed,
                depth,budget:limit,examined,decision,before,after,previous,seal});
            Ok(self.history.last().unwrap())
        }
    }
    #[cfg(test)]
    mod tests {
        use super::*;
        fn c(n:usize,mask:u32)->Customer{
            let source=format!("source-{n}");
            let i=Intent::new(format!("Preserve cinnamon {source}"),Constraint{action:Action::Preserve,object:"cinnamon".into(),source}).unwrap();
            Customer::new(&i,mask).unwrap()
        }
        #[test] fn nested_overflow(){
            let mut h=Hotel::default();
            for k in 0..9{h.admit(c(k,1<<k),0,9).unwrap();}
            assert_eq!(h.admit(c(9,1<<9),0,9).unwrap().decision,Decision::NoPathInScope);
            assert_eq!(h.admit(c(9,1<<9),1,18).unwrap().decision,Decision::Admitted);
            assert_eq!(h.slots()[9],Some(c(9,1<<9)));
        }
        #[test] fn cross_hotel_relocation(){
            let mut h=Hotel::default();let a=c(0,(1<<8)|(1<<9));let b=c(1,1<<8);
            h.admit(a,0,9).unwrap();assert_eq!(h.admit(b,1,18).unwrap().decision,Decision::Admitted);
            assert_eq!(h.slots()[8],Some(b));assert_eq!(h.slots()[9],Some(a));
        }
        #[test] fn global_duplicate(){
            let mut h=Hotel::default();let a=c(0,1<<9);h.admit(a,1,18).unwrap();
            assert_eq!(h.admit(a,0,9).unwrap().decision,Decision::Duplicate);
        }
        #[test] fn budget_atomic(){
            let mut h=Hotel::default();h.admit(c(0,(1<<8)|(1<<9)),0,9).unwrap();let prior=*h.slots();
            let r=h.admit(c(1,1<<8),1,1).unwrap();
            assert_eq!(r.decision,Decision::BudgetExhausted);assert_eq!(r.before,r.after);assert_eq!(*h.slots(),prior);
        }
        #[test] fn global_full(){
            let mut h=Hotel::default();for k in 0..CAPACITY{assert_eq!(h.admit(c(k,1<<k),2,27).unwrap().decision,Decision::Admitted);}
            let prior=*h.slots();assert_eq!(h.admit(c(27,1),2,27).unwrap().decision,Decision::Full);assert_eq!(*h.slots(),prior);
        }
        #[test] fn invalid_depth_no_mutation(){
            let mut h=Hotel::default();assert!(h.admit(c(0,1),3,27).is_err());assert!(h.history().is_empty());
        }
        #[test] fn singular_referent(){
            let mut h=Hotel::default();for k in 0..109{let r=h.admit(c(0,1),2,27).unwrap();assert_eq!(r.position,k%108);}
            assert_eq!(h.referent(),(0,1));for pair in h.history().windows(2){assert_eq!(pair[1].previous,pair[0].seal);}
        }
        #[test] fn full_scope_relocation_chain(){
            let mut h=Hotel::default();for k in 0..26{h.admit(c(k,3<<k),2,27).unwrap();}
            assert_eq!(h.admit(c(26,1),2,27).unwrap().decision,Decision::Admitted);
            assert_eq!(h.slots()[0],Some(c(26,1)));
            for k in 0..26{assert_eq!(h.slots()[k+1],Some(c(k,3<<k)));}
        }
    }
}

// HJC-008: integrated in-memory simulation; signed observations do not authorize external actions.
pub mod unified {
    use super::*;
    use super::witness::{Root,Verdict};
    use ed25519_dalek::Signature;
    #[derive(Clone)]
    pub struct Receipt {pub slot:u8,pub verdict:Verdict,pub signature:Signature}
    #[derive(Clone)]
    pub struct Request {
        pub intent:Intent,pub room:usize,pub capacity:usize,pub discovery_budget:usize,
        pub allowed:u32,pub depth:usize,pub relocation_budget:usize,
        pub proposal:Signature,pub receipts:Vec<Receipt>,
    }
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    #[repr(u8)]
    pub enum Decision { Hold=0,Conflict=1,Admitted=2,Duplicate=3,Full=4,NoPath=5,Budget=6 }
    #[derive(Clone)]
    pub struct Record {pub tick:u64,pub position:u64,pub body:u8,pub request:Request,
        pub decision:Decision,pub previous:Hash,pub occupancy:Hash,pub seal:Hash}
    pub struct Hotel {proposer:Root,roots:[Root;3],session:Hash,context:Hash,
        occupancy:nested::Hotel,records:Vec<Record>}
    impl Hotel {
        pub fn new(proposer:Root,roots:[Root;3],session:Hash)->Result<Self,&'static str>{
            let all=[&proposer,&roots[0],&roots[1],&roots[2]];
            if session==[0;32]{return Err("zero session");}
            for (n,a) in all.iter().enumerate(){
                if a.ancestry==[0;32]{return Err("zero ancestry");}
                for b in &all[..n]{if a.key==b.key || a.ancestry==b.ancestry{return Err("shared root");}}
            }
            let context=hash(b"HJC/unified/policy/v1",&[&session,proposer.key.as_bytes(),&proposer.ancestry,
                roots[0].key.as_bytes(),&roots[0].ancestry,roots[1].key.as_bytes(),&roots[1].ancestry,
                roots[2].key.as_bytes(),&roots[2].ancestry]);
            Ok(Self{proposer,roots,session,context,occupancy:nested::Hotel::default(),records:Vec::new()})
        }
        pub fn records(&self)->&[Record]{&self.records}
        pub fn referent(&self)->(i8,u8){(0,1)}
        pub fn occupied(&self)->usize{self.occupancy.slots().iter().flatten().count()}
        pub fn checkpoint(&self)->(u64,Hash){
            (self.records.len() as u64,self.records.last().map_or([0;32],|r|r.seal))
        }
        fn selected(r:&Request)->Option<Candidate>{
            let report=rooms::discover(&r.intent,r.discovery_budget,r.capacity);
            let room=*rooms::ROOMS.get(r.room)?;
            report.candidates.into_iter().find(|f|f.room==room).map(|f|f.candidate)
        }
        pub fn message(&self,r:&Request)->Hash{
            let(t,p)=self.checkpoint();
            let candidate=Self::selected(r).map_or([0;32],|c|c.digest());
            hash(b"HJC/unified/proposal/v1",&[&self.context,&t.to_be_bytes(),&p,&r.intent.digest(),&candidate,
                &(r.room as u64).to_be_bytes(),&(r.capacity as u64).to_be_bytes(),&(r.discovery_budget as u64).to_be_bytes(),
                &r.allowed.to_be_bytes(),&(r.depth as u64).to_be_bytes(),&(r.relocation_budget as u64).to_be_bytes()])
        }
        pub fn witness_message(msg:Hash,slot:u8,v:Verdict)->Hash{
            hash(b"HJC/unified/witness/v1",&[&msg,&[slot],&[v as u8]])
        }
        fn occupancy_digest(&self)->Hash{
            let mut bytes=Vec::new();
            for c in self.occupancy.slots(){match c{None=>bytes.push(0),Some(c)=>{bytes.push(1);bytes.extend(c.id());}}}
            hash(b"HJC/unified/occupancy/v1",&[&bytes])
        }
        pub fn submit(&mut self,r:Request)->Result<&Record,&'static str>{
            if r.receipts.len()>12 || r.intent.original().len()>rooms::MAX_INPUT_BYTES
                || r.intent.constraint.object.len()>rooms::MAX_INPUT_BYTES || r.intent.constraint.source.len()>rooms::MAX_INPUT_BYTES
                || r.depth>=nested::HOTELS || r.room>=rooms::MAX_ROOMS {return Err("request envelope out of bounds");}
            let customer=nested::Customer::new(&r.intent,r.allowed)?;
            // Each global slot maps to its local representation. Never admit into a room
            // that was not discovered and witnessed in this request.
            for k in 0..nested::CAPACITY {
                if r.allowed & (1u32<<k)!=0 && k%rooms::MAX_ROOMS!=r.room{return Err("mask exceeds witnessed room class");}
            }
            let(tick,previous)=self.checkpoint();tick.checked_add(1).ok_or("tick exhausted")?;
            let msg=self.message(&r);
            let authenticated=self.proposer.key.verify_strict(&msg,&r.proposal).is_ok();
            let mut seen=[false;3];let mut complete=true;let mut conflict=false;
            for w in &r.receipts {
                let k=w.slot as usize;
                if k>=3{complete=false;continue;}
                let valid=self.roots[k].key.verify_strict(&Self::witness_message(msg,w.slot,w.verdict),&w.signature).is_ok();
                if valid && w.verdict==Verdict::Conflict{conflict=true;}
                if seen[k] || !valid || w.verdict!=Verdict::Preserve{complete=false;}
                seen[k]=true;
            }
            let decision=if !authenticated{Decision::Hold}
                else if conflict{Decision::Conflict}
                else if !complete || !seen.iter().all(|x|*x) || Self::selected(&r).is_none(){Decision::Hold}
                else {match self.occupancy.admit(customer,r.depth,r.relocation_budget)?.decision{
                    nested::Decision::Admitted=>Decision::Admitted,nested::Decision::Duplicate=>Decision::Duplicate,
                    nested::Decision::Full=>Decision::Full,nested::Decision::NoPathInScope=>Decision::NoPath,
                    nested::Decision::BudgetExhausted=>Decision::Budget,
                }};
            let occupancy=self.occupancy_digest();
            let mut receipts=Vec::new();
            for w in &r.receipts{receipts.push(w.slot);receipts.push(w.verdict as u8);receipts.extend(w.signature.to_bytes());}
            let seal=hash(b"HJC/unified/event/v1",&[&msg,&r.proposal.to_bytes(),&receipts,&[decision as u8],&occupancy]);
            self.records.push(Record{tick,position:tick%PERIOD,body:SEQUENCE[(tick%12) as usize],request:r,decision,previous,occupancy,seal});
            Ok(self.records.last().unwrap())
        }
        // Full in-memory replay from registered roots and original request envelopes.
        // Externally retained expected head and length are necessary for rollback detection.
        pub fn verify(&self,expected_len:usize,expected_head:Hash)->bool{
            if self.records.len()!=expected_len || self.checkpoint().1!=expected_head{return false;}
            let mut replay=match Self::new(self.proposer.clone(),self.roots.clone(),self.session){Ok(h)=>h,Err(_)=>return false};
            for old in &self.records{
                let new=match replay.submit(old.request.clone()){Ok(r)=>r,Err(_)=>return false};
                if new.tick!=old.tick || new.position!=old.position || new.body!=old.body || new.previous!=old.previous
                    || new.decision!=old.decision || new.occupancy!=old.occupancy || new.seal!=old.seal{return false;}
            }
            replay.occupancy_digest()==self.occupancy_digest() && replay.checkpoint().1==expected_head
        }
    }
    #[cfg(test)]
    mod tests{
        use super::*;
        use ed25519_dalek::{Signer,SigningKey};
        fn fixture()->(Hotel,[SigningKey;4]){
            let k=[1,2,3,4].map(|x|SigningKey::from_bytes(&[x;32]));
            let root=|n:usize|Root{key:k[n].verifying_key(),ancestry:[(10+n) as u8;32]};
            (Hotel::new(root(0),[root(1),root(2),root(3)],[8;32]).unwrap(),k)
        }
        fn request(h:&Hotel,k:&[SigningKey;4],n:usize,allowed:u32,verdict:Verdict)->Request{
            let source=format!("source-{n}");
            let intent=Intent::new(format!("Preserve cinnamon {source}"),Constraint{action:Action::Preserve,object:"cinnamon".into(),source}).unwrap();
            let mut r=Request{intent,room:8,capacity:1000,discovery_budget:9,allowed,depth:2,relocation_budget:27,
                proposal:k[0].sign(b"placeholder"),receipts:Vec::new()};
            let msg=h.message(&r);r.proposal=k[0].sign(&msg);
            for slot in 0..3{r.receipts.push(Receipt{slot,verdict,signature:k[slot as usize+1].sign(&Hotel::witness_message(msg,slot,verdict))});}
            r
        }
        #[test] fn integrated_admission_and_replay(){
            let(mut h,k)=fixture();let r=request(&h,&k,0,1<<8,Verdict::Preserve);
            assert_eq!(h.submit(r).unwrap().decision,Decision::Admitted);
            assert_eq!(h.occupied(),1);assert!(h.verify(1,h.checkpoint().1));assert_eq!(h.referent(),(0,1));
        }
        #[test] fn disagreement_preserves_occupancy(){
            let(mut h,k)=fixture();let r=request(&h,&k,0,1<<8,Verdict::Conflict);
            assert_eq!(h.submit(r).unwrap().decision,Decision::Conflict);assert_eq!(h.occupied(),0);
        }
        #[test] fn missing_witness_holds(){
            let(mut h,k)=fixture();let mut r=request(&h,&k,0,1<<8,Verdict::Preserve);r.receipts.pop();
            assert_eq!(h.submit(r).unwrap().decision,Decision::Hold);assert_eq!(h.occupied(),0);
        }
        #[test] fn stale_receipt_holds(){
            let(mut h,k)=fixture();let r=request(&h,&k,0,1<<8,Verdict::Preserve);
            h.submit(r.clone()).unwrap();assert_eq!(h.submit(r).unwrap().decision,Decision::Hold);
            assert_eq!(h.occupied(),1);assert!(h.verify(2,h.checkpoint().1));
        }
        #[test] fn mask_cannot_escape_witnessed_class(){
            let(mut h,k)=fixture();let r=request(&h,&k,0,(1<<8)|1,Verdict::Preserve);
            assert!(h.submit(r).is_err());assert_eq!(h.occupied(),0);assert!(h.records().is_empty());
        }
        #[test] fn cross_hotel_relocation(){
            let(mut h,k)=fixture();let a=request(&h,&k,0,(1<<8)|(1<<17),Verdict::Preserve);
            h.submit(a).unwrap();let b=request(&h,&k,1,1<<8,Verdict::Preserve);
            assert_eq!(h.submit(b).unwrap().decision,Decision::Admitted);assert_eq!(h.occupied(),2);
            assert!(h.verify(2,h.checkpoint().1));
        }
        #[test] fn external_checkpoint_and_mutation(){
            let(mut h,k)=fixture();let r=request(&h,&k,0,1<<8,Verdict::Preserve);h.submit(r).unwrap();
            let head=h.checkpoint().1;assert!(!h.verify(0,head));assert!(!h.verify(1,[0;32]));
            h.records[0].decision=Decision::Conflict;assert!(!h.verify(1,head));
        }
        #[test] fn undiscovered_room_holds(){
            let(mut h,k)=fixture();let mut r=request(&h,&k,0,1<<8,Verdict::Preserve);r.discovery_budget=8;
            let msg=h.message(&r);r.proposal=k[0].sign(&msg);
            for w in &mut r.receipts{w.signature=k[w.slot as usize+1].sign(&Hotel::witness_message(msg,w.slot,w.verdict));}
            assert_eq!(h.submit(r).unwrap().decision,Decision::Hold);assert_eq!(h.occupied(),0);
        }
    }
}

// HJC-010 — single-writer durable journal prototype. No external action authority.
pub mod journal {
    use super::*;
    use std::{fs::{File,OpenOptions},io::{self,Read,Write},path::Path};
    const MAGIC:&[u8;8]=b"HJCJ001\n";
    pub const MAX_PAYLOAD:usize=256*1024;
    #[derive(Clone,Copy,Debug,PartialEq,Eq)]
    pub enum Fault { Header, Truncated, Oversize, Sequence, Seal, Io, Poisoned }
    #[derive(Clone,Debug,PartialEq,Eq)]
    pub struct Frame {pub tick:u64,pub previous:Hash,pub payload:Vec<u8>,pub seal:Hash}
    fn seal(tick:u64,previous:Hash,payload:&[u8])->Hash{
        hash(b"HJC/journal/frame/v1",&[&tick.to_be_bytes(),&previous,payload])
    }
    fn exact<R:Read>(r:&mut R,b:&mut [u8])->Result<(),Fault>{
        r.read_exact(b).map_err(|e|if e.kind()==io::ErrorKind::UnexpectedEof{Fault::Truncated}else{Fault::Io})
    }
    pub fn scan<R:Read>(mut r:R,mut visit:impl FnMut(Frame))->Result<(u64,Hash),Fault>{
        let mut magic=[0;8];exact(&mut r,&mut magic)?;
        if &magic!=MAGIC{return Err(Fault::Header);}
        let mut tick=0u64;let mut head=[0;32];
        loop {
            let mut len=[0;4];
            match r.read(&mut len[..1]){Ok(0)=>return Ok((tick,head)),Ok(1)=>{},Ok(_)=>unreachable!(),Err(_)=>return Err(Fault::Io)}
            exact(&mut r,&mut len[1..])?;
            let n=u32::from_be_bytes(len) as usize;
            if n>MAX_PAYLOAD{return Err(Fault::Oversize);}
            let mut t=[0;8];let mut previous=[0;32];let mut digest=[0;32];
            exact(&mut r,&mut t)?;exact(&mut r,&mut previous)?;
            let mut payload=vec![0;n];exact(&mut r,&mut payload)?;exact(&mut r,&mut digest)?;
            if u64::from_be_bytes(t)!=tick || previous!=head{return Err(Fault::Sequence);}
            if digest!=seal(tick,head,&payload){return Err(Fault::Seal);}
            visit(Frame{tick,previous,payload,seal:digest});
            tick=tick.checked_add(1).ok_or(Fault::Sequence)?;head=digest;
        }
    }
    pub struct Journal {file:File,tick:u64,head:Hash,poisoned:bool}
    impl Journal {
        // Caller must provide exclusive writer custody. No concurrent open or path replacement.
        pub fn create(path:&Path)->Result<Self,Fault>{
            let mut file=OpenOptions::new().write(true).append(true).create_new(true).open(path).map_err(|_|Fault::Io)?;
            file.write_all(MAGIC).and_then(|_|file.sync_all()).map_err(|_|Fault::Io)?;
            Ok(Self{file,tick:0,head:[0;32],poisoned:false})
        }
        pub fn open(path:&Path)->Result<Self,Fault>{
            let reader=File::open(path).map_err(|_|Fault::Io)?;
            let(tick,head)=scan(reader,|_|{})?;
            let file=OpenOptions::new().append(true).open(path).map_err(|_|Fault::Io)?;
            Ok(Self{file,tick,head,poisoned:false})
        }
        pub fn checkpoint(&self)->(u64,Hash){(self.tick,self.head)}
        pub fn append(&mut self,payload:&[u8])->Result<Hash,Fault>{
            if self.poisoned{return Err(Fault::Poisoned);}
            if payload.len()>MAX_PAYLOAD{return Err(Fault::Oversize);}
            let next=self.tick.checked_add(1).ok_or(Fault::Sequence)?;
            let digest=seal(self.tick,self.head,payload);
            let mut bytes=Vec::with_capacity(76+payload.len());
            bytes.extend((payload.len() as u32).to_be_bytes());bytes.extend(self.tick.to_be_bytes());
            bytes.extend(self.head);bytes.extend(payload);bytes.extend(digest);
            self.poisoned=true;
            self.file.write_all(&bytes).and_then(|_|self.file.sync_all()).map_err(|_|Fault::Io)?;
            self.tick=next;self.head=digest;self.poisoned=false;Ok(digest)
        }
    }
    #[cfg(test)]
    mod tests{
        use super::*;
        fn bytes(payload:&[u8])->Vec<u8>{
            let mut b=MAGIC.to_vec();b.extend((payload.len() as u32).to_be_bytes());b.extend(0u64.to_be_bytes());
            b.extend([0;32]);b.extend(payload);b.extend(seal(0,[0;32],payload));b
        }
        #[test] fn valid_frame(){let b=bytes(b"cinnamon");let mut count=0;let result=scan(&b[..],|f|{count+=1;assert_eq!(f.payload,b"cinnamon");}).unwrap();assert_eq!(count,1);assert_eq!(result.0,1);}
        #[test] fn clean_empty(){assert_eq!(scan(&MAGIC[..],|_|{}),Ok((0,[0;32])));}
        #[test] fn all_partial_frame_boundaries(){let b=bytes(b"cinnamon");for n in 9..b.len(){assert_eq!(scan(&b[..n],|_|{}),Err(Fault::Truncated));}}
        #[test] fn mutation(){let mut b=bytes(b"cinnamon");b[52]^=1;assert_eq!(scan(&b[..],|_|{}),Err(Fault::Seal));}
        #[test] fn wrong_tick(){let mut b=bytes(b"cinnamon");b[19]=1;assert_eq!(scan(&b[..],|_|{}),Err(Fault::Sequence));}
        #[test] fn oversized(){let mut b=MAGIC.to_vec();b.extend(((MAX_PAYLOAD+1) as u32).to_be_bytes());assert_eq!(scan(&b[..],|_|{}),Err(Fault::Oversize));}
        #[test] fn wrong_header(){assert_eq!(scan(&b"BADMAGIC"[..],|_|{}),Err(Fault::Header));}
        #[test] fn file_restart(){
            let p=std::env::temp_dir().join(format!("hjc010-{}-{:?}.journal",std::process::id(),std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));
            let mut j=Journal::create(&p).unwrap();j.append(b"cinnamon").unwrap();let first=j.checkpoint();drop(j);
            let mut j=Journal::open(&p).unwrap();assert_eq!(j.checkpoint(),first);j.append(b"source-42").unwrap();let second=j.checkpoint();drop(j);
            assert_eq!(Journal::open(&p).unwrap().checkpoint(),second);std::fs::remove_file(p).unwrap();
        }
    }
}
