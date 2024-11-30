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
import datetime

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
    def order_tasks(self):
        self.load_tasks()
        # creating a temporary list to store the tasks with no date
        #no_date_tasks = []
        #for task in self.tasks:
        #    if task['date'] == 'No date':
        #        no_date_tasks.append(task)
        # now removing the tasks with no date from the tasks list, this cannot be done in the for loop above, because it will skip some tasks
        #for task in no_date_tasks:
        #    self.tasks.remove(task)
        # ordering the tasks list by date, for now only by day, month and year, hours and minutes will be added later
        #self.tasks = sorted(self.tasks, key=lambda x: datetime.datetime.strptime(x['date'], '%d %m %Y'))
        # adding the tasks with no date to the end of the list
        #for task in no_date_tasks:
        #    self.tasks.append(task)
        # saving the tasks
        self.save_tasks()
    
    # method to add a task to the tasks list
    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()
        self.order_tasks()
        # ordering the tasks every time a new task is added
        #self.order_tasks()
        #print("tasks ordered")
        # re-adding the tasks to the scroll view
        # this has to be done here, so the widgets will become ordered the same way as the now ordered tasks
        #MainGrid().ids.task_list.clear_widgets()
        #for task in self.create_task_widgets():
        #    MainGrid().ids.task_list.add_widget(task)

    # method to delete a task from the tasks list
    def delete_task(self, task):
        # removing the task from the tasks list
        self.tasks.remove(task)
        print(self.tasks)
        # removing the widget from the grid layout
        self.save_tasks()

    # creating the task widgets
    def create_task_widgets(self):
        task_widgets = []
        for task in self.tasks:
            task_widgets.append(TaskWidget(task))
            #print("task widget created")
        return task_widgets

# class for the task widget
class TaskWidget(GridLayout):
    def __init__(self, task):
        super().__init__()
        self.cols = 4
        self.file_m= FileManagement()
        self.add_widget(Label(text=task['task name']))
        self.add_widget(Label(text=task['date']))
        if task['status'] == 'unfinished':
            self.add_widget(Spinner(text='unfinished', values=('unfinished', 'finished'), on_press=lambda x: self.update_status(task)))
        else:
            self.add_widget(Spinner(text='finished', values=('finished', 'unfinished'), on_press=lambda x: self.update_status(task)))
        self.add_widget(Button(text='Info', on_press=lambda x: self.open_popup(task)))

    # method to update the status of a task
    def update_status(self, task):
        if task['status'] == 'unfinished':
            self.file_m.tasks[self.file_m.tasks.index(task)]['status'] = 'finished'
        else:
            self.file_m.tasks[self.file_m.tasks.index(task)]['status'] = 'unfinished'
        self.file_m.save_tasks()
    
    # method to delete a task
    def delete(self, task, popup):
        popup.dismiss()
        #print(len(self.file_m.tasks))
        # removing the task from the file
        #print(self.file_m.tasks)
        self.file_m.delete_task(task)
        #print(self.file_m.tasks)
        # removing the widget from the grid layout
        self.parent.remove_widget(self)
        # resizing the scroll view
        MainGrid().ids.task_list.size_hint_y = None
        MainGrid().ids.task_list.height = len(self.file_m.tasks) * 75
        #print(len(self.file_m.tasks))
        #print("task deleted")

    # method to open a popup with the tasks complete and detailed information
    def open_popup(self, task):
        popup = Popup(title='Task Information', size_hint=(0.5, 0.5))
        popup_content = BoxLayout(orientation='vertical')
        task_name = GridLayout(cols=2)
        task_name.add_widget(Label(text='Task Name'))
        task_name.add_widget(Label(text=task['task name']))
        popup_content.add_widget(task_name)
        task_description = GridLayout(cols=2)
        task_description.add_widget(Label(text='Description'))
        task_description.add_widget(Label(text=task['description']))
        popup_content.add_widget(task_description)
        task_date = GridLayout(cols=2)
        task_date.add_widget(Label(text='Date'))
        task_date.add_widget(Label(text=task['date']))
        popup_content.add_widget(task_date)
        task_status = GridLayout(cols=2)
        task_create_date = GridLayout(cols=2)
        task_create_date.add_widget(Label(text='Created on'))
        task_create_date.add_widget(Label(text=task['created_on']))
        popup_content.add_widget(task_create_date)
        task_status.add_widget(Label(text='Status'))
        task_status.add_widget(Label(text=task['status']))
        popup_content.add_widget(task_status)
        buttons = GridLayout(cols=2, size_hint=(1, 0.7))
        buttons.add_widget(Button(text='Delete', on_press=lambda x: self.delete(task, popup)))
        buttons.add_widget(Button(text='Close', on_press=lambda x: popup.dismiss()))
        popup_content.add_widget(buttons)
        popup.add_widget(popup_content)
        popup.open()

# this is the main grid layout of the app
class MainGrid(GridLayout):
    # method to get the current date and time
    def get_current_date_time(self):
        current_date_time = datetime.datetime.now()
        #print("The current date and time is: " + str(current_date_time))
        return current_date_time
    
    # method to open a popup to add a task
    def add_task_popup(self):
        popup = Popup(title='Add a task', size_hint=(0.5, 0.5))
        popup_content = BoxLayout(orientation='vertical')
        task = GridLayout(cols=2, size_hint=(1, 0.7))
        task.add_widget(Label(text='Name'))
        task.add_widget(TextInput())
        popup_content.add_widget(task)
        description = GridLayout(cols=2)
        description.add_widget(Label(text='Description'))
        description.add_widget(TextInput())
        popup_content.add_widget(description)
        date = GridLayout(cols=4, size_hint=(1, 0.7))
        date.add_widget(Label(text='Date'))
        year_values = []
        month_values = []
        day_values = []
        for i in range(self.get_current_date_time().year, self.get_current_date_time().year + 10):
            year_values.append(str(i))
        self.year = Spinner(text="year", values=(year_values))
        date.add_widget(self.year)
        self.month = Spinner(text="month", values=(month_values))
        date.add_widget(self.month)
        self.day = Spinner(text="day", values=(day_values))
        date.add_widget(self.day)
        popup_content.add_widget(date)
        # I swear to God, these two lines of code took like 30 minutes, because of the on_event thing
        self.month.on_press = lambda x =0: self.update_month_values()
        self.day.on_press = lambda x=0: self.update_day_values()

        buttons = GridLayout(cols=2, size_hint=(1, 0.7))
        buttons.add_widget(Button(text='Cancel', on_press=lambda x: popup.dismiss()))
        buttons.add_widget(Button(text='Add', on_press=lambda x: self.add_task(popup_content, popup)))
        popup_content.add_widget(buttons)
        popup.add_widget(popup_content)
        popup.open()
    
    # method that updates the month values based on the selected year
    # if the year is the current year, the month values will be from the current month to December
    def update_month_values(self):
        #print("updating month values")
        if self.year.text == str(self.get_current_date_time().year) or self.year.text == 'year':
            month_values = [str(i) for i in range(self.get_current_date_time().month-1, 13)]
        else:
            month_values = [str(i) for i in range(1, 13)]
        self.month.values = month_values
        #print("new month values: " + str(month_values))

    # method that updates the day values based on the selected month
    # if the month is the current month, the day values will be from the current day to the last day of the month
    def update_day_values(self):
        if self.month.text == str(self.get_current_date_time().month) or self.month.text == 'month':
            day_values = [str(i) for i in range(self.get_current_date_time().day, 32)]
        else:
            day_values = [str(i) for i in range(1, 32)]
        self.day.values = day_values
        #print("new day values: " + str(day_values))

    # method to add a task to the tasks list
    def add_task(self, popup_content, popup):
        popup.dismiss()
        # getting the information from the popup
        task_name = ""
        if popup_content.children[3].children[0].text != '':
            task_name = popup_content.children[3].children[0].text
        else:
            task_name = 'No name'
        #print(task_name)
        task_description = ""
        if popup_content.children[2].children[0].text != '':
            task_description = popup_content.children[2].children[0].text
        else:
            task_description = 'No description'
        #print(task_description)
        task_date = ""
        #print(popup_content.children[1].children[0].text)
        if popup_content.children[1].children[0].text == 'day' and popup_content.children[1].children[1].text == 'month' and popup_content.children[1].children[2].text == 'year':
            task_date = 'No date'
        else:
            if popup_content.children[1].children[0].text != 'day':
                task_date += popup_content.children[1].children[0].text + ' '
            else:
                task_date += str(self.get_current_date_time().day) + ' '
            if popup_content.children[1].children[1].text != 'month':
                task_date += popup_content.children[1].children[1].text + ' '
            else:
                task_date += str(self.get_current_date_time().month) + ' '
            if popup_content.children[1].children[2].text != 'year':
                task_date += popup_content.children[1].children[2].text + ''
            else:
                task_date += str(self.get_current_date_time().year) + ''
        #print(task_date)
        creation_date = self.get_current_date_time().strftime('%d %m %Y')
        task = {'task name': task_name, 'description': task_description, 'date': task_date,'created_on': creation_date ,'status': 'unfinished'}
        #print(str(task) + ' added to the tasks')
        # adding the task to the file
        self.file_management.add_task(task)

    # method to load the tasks from the file and add them to the scroll view
    def set_up(self):
        self.file_management = FileManagement()
        self.file_management.create_file()
        self.file_management.load_tasks()
        #self.file_management.order_tasks()
        # adding the tasks to the scroll view
        for task in self.file_management.create_task_widgets():
            self.ids.task_list.add_widget(task)
        # modifying the scroll view to be as big as all the tasks inside combined
        #self.ids.task_list.size_hint_y = None
        #self.ids.task_list.height = len(self.file_management.tasks) * 75

    # method to change the light mode
    def change_mode(self):
        pass

# the main app class
class To_DoApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    To_DoApp().run()