from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
import time
import datetime
# import algorithms.py
from ctypes import *
import uuid

pass_value = 0
save_self = 0
tasks = {}
names = []
ready_tasks = {}

# Initalize backend
backend = cdll.LoadLibrary("./back.so")
backend.create_task.argtypes = [c_uint8, c_uint64, c_uint64]
backend.get_task.restype = c_uint64

backend.initalize(None)
backend.initalize_schedulers()

pass_value = 0
save_self = 0
tasks = {}
names = []
ready_tasks = None

class task:
    def __init__(self, name, description, priority, due_date, estimated_time):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.estimated_time = estimated_time

def create_task(name, description, priority, due_date, estimated_time):
    muuid = uuid.uuid4().int >> 64
    tasks[muuid] = task(name, description, priority, due_date, estimated_time)
    print("______",muuid)
    backend.create_task(priority, due_date, muuid)

class MainWindow(Screen):
    Window.clearcolor = (1, 1, 1, 1)


    def self_save(self):
        global save_self
        save_self = self

    """
    add tasks in order
    """


    def sort_tasks(self):
        for i in range(backend.get_task_list_size()):
            # delete all tasks to add widgets in order
            t = backend.get_task(i)

            if t == 0:
                continue

            try:
                self.delete_task(tasks[t].name)

            except:
                pass

        for i in range(backend.get_task_list_size()):
            t = backend.get_task(i);

            # create layouts
            if t == 0:
                continue

            name = tasks[t].name
            print("name:", name)

            task = Button(text=f'{name}', size_hint=(1, None), height=40, background_color=(1, 1, 1, .4))
            print("+++++++++++++++++++++++++++++++++++++=", tasks[t].estimated_time)

            # due_date_time = datetime.datetime.strptime(tasks[t].estimated_time, "%Y-%m-%d")
            if t == 0:
                continue

            due_date_time = datetime.datetime.strptime(pass_value, "%Y-%m-%d")

            task_id_name = f'{name}_ready'


            self.ids[task_id_name] = task
            self.ids.scroll_ready.height += 40
            task.bind(on_press = lambda x: MainWindow.trigger_popup(tasks[t]))

            checkbox_id_name = f'{name}_ready_checkbox'
            print(checkbox_id_name)

            check = CheckBox(size_hint=(.2, None), height=40)
            self.ids[checkbox_id_name] = check
            print(i)
            check.bind(active = lambda self, x: MainWindow.check_running(self, save_self.ids[checkbox_id_name].active, i))

            # add widgets
            self.ids.ready.add_widget(check)
            self.ids.ready.add_widget(task)



    def add_task(self, task_name, task_description, priority, turn_around_time):
        lst = ["A", "B", "C", "D"]

        # {'name': [description, priority, turn_around_time, pass_value, ]}

        """
        add the task uuid
        """

        pass_value_i = int(time.mktime(datetime.datetime.strptime(pass_value, "%Y-%m-%d").timetuple()))
        print(pass_value, lst.index(priority))
        create_task(str(task_name),str(task_description), int(lst.index(priority)),int(pass_value_i) , int(turn_around_time))
        self.sort_tasks()
        backend.call_scheduler(0)

    # Sotring algorithms used here
    def check_running(self, value, idx):
        address = backend.get_task(idx)
        if address == 0:
            return

        task_name = tasks[address].name
        if value:
            save_self.delete_task(tasks[address].name)
            backend.delete_task(idx)
            # create layouts
            task = Button(text=f'{task_name}', size_hint=(1, None), height=40, background_color=(1, 1, 1, .4))
            task.bind(on_press = lambda x: MainWindow.trigger_popup(tasks[address]))
            print("+++++++++++++++++++++++++++++++++++++=", tasks[address].estimated_time)

            # due_date_time = datetime.datetime.strptime(tasks[t].estimated_time, "%Y-%m-%d")
            task_id_name = f'{task_name}_finished'
            print(task_id_name)


            self.ids[task_id_name] = task

            check = CheckBox(size_hint=(.2, None), height=40, active=True)
            check.bind(active=MainWindow.check_running)


            checkbox_id_name = f'{task_name}_finished_checkbox'


            self.ids[checkbox_id_name] = check


            # add widgets
            #def add_task(self, task_name, task_description, priority, turn_around_time):
            save_self.ids.running.add_widget(check)
            save_self.ids.running.add_widget(task)
            save_self.sort_tasks()

        else:
            task_id_name = f'{task_name}_finished'
            checkbox_id_name = f'{task_name}_finished_checkbox'
            try:
                self.ids.running.remove_widget(self.ids[task_id_name])
                self.ids.running.remove_widget(self.ids[checkbox_id_name])

            except:
                pass

            finally:
                backend.delete_task(idx)
                save_self.sort_tasks()

            #TODO: remove task from finished if it is un checked

    def trigger_popup(address):
        layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=Window.height*1.5)
        scroll_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=layout.height)
        # Make sure the height is such that there is something to scroll.

        pr = ['A', 'B', 'C', 'D']

        info = TextInput(text=f'description:\n    {address.description}\n\npriority: {pr[address.priority]}\nestimated_time: {address.estimated_time} hours\nDue: {pass_value}', font_size=20, pos_hint={'y': -.6}, multiline=True)


        delete_button = Button(text="Remove task", font_size=20, size_hint=(.5, None), height=50)
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, height=scroll_layout.height)

        layout.add_widget(scroll)
        scroll.add_widget(scroll_layout)
        scroll_layout.add_widget(info)
        scroll_layout.add_widget(delete_button)
        popup = Popup(title=f'{address.name}', content=layout, size_hint=(.5, .7))
        delete_button.bind(on_release=lambda x: popup.dismiss(), on_press = lambda x: MainWindow.delete_task(save_self, address.name))
        popup.open()

    def delete_task(self, name):
        save_self.ids.ready.remove_widget(save_self.ids[f'{name}_ready'])
        save_self.ids.ready.remove_widget(save_self.ids[f'{name}_ready_checkbox'])

    #if checkbox checked =>
    """
    #shouldn't be needed

    def ready_queue(self):
        print(ready_tasks)

        if len(ready_tasks) == 0:
            global dialog
            dialog = MDDialog(title="No tasks to choose from", text="Please add tasks to choose from", buttons=[MDRectangleFlatButton(text="Ok", text_color=(63/255, 135/255, 242/255, 1), on_release=self.close_warning)])
            dialog.open()
            return 0

        else:
            for i in ready_tasks:
                self.ids.ready.remove_widget(self.ids[f'{i}_ready'])
                self.ids.ready.remove_widget(self.ids[f'{i}_ready_checkbox'])

                task = Button(text=f'{i}', size_hint=(1, None), height=40, background_color=(1, 1, 1, .4))
                task.bind(on_press = lambda x: MainWindow.trigger_popup(i))

                check = Button(text="<", font_size = 20, size_hint=(.4, None), height=40, background_color=(1, 1, 1, .4))
                check.bind(on_active= lambda x: ready_tasks.append(tasks[i]), on_deactive= lambda x: ready_tasks.pop(i))
                self.ids.scroll_ready.height += 40

                self.ids.running_tasks.add_widget(check)
                self.ids.running_tasks.add_widget(task)
"""


class WindowManager(ScreenManager):
    pass

Window.size = (1200, 620)
kv = Builder.load_file('app_UI.kv')


class Smart_Scheduler(MDApp):
    # create a class named app which inherits the App lib

    def build(self):
        return kv
        # create the layoutadd_widget

    def on_save(self, instance, value, date_range):
        global pass_value
        pass_value = str(value)
        print(pass_value)

    def on_cancel(self, instance, value):
        return 0

    def pick_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_cancel=self.on_cancel, on_save=self.on_save)
        date_dialog.open()

    def submit(self, task_name, task_description, priority, turn_around_time):
        #warning ready to open
        global dialog
        dialog = MDDialog(title="Incomplete information", text="Please fill in task name, priority and the due date", buttons=[MDRectangleFlatButton(text="Ok", text_color=(63/255, 135/255, 242/255, 1), on_release=self.close_warning)])

        if task_name and priority and pass_value:
            MainWindow.add_task(save_self, task_name, task_description, priority, turn_around_time)


        else:
            dialog.open()

    def close_warning(self, obj):
        dialog.dismiss()
        return 0

    #call the Mainwindow function for access to ids
    def trigger_add_task():
        MainWindow.add_task(save_self, task_name, task_description, priority, turn_around_time)

    def trigger_ready_queue(self):
        MainWindow.ready_queue(save_self)


if __name__ == '__main__':
    Smart_Scheduler().run()
