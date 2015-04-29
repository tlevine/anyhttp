import os, unittest

import anyhttp

class CacheBase:
    url = 'this-is-totally-a-website.tld'
    body = 'Body goes here.'

    def setUp(self):
        """Set up anyhttp."""
        self.cache_dir = os.path.join('.anyhttp-test-cache', self.text_or_binary)
        os.makedirs(self.cache_dir, exist_ok = True)
        with open(os.path.join(self.cache_dir, self.url), 'w') as fp:
            fp.write(self.body)

    def test_read_cache(self):
        o = anyhttp._get_cached(self.cache_dir, self.text_or_binary, self.url)
        self.assertEqual(o, self.body)

    def test_write_cache(self):
        import warnings
        warnings.warn('Consider implementing CacheBase.test_write_cache.')

class TestCacheText(CacheBase, unittest.TestCase):
    text_or_binary = 'text'

class TestCacheBinary(CacheBase, unittest.TestCase):
    text_or_binary = 'binary'
