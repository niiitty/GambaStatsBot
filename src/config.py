"""`Config` class to load environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    database_url: str
    bot_token: str

    @classmethod
    def get_env(cls):
        load_dotenv()
        return cls(
            database_url=os.environ["DATABASE_URL"], bot_token=os.environ["BOT_TOKEN"]
        )
