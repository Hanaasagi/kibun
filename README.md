# kibun (気分)

通过 [Bosonnlp API](http://bosonnlp.com/) 进行中文语义分析，在每日的 `23:59` 对当日的推文进行分析，得出心情指数并发送一条统计数据  
*`23:59` 为配置文件中时区的时间*

```Bash
# start
➜ git clone https://github.com/Hanaasagi/kibun.git
➜ cd kibun/
➜ python kibun.py
# stop
➜ kill `cat kibun.pid`
```
