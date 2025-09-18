import os, time, shutil

class Logger:

    def __init__(self, directory, name):

        self.file = open(os.path.join(directory, name + ".log"), "a", buffering = 1)

        self.LogLine()
        self.LogBar()
        self.LogLine()
        self.Log(f'[{time.strftime("%Y-%m-%d")}]')
        self.LogLine()
        self.LogTime("Log started")
        self.LogBar()

    def __del__(self):
        if not self.file.closed:
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.file.close()

    def _PrependTime(self, msg):
        return f"[{time.strftime('%H:%M:%S')}] - {msg}"

    def _Bar(self):
        columns, _ = shutil.get_terminal_size(fallback=(80, 0))
        return "-" * columns

    def Close(self):
        self.file.close()

    def Log(self, msg):
        self.file.write(msg + "\n")

    def LogTime(self, msg):
        self.file.write(self._PrependTime(msg) + "\n")

    def PrintLog(self, msg):
        self.file.write(msg + "\n")
        print(msg)

    def PrintTime(self, msg):
        print(self._PrependTime(msg))

    def PrintLogTime(self, msg):
        msg = self._PrependTime(msg)
        self.file.write(msg + "\n")
        print(msg)

    def PrintLine(self):
        print("")

    def LogLine(self):
        self.file.write("\n")

    def PrintLogLine(self):
        print("")
        self.file.write("\n")

    def PrintBar(self):
        print(self._Bar())

    def LogBar(self):
        self.file.write(self._Bar() + "\n")

    def PrintLogBar(self):
        bar = self._Bar()
        print(bar)
        self.file.write(bar + "\n")

    def LogError(self, err):
        self.LogLine()
        self.LogBar()
        self.file.write("|| ERROR:\t" + err + "\n")
        self.LogBar()

    def PrintLogError(self, err):
        self.LogError(err)
        self.PrintLine()
        self.PrintBar()
        print("|| ERROR:\t" + err)
        self.PrintBar()
        self.PrintLine()
