import hashlib
import json
from typing import List

class Vote:
    def __init__(self, proposal_id: str, voter_address: str, vote_value: bool):
        self.proposal_id = proposal_id
        self.voter_address = voter_address
        self.vote_value = vote_value
        self.timestamp = datetime.now().isoformat()
        self.vote_hash = self.calculate_vote_hash()

    def calculate_vote_hash(self) -> str:
        vote_data = {
            'proposal_id': self.proposal_id,
            'voter_address': self.voter_address,
            'vote_value': self.vote_value,
            'timestamp': self.timestamp
        }
        return hashlib.sha256(json.dumps(vote_data).encode()).hexdigest()

class Proposal:
    def __init__(self, proposal_id: str, description: str, start_time: str, end_time: str):
        self.proposal_id = proposal_id
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.votes: List[Vote] = []

    def add_vote(self, vote: Vote):
        self.votes.append(vote)

    def get_vote_count(self, vote_value: bool) -> int:
        return sum(1 for v in self.votes if v.vote_value == vote_value)

    def get_winning_option(self) -> bool:
        yes_votes = self.get_vote_count(True)
        no_votes = self.get_vote_count(False)
        return yes_votes > no_votes

class GovernanceEngine:
    def __init__(self):
        self.proposals: List[Proposal] = []

    def create_proposal(self, proposal_id: str, description: str, start_time: str, end_time: str) -> Proposal:
        proposal = Proposal(proposal_id, description, start_time, end_time)
        self.proposals.append(proposal)
        return proposal

    def cast_vote(self, proposal_id: str, voter_address: str, vote_value: bool) -> Vote:
        proposal = next((p for p in self.proposals if p.proposal_id == proposal_id), None)
        if not proposal:
            raise ValueError(f'Proposal with ID {proposal_id} not found.')
        vote = Vote(proposal_id, voter_address, vote_value)
        proposal.add_vote(vote)
        return vote

    def get_proposal_result(self, proposal_id: str) -> bool:
        proposal = next((p for p in self.proposals if p.proposal_id == proposal_id), None)
        if not proposal:
            raise ValueError(f'Proposal with ID {proposal_id} not found.')
        return proposal.get_winning_option()
