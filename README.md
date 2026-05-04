# Doto

A lightweight, terminal-based todo manager. 

## Installation

```bash
git clone https://github.com/yourname/Doto.git
cd Doto
pip install -r requirements.txt
```

Make `doto` available globally (optional):

```bash
sudo ln ~/file_path_to_doto/Doto /usr/local/bin
```

---

## Usage

```
doto <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `add`    | Add a new task |
| `remove` | Remove a task by name or index |
| `set`    | Edit an existing task |
| `list`   | Print all tasks to the terminal |
| `tui`    | Open the TUI |
| `path`   | Change the tasks file location |

---

### `add` — Add a task

```bash
doto add <name> [options]
```

| Flag | Long | Description |
|------|------|-------------|
| `-s` | `--start` | Start date |
| `-e` | `--end`   | Due date |
| `-p` | `--priority` | Priority: `Low`, `Med`, or `High` |

```bash
doto add "Write tests" -s 2024-01-10 -e 2024-01-15 -p High
```

---

### `remove` — Remove a task

```bash
doto remove [-n <name>] [-i <index>]
```

```bash
doto remove -n "Write tests"
doto remove -i 2
```

---

### `set` — Edit a task

```bash
doto set <target> [options]
```

| Flag | Long | Description |
|------|------|-------------|
| `-n` | `--name`     | Rename the task |
| `-s` | `--start`    | Update start date |
| `-e` | `--end`      | Update due date |
| `-p` | `--priority` | Update priority: `Low`, `Med`, `High` |
| `-t` | `--status`   | Update status: `Incomplete`, `Doing`, `Complete` |

```bash
doto set "Write tests" -t Doing
doto set "Write tests" -p Low -e 2024-01-20
```

---

### `list` — List all tasks

```bash
doto list
```

Output format:

```
# | name | start -> end | priority | status

0 | Write tests | 2024-01-10 -> 2024-01-15 | High | Doing
```

---

### `tui` — Interactive TUI

```bash
doto tui
```

| Key | Action |
|-----|--------|
| `e` | Edit the selected cell |
| `a` | Add a new task |
| `d` | Delete the selected task |
| `q` | Quit |

Use the sidebar to switch between `Incomplete`, `Doing`, and `Complete` views.

---

### `path` — Change tasks file location

```bash
doto path ~/Documents/my-tasks.txt
```

The new path is saved to `~/.config/doto` and used automatically on every future run.

---

## File Format

Tasks are stored as plain CSV with the following columns:

```
name, start_date, end_date, priority, status
```

The default location is `~/Doto/tasks.txt`.

---

Thanks for using my stuff :)
