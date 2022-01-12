# Proxy Class for Pickle

Proxy your attribute gets & sets through it to have it backed by pickle persistent storing automatically:

```
from pickleprox import PickleProx

# have a class holding attributes you want to cover
class YourConfig(object):

    def __init__(self):
        # have defaults
        self.bar = 'bar'

# wrap it into the pickle proxy
conf = PickleProx(YourConfig, "/tmp/config_storage")

# reading values like plain attributes (defaults or formerly persisted ones)
print(conf.bar) 

# writing values like plain attributes (which will result in persisting under the hood)
conf.bar = "no bar no beer"

```