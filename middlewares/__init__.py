from .maintenance import maintenance_check
from .rate_limiter import rate_limit_check


def register_middlewares(app):
    @app.before_request
    def enforce_maintenance():
        return maintenance_check()

    @app.before_request
    def enforce_rate_limit():
        return rate_limit_check()
