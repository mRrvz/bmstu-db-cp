# Результаты тестирования с Apache Benchmark

```bash
$ ab -n 1000000 -c 20000 http://localhost/api/v1/rpd/1
```

С балансировкой:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100000 requests
Completed 200000 requests
Completed 300000 requests
Completed 400000 requests
Completed 500000 requests
Completed 600000 requests
Completed 700000 requests
Completed 800000 requests
Completed 900000 requests
Completed 1000000 requests
Finished 1000000 requests


Server Software:        nginx/1.19.6
Server Hostname:        localhost
Server Port:            80

Document Path:          /api/v1/rpd/1
Document Length:        169 bytes

Concurrency Level:      20000
Time taken for tests:   870.493 seconds
Complete requests:      1000000
Failed requests:        1003511
   (Connect: 0, Receive: 0, Length: 1003511, Exceptions: 0)
Non-2xx responses:      8594
Total transferred:      3171186 bytes
HTML transferred:       1452386 bytes
Requests per second:    1148.77 [#/sec] (mean)
Time per request:       17409.856 [ms] (mean)
Time per request:       0.870 [ms] (mean, across all concurrent requests)
Transfer rate:          3.56 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 6406 4759.5   4040   20597
Processing:    88 10930 5187.8  13594   20771
Waiting:        0  132 1425.9      0   20276
Total:       3420 17335 1316.9  17393   21306

Percentage of the requests served within a certain time (ms)
  50%  17393
  66%  17598
  75%  17707
  80%  17815
  90%  18289
  95%  20600
  98%  21029
  99%  21108
 100%  21306 (longest request)
```

Без балансировки:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
apr_socket_recv: Connection timed out (110)
Total of 91409 requests completed
```

```bash
$ ab -n 100000 -c 20000 http://localhost/api/v1/rpd/1
```

С балансировкой:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 10000 requests
Completed 20000 requests
Completed 30000 requests
Completed 40000 requests
Completed 50000 requests
Completed 60000 requests
Completed 70000 requests
Completed 80000 requests
Completed 90000 requests
Completed 100000 requests
Finished 100000 requests


Server Software:        nginx/1.19.6
Server Hostname:        localhost
Server Port:            80

Document Path:          /api/v1/rpd/1
Document Length:        169 bytes

Concurrency Level:      20000
Time taken for tests:   89.443 seconds
Complete requests:      100000
Failed requests:        115488
   (Connect: 0, Receive: 0, Length: 115488, Exceptions: 0)
Non-2xx responses:      2292
Total transferred:      845748 bytes
HTML transferred:       387348 bytes
Requests per second:    1118.03 [#/sec] (mean)
Time per request:       17888.587 [ms] (mean)
Time per request:       0.894 [ms] (mean, across all concurrent requests)
Transfer rate:          9.23 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 11523 3587.5  12817   15403
Processing:    54 4203 3727.0   2913   16255
Waiting:        0  332 2171.6      0   15403
Total:      11716 15726 508.0  15792   16530

Percentage of the requests served within a certain time (ms)
  50%  15792
  66%  16002
  75%  16100
  80%  16141
  90%  16213
  95%  16249
  98%  16301
  99%  16349
 100%  16530 (longest request)
```

Без балансировки:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 10000 requests
Completed 20000 requests
Completed 30000 requests
Completed 40000 requests
Completed 50000 requests
Completed 60000 requests
Completed 70000 requests
Completed 80000 requests
Completed 90000 requests
Completed 100000 requests
Finished 100000 requests


Server Software:        nginx/1.19.6
Server Hostname:        localhost
Server Port:            80

Document Path:          /api/v1/rpd/1
Document Length:        169 bytes

Concurrency Level:      20000
Time taken for tests:   151.728 seconds
Complete requests:      100000
Failed requests:        114011
   (Connect: 0, Receive: 0, Length: 114011, Exceptions: 0)
Non-2xx responses:      1207
Total transferred:      445383 bytes
HTML transferred:       203983 bytes
Requests per second:    659.07 [#/sec] (mean)
Time per request:       30345.586 [ms] (mean)
Time per request:       1.517 [ms] (mean, across all concurrent requests)
Transfer rate:          2.87 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 17254 9676.4  15733   65941
Processing:    69 10379 8519.0  10323   28640
Waiting:        0  216 2234.0      0   27507
Total:      13957 27632 7879.5  28265   93470

Percentage of the requests served within a certain time (ms)
  50%  28265
  66%  28462
  75%  28507
  80%  28558
  90%  28659
  95%  28722
  98%  40670
  99%  58880
 100%  93470 (longest request)
```