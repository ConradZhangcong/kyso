from tkinter import *
from tkinter import ttk
import time
import threading
import pyautogui


class Application:
  timer = None

  def __init__(self, root):
    root.title("kyso - keep your screen on")
    root.geometry("400x200")

    mainframe=ttk.Frame(root, padding=10)
    mainframe.grid(column=4)

    self.__createWidgets(mainframe)
    self.__init_config()
    self.__run_timer()

  def __init_config(self):
    pass

  def __createWidgets(self, frame):
    self.loop_time=IntVar(value=10)
    self.trigger_type=StringVar(value="keyboard")
    self.main_status=StringVar(value="Start")

    ttk.Label(frame, text='keep your screen on').grid(column=0, row=0, columnspan=4)
    
    ttk.Label(frame, text='循环时间(s)').grid(column=0, row=1)
    ttk.Entry(frame,textvariable=self.loop_time).grid(column=1, row=1)

    ttk.Label(frame, text='触发方式').grid(column=0, row=2)
    ttk.Radiobutton(frame, text="键盘", value="keyboard", variable=self.trigger_type).grid(column=1, row=2)
    # ttk.Radiobutton(frame, text="鼠标", value="mouse", variable=self.trigger_type).grid(column=2, row=2)

    ttk.Button(frame, text='test',command=self.__get_config).grid(column=0, row=4)
    ttk.Button(frame, text='Start/Stop', command=self.__trigger_main).grid(column=1, row=4)
    ttk.Button(frame, text='退出', command=self.quit_process).grid(column=2, row=4)

  # 获取配置信息
  def __get_config(self):
    loop_time_val = self.loop_time.get()
    trigger_type_val = self.trigger_type.get()
    main_status_val = self.main_status.get()
    # 返回配置信息
    result = dict({"loop_time":loop_time_val,"trigger_type":trigger_type_val,"main_status":main_status_val})
    print(result)
    return result
    
  # 启动或触发程序的运行
  def __trigger_main(self):
    main_status=self.main_status.get()
    if main_status=="Start":
      # 改变程序状态
      self.main_status.set("Stop")
      # 关闭定时器
      self.__cancel_timer()
    elif main_status=="Stop":
      # 改变程序状态
      self.main_status.set("Start")
      # 打开定时器
      self.__run_timer()

      # 打开定时器
  def __run_timer(self):
    print('__run_timer: trigger timer at: ', time.strftime('%Y-%m-%d %H:%M:%S'))
    pyautogui.press("scrolllock")
    # pyautogui.move(1,1)
    # pyautogui.move(-1,-1)

    loop_time=self.loop_time.get()
    self.timer = threading.Timer(loop_time, self.__run_timer)
    self.timer.start()

  # 关闭定时器
  def __cancel_timer(self):
    print(self.timer)
    if type(self.timer) == threading.Timer:
      print('__cancel_timer: canceled timer')
      self.timer.cancel()
    else:
      print('__cancel_timer: no timer is running')

  # 关闭应用程序
  def quit_process(self):
    print('quit_process')
    self.__cancel_timer()
    # # root.destory()
    raise ApplicationError('Application canceled')

class ApplicationError(RuntimeError):
  pass


root = Tk()
app = Application(root)

try:
  root.mainloop()
except ApplicationError as e:
  print('process exit caused by ApplicationError')
  root.destroy()
except KeyboardInterrupt as e:
  print('process exit caused by KeyboardInterrupt')
  root.destroy()
  app.quit_process()