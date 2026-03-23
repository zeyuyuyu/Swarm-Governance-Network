import os
import json
from typing import List, Dict

class GovernanceEngine:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.proposals: List[Proposal] = []
        self.votes: Dict[str, Dict[str, int]] = {}

    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return json.load(f)

    def add_proposal(self, proposal: Proposal):
        self.proposals.append(proposal)

    def cast_vote(self, voter_id: str, proposal_id: str, vote: int):
        if proposal_id not in self.votes:
            self.votes[proposal_id] = {}
        self.votes[proposal_id][voter_id] = vote

    def tally_votes(self, proposal_id: str) -> int:
        vote_counts = self.votes.get(proposal_id, {})
        yes_votes = sum(1 for v in vote_counts.values() if v == 1)
        no_votes = sum(1 for v in vote_counts.values() if v == -1)
        return yes_votes - no_votes

    def execute_proposal(self, proposal_id: str):
        proposal = next((p for p in self.proposals if p.id == proposal_id), None)
        if proposal and self.tally_votes(proposal_id) >= self.config['min_approval_threshold']:
            proposal.execute()

class Proposal:
    def __init__(self, id: str, description: str, execute_func: callable):
        self.id = id
        self.description = description
        self.execute = execute_func

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), 'governance_config.json')
    engine = GovernanceEngine(config_path)

    def execute_example_proposal():
        print('Executing example proposal...')

    example_proposal = Proposal('example_proposal', 'Example Proposal', execute_example_proposal)
    engine.add_proposal(example_proposal)

    engine.cast_vote('user1', 'example_proposal', 1)
    engine.cast_vote('user2', 'example_proposal', -1)

    engine.execute_proposal('example_proposal')