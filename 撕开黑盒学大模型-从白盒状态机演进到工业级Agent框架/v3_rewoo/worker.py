from __future__ import annotations

import asyncio


async def fetch_price(product: str) -> str:
    await asyncio.sleep(0.4)
    return f"{product} 预算价格区间已获取"


async def fetch_weather(city: str) -> str:
    await asyncio.sleep(0.4)
    return f"{city} 小雨，建议带伞"


async def unstable_inventory(product: str) -> str:
    await asyncio.sleep(0.8)
    return f"{product} 库存服务返回较慢"


async def summarize(argument: str) -> str:
    await asyncio.sleep(0.2)
    return f"综合结论：{argument}"


TOOLS = {
    "fetch_price": fetch_price,
    "fetch_weather": fetch_weather,
    "unstable_inventory": unstable_inventory,
    "summarize": summarize,
}
