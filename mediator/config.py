from os import environ


class Config:

    @staticmethod
    def get(name, default=None):
        """
        Fetch configurations from Environment variables.
        Pattern: DFUNC_<name of var>
        :param name:
        :param default:
        :return: returns content of the variable
        """
        name = "DFUNC_%s" % name.upper()
        if name in environ:
            return environ[name]
        elif default is not None:
            return default
        else:
            raise KeyError("Setting %s not found in the environment." % name)
