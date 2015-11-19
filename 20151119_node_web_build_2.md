# 20151119 - Node 웹개발 환경 구축 & 어플리케이션 구성 > 2번째 노트
좀더 명확하게 어플리케이션 구성 히스토리를 담기위해, 또 이를 지속 관리하기위해 bower 패키지 매니저를 사용해보았다.

npm > bower 를 설치했다.
```bash
$ npm install bower -g
```

npm > bower-install 을 설치했다.
```bash
$ npm install bower-install -g
```

bower init 을 통해서 bower 사용준비를 했다.
일단 bower를 사용하기 위해 초기화를 해준다.
```bash
$ bower init
```
초기화를 하면 `bower.json`파일을 생성해준다.
여기다 bower로 설치하는 패키지들의 의존성을 관리할수 있게된다. (maven 의 pom.xml 같은 역할)
그리고는 `.bowerrc`파일을 생성한다. 내용은 아래와 같다.
```javascript
{
  "directory": "bower_components",  // bower install path
  "json": "bower.json"              // bower config file path
}
```

## 수다
> 일하다 말고 인터넷 서핑을 잠깐 했는데.. 글쎄 node 개발을 inteliJ로 할수있다고 한다.
> 게다가 편하게 개발할수있다고 한다. (atom + iterm 조합 사용중..)
> 잽싸게 inteliJ로 셋팅해서 잘쓰고있다 :grin:
