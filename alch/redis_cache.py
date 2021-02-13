"""Redis client setup"""
import redis

Client = redis.Redis(host='redis', port=6379, decode_responses=True)
