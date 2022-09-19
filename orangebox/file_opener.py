import time
from io import TextIOWrapper
from pathlib import Path
from threading import Lock

TIMEOUT = 30


class FileOpener:

    class _OpenFile:
        file: TextIOWrapper
        last_used: float

        def __init__(self, path: Path):
            print(f'Opening "{path}"')
            path.parent.mkdir(parents=True, exist_ok=True)
            self.last_used = time.monotonic()
            self.file = open(path, "at")

    _openFiles = dict()

    @classmethod
    def append_line_to_file(self, path: Path, text: str):
        if not path in self._openFiles:
            self._openFiles[path] = self._OpenFile(path)
        print(text, file=self._openFiles[path].file)

        # TODO: What is the performance penalty of flushing after every message?
        # TODO: Should we only flush on qos>0 or after a delay or never?
        self._openFiles[path].file.flush()
        self._openFiles[path].last_used = time.monotonic()

    @classmethod
    def cleanup_thread(self):
        to_close = dict()

        # Find all expired files
        for (path, open_file) in self._openFiles:
            if time.monotonic() - open_file.last_used > TIMEOUT:
                to_close[path] = open_file

        # Close them
        for (path, open_file) in to_close:
            print(f'Closing "{path}"')
            del self._openFiles[path]
            open_file.file.close()
