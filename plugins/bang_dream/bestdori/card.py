from datetime import timedelta

from . import util


def get_card_list() -> dict[str]:
    """
    获取卡片列表

    :return: 卡片列表
    """
    return util.bestdori_api_with_cache("cards/all.5.json", timedelta(days=7))


def get_card_info(card_id: str) -> dict[str]:
    """
    获取卡片信息

    :param card_id: 卡片ID

    :return: 卡片信息
    """
    return util.bestdori_api_with_cache(f"cards/{card_id}.json")
