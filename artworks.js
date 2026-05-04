// === 리아의 작품 목록 ===
// 편집은 admin.html (편집실) 페이지에서 하세요.
// 서버(server.py)가 실행 중일 때 저장 버튼을 누르면 이 파일이 자동으로 갱신됩니다.
//
// 필드 설명:
//   src         : 이미지 경로 (예: "images/IMG_7358.jpg")
//   title       : 작품 제목
//   date        : 그린 날짜 (예: "2026년 4월")
//   category    : 주제 (가족/자연/동시/일상 등). 비워두면 "기타"로 분류됩니다.
//   description : 작품 설명

const artworks = [
  {
    "src": "images/IMG_7437.jpg",
    "title": "TV",
    "date": "2026년 5월",
    "category": "일상",
    "description": "내가 티비를 보고 접었다."
  },
  {
    "src": "images/IMG_7436.jpg",
    "title": "우주",
    "date": "2026년 5월",
    "category": "자연",
    "description": "내가 도서관에서 빌린 망원경이 있어서 내가 이 그림을 만들기 시작했다."
  },
  {
    "src": "images/IMG_7435.jpg",
    "title": "나",
    "date": "2026년 5월",
    "category": "가족",
    "description": "내가 해이랑 같이 식당에서 그림을 그렸다."
  },
  {
    "src": "images/IMG_7434.jpg",
    "title": "엄마 칭찬메모2",
    "date": "2026년 5월",
    "category": "가족",
    "description": "엄마 한 장 만들어준다고 아까 써놨는데 반 장 한다고 하나 더 있다고 했는데 근데 아까 말했던게 아까꺼고 그리고 아까 말했던게 지금꺼다."
  },
  {
    "src": "images/IMG_7433.jpg",
    "title": "엄마 칭찬 메모",
    "date": "2026년 5월",
    "category": "가족",
    "description": "엄마 칭찬 메모 잘해서 두개 만들어줬는데 두개가 아니고 한 장 반 장에 두개"
  },
  {
    "src": "images/IMG_7395.jpg",
    "title": "언젠간",
    "date": "2026년 4월",
    "category": "동시",
    "description": "내가 엄마랑 아까처럼 두개 만든다고 했는데 이거는 첫번째로 만든거고 아까 본거는 두번째로 만든거다."
  },
  {
    "src": "images/IMG_7394.jpg",
    "title": "자동차",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 접다가 자동차 모양이여서 자동차로 했다."
  },
  {
    "src": "images/IMG_7393.jpg",
    "title": "카드 봉투",
    "date": "2026년 4월",
    "category": "일상",
    "description": "조금 책이랑 비슷하지만 이건 카드 봉투다."
  },
  {
    "src": "images/IMG_7392.jpg",
    "title": "책",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 책을 좋아해서 접었다."
  },
  {
    "src": "images/IMG_7391.jpg",
    "title": "대고 그린 작품",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 이모랑 전화통화할때 서로 뭐를 그렸다. 그때 내가 우리 가족 도구를 가지고 그렸다. 근데 너무 빨대 모양이여가지고 내가 분수에서 빨대가 있어서 울타리랑 있는데서 사람들이랑 같이 먹었다."
  },
  {
    "src": "images/IMG_7390.jpg",
    "title": "말랑말랑 마시멜로우",
    "date": "2026년 4월",
    "category": "동시",
    "description": "엄마랑 대회를 했다. 비오는 날 밖에 나가지 못했지만 그래도 동시가 재미있었다. 근데 엄마랑 대회해가지고 나는 두개, 엄마도 두개 똑같이 다르게 동시를 썼다."
  },
  {
    "src": "images/IMG_7389.jpg",
    "title": "바닷속",
    "date": "2026년 4월",
    "category": "자연",
    "description": "내가 클레이로 뭉치고 푸르고 인어공주 모양을 클레이로 만들었다."
  },
  {
    "src": "images/IMG_7388.jpg",
    "title": "액자",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 액자를 보고 비슷하게 만들었다."
  },
  {
    "src": "images/IMG_7379.jpg",
    "title": "말할 수 있는 마이크",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 미술용품 말할때 쓰는 것을 사가지고 기억이 나서 내가 이 작품을 만들었다."
  },
  {
    "src": "images/IMG_7378.jpg",
    "title": "보석",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 다이아몬드 보석을 접었다. 원래 색종이 접기하는 데에서 내가 접으려고 했는데 너무 어려워서 못접었는데 내가 쉬운걸로 발견했다. 도의가 예전에 친구들 좋다고 보석 접어왔는데 (그때 다이아몬드 보석이였는데) 그거는 쉽지만 너무 안예뻐서, 이건 내가 발견했다."
  },
  {
    "src": "images/IMG_7377.jpg",
    "title": "집",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 집을 골랐는데 지붕집이 제일 쉬워가지고 접었다. 그래도 재밌었다."
  },
  {
    "src": "images/IMG_7376.jpg",
    "title": "라이트",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 라이트를 보고 비슷하게 만들었다."
  },
  {
    "src": "images/IMG_7375.jpg",
    "title": "나",
    "date": "2026년 4월",
    "category": "가족",
    "description": "내가 이상한 나라 엘리스 옷을 나에게 입혔다."
  },
  {
    "src": "images/IMG_7374.jpg",
    "title": "선물포장",
    "date": "2026년 4월",
    "category": "가족",
    "description": "내 엄마가 내 생일에 선물 준거다."
  },
  {
    "src": "images/IMG_7373.jpg",
    "title": "하트, 빛나는 날개",
    "date": "2026년 4월",
    "category": "일상",
    "description": "내가 클레이로 귀엽게 날개랑 하트를 만들었다."
  },
  {
    "src": "images/IMG_7372.jpg",
    "title": "리아의 싸인",
    "date": "2026년 4월",
    "category": "가족",
    "description": "미술 선생님이 준 펜으로 그림을 그리고 맨 위에는 하트나라 내 이름이고, 두번째 있는건 내 싸인이고, 세번째 있는건 클레이로 만든 내 이름이예요."
  },
  {
    "src": "images/IMG_7364.jpg",
    "title": "아빠, 엄마, 나",
    "date": "2026년 4월",
    "category": "가족",
    "description": "내가 미술 선생님이 준 펜으로 엄마, 아빠, 나를 자유롭게 그렸어요."
  },
  {
    "src": "images/IMG_7363.jpg",
    "title": "진주와 빵",
    "date": "2026년 4월",
    "category": "일상",
    "description": "리아가 미국에서 처음으로 클레이로 만들어본 음식.\n맨 밑에 있는 클레이는 그릇이고 그다음에 있는 네모난 것은 빵. 위에 있는건 진주. 아래있는건 크림. 그 안에 있는건 빵."
  },
  {
    "src": "images/IMG_7362.jpg",
    "title": "이모2",
    "date": "2026년 4월",
    "category": "가족",
    "description": "지원이모 뒷그림"
  },
  {
    "src": "images/IMG_7361.jpg",
    "title": "이모",
    "date": "2026년 4월",
    "category": "가족",
    "description": "무지개 컬러로 그린 이모"
  },
  {
    "src": "images/IMG_7360.jpg",
    "title": "동서남북과 무지개",
    "date": "2026년 4월",
    "category": "일상",
    "description": "지구 프로젝트에 동서남북 접기를 가르쳐주는 선생님이 있어서 제가 아는데 한번 접어봤어요."
  },
  {
    "src": "images/IMG_7359.jpg",
    "title": "예쁜 자연 꽃과 잎",
    "date": "2026년 4월",
    "category": "자연",
    "description": "책을 가위로 자른 꽃 모양 작품. 미국 도서관에서 작업. 왜냐면 새책들도 쓰려고 지구프로젝트에 나왔어요."
  },
  {
    "src": "images/IMG_7358.jpg",
    "title": "무지개 로켓",
    "date": "2026년 4월",
    "category": "일상",
    "description": "미국에서 날린 로켓 비슷하게 만든 색종이"
  }
];
