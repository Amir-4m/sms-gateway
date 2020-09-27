from rest_framework import throttling


class ServiceThrottle(throttling.SimpleRateThrottle):
    scope = 'service'

    def get_cache_key(self, request, view):
        if request.auth.get('service') is None:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': request.auth['service']
        }


