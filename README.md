# GambaStatsBot 🍇🍋🍒
[![CI](https://github.com/niiitty/GambaStatsBot/actions/workflows/ci.yaml/badge.svg)](https://github.com/niiitty/GambaStatsBot/actions/workflows/ci.yaml) ![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

A Telegram bot to keep track of wins/losses on slot machine spins.

## Setup

Requires
- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### For local deployment

git clone and make `.env` in project root. Add the following:

- `BOT_TOKEN`: [Create a bot](https://core.telegram.org/bots/features#botfather) with [@BotFather](https://t.me/botfather) to get the token.
- `DATABASE_URL`: Url to your Postgres database (e.g. [Neon](https://neon.com/docs/connect/connect-from-any-app#get-a-connection-string-from-the-neon-console)).

Run the bot with

```sh
uv run up
```

## Usage
> Note: the bot's responses are in Finnish.

```
/help - Print this message.

/begin - Start tracking wins/losses.
/stats - Print statistics.
/leaderboard - Print top 10.
```

## License

GambaStatsBot is licensed under the terms of the [MIT license](LICENSE).