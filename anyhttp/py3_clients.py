"""Module for clients which use Python 3 syntax."""
import anyhttp


class aiohttp(anyhttp.Http):

    def raw_worker(self, url):
        response = yield from self.package.request('GET', url)
        return (yield from response.read())

    def raw(self, url):
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.raw_worker(url))


class yieldfrom(anyhttp.HostPortConnectionClass):

    cls = 'HTTPConnection'

    def raw_worker(self, url):
        path = self.get_path(url)
        r = (yield from self.http.request('GET', path))
        result = (yield from self.http.getresponse())
        return (yield from result.read())

    def raw(self, url):
        self.cls_init(url)
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.raw_worker(url))
