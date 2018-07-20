rm -r dist/*
pyinstaller --windowed Plotter.spec --hidden-import PyQt5.sip
