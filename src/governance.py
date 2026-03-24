from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ProposalState(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active' 
    PASSED = 'passed'
    FAILED = 'failed'
    EXECUTED = 'executed'
    CANCELED = 'canceled'

class Proposal:
    def __init__(self, id: str, title: str, description: str, creator: str):
        self.id = id
        self.title = title
        self.description = description
        self.creator = creator
        self.state = ProposalState.DRAFT
        self.votes_for = 0
        self.votes_against = 0
        self.created_at = datetime.now()
        self.voting_ends_at: Optional[datetime] = None
        self.executed_at: Optional[datetime] = None
        self.min_voting_power = 100  # Configurable threshold
        self.required_quorum = 0.4  # 40% participation required

    def activate(self) -> bool:
        if self.state != ProposalState.DRAFT:
            return False
        self.state = ProposalState.ACTIVE
        self.voting_ends_at = datetime.now() + timedelta(days=7)
        return True

    def vote(self, voter: str, voting_power: int, support: bool) -> bool:
        if self.state != ProposalState.ACTIVE:
            return False
        if datetime.now() > self.voting_ends_at:
            return False
            
        if support:
            self.votes_for += voting_power
        else:
            self.votes_against += voting_power
        return True

    def finalize(self, total_voting_power: int) -> bool:
        if self.state != ProposalState.ACTIVE:
            return False
        if datetime.now() < self.voting_ends_at:
            return False

        total_votes = self.votes_for + self.votes_against
        participation = total_votes / total_voting_power

        if participation < self.required_quorum:
            self.state = ProposalState.FAILED
            return True

        if self.votes_for > self.votes_against:
            self.state = ProposalState.PASSED
        else:
            self.state = ProposalState.FAILED
        return True

    def execute(self) -> bool:
        if self.state != ProposalState.PASSED:
            return False
        self.state = ProposalState.EXECUTED
        self.executed_at = datetime.now()
        return True

    def cancel(self) -> bool:
        if self.state in [ProposalState.EXECUTED, ProposalState.CANCELED]:
            return False
        self.state = ProposalState.CANCELED
        return True

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.next_proposal_id = 1
        self.total_voting_power = 1000  # Example fixed total

    def create_proposal(self, title: str, description: str, creator: str) -> str:
        proposal_id = str(self.next_proposal_id)
        self.next_proposal_id += 1
        
        proposal = Proposal(proposal_id, title, description, creator)
        self.proposals[proposal_id] = proposal
        return proposal_id

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        return self.proposals.get(proposal_id)

    def get_active_proposals(self) -> List[Proposal]:
        return [p for p in self.proposals.values() if p.state == ProposalState.ACTIVE]

    def process_expired_proposals(self):
        for proposal in self.get_active_proposals():
            if datetime.now() > proposal.voting_ends_at:
                proposal.finalize(self.total_voting_power)
