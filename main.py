from kivy.uix.actionbar import BoxLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import json
import os

# Class for the managing of the .json file with the tasks
class FileManagement:
    def __init__(self):
        self.file = 'tasks.json'
        self.tasks = []
        self.load_tasks()
    
    # method to create the .json file if it doesn't exist
    def create_file(self):
        if not os.path.exists(self.file):
            with open(self.file, 'w') as file:
                json.dump([], file)
            file.close()

    # method to load the tasks from the .json file # will have to be enhanced later when I start using dates and times and priorities and so on
    def load_tasks(self):
        try:
            with open(self.file, 'r') as file:
                self.tasks = json.load(file)
            file.close()
        except:
            pass
    
    # method to save the tasks to the .json file
    def save_tasks(self):
        with open(self.file, 'w') as file:
            json.dump(self.tasks, file)
        file.close()

    # method for ordering the tasks by date from the most urgent to the least urgent
    def order_tasks(self): # will have to be implemented and tested, because I'm not sure if this will work
        # loading the tasks and sorting them by date
        self.load_tasks()
        #self.tasks.sort(key = lambda x: x['date'])
        # saving the tasks
        self.save_tasks()
    
    # method to add a task to the tasks list
    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()
        # ordering the tasks every time a new task is added
        self.order_tasks()

    # method to delete a task from the tasks list
    def delete_task(self, task):
        # removing the task from the tasks list
        self.tasks.remove(task)
        # removing the widget from the grid layout
        self.save_tasks()

    # creating the task widgets
    def create_task_widgets(self):
        task_widgets = []
        for task in self.tasks:
            task_widgets.append(TaskWidget(task))
        return task_widgets

# class for the task widget
class TaskWidget(GridLayout):
    def __init__(self, task):
        super().__init__()
        self.cols = 3
        self.add_widget(Label(text=task['task name']))
        self.add_widget(Label(text=task['date']))
        self.add_widget(Button(text='Delete', on_press=lambda x: self.delete_task(task)))
    
    def delete_task(self, instance):
        self.parent.delete_task(self)

# this is the main grid layout of the app
class MainGrid(GridLayout):
    def add_task_popup(self):
        popup = Popup(title='Add a task', size_hint=(0.5, 0.5))
        popup_content = BoxLayout(orientation='vertical')
        task = GridLayout(cols=2)
        task.add_widget(Label(text='Task'))
        task.add_widget(TextInput())
        popup_content.add_widget(task)
        date = GridLayout(cols=2)
        date.add_widget(Label(text='Date'))
        date.add_widget(Spinner(text='Select a date', values=('Today', 'Tomorrow', 'Next week', 'Next month'))) # will be enhanced later, this is just for testing that everything else works
        popup_content.add_widget(date)
        buttons = GridLayout(cols=2, size_hint=(1, 0.7))
        buttons.add_widget(Button(text='Cancel', on_press=lambda x: popup.dismiss()))
        buttons.add_widget(Button(text='Add', on_press=lambda x: self.add_task(popup_content)))
        popup_content.add_widget(buttons)
        popup.add_widget(popup_content)
        popup.open()

    def add_task(self, popup_content):
        # this isnt exactly the best but it works...
        task_text = popup_content.children[2].children[0].text
        task_date = popup_content.children[1].children[0].text
        task = {'task': task_text, 'date': task_date, 'status': 'unfinished'}
        print(task + ' added to the tasks')
        self.file_management.add_task(task)

    def set_up(self):
        self.file_management = FileManagement()
        self.file_management.create_file()
        self.file_management.load_tasks()
        self.file_management.order_tasks()
        # adding the tasks to the scroll view of id task_list
        for task in self.file_management.create_task_widgets():
            self.ids.task_list.add_widget(task)

class To_DoApp(App):
    def build(self):
        return MainGrid()
    
if __name__ == '__main__':
    To_DoApp().run()