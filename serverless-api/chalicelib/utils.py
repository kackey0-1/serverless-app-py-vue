import datetime
from chalice import BadRequestError

def get_timestamp():
  now = datetime.datetime.utcnow()
  return int(now.timestamp())

