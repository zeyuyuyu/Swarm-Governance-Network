from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ProposalState(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active' 
    PASSED = 'passed'
    FAILED = 'failed'
    EXECUTED = 'executed'
    CANCELLED = 'cancelled'

class Proposal:
    def __init__(self, id: str, title: str, description: str, proposer: str):
        self.id = id
        self.title = title
        self.description = description
        self.proposer = proposer
        self.state = ProposalState.DRAFT
        self.votes_for = 0
        self.votes_against = 0
        self.created_at = datetime.now()
        self.voting_ends_at: Optional[datetime] = None
        self.executed_at: Optional[datetime] = None
        self.votes: Dict[str, bool] = {}  # voter_address -> vote

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.voting_period = timedelta(days=7)
        self.quorum_threshold = 100  # Minimum votes needed
        self.pass_threshold = 0.5  # >50% votes needed to pass
        
    def create_proposal(self, id: str, title: str, description: str, proposer: str) -> Proposal:
        if id in self.proposals:
            raise ValueError(f'Proposal {id} already exists')
            
        proposal = Proposal(id, title, description, proposer)
        self.proposals[id] = proposal
        return proposal
        
    def activate_proposal(self, id: str) -> None:
        proposal = self.proposals.get(id)
        if not proposal:
            raise ValueError(f'Proposal {id} not found')
            
        if proposal.state != ProposalState.DRAFT:
            raise ValueError(f'Proposal {id} is not in DRAFT state')
            
        proposal.state = ProposalState.ACTIVE
        proposal.voting_ends_at = datetime.now() + self.voting_period
        
    def vote(self, id: str, voter: str, support: bool) -> None:
        proposal = self.proposals.get(id)
        if not proposal:
            raise ValueError(f'Proposal {id} not found')
            
        if proposal.state != ProposalState.ACTIVE:
            raise ValueError(f'Proposal {id} is not ACTIVE')
            
        if datetime.now() > proposal.voting_ends_at:
            raise ValueError(f'Voting period has ended for proposal {id}')
            
        if voter in proposal.votes:
            # Remove old vote
            old_vote = proposal.votes[voter]
            if old_vote:
                proposal.votes_for -= 1
            else:
                proposal.votes_against -= 1
                
        # Add new vote
        proposal.votes[voter] = support
        if support:
            proposal.votes_for += 1
        else:
            proposal.votes_against += 1
            
    def process_proposal(self, id: str) -> None:
        proposal = self.proposals.get(id)
        if not proposal:
            raise ValueError(f'Proposal {id} not found')
            
        if proposal.state != ProposalState.ACTIVE:
            raise ValueError(f'Proposal {id} is not ACTIVE')
            
        if datetime.now() < proposal.voting_ends_at:
            raise ValueError(f'Voting period has not ended for proposal {id}')
            
        total_votes = proposal.votes_for + proposal.votes_against
        
        if total_votes < self.quorum_threshold:
            proposal.state = ProposalState.FAILED
            return
            
        vote_percentage = proposal.votes_for / total_votes
        if vote_percentage > self.pass_threshold:
            proposal.state = ProposalState.PASSED
        else:
            proposal.state = ProposalState.FAILED
            
    def execute_proposal(self, id: str) -> None:
        proposal = self.proposals.get(id)
        if not proposal:
            raise ValueError(f'Proposal {id} not found')
            
        if proposal.state != ProposalState.PASSED:
            raise ValueError(f'Proposal {id} has not PASSED')
            
        # Execute proposal logic here
        proposal.state = ProposalState.EXECUTED
        proposal.executed_at = datetime.now()
        
    def cancel_proposal(self, id: str, canceller: str) -> None:
        proposal = self.proposals.get(id)
        if not proposal:
            raise ValueError(f'Proposal {id} not found')
            
        if proposal.state in [ProposalState.EXECUTED, ProposalState.CANCELLED]:
            raise ValueError(f'Proposal {id} cannot be cancelled')
            
        if canceller != proposal.proposer:
            raise ValueError(f'Only proposer can cancel proposal {id}')
            
        proposal.state = ProposalState.CANCELLED
        
    def get_active_proposals(self) -> List[Proposal]:
        return [p for p in self.proposals.values() if p.state == ProposalState.ACTIVE]
        
    def get_proposal(self, id: str) -> Optional[Proposal]:
        return self.proposals.get(id)