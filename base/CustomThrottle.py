import time

from rest_framework.throttling import BaseThrottle, SimpleRateThrottle, ScopedRateThrottle
from rest_framework.settings import api_settings

# 保存访问记录
RECORD = {
    '用户IP': [12312139, 12312135, 12312133, ]
}


# a. 基于用户IP限制访问频率
class CustomThrottle(BaseThrottle):
    ctime = time.time

    def get_ident(self, request):
        """
        根据用户IP和代理IP，当做请求者的唯一IP
        Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
        if present and number of proxies is > 0. If not use all of
        HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.
        """
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        num_proxies = api_settings.NUM_PROXIES

        if num_proxies is not None:
            if num_proxies == 0 or xff is None:
                return remote_addr
            addrs = xff.split(',')
            client_addr = addrs[-min(num_proxies, len(addrs))]
            return client_addr.strip()

        return ''.join(xff.split()) if xff else remote_addr

    def allow_request(self, request, view):
        """
        是否仍然在允许范围内
        Return `True` if the request should be allowed, `False` otherwise.
        :param request:
        :param view:
        :return: True，表示可以通过；False表示已超过限制，不允许访问
        """
        # 获取用户唯一标识（如：IP）

        # 允许一分钟访问10次
        num_request = 10
        time_request = 60

        now = self.ctime()
        ident = self.get_ident(request)
        self.ident = ident
        if ident not in RECORD:
            RECORD[ident] = [now, ]
            return True
        history = RECORD[ident]
        while history and history[-1] <= now - time_request:
            history.pop()
        if len(history) < num_request:
            history.insert(0, now)
            return True

    def wait(self):
        """
        多少秒后可以允许继续访问
        Optionally, return a recommended number of seconds to wait before
        the next request.
        """
        last_time = RECORD[self.ident][0]
        now = self.ctime()
        return int(60 + last_time - now)


# b. 基于用户IP显示访问频率（利用Django缓存）
class CustomSimpleRateThrottle(SimpleRateThrottle):
    # 配置文件定义的显示频率的Key
    scope = "test_scope"  # 配置在settings.py文件REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']中

    def get_cache_key(self, request, view):
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.

        May return `None` if the request should not be throttled.
        """
        if not request.user:
            ident = self.get_ident(request)
        else:
            ident = request.user

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


# c. view中限制请求频率
class CustomScopedRateThrottle(ScopedRateThrottle):

    def get_cache_key(self, request, view):
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.

        May return `None` if the request should not be throttled.
        """
        if not request.user:
            ident = self.get_ident(request)
        else:
            ident = request.user

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

# d. 匿名时用IP限制+登录时用Token限制
class LuffyAnonRateThrottle(SimpleRateThrottle):
    """
    匿名用户，根据IP进行限制
    """
    scope = "luffy_anon"

    def get_cache_key(self, request, view):
        # 用户已登录，则跳过 匿名频率限制
        if request.user:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

class LuffyUserRateThrottle(SimpleRateThrottle):
    """
    登录用户，根据用户token限制
    """
    scope = "luffy_user"

    def get_ident(self, request):
        """
        认证成功时：request.user是用户对象；request.auth是token对象
        :param request:
        :return:
        """
        # return request.auth.token
        return "user_token"

    def get_cache_key(self, request, view):
        """
        获取缓存key
        :param request:
        :param view:
        :return:
        """
        # 未登录用户，则跳过 Token限制
        if not request.user:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }