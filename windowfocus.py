import os,sys
import pygetwindow as gw

def find_window_by_name(name):
    for title in gw.getAllTitles():
        if name in title:
            return gw.getWindowsWithTitle(title)[0]
    # Not found
    return None

def focus_window(name):
    "Return a list of processes matching 'name'."
    window = find_window_by_name(name)
    window.activate()
    return

if __name__ == '__main__':
    window_name = sys.argv[1]
    focus_window(window_name)
