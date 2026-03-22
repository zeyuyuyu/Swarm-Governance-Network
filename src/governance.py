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
    def __init__(self, id: str, title: str, description: str, creator: str):
        self.id = id
        self.title = title
        self.description = description
        self.creator = creator
        self.status = ProposalStatus.DRAFT
        self.votes_for = 0
        self.votes_against = 0
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.voters: Dict[str, float] = {}

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.stake_weights: Dict[str, float] = {}
        self.proposal_duration = timedelta(days=7)
        self.quorum_threshold = 0.4  # 40% participation required
        self.pass_threshold = 0.6    # 60% yes votes required
    
    def create_proposal(self, id: str, title: str, description: str, creator: str) -> Proposal:
        if id in self.proposals:
            raise ValueError(f'Proposal with ID {id} already exists')
        
        proposal = Proposal(id, title, description, creator)
        self.proposals[id] = proposal
        return proposal

    def activate_proposal(self, proposal_id: str) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        proposal.status = ProposalStatus.ACTIVE
        proposal.start_time = datetime.now()
        proposal.end_time = proposal.start_time + self.proposal_duration

    def cast_vote(self, proposal_id: str, voter: str, vote_for: bool) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f'Proposal {proposal_id} is not active')
            
        if datetime.now() > proposal.end_time:
            raise ValueError(f'Proposal {proposal_id} voting period has ended')

        voter_weight = self.stake_weights.get(voter, 0)
        if voter_weight == 0:
            raise ValueError(f'Voter {voter} has no voting weight')

        # Remove previous vote if exists
        if voter in proposal.voters:
            old_weight = proposal.voters[voter]
            if vote_for:
                proposal.votes_for -= old_weight
            else:
                proposal.votes_against -= old_weight

        # Record new vote
        proposal.voters[voter] = voter_weight
        if vote_for:
            proposal.votes_for += voter_weight
        else:
            proposal.votes_against += voter_weight

    def update_stake_weight(self, address: str, weight: float) -> None:
        if weight < 0:
            raise ValueError('Stake weight cannot be negative')
        self.stake_weights[address] = weight

    def finalize_proposal(self, proposal_id: str) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')

        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f'Proposal {proposal_id} is not active')

        if datetime.now() < proposal.end_time:
            raise ValueError(f'Proposal {proposal_id} voting period has not ended')

        total_votes = proposal.votes_for + proposal.votes_against
        total_possible_votes = sum(self.stake_weights.values())

        # Check quorum
        if total_votes / total_possible_votes < self.quorum_threshold:
            proposal.status = ProposalStatus.FAILED
            return

        # Check if proposal passed
        if proposal.votes_for / total_votes >= self.pass_threshold:
            proposal.status = ProposalStatus.PASSED
        else:
            proposal.status = ProposalStatus.FAILED

    def get_proposal_status(self, proposal_id: str) -> ProposalStatus:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
        return proposal.status

    def get_vote_results(self, proposal_id: str) -> Dict:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')

        total_votes = proposal.votes_for + proposal.votes_against
        return {
            'votes_for': proposal.votes_for,
            'votes_against': proposal.votes_against,
            'total_votes': total_votes,
            'participation_rate': total_votes / sum(self.stake_weights.values()) if self.stake_weights else 0
        }