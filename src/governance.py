import math

class Voter:
    def __init__(self, address, stake):
        self.address = address
        self.stake = stake
        self.vote_weight = self.calculate_vote_weight()

    def calculate_vote_weight(self):
        # Use a logarithmic function to calculate vote weight based on stake
        return math.log(self.stake + 1)

class Proposal:
    def __init__(self, id, description, options):
        self.id = id
        self.description = description
        self.options = options
        self.votes = {option: 0 for option in options}

    def cast_vote(self, voter, option):
        self.votes[option] += voter.vote_weight

class GovernanceEngine:
    def __init__(self):
        self.voters = []
        self.proposals = []

    def add_voter(self, address, stake):
        voter = Voter(address, stake)
        self.voters.append(voter)

    def add_proposal(self, id, description, options):
        proposal = Proposal(id, description, options)
        self.proposals.append(proposal)

    def vote(self, voter_address, proposal_id, option):
        voter = next((v for v in self.voters if v.address == voter_address), None)
        if voter:
            proposal = next((p for p in self.proposals if p.id == proposal_id), None)
            if proposal:
                proposal.cast_vote(voter, option)
            else:
                print(f'Proposal with ID {proposal_id} not found.')
        else:
            print(f'Voter with address {voter_address} not found.')

    def get_proposal_results(self, proposal_id):
        proposal = next((p for p in self.proposals if p.id == proposal_id), None)
        if proposal:
            return proposal.votes
        else:
            print(f'Proposal with ID {proposal_id} not found.')
            return None