# 导入requests模块用来发HTTP请求
import requests

# 导入datetime模块用来获取当前时间
from datetime import datetime

# 定义一个函数 获取经纬度 需要传入城市名 这个函数的作用是 输入地名 自动查出这个地方的经纬度坐标
def 获取经纬度(城市名):  # 输入城市名 调用地理编码API 返回经纬度字典

    # 地理编码API地址
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

    # 设置请求参数 告诉API我们要查什么 就像你去搜索引擎 输入关键词和各种筛选条件
    params = {
        "name": 城市名,  # 要查询的城市名
        "count": 1,  # 只取最匹配的第一个结果
        "language": "zh",  # 返回中文地名
        "format": "json"  # 返回JSON格式数据
    }

    # try尝试执行 如果网络出错就跳到except
    try:
        # 向地理编码API发送get请求 params=params把参数传给服务器
        r = requests.get(geocode_url, params=params)

        # 状态码200表示请求成功
        if r.status_code == 200:
            # 把返回的数据转成字典
            data = r.json()

            # "results"是返回数据里的一个键 它的值是一个列表
            # 列表里每个元素都是一个可能匹配的地点
            # 检查results是否存在并且里面至少有一个结果
            if "results" in data and len(data["results"]) > 0:
                # 取最匹配一个结果
                结果 = data["results"][0]

                # 返回一个包含经纬度和官方地名的字典
                # .get() 是字典的安全取值方法 如果键不存在不会报错 而是返回默认值
                return {
                    "纬度": 结果["latitude"],         # 取出纬度
                    "经度": 结果["longitude"],        # 取出经度
                    "全名": 结果.get("name", 城市名)   # 取官方地名
                }

        # 如果请求失败或者没找到结果 返回None表示空
        return None

    except Exception as e:
        # 网络出错时打印错误信息
        print(f"地理编码出错: {e}")
        # 返回None表示没拿到数据
        return None

# 获取天气描述函数
# 定义一个新函 获取天气描述 需要传入纬度和经度
# 这个函数专门用来获取天气状况的描述
def 获取天气描述(纬度, 经度):
    """获取天气状况的中文描述，如：晴天、阴天、小雨"""

    # 天气API地址 和之前的基础版一样 但多加了一个参数：&daily=weathercode 表示额外获取每天的天气代码数据
    url = f"https://api.open-meteo.com/v1/forecast?latitude={纬度}&longitude={经度}&current_weather=true&daily=weathercode"

    try:
        # 发送请求获取天气数据
        r = requests.get(url)
        if r.status_code == 200:
            # 转为字典
            data = r.json()

            # 从数据里一步步取出当天的天气代码
            # .get() 是安全取值，每一步如果键不存在就返回空字典{}，不会报错
            # 最终 [0] 取列表的第一个元素（当天的天气代码）
            weathercode = data.get("daily", {}).get("weathercode", [None])[0]

            # 这是一个对照表字典 把数字代码翻译成中文描述和emoji形式 emoji按键盘win+。就可以搜索
            # 每个数字代表一种天气类型
            天气表 = {
                0: "☀️ 晴天",  # 天气晴朗
                1: "🌤️ 小晴天", 2: "⛅ 多云", 3: "☁️ 阴天",  # 不同云量等级
                45: "🌫️ 雾", 48: "🌫️ 雾凇",  # 雾相关天气
                51: "🌦️ 小毛毛雨", 53: "🌦️ 毛毛雨", 55: "🌦️ 大毛毛雨",  # 毛毛雨
                61: "🌧️ 小雨", 63: "🌧️ 中雨", 65: "🌧️ 大雨",  # 正常降雨
                71: "❄️ 小雪", 73: "❄️ 中雪", 75: "❄️ 大雪",  # 降雪
                80: "🌦️ 阵雨", 81: "🌦️ 大阵雨", 82: "🌦️ 强阵雨",  # 阵雨
                95: "⛈️ 雷暴", 96: "⛈️ 冰雹雷暴", 99: "⛈️ 强冰雹雷暴"  # 雷暴天气
            }

            # .get(weathercode, "未知天气") 是从天气表里查找对应代码的描述
            # 如果代码不在表里 就返回默认值"未知天气"
            return 天气表.get(weathercode, "未知天气")

        # 请求失败时返回提示
        return "获取失败"
    except:
        # 网络异常时返回提示
        return "获取失败"

# 获取天气函数
def 获取天气(纬度, 经度):
    """获取指定经纬度的当前天气，返回包含温度、风速、风向、时间和天气描述的字典"""

    # 拼接天气API地址
    url = f"https://api.open-meteo.com/v1/forecast?latitude={纬度}&longitude={经度}&current_weather=true"

    try:
        # 发送请求
        r = requests.get(url)
        if r.status_code == 200:
            # 解析JSON
            data = r.json()
            # 取出当前天气内层字典
            天气 = data["current_weather"]

            # 新增调用获取天气描述函数 把经纬度传进去
            # 这个函数会返回类似"☀️ 晴天"这样的中文描述
            描述 = 获取天气描述(纬度, 经度)

            # 返回完整天气信息 比基础版多了一个"天气"字段
            return {
                "温度": 天气["temperature"],    # 温度（摄氏度）
                "风速": 天气["windspeed"],      # 风速（km/h）
                "风向": 天气["winddirection"],  # 风向角度
                "时间": 天气["time"],           # 观测时间
                "天气": 描述                    # 新增天气状况描述 eg"☀️ 晴天"
            }
        else:
            print(f"请求失败，状态码: {r.status_code}")
            return None
    except Exception as e:
        print(f"网络出错: {e}")
        return None

# 保存天气函数 这个函数和基础款几乎一样 只是在保存内容里多了天气描述
def 保存天气(城市名, 数据):
    """将天气数据追加写入本地日志文件"""

    # 数据为空直接返回
    if 数据 is None:
        return

    # 获取当前时间并格式化
    时间 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 拼接保存内容 比22多了 {数据['天气']} 这个字段
    # 所以日志文件里会显示天气状况 eg“☀️ 晴天”
    内容 = f"[{时间}] {城市名}: {数据['天气']}, 温度{数据['温度']}°C, 风速{数据['风速']}km/h\n"

    # 追加模式写入内容
    with open("weather_log.txt", "a", encoding="utf-8") as f:
        f.write(内容)

    # 打印保存成功提示
    print(f"已保存: {内容.strip()}")

# 显示天气函数
# 这个函数和22几乎一样 只是多了一行天气描述
def 显示天气(城市名, 数据):
    """在屏幕上格式化显示天气信息面板"""

    # 数据为空直接返回
    if 数据 is None:
        return

    # 打印天气信息面板
    print("\n" + "=" * 30)           # 顶部30个等号
    print(f"  {城市名} 当前天气")       # 城市名
    print("=" * 30)                  # 中间分隔线
    print(f"  {数据['天气']}")         # 显示天气状况
    print(f"  温度: {数据['温度']}°C")  # 温度
    print(f"  风速: {数据['风速']} km/h")  # 风速
    print(f"  风向: {数据['风向']}°")   # 风向角度
    print(f"  时间: {数据['时间']}")    # 观测时间
    print("=" * 30)                  # 底部30个等号

# 主程序
def main():
    """主程序：循环接收用户输入 → 地名转经纬度 → 查天气 → 显示并保存"""

    # 打印系统标题和说明
    print("=" * 30)
    print("      🌤️智能天气查询系统")
    print("=" * 30)
    print("  输入任意城市名即可查询天气")
    print("  输入 0 退出系统")
    print("=" * 30)

    # 无限循环 可反复查询
    while True:
        # 获取用户输入的城市名
        # .strip() 去掉输入内容首尾的空格
        城市名 = input("\n请输入城市名称: ").strip()

        # 输入0退出
        if 城市名 == "0":
            print("感谢使用，再见！")
            break  # 跳出循环，程序结束

        # not 城市名 的意思是“城市名为空字符串”
        if not 城市名:
            print("请输入有效城市名")
            continue  # 跳过本次循环的剩余代码回到开头while循环

        # 第一步 地名转经纬度
        # 打印查找提示
        print(f"正在查找「{城市名}」...")
        # 调用获取经纬度函数，传入城市名
        位置 = 获取经纬度(城市名)

        # 如果返回None 说明API里找不到这个城市
        if 位置 is None:
            print(f"找不到「{城市名}」，请检查拼写或换个城市试试")
            continue  # 跳过本次循环，让用户重新输入

        # 打印定位成功的信息 显示城市名 纬度 经度
        print(f"已定位到: {位置['全名']} (纬度{位置['纬度']}, 经度{位置['经度']})")

        # 第二步 用经纬度查天气
        # 调用获取天气函数，传入经纬度
        天气数据 = 获取天气(位置["纬度"], 位置["经度"])

        # 第三步 显示和保存
        # 调用显示天气函数 在屏幕上展示天气面板
        显示天气(位置["全名"], 天气数据)
        # 调用保存天气函数，把天气数据写入本地文件
        保存天气(位置["全名"], 天气数据)

# 直接运行这个文件就执行main函数
if __name__ == "__main__":
    main()
