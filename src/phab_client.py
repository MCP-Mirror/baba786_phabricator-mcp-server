from phabricator import Phabricator
from typing import Dict, List

class PhabricatorClient:
    def __init__(self, token: str, host: str = "https://phabricator.wikimedia.org/api/"):
        self.phab = Phabricator(host=host, token=token)
        self.phab.update_interfaces()
    
    async def get_task(self, task_id: str) -> Dict:
        """Get detailed information about a specific task."""
        task = self.phab.maniphest.search(constraints={'ids': [int(task_id)]})
        if not task.data:
            raise ValueError(f"Task T{task_id} not found")
        return task.data[0]

    async def get_task_comments(self, task_id: str) -> List[Dict]:
        """Get all comments on a task."""
        transactions = self.phab.maniphest.gettasktransactions(ids=[int(task_id)])
        return [t for t in transactions[task_id] if t['type'] == 'comment']
