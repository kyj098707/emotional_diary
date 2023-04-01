# pip install kiwipiepy

from kiwipiepy import Kiwi as kw
sents = kw()
text = '''프론트엔드 개발의 현재와 미래에 대하여.
프론트엔드 개발은 웹과 앱의 사용자 인터페이스를 설계하고 구현하는 분야로, 시각적 요소와 사용자 경험(UX)을 중시합니다. 최근 몇 년 동안 프론트엔드 개발은 빠른 변화와 함께 기술적 발전을 이루어 왔습니다. 기존에는 HTML, CSS, 자바스크립트와 같은 기본적인 웹 기술만 사용되었지만, 이제는 다양한 프레임워크와 라이브러리를 활용하여 개발이 이루어지고 있습니다.
대표적인 프론트엔드 프레임워크로는 Angular, React, Vue.js 등이 있으며, 이러한 프레임워크들은 개발 속도를 높이고, 유지보수성을 높여주며, 코드의 재사용성을 높이는 데 큰 역할을 합니다. 또한 웹 성능 최적화, 반응형 디자인, 웹 접근성 등 다양한 분야에서 발전을 거듭하고 있습니다.
그리고 웹 개발의 경계가 모바일 앱 개발로 확장되면서, PWA(Progressive Web App)와 같은 기술들도 주목받고 있습니다. PWA는 웹 앱의 장점과 네이티브 앱의 장점을 결합한 기술로, 오프라인 작동, 푸시 알림 등을 지원하며, 높은 성능과 사용자 경험을 제공합니다.
'''

result = sents.split_into_sents(text)

for i in result :
    print(i.text)