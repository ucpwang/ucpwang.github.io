# 2016.03.11 docker 따라해보기

## docker 라고 쓰고 도커라 읽는다.
- 도커 : https://www.docker.com/
- 도커 허브(레파지토리) : https://hub.docker.com/
  - Docker 공식 이미지를 제공
  - 사용자별 이미지 공유
  - 공개 저장소(Public Repository), 개인 저장소(Private Repository)
- 추천 도서 : http://pyrasis.com/docker.html

### Immutable Infrastructure 패러다임 : 불변 운영 환경
![그림1](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter01/1.png)

### Docker install
- [맥에서 도커 환경 구축하기](https://docs.docker.com/engine/installation/mac/)
- docker toolbox : https://www.docker.com/products/docker-toolbox
- (비추) boot2docker 로 설치 및 사용하기 : http://blog.saltfactory.net/docker/upgrade-latest-docker-using-with-homebrew.html
- https://github.com/boot2docker/boot2docker

### Docker 사용해보기
- http://pyrasis.com/book/DockerForTheReallyImpatient/Chapter03

### Dockerfile
- [Dockerfile](http://pyrasis.com/book/DockerForTheReallyImpatient/Chapter07)
- ex
  ```
  FROM ubuntu:14.04
  MAINTAINER Foo Bar <foo@bar.com>

  RUN apt-get update
  RUN apt-get install -y nginx
  RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
  RUN chown -R www-data:www-data /var/lib/nginx

  VOLUME ["/data", "/etc/nginx/site-enabled", "/var/log/nginx"]

  WORKDIR /etc/nginx

  CMD ["nginx"]

  EXPOSE 80
  EXPOSE 443
  ```

### Git hook + Docker = deploy
![Git과 Docker로 서버 한 대에 애플리케이션 배포](http://pyrasis.com/assets/images/DockerForTheReallyImpatientChapter08/1.png)

### Docker Registry
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
