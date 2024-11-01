from environs import Env

env = Env()
env.read_env()

API_Worker = env.str("API_Worker")
API_Trade = env.str('API_Trade')

LOG_CHANNEL = env.str("LOG_CHANNEL")

####PHOTO####
lk_photo = 'https://imgur.com/a/No3qvUx'
my_aktive = 'https://imgur.com/a/qmeVjvU'
about_service = 'https://imgur.com/a/a2jSpoO'
support = 'https://imgur.com/a/NxVlHZN'
verif = 'https://imgur.com/a/8AQppfg'