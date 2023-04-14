from nonebot import on_command
from nonebot.adapters import Message, Event, Bot
from nonebot.params import CommandArg
import random

from ..data import add_help_message, get_data
from ..universal_adapters import get_user_name

add_help_message('science-joke', '理科笑话')
science_joke_data: list[str] = [x[1] for x in get_data('science_joke')]

# message
science_joke = on_command('science-joke', aliases={'理科笑话', 'science_joke'}, block=True)
@science_joke.handle()
async def _(event: Event, bot: Bot, args: Message = CommandArg()):
    name = await get_user_name(event, bot, 'ta')
    if msg := args.extract_plain_text():
        name = msg
    await science_joke.finish(random.choice(science_joke_data).format(name=name))