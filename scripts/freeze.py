from cx_Freeze import setup, Executable

setup(name = "Plotter" ,
      version = "1.0" ,
      description = "" ,
      executables = [Executable("run.py")])