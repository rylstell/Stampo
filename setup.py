from setuptools import setup

APP = ["stampo.py"]
NAME = "Stampo"

OPTIONS = {
    "iconfile": "images/stampo_icon.icns"
}

setup(
    app = APP,
    name = NAME,
    options = {"py2app": OPTIONS},
    setup_requires = ["py2app"]
)
