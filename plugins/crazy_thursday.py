import random

from nonebot import on_keyword
from nonebot.plugin import PluginMetadata

from storage import asset

__plugin_meta__ = PluginMetadata(
    name="疯狂星期四",
    description="随机发送疯狂星期四文案",
    usage="消息包含疯狂星期四就会触发",
    config=None,
)


crazy_thursday_posts: list[str] = asset.LocalAsset("crazy_thursday.json").json()
crazy_thursday_matcher = on_keyword({"疯狂星期四"}, block=True)


@crazy_thursday_matcher.handle()
async def _():
    await crazy_thursday_matcher.finish(random.choice(crazy_thursday_posts))
