from environs import Env

env = Env()
env.read_env()

API_Worker = env.str("API_Worker")
API_Casino = env.str('API_Casino')
admin = env.str('ADMIN')

LOG_CHANNEL = env.str("LOG_CHANNEL")