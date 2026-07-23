from src.config import Config
   
FAKE_DATABASE_URL = "postgres://user:password@your-neon-hostname.neon.tech/neondb?sslmode=require&channel_binding=require"
FAKE_BOT_TOKEN = "5BWwl5dr$78wsC#Y"


def test_get_env_correctly(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", FAKE_DATABASE_URL)
    monkeypatch.setenv("BOT_TOKEN", FAKE_BOT_TOKEN)
    
    assert Config.get_env().database_url == FAKE_DATABASE_URL
    assert Config.get_env().bot_token == FAKE_BOT_TOKEN
