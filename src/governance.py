from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

class VoteType(Enum):
    YES = 'yes'
    NO = 'no'
    ABSTAIN = 'abstain'

class ProposalStatus(Enum):
    ACTIVE = 'active'
    EXECUTED = 'executed' 
    DEFEATED = 'defeated'
    EXPIRED = 'expired'

class Proposal:
    def __init__(self, id: str, title: str, description: str, 
                 proposer: str, voting_period_days: int = 7):
        self.id = id
        self.title = title
        self.description = description
        self.proposer = proposer
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(days=voting_period_days)
        self.votes: Dict[str, VoteType] = {}
        self.status = ProposalStatus.ACTIVE
        self.execution_data: Optional[str] = None

    def cast_vote(self, voter: str, vote: VoteType) -> bool:
        if self.status != ProposalStatus.ACTIVE:
            return False
        if datetime.now() > self.expires_at:
            self.status = ProposalStatus.EXPIRED
            return False
            
        self.votes[voter] = vote
        return True

    def get_vote_counts(self) -> Dict[VoteType, int]:
        counts = {vote_type: 0 for vote_type in VoteType}
        for vote in self.votes.values():
            counts[vote] += 1
        return counts

    def can_execute(self) -> bool:
        if self.status != ProposalStatus.ACTIVE:
            return False
            
        vote_counts = self.get_vote_counts()
        total_votes = sum(vote_counts.values())
        
        if total_votes == 0:
            return False
            
        yes_ratio = vote_counts[VoteType.YES] / total_votes
        return yes_ratio > 0.5

    def execute(self, execution_data: str) -> bool:
        if not self.can_execute():
            return False
            
        self.execution_data = execution_data
        self.status = ProposalStatus.EXECUTED
        return True

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}

    def create_proposal(self, id: str, title: str, 
                       description: str, proposer: str) -> Proposal:
        proposal = Proposal(id, title, description, proposer)
        self.proposals[id] = proposal
        return proposal

    def get_proposal(self, id: str) -> Optional[Proposal]:
        return self.proposals.get(id)

    def get_active_proposals(self) -> List[Proposal]:
        return [p for p in self.proposals.values() 
                if p.status == ProposalStatus.ACTIVE]

    def vote_on_proposal(self, proposal_id: str, 
                        voter: str, vote: VoteType) -> bool:
        proposal = self.get_proposal(proposal_id)
        if not proposal:
            return False
        return proposal.cast_vote(voter, vote)

    def execute_proposal(self, proposal_id: str, 
                        execution_data: str) -> bool:
        proposal = self.get_proposal(proposal_id)
        if not proposal:
            return False
        return proposal.execute(execution_data)
