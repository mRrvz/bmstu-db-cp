# Результаты тестирования с Apache Benchmark

```bash
$ ab -n 1000 -c 6 http://localhost/api/v1/rpd/1
```

С балансировкой:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        nginx/1.20.1
Server Hostname:        localhost
Server Port:            80

Document Path:          /api/v1/rpd/1
Document Length:        27452 bytes

Concurrency Level:      6
Time taken for tests:   3.935 seconds
Complete requests:      1000
Failed requests:        121
   (Connect: 0, Receive: 0, Length: 121, Exceptions: 0)
Total transferred:      24290332 bytes
HTML transferred:       24138695 bytes
Requests per second:    254.16 [#/sec] (mean)
Time per request:       23.607 [ms] (mean)
Time per request:       3.935 [ms] (mean, across all concurrent requests)
Transfer rate:          6028.95 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     1   23  52.8      3     428
Waiting:        1   23  52.9      3     428
Total:          1   23  52.8      3     428

Percentage of the requests served within a certain time (ms)
  50%      3
  66%      4
  75%      4
  80%      4
  90%    110
  95%    114
  98%    218
  99%    233
 100%    428 (longest request)
```

Без балансировки:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Finished 1000 requests

Server Software:        Werkzeug/0.16.1
Server Hostname:        localhost
Server Port:            80

Document Path:          /api/v1/rpd/1
Document Length:        27452 bytes

Concurrency Level:      6
Time taken for tests:   25.273 seconds
Complete requests:      1000
Failed requests:        103
   (Connect: 0, Receive: 0, Length: 103, Exceptions: 0)
Total transferred:      24772735 bytes
HTML transferred:       24604213 bytes
Requests per second:    39.53 [#/sec] (mean)
Time per request:       151.788 [ms] (mean)
Time per request:       25.298 [ms] (mean, across all concurrent requests)
Transfer rate:          957.24 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     1   22  48.0      4     324
Waiting:        1   22  48.0      4     324
Total:          1   22  48.0      4     324

Percentage of the requests served within a certain time (ms)
  50%      4
  66%      4
  75%      4
  80%      4
  90%    110
  95%    114
  98%    214
  99%    222
 100%    324 (longest request)
```