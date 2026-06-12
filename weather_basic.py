from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import requests


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
LOG_FILE = Path("weather_log.txt")

城市列表 = {
    "1": {"名字": "深圳", "纬度": 22.5, "经度": 114.0},
    "2": {"名字": "北京", "纬度": 39.9, "经度": 116.4},
    "3": {"名字": "上海", "纬度": 31.2, "经度": 121.4},
    "4": {"名字": "长沙", "纬度": 28.2, "经度": 113.0},
    "5": {"名字": "广州", "纬度": 23.1, "经度": 113.3},
    "6": {"名字": "杭州", "纬度": 30.3, "经度": 120.2},
    "7": {"名字": "益阳", "纬度": 28.6, "经度": 112.3},
    "8": {"名字": "邵阳", "纬度": 27.3, "经度": 111.5},
}


def 获取天气(纬度: float, 经度: float, timeout: float = 10) -> dict[str, Any] | None:
    """获取指定经纬度的当前天气。"""
    params = {
        "latitude": 纬度,
        "longitude": 经度,
        "current_weather": "true",
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=timeout)
        response.raise_for_status()
        天气 = response.json()["current_weather"]
    except (requests.RequestException, KeyError, ValueError) as exc:
        print(f"天气查询失败: {exc}")
        return None

    return {
        "温度": 天气["temperature"],
        "风速": 天气["windspeed"],
        "风向": 天气["winddirection"],
        "时间": 天气["time"],
    }


def 保存天气(城市名: str, 数据: dict[str, Any] | None, log_file: Path = LOG_FILE) -> None:
    """将天气数据追加写入文件。"""
    if 数据 is None:
        return

    时间 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    内容 = f"[{时间}] {城市名}: 温度{数据['温度']}°C, 风速{数据['风速']}km/h, 风向{数据['风向']}°\n"
    with log_file.open("a", encoding="utf-8") as file:
        file.write(内容)
    print(f"已保存: {内容.strip()}")


def 显示天气(城市名: str, 数据: dict[str, Any] | None) -> None:
    """格式化显示天气信息。"""
    if 数据 is None:
        print("暂无天气数据")
        return

    print("\n" + "=" * 30)
    print(f"       {城市名} 当前天气")
    print("=" * 30)
    print(f"  温度: {数据['温度']}°C")
    print(f"  风速: {数据['风速']} km/h")
    print(f"  风向: {数据['风向']}°")
    print(f"  时间: {数据['时间']}")
    print("=" * 30)


def 显示菜单() -> None:
    print("\n          天气查询系统")
    print("-" * 30)
    for 编号, 城市 in 城市列表.items():
        print(f"  {编号}. {城市['名字']}")
    print("  0. 退出")
    print("-" * 30)


def main() -> None:
    while True:
        显示菜单()
        选择 = input("请选择城市编号: ").strip()

        if 选择 == "0":
            print("感谢使用，欢迎下次使用")
            break
        if 选择 not in 城市列表:
            print("无效选择，请重试")
            continue

        城市 = 城市列表[选择]
        print(f"\n正在查询{城市['名字']}天气...")
        数据 = 获取天气(城市["纬度"], 城市["经度"])
        显示天气(城市["名字"], 数据)
        保存天气(城市["名字"], 数据)


if __name__ == "__main__":
    main()
