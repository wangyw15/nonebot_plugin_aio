import re

from nonebot.adapters import Bot, Event, MessageSegment
from ..adapters import unified


def generate_onebot_group_forward_message(content: list[str], name: str, sender_id: str) -> list[dict]:
    """生成OneBot群组转发消息"""
    msg_nodes: list[dict] = []
    for msg in content:
        msg_nodes.append({
            'type': 'node',
            'data': {
                'name': name,
                'uin': sender_id,
                'content': msg.strip()
            }
        })
    return msg_nodes


async def send_group_forward_message(content: list[str], bot: Bot, event: Event, default_bot_name: str = 'Canrot',
                                     split: str = unified.util.MESSAGE_SPLIT_LINE, header: str = '') -> None:
    if unified.Detector.is_onebot_v11(bot) or unified.Detector.is_onebot_v12(bot):
        if header:
            content.insert(0, header)
        msg_nodes = generate_onebot_group_forward_message(content,
                    await unified.util.get_bot_name(event, bot, default_bot_name), bot.self_id)
        if isinstance(event, unified.adapters.onebot_v11.GroupMessageEvent) \
                or isinstance(event, unified.adapters.onebot_v12.GroupMessageEvent):
            await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_nodes)
            return
    header = header + '\n\n' if header else ''
    msg = header + ('\n' + split + '\n').join(content)
    if unified.Detector.is_onebot_v11(bot):
        await bot.send(event, unified.adapters.onebot_v11.Message(msg))
        return
    elif unified.Detector.is_onebot_v12(bot):
        await bot.send(event, unified.adapters.onebot_v12.Message(msg))
        return
    await bot.send(event, msg)


def is_url(msg: MessageSegment | str) -> bool:
    """检测是否为URL"""
    if isinstance(msg, str):
        return re.match(r'^https?://', msg) is not None
    elif msg.is_text():
        msg = str(msg)
        return re.match(r'^https?://', msg) is not None
    elif isinstance(msg, unified.adapters.kook.MessageSegment):
        if msg.type == 'kmarkdown':
            msg = re.search(r'\[.*]\((\S+)\)', msg.plain_text()).groups()[0]
            return re.match(r'^https?://', msg) is not None
        elif msg.type == 'text':
            return re.match(r'^https?://', msg.plain_text()) is not None
    return False


def seconds_to_time(seconds: float) -> str:
    ms = int(seconds % 1 * 1000)
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}.{str(ms).zfill(3)}"

