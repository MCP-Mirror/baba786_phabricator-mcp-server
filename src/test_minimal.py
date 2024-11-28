import os
from phabricator import Phabricator

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def test_connection():
    phab = Phabricator(
        host='https://phabricator.wikimedia.org/api/',
        token=os.getenv('PHABRICATOR_TOKEN')
    )
    phab.update_interfaces()
    
    # Test with a simple whoami call
    print('Connected as:', phab.user.whoami()['userName'])
    
    # Try getting a task
    task_id = input('Enter task ID (without T): ')
    task = phab.maniphest.search(constraints={'ids': [int(task_id)]}).data
    if task:
        print(f"\nFound task T{task[0]['id']}: {task[0]['fields']['name']}")

if __name__ == '__main__':
    load_env()
    if not os.getenv('PHABRICATOR_TOKEN'):
        print('Error: PHABRICATOR_TOKEN not set')
        exit(1)
    test_connection()