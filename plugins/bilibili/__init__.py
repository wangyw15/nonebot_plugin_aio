from datetime import datetime

from nonebot import on_regex, on_fullmatch
from nonebot.adapters import Bot, Event
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

from ...adapters import unified
from . import bilibili

__plugin_meta__ = PluginMetadata(
    name='Bilibili',
    description='哔哩哔哩相关，比如从B站url提取信息，还有展览信息',
    usage='B站url会自动触发',
    config=None
)


def _generate_bilibili_message(data: dict) -> str:
    # 描述删掉所有空行，并且只取前200个字符
    desc = '\n'.join([x.strip() for x in data['desc'].split('\n') if x.strip() != ''])
    if len(desc) > 200:
        desc = desc[:200] + '...'
    # 视频发布时间
    date = datetime.fromtimestamp(data['pubdate'])
    # 生成信息
    msg = f'标题: \n{data["title"]}\n' \
          f'UP主: \n{data["owner"]["name"]}\n' \
          f'发布时间: {date.strftime("%Y年%m月%d日 %H:%M:%S")}\n' \
          f'播放: {data["stat"]["view"]}\n' \
          f'弹幕: {data["stat"]["danmaku"]}\n' \
          f'点赞: {data["stat"]["like"]}\n' \
          f'投币: {data["stat"]["coin"]}\n' \
          f'简介:\n{desc}\n' \
          f'视频链接: \nhttps://www.bilibili.com/video/{data["bvid"]}'
    return msg


_bilibili_video = on_regex(bilibili.bilibili_vid_pattern, block=True)
@_bilibili_video.handle()
async def _(state: T_State, bot: Bot, event: Event):
    data = await bilibili.fetch_video_data(state['_matched_groups'][0])
    if data:
        msg = _generate_bilibili_message(data)
        final_msg = unified.Message()
        final_msg.append(unified.MessageSegment.image(data['pic'], '视频封面图'))
        final_msg.append(msg)
        await final_msg.send(bot, event)
        await _bilibili_video.finish()


_bilibili_video_short_link = on_regex(r'https:\/\/b23.tv\/(?!BV)[0-9A-Za-z]{7}', block=True)
@_bilibili_video_short_link.handle()
async def _(state: T_State, bot: Bot, event: Event):
    vid = await bilibili.get_bvid_from_short_link(state['_matched_str'])
    if vid:
        data = await bilibili.fetch_video_data(vid)
        if data:
            msg = _generate_bilibili_message(data)
            final_msg = unified.Message()
            final_msg.append(unified.MessageSegment.image(data['pic'], '视频封面图'))
            final_msg.append(msg)
            await final_msg.send(bot, event)
            await _bilibili_video_short_link.finish()


_bilibili_projects_handlers = on_fullmatch('我要看展', block=True)
@_bilibili_projects_handlers.handle()
async def _(bot: Bot, event: Event):
    projects = await bilibili.fetch_all_projects()
    if projects:
        msg = '现在的正在进行的展览有:\n\n'
        for project in projects:
            start_time = datetime.strptime(project['start_time'], '%Y.%m.%d')
            try:
                end_time = datetime.strptime(project['end_time'], '%Y.%m.%d')
            except ValueError:
                end_time = datetime.strptime(str(start_time.year) + '.' + project['end_time'], '%Y.%m.%d')
            if start_time <= datetime.now() <= end_time:
                msg += f'{project["project_name"]}\n' \
                       f'开始时间: {start_time.strftime("%Y年%m月%d日")}\n' \
                       f'结束时间: {end_time.strftime("%Y年%m月%d日")}\n' \
                       f'链接: https://show.bilibili.com/platform/detail.html?id={project["id"]}\n\n'
        await _bilibili_projects_handlers.finish(msg)