class package_checker(Exception):
    def __init__(self):
        pass

    def check(self, packages: list):
        from importlib import import_module
        notinstalled = []
        installed = []
        for package in packages:
            try:
                import_module(package)
            except ImportError:
                notinstalled.append(package)
            installed.append(package)
        if notinstalled == []: result = True
        else: result = False
        return {"installed": installed, "notinstalled": notinstalled, result: result}


class logger(Exception):
    def __init__(self, logfile = "log.txt"):
        # Check logfile is str
        if type(logfile) != str:
            raise TypeError("logfile must be a string")

        pass

    def log(self, message: str):
        print(message)

    def loadfile(self, logfile: str):
        files = self.getfilelist(self.conf["logpath"])

        pass


    def get_filelist(path: str):
        import os
        filelist = []
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                filelist.append(file)
        return filelist