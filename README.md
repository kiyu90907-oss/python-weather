# 🌤️ Python 天气查询系统

Python 入门学习项目，通过 API 实时查询城市天气。

## 两个版本
| 文件 | 说明 |
|------|------|
|  | 基础版 — 8 个预设城市，编号选择查询 |
|  | 智能版 — 输入任意城市名，自动定位+天气描述+emoji |

## 功能
- 实时温度、风速、风向查询
- 智能版支持任意城市名输入，自动地理编码
- 天气状况中文描述 + emoji（☀️晴天、🌧️小雨、⛈️雷暴等）
- 查询记录自动保存到本地日志

## 运行
```bash
pip install requests
python weather_basic.py   # 基础版
python weather_smart.py   # 智能版
```
