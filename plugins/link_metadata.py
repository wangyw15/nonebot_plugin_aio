from nonebot import on_regex, logger
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata

from ..libraries import link_metadata

__plugin_meta__ = PluginMetadata(
    name='计算器',
    description='简单的计算器',
    usage='输入表达式，以等号结尾，比如：1+1=',
    config=None
)

_bilibili_video = on_regex(r'(?:https?:\/\/)?(?:www\.)?bilibili.com\/video\/((?:BV|av)[0-9A-Za-z]+)', block=True)
@_bilibili_video.handle()
async def _(state: T_State):
    vid = state['_matched_groups'][0]
    if vid.startswith('BV'):
        data = await link_metadata.fetch_bilibili_data(vid, 'bv')
    elif vid.startswith('av'):
        data = await link_metadata.fetch_bilibili_data(vid, 'av')
    if data:
        logger.error(data)
        msg = f'[CQ:image,file={data["pic"]}]标题: {data["title"]}\nUP主: {data["owner"]["name"]}\n简介: {data["desc"]}\n播放: {data["stat"]["view"]}\n弹幕: {data["stat"]["danmaku"]}\n点赞: {data["stat"]["like"]}\n投币: {data["stat"]["coin"]}'
        await _bilibili_video.finish(msg)
