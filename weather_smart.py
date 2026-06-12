from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import requests


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
LOG_FILE = Path("weather_log.txt")

天气表 = {
    0: "晴天",
    1: "小晴天",
    2: "多云",
    3: "阴天",
    45: "雾",
    48: "雾凇",
    51: "小毛毛雨",
    53: "毛毛雨",
    55: "大毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    80: "阵雨",
    81: "大阵雨",
    82: "强阵雨",
    95: "雷暴",
    96: "冰雹雷暴",
    99: "强冰雹雷暴",
}


def 请求_json(url: str, params: dict[str, Any], timeout: float = 10) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def 获取经纬度(城市名: str, timeout: float = 10) -> dict[str, Any] | None:
    """输入城市名，返回最匹配地点的经纬度。"""
    params = {
        "name": 城市名,
        "count": 1,
        "language": "zh",
        "format": "json",
    }

    try:
        data = 请求_json(GEOCODE_URL, params, timeout=timeout)
    except (requests.RequestException, ValueError) as exc:
        print(f"地理编码出错: {exc}")
        return None

    results = data.get("results") or []
    if not results:
        return None

    result = results[0]
    return {
        "纬度": result["latitude"],
        "经度": result["longitude"],
        "全名": result.get("name", 城市名),
        "国家": result.get("country", ""),
    }


def 获取天气描述(weathercode: int | None) -> str:
    """把 Open-Meteo 天气代码转换为中文描述。"""
    if weathercode is None:
        return "未知天气"
    return 天气表.get(weathercode, f"未知天气({weathercode})")


def 获取天气(纬度: float, 经度: float, timeout: float = 10) -> dict[str, Any] | None:
    """获取当前天气，包含温度、风速、风向、天气描述和观测时间。"""
    params = {
        "latitude": 纬度,
        "longitude": 经度,
        "current_weather": "true",
        "timezone": "auto",
    }

    try:
        data = 请求_json(FORECAST_URL, params, timeout=timeout)
        天气 = data["current_weather"]
    except (requests.RequestException, KeyError, ValueError) as exc:
        print(f"天气查询失败: {exc}")
        return None

    return {
        "温度": 天气["temperature"],
        "风速": 天气["windspeed"],
        "风向": 天气["winddirection"],
        "时间": 天气["time"],
        "天气": 获取天气描述(天气.get("weathercode")),
    }


def 保存天气(城市名: str, 数据: dict[str, Any] | None, log_file: Path = LOG_FILE) -> None:
    """将天气数据追加写入本地日志文件。"""
    if 数据 is None:
        return

    时间 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    内容 = f"[{时间}] {城市名}: {数据['天气']}, 温度{数据['温度']}°C, 风速{数据['风速']}km/h\n"
    with log_file.open("a", encoding="utf-8") as file:
        file.write(内容)
    print(f"已保存: {内容.strip()}")


def 显示天气(城市名: str, 数据: dict[str, Any] | None) -> None:
    """在屏幕上格式化显示天气信息面板。"""
    if 数据 is None:
        print("暂无天气数据")
        return

    print("\n" + "=" * 30)
    print(f"  {城市名} 当前天气")
    print("=" * 30)
    print(f"  天气: {数据['天气']}")
    print(f"  温度: {数据['温度']}°C")
    print(f"  风速: {数据['风速']} km/h")
    print(f"  风向: {数据['风向']}°")
    print(f"  时间: {数据['时间']}")
    print("=" * 30)


def main() -> None:
    print("=" * 30)
    print("      智能天气查询系统")
    print("=" * 30)
    print("  输入任意城市名即可查询天气")
    print("  输入 0 退出系统")
    print("=" * 30)

    while True:
        城市名 = input("\n请输入城市名称: ").strip()

        if 城市名 == "0":
            print("感谢使用，再见！")
            break
        if not 城市名:
            print("请输入有效城市名")
            continue

        print(f"正在查找「{城市名}」...")
        位置 = 获取经纬度(城市名)
        if 位置 is None:
            print(f"找不到「{城市名}」，请检查拼写或换个城市试试")
            continue

        国家 = f", {位置['国家']}" if 位置.get("国家") else ""
        print(f"已定位到: {位置['全名']}{国家} (纬度{位置['纬度']}, 经度{位置['经度']})")

        天气数据 = 获取天气(位置["纬度"], 位置["经度"])
        显示天气(位置["全名"], 天气数据)
        保存天气(位置["全名"], 天气数据)


if __name__ == "__main__":
    main()
