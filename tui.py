from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, OptionList, DataTable, Input
from textual.message import Message
from textual.widgets.option_list import Option
from dataclasses import dataclass

class Sections(OptionList):

    def on_mount(self) -> None:
        self.add_options([
            Option("Incomplete", id="incomplete"),
            Option("Doing", id="doing"),
            Option("Complete", id="complete"),
        ])

@dataclass
class TaskData:
    HEADER = ("Name", "Start", "End", "Prority")
    INCOMPLETE =[
        ["incomplete", "date", "date", "None"]
    ]
    DOING = [
        ["doing", "date", "date", "None"]
    ]
    COMPLETE = [
        ["complete", "date", "date", "None"]
    ]

    ##Add communtcation with backend here


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
        new_row = ["New Task", "-", "-", "-"]
        
        table.add_row(*new_row)
        
        last_row_index = table.row_count - 1
        
        table.move_cursor(row=last_row_index, animate=True)

        #commincate with backend

    def action_delete_row(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            table.remove_row(row_key)

        #commincate with backend

    def action_edit_cell(self) -> None:
        table = self.query_one(DataTable)
        edit_input = self.query_one("#edit_input")
        
        edit_input.display = True
        edit_input.focus()

        row_key, col_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        edit_input.value = str(table.get_cell(row_key, col_key))

        #commincate with backend

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id:
            self.update_table(event.option_id)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        table = self.query_one(DataTable)
        edit_input = self.query_one("#edit_input")
        
        row_key, col_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        table.update_cell(row_key, col_key, event.value)
        
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
            new_rows = data.INCOMPLETE
        elif category_id == "doing":
            new_rows = data.DOING
        elif category_id == "complete":
            new_rows = data.COMPLETE

        table.add_rows(new_rows)


if __name__ == "__main__":
    app = TaskManager()
    app.run()