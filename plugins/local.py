import plugins
from os import listdir
from os.path import isfile, join
import glob


class Local(plugins.Base):

    def play(self, path: str) -> str:
        name = join("local", path)
        return name

    def playlist(self, name: str) -> list[str]:
        path = join("local", name)
        return [name + '/' + f for f in listdir(path) if isfile(join(path, f))]

    def search(self, name: str) -> list[dict[str, str]]:
        s = glob.glob('local/*' + name + '*')
        out = []
        for i in s:
            i = i.removeprefix('local\\')
            item = {"url": i, "title": i}
            out.append(item)
        return out
