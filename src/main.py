import os
import json
from typing import List, Dict

class SwarmGovernance:
    def __init__(self, config_file: str = 'config.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.proposals: List[Dict] = []
        self.votes: Dict[str, Dict] = {}
        
    def submit_proposal(self, proposal: Dict) -> bool:
        self.proposals.append(proposal)
        return True
    
    def vote(self, voter_id: str, proposal_id: str, vote: bool) -> bool:
        if proposal_id not in self.votes:
            self.votes[proposal_id] = {}
        self.votes[proposal_id][voter_id] = vote
        return True
    
    def tally_votes(self, proposal_id: str) -> bool:
        votes = self.votes[proposal_id]
        total_votes = len(votes)
        yes_votes = sum(1 for v in votes.values() if v)
        
        if yes_votes > total_votes // 2:
            # Proposal passed
            self.execute_proposal(proposal_id)
            return True
        else:
            # Proposal failed
            return False
        
    def execute_proposal(self, proposal_id: str) -> bool:
        proposal = next(p for p in self.proposals if p['id'] == proposal_id)
        
        # Execute the proposal
        os.system(proposal['command'])
        
        return True
