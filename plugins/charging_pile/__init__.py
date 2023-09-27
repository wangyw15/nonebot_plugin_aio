import json

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg, Arg
from nonebot.plugin import PluginMetadata

from . import charging_pile
from adapters import unified

__plugin_meta__ = PluginMetadata(
    name='找充电桩',
    description='电瓶车没电了！我应该去哪充电？',
    usage='/charge',
    config=None
)


_charging_pile_handler = on_command('charge', aliases={'充电', '充电桩'}, block=True)


@_charging_pile_handler.handle()
async def _():
    if not unified.Detector.is_onebot():
        await _charging_pile_handler.finish('抱歉，目前只支持 OneBot 协议')


@_charging_pile_handler.got('location', prompt='请发送定位')
async def _(location: Message = Arg()):
    if location[0].type == 'json':
        await _charging_pile_handler.send('正在查询喵~')
        json_data = json.loads(location[0].data['data'])
        stations = await charging_pile.get_station_list(
            json_data['meta']['Location.Search']['lng'], json_data['meta']['Location.Search']['lat'])
        await _charging_pile_handler.finish(await charging_pile.generate_message(stations))
