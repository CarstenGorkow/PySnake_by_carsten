
REM this file is used to translate the user interface (ui) files to python code
REM htis ui files are created with the QT degsigner

pyuic5 PyQt_Gui\Snake_main_window.ui -o PyQt_Gui\Snake_main_window.py
pyuic5 PyQt_Gui\Widget_Ui_start_game.ui -o PyQt_Gui\Widget_Ui_start_game.py


exit