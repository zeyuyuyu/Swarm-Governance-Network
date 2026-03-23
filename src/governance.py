from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

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
        self.member_weights: Dict[str, float] = {}
        self.voting_period = timedelta(days=7)
        self.approval_threshold = 0.66  # 66% majority required

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
        proposal.end_time = proposal.start_time + self.voting_period

    def cast_vote(self, proposal_id: str, voter: str, support: bool) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError('Proposal is not active')
            
        if datetime.now() > proposal.end_time:
            raise ValueError('Voting period has ended')

        voter_weight = self.member_weights.get(voter, 1.0)
        
        # Remove previous vote if exists
        if voter in proposal.voters:
            old_weight = proposal.voters[voter]
            if proposal.voters[voter] > 0:
                proposal.votes_for -= old_weight
            else:
                proposal.votes_against -= abs(old_weight)

        # Add new vote
        if support:
            proposal.votes_for += voter_weight
            proposal.voters[voter] = voter_weight
        else:
            proposal.votes_against += voter_weight
            proposal.voters[voter] = -voter_weight

    def check_proposal_status(self, proposal_id: str) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')

        if proposal.status != ProposalStatus.ACTIVE:
            return

        if datetime.now() <= proposal.end_time:
            return

        total_votes = proposal.votes_for + proposal.votes_against
        if total_votes == 0:
            proposal.status = ProposalStatus.FAILED
            return

        approval_rate = proposal.votes_for / total_votes
        if approval_rate >= self.approval_threshold:
            proposal.status = ProposalStatus.PASSED
        else:
            proposal.status = ProposalStatus.FAILED

    def execute_proposal(self, proposal_id: str) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')

        if proposal.status != ProposalStatus.PASSED:
            raise ValueError('Proposal must be passed before execution')

        # Execute proposal logic here
        proposal.status = ProposalStatus.EXECUTED

    def set_member_weight(self, member: str, weight: float) -> None:
        if weight < 0:
            raise ValueError('Weight cannot be negative')
        self.member_weights[member] = weight

    def get_proposal_results(self, proposal_id: str) -> dict:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')

        total_votes = proposal.votes_for + proposal.votes_against
        approval_rate = proposal.votes_for / total_votes if total_votes > 0 else 0

        return {
            'id': proposal.id,
            'status': proposal.status.value,
            'votes_for': proposal.votes_for,
            'votes_against': proposal.votes_against,
            'approval_rate': approval_rate,
            'total_votes': total_votes
        }