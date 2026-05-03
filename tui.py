from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, OptionList, DataTable, Input
from textual.widgets.option_list import Option
from textual.coordinate import Coordinate

import subprocess

from main import get_tasks

TASK_FLAGS: dict[str, str] = {
    "Name":     "-n",
    "Start":    "-s",
    "End":      "-e",
    "Priority": "-p",
    "Status":   "-t",
}

class Sections(OptionList):

    def on_mount(self) -> None:
        self.add_options([
            Option("Incomplete", id="incomplete"),
            Option("Doing",      id="doing"),
            Option("Complete",   id="complete"),
        ])


class TaskData:

    def __init__(self):
        self.task_list: list = get_tasks()

        self.HEADER: tuple[str, ...] = ("Name", "Start", "End", "Priority", "Status")

        self.incomplete: list[list] = []
        self.doing:      list[list] = []
        self.complete:   list[list] = []

        self.separate_status()

    def separate_status(self):
        for task in self.task_list:
            row = [task.name, task.start_date, task.end_date, task.priority, task.status]
            if task.status == "Doing":
                self.doing.append(row)
            elif task.status == "Complete":
                self.complete.append(row)
            else:
                self.incomplete.append(row)


class TaskManager(App):
    """Task Manager application"""
    CSS_PATH = "layout.tcss"
    BINDINGS = [
        ("q", "quit",       "Quit"),
        ("e", "edit_cell",  "Edit Task"),
        ("a", "add_row",    "Add Task"),
        ("d", "delete_row", "Remove Task"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sections()
        yield DataTable()
        yield Input(placeholder="Enter a new value: ", id="edit_input")
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "nord"

        self._data = TaskData()
        self._current_category = "incomplete"

        table = self.query_one(DataTable)
        table.cursor_type = "cell"
        table.zebra_stripes = True

        self.query_one("#edit_input").display = False
        self._render_table("incomplete")

    def _reload_data(self) -> None:
        self._data = TaskData()
        self._render_table(self._current_category)

    def _render_table(self, category_id: str) -> None:
        self._current_category = category_id

        table = self.query_one(DataTable)
        table.clear()

        if not table.columns:
            table.add_columns(*self._data.HEADER)

        rows = {
            "incomplete": self._data.incomplete,
            "doing":      self._data.doing,
            "complete":   self._data.complete,
        }.get(category_id, [])

        table.add_rows(rows)

    def action_add_row(self) -> None:
        table = self.query_one(DataTable)
        new_row = ["New_Task", "-", "-", "-", "-"]
        table.add_row(*new_row)
        subprocess.run(["doto", "add", "New_Task"])
        last_row_index = table.row_count - 1
        table.move_cursor(row=last_row_index, animate=True)
        self._reload_data()

    def action_delete_row(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            value = str(table.get_cell_at(Coordinate(table.cursor_row, 0)))
            table.remove_row(row_key)
            subprocess.run(["doto", "remove", "-n", str(value)])
            self._reload_data()

    def action_edit_cell(self) -> None:
        table = self.query_one(DataTable)
        edit_input = self.query_one("#edit_input", Input)

        edit_input.display = True
        edit_input.focus()

        edit_input.value = str(table.get_cell_at(Coordinate(table.cursor_row, 0)))
        self._original_name = str(table.get_cell_at(Coordinate(table.cursor_row, 0)))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id:
            self._render_table(event.option_id)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        table = self.query_one(DataTable)
        edit_input = self.query_one("#edit_input", Input)
        edit_input.value = ""

        row_key, col_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        table.update_cell(row_key, col_key, event.value)

        col_label = table.columns[col_key].label.plain

        to_set = TASK_FLAGS.get(col_label)
        if to_set is None:
            edit_input.display = False
            edit_input.value = ""
            table.focus()
            return

        subprocess.run(["doto", "set", self._original_name, to_set, edit_input.value])

        edit_input.display = False
        edit_input.value = ""
        table.focus()

        self._reload_data()


def start():
    app = TaskManager()
    app.run()
