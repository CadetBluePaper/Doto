from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, OptionList, DataTable, Input
from textual.message import Message
from textual.widgets.option_list import Option
from textual.coordinate import Coordinate

from dataclasses import dataclass
import subprocess

from main import get_tasks

class Sections(OptionList):

    def on_mount(self) -> None:
        self.add_options([
            Option("Incomplete", id="incomplete"),
            Option("Doing", id="doing"),
            Option("Complete", id="complete"),
        ])

class TaskData:

    def __init__(self):
        self.task_list: list["Task"] = get_tasks()
        self.HEADER: set(str)  = ("Name", "Start", "End", "Priority", "Status")

        self.incomplete: list["Task"] = []
        self.doing: list["Task"] = []
        self.complete: list["Task"] = []

        self.seperate_status()

        
    def seperate_status(self):
        
        for task in self.task_list:
            if task.status == "Incomplete":
                self.incomplete.append([task.name, task.start_date, task.end_date, task.priority, task.status])
            elif task.status == "Doing":
                self.doing.append([task.name, task.start_date, task.end_date, task.priority, task.status])
            elif task.status == "Complete":
                self.complete.append([task.name, task.start_date, task.end_date, task.priority, task.status])
            else:
                self.incomplete.append([task.name, task.start_date, task.end_date, task.priority, task.status])
        


class TaskManager(App):
    """Task Manager application"""
    CSS_PATH = "layout.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"), 
        ("e", "edit_cell", "Edit Task"),
        ("a", "add_row", "Add Task"),
        ("d", "delete_row", "Remove Task")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sections()
        yield DataTable()
        yield Input(placeholder="Enter a new value: ", id="edit_input")
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "nord"

        data = TaskData()

        table = self.query_one(DataTable)
        table.cursor_type = "cell"
        table.zebra_stripes = True

        self.query_one("#edit_input").display = False
        self.update_table("incomplete")

    def action_add_row(self) -> None:
        table = self.query_one(DataTable)
        new_row = ["New_Task", "-", "-", "-", "-"]
        
        table.add_row(*new_row)
        subprocess.run(["doto", "add", "New_Task"])

        last_row_index = table.row_count - 1
        
        table.move_cursor(row=last_row_index, animate=True)


    def action_delete_row(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            value = str(table.get_cell_at(Coordinate(table.cursor_row, 0)))
            table.remove_row(row_key)

        subprocess.run(["doto", "remove", "-n", str(value)])


    def action_edit_cell(self) -> None:
        table = self.query_one(DataTable)
        edit_input = self.query_one("#edit_input")
        
        edit_input.display = True
        edit_input.focus()

        row_key, col_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        edit_input.value = str(table.get_cell_at(Coordinate(table.cursor_row, 0)))

        self._original_name = str(table.get_cell_at(Coordinate(table.cursor_row, 0)))


    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id:
            self.update_table(event.option_id)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        table = self.query_one(DataTable)
        edit_input = self.query_one("#edit_input")
        
        row_key, col_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        table.update_cell(row_key, col_key, event.value)

        col_label = table.columns[col_key].label.plain

        if col_label == "Name":
            to_set = "-n"
        elif col_label == "Start":
            to_set = "-s"
        elif col_label == "End":
            to_set = "-e"
        elif col_label == "Priority":
            to_set = "-p"
        elif col_label == "Status":
            to_set = "-t"
            
        item_name = self._original_name
        
        subprocess.run(["doto", "set", item_name, to_set, edit_input.value])  

        edit_input.display = False
        edit_input.value = ""
        table.focus()

        

    def update_table(self, category_id: str) -> None:
        
        data = TaskData()
        table = self.query_one(DataTable)

        table.clear()

        if not table.columns:
            table.add_columns(*data.HEADER)

        new_rows = []
        if category_id == "incomplete":
            new_rows = data.incomplete
        elif category_id == "doing":
            new_rows = data.doing
        elif category_id == "complete":
            new_rows = data.complete

        table.add_rows(new_rows)

def start():
    app = TaskManager()
    app.run()
    