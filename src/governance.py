from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Vote:
    voter: str
    proposal_id: int
    vote_weight: float
    timestamp: datetime
    choice: bool  # True for yes, False for no

@dataclass 
class Proposal:
    id: int
    title: str
    description: str
    creator: str
    start_time: datetime
    end_time: datetime
    min_weight_required: float
    votes: List[Vote]
    
class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[int, Proposal] = {}
        self.delegations: Dict[str, str] = {}  # voter -> delegate
        self.voting_weights: Dict[str, float] = {}
        self._next_proposal_id: int = 0
        
    def create_proposal(self, title: str, description: str, creator: str,
                       start_time: datetime, end_time: datetime,
                       min_weight_required: float = 0.0) -> int:
        proposal_id = self._next_proposal_id
        self._next_proposal_id += 1
        
        self.proposals[proposal_id] = Proposal(
            id=proposal_id,
            title=title,
            description=description,
            creator=creator,
            start_time=start_time,
            end_time=end_time,
            min_weight_required=min_weight_required,
            votes=[]
        )
        return proposal_id
    
    def delegate_vote(self, voter: str, delegate: str) -> bool:
        if voter == delegate:
            return False
        self.delegations[voter] = delegate
        return True
        
    def get_effective_weight(self, voter: str) -> float:
        base_weight = self.voting_weights.get(voter, 1.0)
        delegated_weight = 0.0
        
        # Add weights from all accounts delegating to this voter
        for delegator, delegate in self.delegations.items():
            if delegate == voter:
                delegated_weight += self.voting_weights.get(delegator, 1.0)
                
        return base_weight + delegated_weight
    
    def cast_vote(self, voter: str, proposal_id: int, choice: bool) -> bool:
        if proposal_id not in self.proposals:
            return False
            
        proposal = self.proposals[proposal_id]
        now = datetime.now()
        
        if now < proposal.start_time or now > proposal.end_time:
            return False
            
        # Check if voter already voted
        for vote in proposal.votes:
            if vote.voter == voter:
                return False
                
        # Get effective voting weight including delegations
        weight = self.get_effective_weight(voter)
        
        # Create and record the vote
        vote = Vote(
            voter=voter,
            proposal_id=proposal_id,
            vote_weight=weight,
            timestamp=now,
            choice=choice
        )
        proposal.votes.append(vote)
        return True
        
    def get_proposal_result(self, proposal_id: int) -> Optional[Dict]:
        if proposal_id not in self.proposals:
            return None
            
        proposal = self.proposals[proposal_id]
        yes_weight = 0.0
        no_weight = 0.0
        
        for vote in proposal.votes:
            if vote.choice:
                yes_weight += vote.vote_weight
            else:
                no_weight += vote.vote_weight
                
        total_weight = yes_weight + no_weight
        
        if total_weight < proposal.min_weight_required:
            status = 'Insufficient Participation'
        elif yes_weight > no_weight:
            status = 'Passed'
        else:
            status = 'Rejected'
            
        return {
            'proposal_id': proposal_id,
            'yes_weight': yes_weight,
            'no_weight': no_weight,
            'total_weight': total_weight,
            'status': status
        }
