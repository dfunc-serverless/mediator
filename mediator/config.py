from os import environ


class Config:
    # Config cache
    cache = {}

    @classmethod
    def get(cls, name, default=None):
        """
        Fetch configurations from Environment variables.
        Pattern: DFUNC_<name of var>
        :param name:
        :param default:
        :return: returns content of the variable
        """
        name = "DFUNC_%s" % name.upper()
        if name in cls.cache:
            return cls.cache[name]
        if name in environ:
            val = environ[name]
            cls.cache[name] = val
            return
        elif default is not None:
            return default
        else:
            raise KeyError("Setting %s not found in the environment." % name)
