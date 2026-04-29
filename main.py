#!/usr/bin/env python3
import argparse
import csv
import os

from dataclasses import dataclass
from typing import Optional

def save(filepath: str, content: list):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        for t in content:
            writer.writerow([t.name, t.start_date, t.end_date, t.priority, t.status])

def read(filepath: str) -> list[Task]:
    tasks = []
    if not os.path.exists(filepath):
        return tasks
    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                tasks.append(Task(
                    name=row[0],
                    start_date=row[1] or None,
                    end_date=row[2] or None,
                    priority=row[3] or None,
                    status=row[4] or None
                ))
    return tasks

@dataclass
class Task:
    name: str
    status: str = "Incomplete"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    priority: Optional[str] = None

    def display(self):
        print(f" {self.name} | {self.start_date} -> {self.end_date} | {self.priority} | {self.status}")

class TaskManager:

    def __init__(self):

        self.filepath = os.path.expanduser("~/Documents/Code_Projects/Doto/tasks.txt")
        self.tasks: list[Task] = read(self.filepath)

    def _find(self, name) -> Optional[Task]:
        for t in self.tasks:
            if t.name == name:
                return t
        return None

    def add_task(self, args):
        task = Task(
            name = args.name,
            start_date = args.start,
            end_date = args.end,
            priority = args.priority
        )
        self.tasks.append(task)
        save(self.filepath, self.tasks)
        print(f"Added Task \"{task.name}\"")
        

    def remove_task(self, args):
        if args.index != None:
            if int(args.index) >= 0 and int(args.index) <= len(self.tasks) - 1:
                self.tasks.pop(int(args.index))
                print(f"Removed task index {args.index}")
            else:
                print(f"Cant find task \'{args.index}\'")

        elif args.name != None:
            target = self._find(args.name)
            if target != None:
                self.tasks.remove(target)
                print(f"Removed {target.name}")
            else: 
                print(f"Cant find task named \"{args.name}\"")

        save(self.filepath, self.tasks)

    def edit_task(self, args):
        target = self._find(args.target)
        
        if target.name != args.name and args.name != None:
            print(f"Set {target.name}'s name to {args.name}")
            target.name = args.name
        if target.start_date != args.start and args.start != None:
            print(f"Set {target.name}'s start date to {args.start}")
            target.start_date = args.start
        if target.end_date != args.end and args.end != None:
            print(f"Set {target.name}'s due date to {args.end}")
            target.end_date = args.end
        if target.priority != args.priority and args.priority != None:
            print(f"Set {target.name}'s priority to {args.priority}")
            target.priority = args.priority
        if target.status != args.status and args.status != None:
            print(f"Set {target.name}'s status to {args.status}")
            target.status = args.status
            

        save(self.filepath, self.tasks)

    def list_tasks(self, args) -> None:
        print("# | name | start -> end | priority")
        print("")
        i = 0
        for t in self.tasks:
            print(f"{i} |", end="")
            t.display()
            i += 1

    def start_tui(self, args) -> None:
        from tui import start
        start()

def get_tasks() -> list["Task"]:
    task_list = read(os.path.expanduser("~/Documents/Code_Projects/Doto/tasks.txt"))
    return task_list

def main():

    manager = TaskManager()

    parser = argparse.ArgumentParser(prog="doto", description="A lightweight todo program that runs in the terminal.")
    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser("add", help="Adds a new task")
    add_parser.add_argument("name", help="The name of the task")
    add_parser.add_argument('-s', '--start', help="The start date of the task")
    add_parser.add_argument('-e', '--end', help="The end date of the task")
    add_parser.add_argument('-p', '--priority', help="The prioirty of the task (Low, Med, High)")
    add_parser.set_defaults(func=manager.add_task)

    remove_parser = subparsers.add_parser("remove", help="Removes a task")
    remove_parser.add_argument('-n', '--name', help="Remove by name of task")
    remove_parser.add_argument('-i', '--index', help="Remove by the index of the task")
    remove_parser.set_defaults(func=manager.remove_task)

    edit_parser = subparsers.add_parser("set", help="Edits an existing task")
    edit_parser.add_argument("target", help="The target task to be edited")
    edit_parser.add_argument('-n', '--name', help="The name of the task")
    edit_parser.add_argument('-s', '--start', help="The start date of the task")
    edit_parser.add_argument('-e', '--end', help="The end date of the task")
    edit_parser.add_argument('-p', '--priority', help="The priority of the task (Low, Med, High)")
    edit_parser.add_argument('-t', '--status', help="The status of the task (Incomplete, Doing, Complete)")
    edit_parser.set_defaults(func=manager.edit_task)

    list_parser = subparsers.add_parser("list", help="Lists the active tasks")
    list_parser.add_argument('-c', '--complete', type=bool, help="Marks a task as complete")
    list_parser.set_defaults(func=manager.list_tasks)

    tui_parser = subparsers.add_parser("tui", help="Opens up the tui")
    tui_parser.set_defaults(func=manager.start_tui)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()