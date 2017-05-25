import inspect
import os


def get_func_name():
    return inspect.currentframe().f_back.f_code.co_name


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise Exception(error_msg)
