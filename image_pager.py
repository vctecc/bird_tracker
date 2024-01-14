from pathlib import Path


class ImgPager:
    def __init__(self, folder: Path):
        self.idx = 0
        self.folder = folder
        self.fill_buffer()

    def fill_buffer(self):
        self.buffer = [
            p for p in self.folder.iterdir() if p.suffix in (".jpeg", ".jpg")
        ]

    def get(self, index: int):
        if index > len(self.buffer):
            self.fill_buffer()
        try:
            return self.buffer[index]
        except IndexError:
            return None

    def set(self, idx: int):
        self.idx = idx

    @property
    def next(self):
        idx = self.idx + 1
        if idx >= len(self.buffer):
            self.fill_buffer()
            idx = 0
        return idx

    @property
    def prev(self):
        idx = self.idx - 1
        if idx < 0:
            idx = len(self.buffer) - 1
            self.fill_buffer()
        return idx


if __name__ == "__main__":
    pager = ImgPager(Path("./static/images"))
    for i in range(10):
        print(pager.next)
