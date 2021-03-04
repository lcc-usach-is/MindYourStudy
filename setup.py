import cx_Freeze
import sys

from sqlite3.dbapi2 import threadsafety, version
import tkinter as tk
from tkinter import ttk
from tkinter.constants import ANCHOR, FLAT, GROOVE, SOLID
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter.font as font
import datetime
import sqlite3
import webbrowser
import re

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("app.py", base=base, icon='assets/favicon.ico')]

cx_Freeze.setup(
    name="Mind your Study",
    options =   {"build_exe":   {   "packages":["tkinter", "sqlite3","PIL"], 
                                    "include_files":["mys_icon.ico","MindYourStudy.db","image.gif","text_bubble.png","chinchilla.png"]
                                }
                },
    version = "0.2",
    description = "Aplicacion para organizar estudios",
    executables = executables
)