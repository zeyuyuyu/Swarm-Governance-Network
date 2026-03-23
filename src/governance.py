from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional

class ProposalStatus(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active' 
    PASSED = 'passed'
    FAILED = 'failed'
    EXECUTED = 'executed'

@dataclass
class Vote:
    voter: str
    weight: float
    approve: bool
    timestamp: datetime

@dataclass 
class Proposal:
    id: str
    title: str
    description: str
    proposer: str
    status: ProposalStatus
    created_at: datetime
    voting_ends_at: datetime
    votes: Dict[str, Vote]
    min_approval_threshold: float
    execution_delay: timedelta

    def calculate_results(self) -> tuple[float, float]:
        approve_weight = sum(v.weight for v in self.votes.values() if v.approve)
        reject_weight = sum(v.weight for v in self.votes.values() if not v.approve)
        total_weight = approve_weight + reject_weight
        
        if total_weight == 0:
            return 0.0, 0.0
            
        return approve_weight/total_weight, reject_weight/total_weight

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.user_weights: Dict[str, float] = {}
        self.default_voting_period = timedelta(days=7)
        self.default_execution_delay = timedelta(days=2)
    
    def create_proposal(self, id: str, title: str, description: str,
                        proposer: str, min_approval: float = 0.5) -> Proposal:
        if id in self.proposals:
            raise ValueError(f'Proposal {id} already exists')
            
        proposal = Proposal(
            id=id,
            title=title, 
            description=description,
            proposer=proposer,
            status=ProposalStatus.DRAFT,
            created_at=datetime.now(),
            voting_ends_at=datetime.now() + self.default_voting_period,
            votes={},
            min_approval_threshold=min_approval,
            execution_delay=self.default_execution_delay
        )
        
        self.proposals[id] = proposal
        return proposal

    def cast_vote(self, proposal_id: str, voter: str, approve: bool) -> None:
        if proposal_id not in self.proposals:
            raise ValueError(f'Invalid proposal ID: {proposal_id}')
            
        proposal = self.proposals[proposal_id]
        
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f'Proposal {proposal_id} is not active')
            
        if datetime.now() > proposal.voting_ends_at:
            raise ValueError(f'Voting period has ended for proposal {proposal_id}')

        weight = self.user_weights.get(voter, 1.0)
        vote = Vote(voter=voter, weight=weight, approve=approve, 
                   timestamp=datetime.now())
        proposal.votes[voter] = vote

    def update_proposal_status(self, proposal_id: str) -> None:
        proposal = self.proposals[proposal_id]
        now = datetime.now()

        if proposal.status == ProposalStatus.ACTIVE and now > proposal.voting_ends_at:
            approve_ratio, _ = proposal.calculate_results()
            
            if approve_ratio >= proposal.min_approval_threshold:
                proposal.status = ProposalStatus.PASSED
            else:
                proposal.status = ProposalStatus.FAILED

        elif (proposal.status == ProposalStatus.PASSED and 
              now > proposal.voting_ends_at + proposal.execution_delay):
            proposal.status = ProposalStatus.EXECUTED

    def get_active_proposals(self) -> List[Proposal]:
        return [p for p in self.proposals.values() 
                if p.status == ProposalStatus.ACTIVE]

    def set_user_weight(self, user: str, weight: float) -> None:
        if weight < 0:
            raise ValueError('Weight cannot be negative')
        self.user_weights[user] = weight

    def get_user_weight(self, user: str) -> float:
        return self.user_weights.get(user, 1.0)
