
from Menu import Menu
from Option import Option
"""
Declares menues, changed from professors code. 
Two main functions changed - menu_main which prompts user
what to do with database, and department_select which decides
how user will select the department wether searching or deleting
"""

# The main options for operating on Departments.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add Department", "add_department(sess)"),
    Option("Delete department", "delete_department(sess)"),
    Option("Search for a department", "find_department(sess)"),
    Option("List all departments", "list_departments(sess)"),
    Option("Exit", "pass")
])

# A menu for how the user will specify which department they want to access,
# based on uniqueness constraints
department_select = Menu('department select', 'Please select how you want to select a department:', [
    Option("Abbreviation", "Abbreviation"),
    Option("Chair name", "chair_name"),
    Option("Description", "description")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])
