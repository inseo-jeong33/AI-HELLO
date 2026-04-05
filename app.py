from flask import Flask, render_template, request, redirect
import requests
import random

app = Flask(__name__)

# ---------------------------------------------------------
# 본인의 API 정보를 입력하세요 (따옴표 유지)
# ---------------------------------------------------------
NAVER_CLIENT_ID = "s5PlfA8iRSiMjKuvzF4s"
NAVER_CLIENT_SECRET = "tmjxQBEp0C"
YOUTUBE_API_KEY = "AIzaSyCyBZqGGV6zy6XqPoFQUkagoDKW45bM3FE"
WEATHER_API_KEY = "5b220e1ef91f97615b018fd0251c2af3"
# ---------------------------------------------------------

@app.route('/')
def index():
    # 1. 날씨 데이터를 가져와서 실시간 추천 로직 가동
    city = "Busan"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        res = requests.get(weather_url).json()
        w_main = res.get('weather', [{}])[0].get('main', 'Clear')
        temp = res.get('main', {}).get('temp', 20)
    except:
        # 에러 발생 시 기본값 설정
        w_main, temp = 'Clear', 20

    # 2. 다차원 음식 데이터베이스 (랜덤 추천용)
    food_db = {
        "Rain": ["파전", "짬뽕", "수제비", "칼국수", "부대찌개", "훠궈"],
        "Snow": ["우동", "어묵탕", "샤브샤브", "라멘", "만두전골"],
        "Clear_Hot": ["냉면", "밀면", "막국수", "물회", "아이스크림"],
        "Clear_Nice": ["파스타", "수제버거", "돈가스", "샌드위치", "초밥"],
        "Chilly": ["돼지국밥", "순대국", "감자탕", "매운탕", "쌀국수"],
        "Cloudy": ["베이커리 카페", "찜닭", "아구찜", "닭갈비", "떡볶이"]
    }

    # 3. 상황별 추천 문구 및 키워드 선정 로직
    if w_main in ['Rain', 'Drizzle', 'Thunderstorm']:
        pick = random.choice(food_db["Rain"])
        msg = "비 오는 날, 빗소리 들으며 이런 음식 어때요? ☔"
    elif w_main == 'Snow':
        pick = random.choice(food_db["Snow"])
        msg = "하얀 눈이 내리네요! 따뜻한 음식을 추천해요 ❄️"
    elif temp >= 27:
        pick = random.choice(food_db["Clear_Hot"])
        msg = "오늘 정말 덥죠? 시원한 음식을 준비했어요 ☀️"
    elif temp <= 10:
        pick = random.choice(food_db["Chilly"])
        msg = "코끝이 찡한 추위! 든든하고 따뜻한 메뉴입니다 🧣"
    elif w_main == 'Clouds':
        pick = random.choice(food_db["Cloudy"])
        msg = "구름이 많아 차분한 날, 이런 메뉴는 어떠세요? ☁️"
    else:
        pick = random.choice(food_db["Clear_Nice"])
        msg = "날씨가 정말 좋아요! 기분 전환용 추천 메뉴입니다 🌈"

    recommend = {"desc": msg, "keyword": pick}
    return render_template('index.html', recommend=recommend, temp=temp, w_main=w_main)

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return redirect('/')

    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    # 1. 네이버 블로그 검색 (텍스트)
    blog_url = f"https://openapi.naver.com/v1/search/blog.json?query={query}&display=6"
    blog_res = requests.get(blog_url, headers=headers).json()
    blog_items = blog_res.get('items', [])

    # 2. 네이버 이미지 검색 (카드 이미지용)
    img_url = f"https://openapi.naver.com/v1/search/image.json?query={query}&display=6"
    img_res = requests.get(img_url, headers=headers).json()
    img_items = img_res.get('items', [])

    # 블로그와 이미지 데이터 매칭
    combined_data = []
    for i in range(len(blog_items)):
        img_src = img_items[i]['link'] if i < len(img_items) else "https://via.placeholder.com/400x300"
        combined_data.append({
            'title': blog_items[i]['title'],
            'link': blog_items[i]['link'],
            'description': blog_items[i]['description'],
            'image': img_src
        })

    # 3. 유튜브 데이터 API 검색 (영상 임베드용)
    # ⚠️ URL 오타 주의: googleapis.com/youtube/v3/search
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}+맛집+리뷰&maxResults=3&type=video&key={YOUTUBE_API_KEY}"
    youtube_res = requests.get(youtube_url).json()
    youtube_items = youtube_res.get('items', [])
    
    video_ids = []
    for video in youtube_items:
        if 'videoId' in video.get('id', {}):
            video_ids.append(video['id']['videoId'])

    return render_template('index.html', items=combined_data, video_ids=video_ids, query=query)

if __name__ == '__main__':
    app.run(debug=True)