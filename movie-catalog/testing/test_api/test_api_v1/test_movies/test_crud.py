from os import getenv

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing."
    raise OSError(msg)
