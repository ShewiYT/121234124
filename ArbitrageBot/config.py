from environs import Env

env = Env()
env.read_env()

API_Arbitrage = env.str("API_Arbitrage")
API_Worker = env.str("API_Worker")

LOG_CHANNEL = env.str("LOG_CHANNEL")