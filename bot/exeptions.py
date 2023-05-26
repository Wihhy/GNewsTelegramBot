class GNewsServiceException(Exception):
    pass


class NoArticles(GNewsServiceException):
    pass


class ReachedDailyQuota(GNewsServiceException):
    pass


class ConnectionError(GNewsServiceException):
    pass
