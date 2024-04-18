import sys

from app.view.desktop_view.desktop_view import DesktopView

from app.config import *


if __name__ == "__main__":
    Config.load()
    DesktopView(sys.argv)