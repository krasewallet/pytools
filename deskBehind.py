#coding:utf-8
from ctypes import *

hwndDesktop = windll.user32.GetDesktopWindow()
hwndProgman = windll.user32.FindWindowExA(hwndDesktop,0,"Progman",0)
windll.user32.SendMessageTimeoutA(hwndProgman,0x052c,0,0,0,1000,None)
hwndWorker = 0
while True:
  hwndWorker = windll.user32.FindWindowExA(hwndDesktop,hwndWorker,"WorkerW",0)
  hwndShellDLL = windll.user32.FindWindowExA(hwndWorker, 0, "SHELLDLL_DefView", 0)
  if hwndShellDLL:
    break
hwndParent = windll.user32.FindWindowExA(0, hwndWorker, "WorkerW", 0)
childHandle = 0x00150520
windll.user32.SetParent(childHandle,hwndParent)