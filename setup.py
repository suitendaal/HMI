from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py 1", base=base)]

packages = ["idna", "numpy", "json", "os", "socket", "struct", "sys", "time", "tkinter"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="HMI",
    options=options,
    version="1.0",
    description="Choose between level 1 to 4 to get different levels of HMI supporting systems",
    executables=executables, requires=['numpy']
)


# Doet het niet :(
