# NotPy
A command line tool to manage markdown files for taking notes.

## Introduction
NotPy is a tool to help you manage markdown files for taking notes. You can create, edit, and delete notebooks and pages with simple CLI commands. NotPy is built using Python, and it uses some third-party libraries such as `click`, `pathlib`, and `toml`.

## Getting started
To use NotPy, you need to install Python 3.6 or later. To install NotPy, clone the repository and install the requirements:


```

git clone https://github.com/NotPy/notpy.git
cd notpy
pip install -r requirements.txt

```

To start NotPy, you can run the command:

```
python notpy.py
```

You can also run NotPy from anywhere by adding the path to the `notpy.py` file to your system's `PATH` variable.

## Usage
NotPy has four main commands: `ls`, `edit`, `create`, and `delete`.

### `ls`
The `ls` command is used to list notebooks and pages. To list notebooks, use the command:

```
notpy ls nb
```

To list pages in a notebook, use the command:

```
notpy ls pg <notebook_id_or_name>
```

Replace `<notebook_id_or_name>` with the ID or name of the notebook you want to list the pages for.

### `edit`
The `edit` command is used to edit pages. To edit a page, use the command:

```
notpy edit pg <notebook_id_or_name> <page_id_or_name>
```

Replace `<notebook_id_or_name>` with the ID or name of the notebook the page is in, and replace `<page_id_or_name>` with the ID or name of the page you want to edit.

### `create`
The `create` command is used to create notebooks and pages. To create a notebook, use the command:

```
notpy create nb <notebook_id_or_name>
```

Replace `<notebook_id_or_name>` with the ID or name of the notebook you want to create.

To create a page, use the command:

```
notpy create pg <notebook_id_or_name> <page_name>
```

Replace `<notebook_id_or_name>` with the ID or name of the notebook you want to create the page in, and replace `<page_name>` with the name of the page you want to create.

### `delete`
The `delete` command is used to delete notebooks and pages. To delete a notebook, use the command:

```
notpy delete nb <notebook_id_or_name>
```

Replace `<notebook_id_or_name>` with the ID or name of the notebook you want to delete.

To delete a page, use the command:

```
notpy delete pg <notebook_id_or_name> <page_id_or_name>
```

Replace `<notebook_id_or_name>` with the ID or name of the notebook the page is in, and replace `<page_id_or_name>` with the ID or name of the page you want to delete.

## Configuration
NotPy reads its configuration from a JSON file located at `$HOME/.config/notpy/config.json`. You can modify this file to change the default settings for NotPy.

## Contributing
Contributions to NotPy are welcome! If you find a bug, have a feature request, or want to contribute code, please create an issue or a pull request on GitHub.

## License
NotPy is licensed under the GPLv3 License. See the LICENSE file for more information.