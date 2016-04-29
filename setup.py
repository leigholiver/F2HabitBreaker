import sys
from cx_Freeze import setup, Executable

setup(
    name = "F2HabitBreaker",
    version = "0.1",
    description = "Overlay to cover the All Army button in SC2.",
    options = {'build_exe': {'include_files':['F2HabitBreaker.csv']}},
    executables = [Executable("F2HabitBreaker.py", base = "Win32GUI")])