# Python 天气查询系统

Python 入门学习项目，通过 Open-Meteo API 实时查询城市天气。项目包含固定城市选择版和智能城市搜索版，适合展示 API 调用、异常处理、文件日志和基础单元测试。

## 两个版本
| 文件 | 说明 |
|------|------|
| `weather_basic.py` | 基础版：8 个预设城市，编号选择查询 |
| `weather_smart.py` | 智能版：输入任意城市名，自动定位并显示天气描述 |

## 功能
- 实时温度、风速、风向查询
- 智能版支持任意城市名输入，自动地理编码
- 天气状况中文描述
- 查询记录自动保存到本地日志
- 网络请求包含超时和错误处理
- 单元测试覆盖天气代码、定位解析、天气解析和日志写入

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

基础版：

```bash
python weather_basic.py
```

智能版：

```bash
python weather_smart.py
```

## 测试

```bash
python -m unittest discover -s tests
```

## 输出文件

查询结果会追加写入 `weather_log.txt`。该文件是本地运行日志，已经加入 `.gitignore`，不会上传到 GitHub。
