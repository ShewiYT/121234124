from environs import Env

env = Env()
env.read_env()

API_Worker = env.str("API_Worker")
API_Arbitrage = env.str("API_Arbitrage")
API_Casino = env.str("API_Casino")
API_Trade = env.str("API_Trade")

LOG_CHANNEL = env.str("LOG_CHANNEL")

ADMIN = env.str("ADMIN")
