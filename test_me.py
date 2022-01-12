from pickle_proxy import PickleProx

class YourConfig(object):

    def __init__(self):
        # have defaults
        self.fool = 'fool'
        self.beers = 50

conf = PickleProx(YourConfig, "/tmp/config_store")

# shows defaults or former persisted values
print(" a fool in a bar is still a {}".format(conf.fool))
print(" so the bar still holds '{}' beers".format(conf.beers))

# actualize values in memory and on persistent storage file
conf.fool = conf.fool + " + beer"
conf.beers = conf.beers - 1

conf2 = PickleProx(YourConfig, "/tmp/config_store")

# shows persisted values
print(" a fool in a bar is still a {}".format(conf2.fool))
print(" so the bar still holds '{}' beers".format(conf2.beers))
