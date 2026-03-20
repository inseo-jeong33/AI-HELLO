import requests

def get_weather(city_name):
    # 1. API 키와 주소 설정
    API_KEY = "5b220e1ef91f97615b018fd0251c2af3"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=kr"

    # 2. 데이터 요청하기
    response = requests.get(url)
    data = response.json() # 데이터를 파이썬이 이해하기 쉬운 딕셔너리로 변환
    print(f"DEBUG: 서버 응답 데이터 -> {data}")

    # 3. 결과 보여주기
    if data["cod"] == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        
        print(f"\n🌍 {city_name}의 현재 날씨 정보")
        print(f"☁️ 상태: {weather}")
        print(f"🌡️ 온도: {temp}°C (체감 온도: {feels_like}°C)")
    else:
        print("❌ 도시 이름을 찾을 수 없어요. 영문으로 입력해보세요! (예: Seoul, Busan)")

# 프로그램 실행
city = input("날씨가 궁금한 도시 이름을 영어로 입력하세요: ")
get_weather(city)