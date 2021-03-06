# 2016.03.11 hello docker

## docker 라고 쓰고 도커라 읽는다.
- 도커 : https://www.docker.com/
- 도커 허브(레파지토리) : https://hub.docker.com/
  - Docker 공식 이미지들을 제공
  - 사용자별/팀별/서비스별 이미지 공유장을 마련해줌
  - 공개 저장소(Public Repository), 개인 저장소(Private Repository)
- 추천 도서 : http://pyrasis.com/docker.html

## 개념
- CD <-> CD Driver
- iso, bin, lcd <-> 시디스페이스, 네로버닝룸
- 응용프래그램 <-> windows, lenux

### Immutable Infrastructure 패러다임 : 불변 운영 환경
![그림1](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter01/1.png)

## Docker install
- [맥에서 도커 환경 구축하기](https://docs.docker.com/engine/installation/mac/)
- docker toolbox : https://www.docker.com/products/docker-toolbox
- (비추) boot2docker 로 설치 및 사용하기 : http://blog.saltfactory.net/docker/upgrade-latest-docker-using-with-homebrew.html
  - https://github.com/boot2docker/boot2docker

## Docker 사용해보기
- [local in docker (spring-boot + tomcat / use 'Dockerfile')](http://ucpwang.github.io/20160415_local_use_docker_review.html)
- [가장 빨리 만나는 Docker 3장 Docker 사용해보기](http://pyrasis.com/book/DockerForTheReallyImpatient/Chapter03)

## 활용
### 대략적인 가이드라인
[docker 사용시 겪게되는 기본적인 개발 및 배포 흐름](https://gist.github.com/ucpwang/7bc0acdd5b1cec5b745474793ec940ea)

### Git hook + Docker = deploy
![Git과 Docker로 서버 한 대에 애플리케이션 배포](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter08/1.png)

### 로드 밸런서와 연계한 확장 전개
![로드 밸런서와 연계한 확장 전개](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter19/1.png)

### 개발, 테스트, 운영을 통합
![개발, 테스트, 운영을 통합](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter19/2.png)

### 손쉬운 서비스 이전
![손쉬운 서비스 이전](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter19/3.png)
![손쉬운 서비스 이전 > 클라우드](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter19/4.png)

### 복잡한 아키텍쳐 구성 및 특수성을 띈 라이브러리에 대한 테스트 환경 구축 용이
![복잡한 아키텍쳐 구성 및 특수성을 띈 라이브러리에 대한 테스트 환경 구축 용이](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter19/5.png)

## Docker Registry
- [docker.com > registry](https://docs.docker.com/registry)
- [Docker Registry (1) : 로컬머신에 설치해서 사용하기](https://dobest.io/docker-registry-01-install-on-local-machine/)
- [AWS > EC2 Container Registry](https://aws.amazon.com/ko/ecr/)

## 링크 모음
- [도커 무작정 따라하기 / 슬라이드](http://www.slideshare.net/pyrasis/docker-fordummies-44424016)
- [Docker Machine을 이용하여 Mac에서 docker 운영하기](http://blog.saltfactory.net/docker/running-docker-on-mac-using-with-docker-machine.html)
- [도커 개인 스터디](http://blog.naver.com/alice_k106)
- [도커(Docker) 튜토리얼 : 깐 김에 배포까지](http://blog.nacyot.com/articles/2014-01-27-easy-deploy-with-docker/)
- [Docker 설치 및 구동 무작정 따라하기](http://infoages.tistory.com/1557)
- [시스템엔지니어 성향의 글](http://judekim.tistory.com/15)
