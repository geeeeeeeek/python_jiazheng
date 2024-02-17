from rest_framework.throttling import AnonRateThrottle


class MyRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "2/min"}
