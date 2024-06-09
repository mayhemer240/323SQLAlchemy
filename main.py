import logging
from menu_definitions import menu_main, department_select, debug_select
from db_connection import engine, Session
from orm_base import metadata
from Department import Department
from Option import Option
from Menu import Menu

def add_department(session: Session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    # unique constraints: abbreviation, chair_name, room(building/office), description
    unique_name = False
    unique_abbreviation = False
    unique_chair_name = False
    unique_room = False
    unique_description = False
    while not unique_name or not unique_abbreviation or not unique_chair_name or not unique_room or not unique_description:
        name = input("Department Name--> ")
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation = input("Abbreviation--> ")
            abbreviation_count = session.query(Department).filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation. Try again")
            if unique_abbreviation:
                chair_name = input("Chair Name-->")
                chair_name_count: int = session.query(Department).filter(Department.chair_name == chair_name).count()
                unique_chair_name = chair_name_count == 0
                if not unique_chair_name:
                    print("That professor is already chair in another department. Try again.")
                if unique_chair_name:
                    building = input("Building-->")
                    office = input("Office-->")
                    room_count: int = session.query(Department).filter(Department.building == building, Department.office == office).count()
                    unique_room = room_count == 0
                    if not unique_room:
                        print("There's already another department in that room. Try again.")
                    if unique_room:
                        description = input("Description-->")
                        description_count: int = session.query(Department).filter(Department.description == description).count()
                        unique_description = description_count == 0
                        if not unique_description:
                            print("There's already another department with that same description. Try again.")
                    
    newDepartment = Department(name, abbreviation, chair_name, building, office, description)
    session.add(newDepartment)
    session.commit()

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

def select_department(session: Session):
    while True:
        # Prompt user for the unique constraint value(s)
        name = input("Enter the department name: ").strip()
        abbreviation = input("Enter the department abbreviation: ").strip()

        try:
            # Attempt to select the department based on the provided values
            department = session.query(Department).filter_by(name=name, abbreviation=abbreviation).one()
            print(f"Selected Department: {department}")
            return department

        except NoResultFound:
            # If no department is found, inform the user and prompt again
            print("No department found with the provided name and abbreviation. Please try again.")
        except MultipleResultsFound:
            # If multiple departments are found, inform the user and prompt again
            print("Multiple departments found with the provided name and abbreviation. Please refine your search and try again.")

# Example usage:
# with Session(engine) as session:
#     select_department(session)



def select_department_abbreviation(sess: Session)-> Department:
    """
    Select a department by abbreviation
    :return:    The selected department
    """
    found: bool = False
    abbreviation = ""
    while not found:
        abbreviation = input("Enter the department abbreviation-->")
        abbreviation_count: int = sess.query(Department).filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department by that abbreviation. Try again.")
        oldDepartment = sess.query(Department).filter(Department.abbreviation == abbreviation).first()

def select_department_chair(sess: Session) -> Department:
    """
    Select a department by the chair_name - no professor can chair > department
    :param sess:    The connection to the database.
    :return:        The selected department
    """
    found: bool = False
    chair_name = ''
    while not found:
        chair_name = input("Enter the Department chair name--> ")
        chair_name_count: int = sess.query(Department).filter(Department.chair_name == chair_name).count()
        found = chair_name_count == 1
        if not found:
            print("No department by that name.  Try again.")
    oldDepartment = sess.query(Department).filter(Department.chair_name == chair_name).first()
    return oldDepartment

def select_department_room(sess: Session) -> Department:
    """
    Select a department by the room (building and office)
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    building: str = ''
    office: int = 0
    while not found:
        building = input("Enter the building name --> ")
        office = input("Enter the office number-->")
        room_count: int = sess.query(Department).filter_by(Department.building == building, Department.office == office).count()
        found = room_count == 1
        if not found:
            print("No department exists in that room.  Try again.")
    return_department: Department = sess.query(Department).filter(Department.building == building, Department.office == office).first()
    return return_department

def select_department_description(sess: Session)-> Department:
    """
    Select a department by the description
    :return:    The selected department
    """
    found: bool = False
    description: str = ''
    while not found:
        description = input("Enter the department description-->")
        description_count: int = sess.query(Department).filter(Department.description == description).count()
        found = description_count == 1
        if not found:
            print("No department exists with that description. Try again.")
    return_department: Department = sess.query(Department).filter(Department.description == description).first()
    return return_department

def find_department(sess: Session) -> Department:
    """
    Prompt the user for attributes in uniqueness constraints to find the department
    :param sess:    The connection to the database.
    :return:        The instance of Department that the user selected.
                    Note: there is no provision for the user to simply "give up".
    """
    find_department_command = department_select.menu_prompt()
    match find_department_command:
        case "Abbreviation":
            old_department = select_department_abbreviation(sess)
        case "Chair name":
            old_department = select_department_chair(sess)
        case "room": 
            old_department = select_department_room(sess)
        case "description":
            old_department = select_department_description(sess)
        case _:
            old_department = None
    return old_department

def delete_department(session: Session):
    """
    Prompt the user for a department by uniqueness constraint, 
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    oldDepartment = find_department(session)
    session.delete(oldDepartment)

def list_departments(session: Session):
    """
    List all of the departments, sorted by the name.
    :param session:
    :return:
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the department class.
    departments: [Department] = list(session.query(Department).order_by(Department.name))
    for department in departments:
        print(department)

if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
