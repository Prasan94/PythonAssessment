"""
"""
if __name__ == "__main__":
    import multiprocessing

def get_cpu_count():
    """
    """
    return multiprocessing.cpu_count()

class SingleTon(object):
    """
    """
    instance = False

    def __new__(cls, *args, **kwargs):
        """
        """
        if not SingleTon.instance:
            SingleTon.instance = object.__new__(cls, *args, **kwargs)
        return SingleTon.instance