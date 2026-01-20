# test_amap_api.py
import requests
import os


def test_amap_api():
    # 获取高德地图API密钥
    api_key = os.getenv("AMAP_API_KEY", "386a7f31819da3ffddc244c0e8ebd1ff")

    # 测试天气API
    weather_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "city": "430100",  # 长沙的城市编码
        "key": api_key,
        "extensions": "base"  # base:实时天气, all:预报天气
    }

    print(f"测试高德地图API密钥: {api_key[:10]}...")

    try:
        response = requests.get(weather_url, params=params, timeout=10)
        data = response.json()

        print(f"状态码: {response.status_code}")
        print(f"响应: {data}")

        if data.get("status") == "1":
            print("✅ API密钥有效！")
            lives = data.get("lives", [])
            if lives:
                weather = lives[0]
                print(f"""
🌤️ 测试成功！长沙天气：
- 天气: {weather.get('weather', '未知')}
- 温度: {weather.get('temperature', '未知')}°C
- 风向: {weather.get('winddirection', '未知')}
- 风力: {weather.get('windpower', '未知')}级
- 湿度: {weather.get('humidity', '未知')}%
                """)
        else:
            print(f"❌ API错误: {data.get('info', '未知错误')}")

    except Exception as e:
        print(f"❌ 请求失败: {e}")


if __name__ == "__main__":
    test_amap_api()