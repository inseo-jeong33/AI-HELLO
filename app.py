from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 네이버 API 설정 (본인의 키를 넣으세요)
NAVER_CLIENT_ID = "s5PlfA8iRSiMjKuvzF4s"
NAVER_CLIENT_SECRET = "tmjxQBEp0C"

# 1. 메인 페이지 (맛집 검색 화면)
@app.route('/')
def index():
    return render_template('index.html')

# 2. 맛집 검색 결과 페이지
@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return render_template('index.html')

    url = f"https://openapi.naver.com/v1/search/blog.json?query={query} 맛집&display=10"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    response = requests.get(url, headers=headers)
    items = response.json().get('items', [])
    
    return render_template('index.html', items=items, query=query)

# 3. 멜론 차트 페이지
@app.route('/melon')
def melon():
    url = "https://www.melon.com/chart/index.htm"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    titles = soup.select('.rank01 span a')[:100]
    artists = soup.select('.rank02 span')[:100]
    images = soup.select('.image_typeAll img')[:100]
    
    chart_list = []
    for i in range(len(titles)):
        chart_list.append({
            'rank': i + 1,
            'title': titles[i].text,
            'artist': artists[i].find('a').text if artists[i].find('a') else artists[i].text,
            'image': images[i]['src']
        })
        
    return render_template('melon.html', charts=chart_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)