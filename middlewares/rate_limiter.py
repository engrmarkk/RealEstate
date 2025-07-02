from flask import request, redirect, url_for
from connections import redis_conn
from constants import RATE_LIMIT, WINDOW_SECONDS


def rate_limit_check():
    if request.endpoint == "error_blp.too_many_requests":
        return  # don't rate-limit the error page itself

    ip = request.remote_addr
    key = f"ratelimit:{ip}"
    current = redis_conn.get(key)

    if current and int(current) >= RATE_LIMIT:
        return redirect(url_for("error_blp.too_many_requests"))

    pipe = redis_conn.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, WINDOW_SECONDS)
    pipe.execute()
