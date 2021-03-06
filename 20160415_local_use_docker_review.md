# 20160415 - local in docker (spring-boot + tomcat / use 'Dockerfile')

## 1. 시작에 앞서 docker가 뭘까?
- http://ucpwang.github.io/20160311_docker_study.html

## 2. local in docker (spring-boot + tomcat / use 'Dockerfile')
> 해당 튜토리얼은 'Mac OS X' 환경에서 'Docker Toolbox' 설치 후 진행되었음 (https://docs.docker.com/mac/step_one)

#### 먼저 주워들어야 할것

도커는 '리눅스 커널' 기반으로 동작하는 플랫폼이라서 MAC OSX 에서는 도커 실행 환경 구성이 어려움

(도커 실행 환경을 구성하기 위해서는 도커 엔진 데몬을 실행해야하는데, 이또한 리눅스 커널이 필요함)

하지만, 이를 가능하게 하기 위해 `boot2docker`라는 경량 리눅스 배포판이 배포되었고,

이를 통해서 맥에서도 경량리눅스서버를 가상화하고 도커 엔진 데몬(이하 도커 머신)을 실행하여 도커 실행 환경을 구축할 수 있음

![boot2docker](./images/boot2docker.png)

(이때 필요한게 또 하나 있는데 리눅스가상화를 위한 가상화 장비인 virtualBox 임 -> boot2docker에서 참조함)

#### 'boot2docker'는 알겠고, 그럼 현재는

도커 기술 그룹이 성장해오면서, 공식적으로 `Docker Toolbox`를 지원하면서 도커 실행 환경 구축을 원활하게 하고 있음

(이후 MAC OSX docker에 대한 공식적인 개발도 진행중이라고 함)

---

#### 2-1. 먼저 도커 확인
```bash
$ docker version
Client:
 Version:      1.10.3
 API version:  1.22
 Go version:   go1.5.3
 Git commit:   20f81dd
 Built:        Thu Mar 10 21:49:11 2016
 OS/Arch:      darwin/amd64
Cannot connect to the Docker daemon. Is the docker daemon running on this host?
```
`Cannot connect to the Docker daemon. Is the docker daemon running on this host?` 라고 뜨는걸 보니 도커 머신 실행이 필요함
(혹시 iTerm2 Build 2.9.x 에서 잘안되면 [Mac 에서 iTerm2.app 으로 Docker 하기](https://gist.github.com/ucpwang/ca238b80ee9c5e64567232ffaa7fdd32) 참고)

#### 2-2. Docker Toolbox > Docker Quickstart Terminal 을 통해서 MAC에서 도커 실행 환경을 준비
```
Starting "default"...
(default) Check network to re-create if needed...
(default) Waiting for an IP...
Machine "default" was started.
Waiting for SSH to be available...
Detecting the provisioner...
Started machines may have new IP addresses. You may need to re-run the `docker-machine env` command.
Regenerate TLS machine certs?  Warning: this is irreversible. (y/n): Regenerating TLS certificates
Waiting for SSH to be available...
Detecting the provisioner...
Copying certs to the local machine directory...
Copying certs to the remote machine...
Setting Docker configuration on the remote daemon...


                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/


docker is configured to use the default machine with IP 192.168.99.100
For help getting started, check out the docs at https://docs.docker.com

ucpwang@ucpwang-MacBook-Pro ~
$ docker version
Client:
 Version:      1.10.3
 API version:  1.22
 Go version:   go1.5.3
 Git commit:   20f81dd
 Built:        Thu Mar 10 21:49:11 2016
 OS/Arch:      darwin/amd64

Server:
 Version:      1.10.3
 API version:  1.22
 Go version:   go1.5.3
 Git commit:   20f81dd
 Built:        Thu Mar 10 21:49:11 2016
 OS/Arch:      linux/amd64
```
도커 머신을 띄우고 `docker version`을 확인해보니 `Server:`항목으로 `OS/Arch: linux/amd64` 리눅스 환경이 준비되었음을 확인할 수 있음

#### 2-3. 본격적인 튜토리얼 시작

> 도커 공식 저장소를 통해서 tomcat을 실행하는 도커 이미지를 다운받아서 로컬에서 띄워볼것임 (https://hub.docker.com/_/tomcat/)

`docker pull` 명령을 통해 `tomcat` 도커 이미지를 다운받음
```bash
$ docker pull tomcat
Using default tag: latest
latest: Pulling from library/tomcat
efd26ecc9548: Pull complete
a3ed95caeb02: Pull complete
d1784d73276e: Pull complete
52a884c93bb2: Pull complete
c35f0a4a3a31: Pull complete
d01b68d70ee0: Pull complete
73faba584c67: Pull complete
d4f8ecdef04d: Pull complete
b23bdd8f4c62: Pull complete
Digest: sha256:d2eeba2fc1da6d9a092bd103b69b527196155568b723eb67e0355033f3a3af29
Status: Downloaded newer image for tomcat:latest
```

`docker images` 명령을 통해서 로컬에 설치된 도커 이미지 목록을 볼 수 있음
```bash
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
tomcat              latest              1d71cd869100        12 days ago         357.3 MB
```

이제 설치된 톰캣 도커 이미지를 `docker run` 명령을 통해 8888포트로 띄워볼것임
```bash
$ docker run -it --rm -p 8888:8080 tomcat:latest
...
18-Apr-2016 03:03:54.776 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 62371 ms
```

이제 도커 머신을 실행하고 있는 VM의 IP:8888 으로 접근하여 확인하면되는데

도커 머신의 IP 확인은 다음과 같음
(각자 환경에 따라 다를 수 있음, 더 깊이 얘기하자면 자동으로 할당 받은거고, 특정 IP로 고정 가능)
```bash
$ docker-machine ip
192.168.99.100
```

`192.168.99.100:8888` 요청 화면
![dm-tomcat.png](./images/dm-tomcat.png)

여기까지가 로컬에서 docker를 이용하여 tomcat을 띄워본것임

(`ctrl + c` 하면 도커 인스턴스 자동 종료됨)

#### 2-4. Dockerfile 작성 -> tomcat 위에 샘플 프로젝트 띄우기

이제는 직접 Dockerfile을 작성하여 tomcat 위에 샘플 프로젝트를 띄워볼것임

미리 자바 스프링 부트로 셋팅되어있는 샘플 프로젝트를 준비해두었음 (https://github.com/ucpwang/sample-app.git)

해당 프로젝트를 깃 클론해서 `~/sample-app` 폴더에 위치 시킴
```bash
$ git clone https://github.com/ucpwang/sample-app.git ~/sample-app
```

해당 자바 프로젝트를 maven > clean, package 하여 war 생성
```bash
$ mvn -f ~/sample-app/pom.xml clean package
```

(`~/sample-app/target/sample-app.war` 위치로 생성됨)

로컬에서 그냥 spring-boot로 실행
```bash
$ java -jar ~/sample-app/target/sample-app.war
...
```
(spring-boot로 테스트해봤지만, docker image 내에서는 tomcat에 war배포 할 계획임)

로컬에서 잘되는지 확인
```bash
$ curl localhost:8080/status
OK <------------------- 이게 나와야 정상적으로 올라온거임
```

이제 docker image build 를 위해 `Dockerfile` 생성
```bash
$ vi ~/sample-app/Dockerfile
```

에디터에 아래 내용을 입력
```
FROM java:8-jre
MAINTAINER jacob.c <ghkddbguse@gmail.com>

ENV CATALINA_HOME /usr/local/tomcat
ENV PATH $CATALINA_HOME/bin:$PATH
RUN mkdir -p "$CATALINA_HOME"
WORKDIR $CATALINA_HOME

# see https://www.apache.org/dist/tomcat/tomcat-8/KEYS
RUN set -ex \
	&& for key in \
		05AB33110949707C93A279E3D3EFE6B686867BA6 \
		07E48665A34DCAFAE522E5E6266191C37C037D42 \
		47309207D818FFD8DCD3F83F1931D684307A10A5 \
		541FBE7D8F78B25E055DDEE13C370389288584E7 \
		61B832AC2F1C5A90F0F9B00A1C506407564C17A3 \
		79F7026C690BAA50B92CD8B66A3AD3F4F22C4FED \
		9BA44C2621385CB966EBA586F72C284D731FABEE \
		A27677289986DB50844682F8ACB77FC2E86E29AC \
		A9C5DF4D22E99998D9875A5110C01C5A2F6059E7 \
		DCFD35E0BF8CA7344752DE8B6FB21E8933C60243 \
		F3A04C595DB5B6A5F1ECA43E3B7BBB100D811BBE \
		F7DA48BB64BCB84ECBA7EE6935CD23C10D498E23 \
	; do \
		gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
	done

ENV TOMCAT_MAJOR 8
ENV TOMCAT_VERSION 8.0.33
ENV TOMCAT_TGZ_URL https://www.apache.org/dist/tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz

RUN set -x \
	&& curl -fSL "$TOMCAT_TGZ_URL" -o tomcat.tar.gz \
	&& curl -fSL "$TOMCAT_TGZ_URL.asc" -o tomcat.tar.gz.asc \
	&& gpg --batch --verify tomcat.tar.gz.asc tomcat.tar.gz \
	&& tar -xvf tomcat.tar.gz --strip-components=1 \
	&& rm bin/*.bat \
	&& rm tomcat.tar.gz*

## add application war file
ADD ./target/sample-app.war /sample-app/sample-app.war

## tomcat war deploy
RUN rm -rf $CATALINA_HOME/webapps/ROOT \
    && cp /sample-app/sample-app.war $CATALINA_HOME/webapps/ROOT.war

EXPOSE 8080
CMD ["catalina.sh", "run"]
```
(위 `Dockerfile` 내용은 [도커 공식 이미지 저장소 > tomcat 이미지 저장소](https://hub.docker.com/_/tomcat)를 참고 하였음)

이제 `docker build` 명령을 통해 도커 이미지를 만들어보자
```bash
$ cd ~/sample-app
$ docker build --tag sample-app:0.1 .
...
Successfully built e6856cfe9546
```
`Successfully` 라고 했으니 도커 이미지 빌드가 성공적으로 완료되었다는 것으로 추측할 수 있음

이제 도커 이미지가 생겼을테니 확인 !!
```bash
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
tomcat              latest              1d71cd869100        12 days ago         357.3 MB
java                8-jre               570b0e0945fe        13 days ago         310.9 MB
sample-app          0.1                 e6856cfe9546        7 minutes ago       351 MB
```
('tomcat:latest'는 아까부터 있던애고, 'java:8-jre' 랑 'sample-app:0.1' 가 생긴것이 관전포인트)

그럼 이제 도커 이미지를 실행해 볼 차례

실행은 역시 `docker run` 명령을 이용할거임 (좀더 친절하게 옵션에 대한 설명도 추가하였슴다.)
```bash
# -it : STDIN + pseudo-TTY, --rm : 종료시 컨테이너 자동 제거, -p : 호스트OS <-> 컨테이너 포트 연결, 마지막은 이미지 [REPOSITORY]:[TAG]
$ docker run -it --rm -p 8888:8080 sample-app:0.1

or

# -d : 데몬으로 띄우고, -p : 호스트OS <-> 컨테이너 포트 연결, --name : 이름주고, 마지막은 이미지 [REPOSITORY]:[TAG]
$ docker run -d -p 8888:8080 --name sample-app sample-app:0.1
```
(튜토리얼에서 나오는 docker 명령들은 정말 다양한 옵션으로 활용이 가능하니 필요시 직접 찾아가며 해보도록 하자, 필자는 지금 꼭 필요한 부분에 대한 설명만 적고 넘어갈꺼임)

이제 최종적으로 도커를 통해서 tomcat에 war 배포된 어플리케이션을 확인하며 마무리 :)
```
$ curl http://192.168.99.100:8888/status
OK
```

현재까지는 단순히 로컬에서 돌리던

'자바 스프링 어플리케이션'을 도커 in 톰캣 환경에서 구동해본 것임

> 이것이 Caas(container as a service)의 기초가 될수 있다고 필자는 생각함
