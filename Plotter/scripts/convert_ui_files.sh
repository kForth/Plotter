cd 'Plotter'
for filename in ui/*.ui; do
    python3 -m "PyQt5.uic.pyuic" "$filename" > "py_${filename%.ui}.py"
done