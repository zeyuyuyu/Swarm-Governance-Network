from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime, timedelta

class ProposalStatus(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active' 
    PASSED = 'passed'
    FAILED = 'failed'
    EXECUTED = 'executed'

class Proposal:
    def __init__(self, id: str, title: str, description: str, creator: str, 
                 voting_period_days: int = 7):
        self.id = id
        self.title = title
        self.description = description
        self.creator = creator
        self.status = ProposalStatus.DRAFT
        self.created_at = datetime.now()
        self.voting_end = self.created_at + timedelta(days=voting_period_days)
        self.votes_for: Dict[str, float] = {}
        self.votes_against: Dict[str, float] = {}
        
    def get_vote_tallies(self) -> tuple[float, float]:
        return (sum(self.votes_for.values()), sum(self.votes_against.values()))

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.stake_weights: Dict[str, float] = {}
        self.quorum_threshold = 0.4  # 40% of total stake needed
        self.pass_threshold = 0.6    # 60% yes votes needed to pass
        
    def register_stake(self, address: str, stake_amount: float) -> None:
        """Register or update a participant's voting weight based on stake"""
        self.stake_weights[address] = stake_amount
        
    def create_proposal(self, id: str, title: str, description: str, 
                       creator: str) -> Proposal:
        """Create a new governance proposal"""
        if id in self.proposals:
            raise ValueError(f'Proposal with ID {id} already exists')
            
        proposal = Proposal(id, title, description, creator)
        self.proposals[id] = proposal
        return proposal
        
    def activate_proposal(self, proposal_id: str) -> None:
        """Move proposal from draft to active voting state"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        proposal.status = ProposalStatus.ACTIVE
        
    def cast_vote(self, proposal_id: str, voter: str, support: bool) -> None:
        """Cast a weighted vote on an active proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f'Proposal {proposal_id} is not active')
            
        if datetime.now() > proposal.voting_end:
            raise ValueError(f'Voting period has ended for proposal {proposal_id}')
            
        weight = self.stake_weights.get(voter, 0)
        if weight == 0:
            raise ValueError(f'Voter {voter} has no stake weight')
            
        if support:
            proposal.votes_for[voter] = weight
        else:
            proposal.votes_against[voter] = weight
            
    def process_proposal(self, proposal_id: str) -> None:
        """Process proposal after voting period to determine outcome"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f'Proposal {proposal_id} is not active')
            
        if datetime.now() < proposal.voting_end:
            raise ValueError(f'Voting period still active for {proposal_id}')
            
        total_stake = sum(self.stake_weights.values())
        votes_for, votes_against = proposal.get_vote_tallies()
        total_votes = votes_for + votes_against
        
        # Check quorum
        if total_votes < (total_stake * self.quorum_threshold):
            proposal.status = ProposalStatus.FAILED
            return
            
        # Check pass threshold
        if votes_for / total_votes >= self.pass_threshold:
            proposal.status = ProposalStatus.PASSED
        else:
            proposal.status = ProposalStatus.FAILED
            
    def execute_proposal(self, proposal_id: str) -> None:
        """Mark proposal as executed after implementation"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.PASSED:
            raise ValueError(f'Proposal {proposal_id} has not passed')
            
        proposal.status = ProposalStatus.EXECUTED