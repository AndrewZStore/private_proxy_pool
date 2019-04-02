"""
维护一个付费代理池
功能：1、保证代理池始终有一定数量的代理
      2、每个代理只能存活一定的时间（默认5分钟）  利用redis数据库的时间
      3、编写代理返回算法（需求：同一个代理尽量在间隔1-3s再继续访问）
      4、代理检测（可省略）。。。

"""
import redis


r = redis.Redis(host='localhost', port=6379)
r.hset('hash', 'test', 'hellow')
r.hset('hash', 'test1', 'hellow1')

class run():
    pass


