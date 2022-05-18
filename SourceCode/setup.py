from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Car Racing Bet 888",
    options = options,
    version = "1.0",
    description = 'First Release',
    executables = executables
)
