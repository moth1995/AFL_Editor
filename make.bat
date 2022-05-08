@echo on
pyinstaller --onefile "afl_editor.py" --name "AFL Editor" --noconsole  --version-file file_version_info.txt
pause