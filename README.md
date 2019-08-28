# K-pop-Idol-Crawling
- python의 beautifulSoup, Selenium을 이용 
- 나무위키와 네이버 인물검색을 통해 한국의 모든 아이돌 그룹과 아이돌 멤버를 크롤링함

- 그룹 : 이름, 사진 url을 저장
- 멤버 : 그룹의 id와 연관시켜 이름, 생년월일, 사진 url을 저장

![image](https://user-images.githubusercontent.com/32324250/63890637-5d05c680-ca1e-11e9-9c80-5c898a419ec5.png)
![image](https://user-images.githubusercontent.com/32324250/63890647-60994d80-ca1e-11e9-8542-f29d6acf1f7a.png)

 


- beautifulSoup : HTML과 XML로부터 데이터를 가져오기 위한 라이브러리
- request : 인터넷 상에 있는 HTMl파일을 읽어옴. HTML 소스를 String으로 변환시켜 변수에 저장
- selenium : 웹 애플리케이션을 위한 테스팅 프레임워크. 자동화를 통해 직접적으로 웹사이트에 접근할 수 있게 해줌. ex) 버튼 클릭, javascript사용
    - webdriver : seleni~~~~um이 사용할 웹 브라우저
