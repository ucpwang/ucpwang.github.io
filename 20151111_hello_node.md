2015.11.11 (수) 헬로 node
----

#### hello_node1.js
```javascript
setTimeout(function() {
  console.log("node");
}, 2000);
console.log("hello");
```
```bash
$ node hello_node1.js
hello
node
```

#### hello_node2.js
```javascript
setInterval(function() {
  console.log("hello");
}, 500);
process.addListener("SIGINT", function() {
  console.log("\r\ngood-bye");
  process.exit(0);
});
```
```bash
$ node hello_node2.js
hello
hello
hello
^C
good-bye
```

#### tcp_hello_node.js
```javascript
var http = require("http");
http.createServer(function(req, res) {
  res.writeHead(200, {"Content-Type": "application/json; charset=utf-8"});
  res.write(JSON.stringify({ title: 'Hello Node-!', content: '나는 노드를 보았노라.'}));
  res.end();
}).listen(8000);
```

###### [번외] tcp_hello_node.js 파일을 데몬으로 띄워보자
- 먼저 'forever'를 설치하자 ([github](https://github.com/foreverjs/forever))
```bahs
$ sudo /usr/local/bin/npm install -g forever
```
- 이제 forever를 사용해서 해당 js를 실행하자
```bahs
$ forever start tcp_hello_node.js
warn:    --minUptime not set. Defaulting to: 1000ms
warn:    --spinSleepTime not set. Your script will exit if it does not stay up for at least 1000ms
info:    Forever processing file: tcp_hello_node.js
```
- 데몬으로 수행되는 모습을 볼수 있음


#### sys_test_node.js
```javascript
var spawn = require("child_process").spawn;
var ls = spawn("ls", ["-ls", "./"]);
ls.stdout.addListener("data", function(data) {
  console.log(data);
});
```
```bash
$ node sys_test_node.js
합계 16
4 -rw-rw-r--. 1 ec2-user ec2-user 100 11월 11 02:16 hello_node.js
4 -rw-rw-r--. 1 ec2-user ec2-user 173 11월 11 02:20 hello_node2.js
4 -rw-rw-r--. 1 ec2-user ec2-user 179 11월 11 02:30 sys_test_node.js
4 -rw-rw-r--. 1 ec2-user ec2-user 211 11월 11 02:22 tcp_hello_node.js
```


#### sys_info_process.js
```javascript
console.log(process.env);           // 컴퓨터 환경과 관련된 정보를 가진 객체
console.log(process.version);       // node.js의 버전
console.log(process.versions);      // node.js와 연관된 프로그램들의 버전을 가진 객체
console.log(process.arch);          // 프로세서의 아키텍처(arm/ia32/x64)
console.log(process.platform);      // 플랫폼(win32/linux/sunos/freebsd/darwin)
console.log(process.memoryUsage()); // 메모리 사용 정보를 가진 객체
console.log(process.uptime());      // 현재 프로그램이 실행된 시간
```
