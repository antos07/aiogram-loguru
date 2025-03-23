# aiogram-loguru

**aiogram-loguru** is a small library that ships some boilerplate code needed for integrating
[aiogram](https://pypi.org/project/aiogram/) with [loguru](https://pypi.org/project/loguru/).

## Features

- A [sink](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add)
  for loguru that sends logs to a Telegram chat via a bot.
- *and more features soon...*

## Requirements

As for now, only **Python 3.13** is supported.
It also requires **aiogram** (v3.18) and **loguru** (v0.7.3) to be installed.

## Installation

    pip install aiogram-loguru
  
## Usage

You can use the sink like this:

```python
from aiogram import Bot
from aiogram_loguru import AiogramSink
from loguru import logger

CHAT_ID = 12345  # the ID of a chat, where the logs will be sent to

bot = Bot("YOUR BOT TOKEN")
sink = AiogramSink(bot, CHAT_ID)
logger.add(sink)
```

Now all the logs will be sent to the selected Telegram chat. 
However, Telegram Bot API has rather painful [limits](https://limits.tginfo.me/en),
so you would probably want to limit the number of sent logs to the most important ones like this:

```python
logger.add(sink, level='ERROR')
```

Lastly, for the sink to work, you should actually have an event loop running.
You should also await `logger.complete()` when your program is exiting to ensure that all logs
have been actually sent. 
See the [docs](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.complete) for details.


## License

This project is licensed under the terms of the [MIT license](https://github.com/antos07/aiogram-loguru/blob/master/LICENSE).
