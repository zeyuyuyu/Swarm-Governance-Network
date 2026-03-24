import hashlib
import json
from typing import List, Tuple

class Proposal:
    def __init__(self, title: str, description: str, vote_start: int, vote_end: int):
        self.title = title
        self.description = description
        self.vote_start = vote_start
        self.vote_end = vote_end
        self.votes = {}

    def add_vote(self, voter_address: str, vote: bool) -> None:
        self.votes[voter_address] = vote

    def get_vote_count(self) -> Tuple[int, int]:
        yes_votes = 0
        no_votes = 0
        for vote in self.votes.values():
            if vote:
                yes_votes += 1
            else:
                no_votes += 1
        return yes_votes, no_votes

    def is_active(self, current_time: int) -> bool:
        return self.vote_start <= current_time <= self.vote_end

class VotingSystem:
    def __init__(self, initial_voters: List[str]):
        self.proposals = []
        self.voter_addresses = set(initial_voters)

    def add_proposal(self, proposal: Proposal) -> None:
        self.proposals.append(proposal)

    def cast_vote(self, voter_address: str, proposal_index: int, vote: bool) -> None:
        if voter_address in self.voter_addresses:
            self.proposals[proposal_index].add_vote(voter_address, vote)

    def get_proposal_results(self, proposal_index: int) -> Tuple[int, int]:
        return self.proposals[proposal_index].get_vote_count()

    def get_active_proposals(self, current_time: int) -> List[Proposal]:
        return [p for p in self.proposals if p.is_active(current_time)]

    def add_voter(self, voter_address: str) -> None:
        self.voter_addresses.add(voter_address)

    def remove_voter(self, voter_address: str) -> None:
        self.voter_addresses.remove(voter_address)
