import httpx
import typing
import re

from adapters import unified

_client = httpx.AsyncClient()


async def get_thread_data(thread_number: str) -> typing.Any | None:
    """
    获取串号内容

    :param thread_number: 串号

    :return: 串的第一页内容
    """
    resp = await _client.get(f'https://api.nmb.best/api/thread?id={thread_number}&page=1')
    if resp.is_success and resp.status_code == 200:
        return resp.json()
    return None


def translate_time(t: str) -> str:
    parsed = re.match(r'(\d{4})-(\d{2})-(\d{2})\((\S)\)(\d{2}):(\d{2}):(\d{2})', t)
    if parsed:
        return f'{parsed[1]}/{parsed[2]}/{parsed[3]} {parsed[5]}:{parsed[6]}'
    return ''


def generate_message(thread_data, head: bool = False) -> unified.Message:
    msg = unified.Message()
    if thread_data['id'] == 9999999:
        msg.append(f'Tips:\n{thread_data["content"]}\n')
        return msg
    if head:
        msg.append(f'https://www.nmbxd.com/t/{thread_data["id"]}\n')
    msg.append(thread_data['user_hash'] + ' ' + translate_time(thread_data['now']) + '\n')
    msg.append(f'No.{thread_data["id"]}')
    if head:
        msg.append(' ' + str(thread_data['ReplyCount']) + '条回复')
    msg.append('\n')
    if thread_data['title'] and thread_data['title'] != '无标题':
        msg.append('标题: ' + thread_data['title'] + '\n')
    msg.append(re.sub(r'<br\s?/>', '\n', thread_data['content']) + '\n')
    if thread_data['img']:
        msg.append(unified.MessageSegment.image(
            f'https://image.nmb.best/image/{thread_data["img"]}{thread_data["ext"]}'))
    return msg


__all__ = ['get_thread_data', 'translate_time', 'generate_message']
