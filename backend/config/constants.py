UID_LENGTH = 4  # user id length in bytes
LOBBYID_LENGTH = 2  # lobby id length in bytes
COUNTDOWN_SECONDS = 3
# how many clients need to connect to a lobby before starting the game
CLIENT_THRESHOLD = 2
TIME_LIMIT = 900  # 15 minutes lobby time limit after started

# game status
QUEUE = "q"
COUNTDOWN = "c"
ONGOING = "o"
ENDED = "e"

# path
TEXTS_PATH = "data/texts.json"
DB_PATH = "data/users.db"