import datetime
import hashlib
import json
from typing import List, Dict

class Proposal:
    def __init__(self, title: str, description: str, creator: str, start_time: datetime.datetime, end_time: datetime.datetime):
        self.title = title
        self.description = description
        self.creator = creator
        self.start_time = start_time
        self.end_time = end_time
        self.votes = {}
        self.result = None

    def add_vote(self, voter: str, vote: bool):
        self.votes[voter] = vote

    def calculate_result(self):
        yes_votes = sum(1 for vote in self.votes.values() if vote)
        no_votes = sum(1 for vote in self.votes.values() if not vote)
        self.result = yes_votes > no_votes

class VotingSystem:
    def __init__(self, members: List[str]):
        self.members = members
        self.proposals: Dict[str, Proposal] = {}

    def create_proposal(self, title: str, description: str, creator: str, start_time: datetime.datetime, end_time: datetime.datetime) -> Proposal:
        proposal = Proposal(title, description, creator, start_time, end_time)
        self.proposals[proposal.title] = proposal
        return proposal

    def vote_on_proposal(self, proposal_title: str, voter: str, vote: bool):
        if proposal_title in self.proposals:
            self.proposals[proposal_title].add_vote(voter, vote)

    def finalize_proposal(self, proposal_title: str):
        if proposal_title in self.proposals:
            self.proposals[proposal_title].calculate_result()

    def get_proposal_result(self, proposal_title: str) -> bool:
        if proposal_title in self.proposals:
            return self.proposals[proposal_title].result
        return False

    def get_all_proposals(self) -> List[Proposal]:
        return list(self.proposals.values())
