import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import weather_smart


class WeatherSmartTests(unittest.TestCase):
    def test_weather_code_description(self):
        self.assertEqual(weather_smart.获取天气描述(0), "晴天")
        self.assertEqual(weather_smart.获取天气描述(61), "小雨")
        self.assertEqual(weather_smart.获取天气描述(999), "未知天气(999)")

    @patch("weather_smart.请求_json")
    def test_get_location_returns_first_result(self, mock_request):
        mock_request.return_value = {
            "results": [
                {
                    "name": "深圳",
                    "country": "中国",
                    "latitude": 22.5,
                    "longitude": 114.0,
                }
            ]
        }

        location = weather_smart.获取经纬度("深圳")

        self.assertEqual(location["全名"], "深圳")
        self.assertEqual(location["国家"], "中国")
        self.assertEqual(location["纬度"], 22.5)

    @patch("weather_smart.请求_json")
    def test_get_weather_uses_current_weather_code(self, mock_request):
        mock_request.return_value = {
            "current_weather": {
                "temperature": 26.5,
                "windspeed": 8.1,
                "winddirection": 90,
                "weathercode": 2,
                "time": "2026-06-12T10:00",
            }
        }

        weather = weather_smart.获取天气(22.5, 114.0)

        self.assertEqual(weather["天气"], "多云")
        self.assertEqual(weather["温度"], 26.5)

    def test_save_weather_appends_log_line(self):
        data = {
            "天气": "晴天",
            "温度": 28,
            "风速": 10,
        }
        with TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "weather.log"

            weather_smart.保存天气("深圳", data, log_file=log_file)
            weather_smart.保存天气("深圳", data, log_file=log_file)

            lines = log_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("深圳", lines[0])


if __name__ == "__main__":
    unittest.main()
