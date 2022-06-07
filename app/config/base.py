from environs import Env

env = Env()
env.read_env()

SECRET = env.str("SECRET")
DATABASE_URL = env.str("DATABASE_URL")

