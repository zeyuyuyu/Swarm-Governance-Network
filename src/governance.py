import datetime
import hashlib
import json

class Proposal:
    def __init__(self, title, description, author, start_time, end_time):
        self.title = title
        self.description = description
        self.author = author
        self.start_time = start_time
        self.end_time = end_time
        self.votes = {}
        self.hash = self.compute_hash()

    def compute_hash(self):
        data = {
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def add_vote(self, voter, vote):
        self.votes[voter] = vote

    def get_vote_count(self, vote_type):
        return sum(1 for v in self.votes.values() if v == vote_type)

    def is_active(self):
        now = datetime.datetime.now()
        return self.start_time <= now <= self.end_time

class VotingSystem:
    def __init__(self):
        self.proposals = []

    def create_proposal(self, title, description, author, start_time, end_time):
        proposal = Proposal(title, description, author, start_time, end_time)
        self.proposals.append(proposal)
        return proposal

    def cast_vote(self, proposal_hash, voter, vote):
        for proposal in self.proposals:
            if proposal.hash == proposal_hash:
                proposal.add_vote(voter, vote)
                return
        raise ValueError(f'Proposal with hash {proposal_hash} not found.')

    def get_proposal_result(self, proposal_hash):
        for proposal in self.proposals:
            if proposal.hash == proposal_hash:
                yes_votes = proposal.get_vote_count('yes')
                no_votes = proposal.get_vote_count('no')
                return yes_votes > no_votes
        raise ValueError(f'Proposal with hash {proposal_hash} not found.')

    def get_active_proposals(self):
        return [p for p in self.proposals if p.is_active()]
