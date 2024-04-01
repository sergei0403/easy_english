import redis


class RedisConnection:
    def __init__(self, redis_url: str):
        """Конструктор"""
        self.url = redis_url

    def __enter__(self):
        """
        Открываем подключение с базой данных Redis.
        """
        self.redis_client = redis.from_url(self.url)
        return self.redis_client

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем подключение.
        """
        self.redis_client.close()
        if exc_val:
            raise
