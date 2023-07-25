#!/usr/bin/env python3
import sys, os

prjPath = os.path.dirname(__file__).split('src')[0]
sys.path.insert(0, prjPath)
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

import src.val_tree.entities.GUI as gui
if '__main__' == __name__:
    x = gui.GUI()