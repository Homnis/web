# 中间人关键字参数，指定使用的woker的 URL，对于 RabbitMQ 可以写 amqp://localhost ，对于 Redis 可以写 redis://localhost .
BROKER_URL = 'redis://localhost:6379/1'
# 如果想要保持追踪任务的状态，Celery 需要在某个地方存储或发送这些状态。举例使用后端：Redis。
RESULT_BACKEND = 'redis://localhost:6379/0'
# 任务序列化方式
CELERY_TASK_SERIALIZER = 'json'
# 任务执行结果序列化方式
CELERY_RESULT_SERIALIZER = 'json'
# 任务过期时间
CELERY_RESULT_TASK_EXPIRES = 60 * 60 * 24
# 指定任务接收的内容类型
CELERY_ACCEPT_CONTENT = ['json']
