echo "Clearing dist"
rm -r dist/*
echo "Freezing with PyInstaller"
pyinstaller --windowed Plotter.spec --hidden-import PyQt5.sip
# echo "Creating temp folder"
# mkdir "dist/Plotter_dmg"
# cp -r "dist/Plotter.app" "dist/Plotter_dmg/Plotter.app"
# ln -s "/Applications" "dist/Plotter_dmg/Applications"
# echo "Creating dmg"
# hdiutil create -volname "Plotter" -srcfolder "dist/Plotter_dmg" -ov -format UDZO "dist/Plotter.dmg"
# echo "Removing temp folder"
# rm -r "dist/Plotter_dmg"
echo "Zipping app"
cd dist
zip Plotter_For_Mac.zip Plotter.app
cd ..
echo "Done"
