import os
from .ledger import AccountDB
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    dotenv_path = os.path.join('/app','docker', '.env')
    load_dotenv(dotenv_path)
    config = {
        "host":      os.environ.get('host'),
        "user":      os.environ.get('user'),
        "password":  os.environ.get('password'),
        "db":        os.environ.get('db'),
    }
    sql = AccountDB(config)
    test = sql.get_monthly_summary()
    print(test.keys())
    print(test.value())
