#!/usr/bin/env python3

'''
Author      : tonybnya <nya.tony2010@gmail.com>
Date        : 2021-07-12
Purpose     : Build an Address Book Management Application with SQLite.

An address book is a book or a database used for storing
contacts. Each contact entry usually consists of standard fields:
name, job, company, email, phone number, address.
'''

import sys
import sqlite3
from sqlite3 import Error


# Define a function to create a connection with the database.
def create_connection(db_file):
    '''
    Create a connection to the SQLite database.
    Arg:
        db_file (database): database file.
    Return:
        con (obj): connection object or None.
    '''

    con = None
    try:
        # Create a connection object to the database.
        con = sqlite3.connect('db_file')
    except Error as e:
        print(e)
    else:
        return con


# Define a function to check if a table exists in the database.
def check_table(table_name, db_file):
    '''
    Function to check if a table exists in the SQLite database.
    Args:
        table_name (table): table name for a database.
        db_file (database): database file.
    Return:
        True: if the table exists.
        False: if the table does not exists.
    '''

    con = create_connection(db_file)
    cur = con.cursor()
    list_table = cur.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table'
        AND name='person';
        """
    ).fetchall()

    if list_table == []:
        return False
    else:
        return True


# Define a function to add a contact to the database.
def add_contact(db_file, query):
    '''
    Function to add a contact to the database.
    Args:
        db_file (database): database file. 
        query (str): string format of the SQL query INSERT.
    Return:
        message to confirm the record.
    '''

    # Call create_connection() and assign it to a variable.
    con = create_connection(db_file)
    # Create a cursor object.
    cur = con.cursor()

    # Call the execute() method to perform SQL.
    # Insert a row of data.
    cur.execute(query)

    # Save (commit) changes.
    con.commit()
    # Close the connection.
    con.close()

    return 'Contact registered successfully!'


# Define a function to consult the list of added contacts.
# The same function is used to view a specific contact.
def view_db(db_file, query):
    '''
    Function to view the contents of the database.
    Args:
        db_file (database): database file.
        query (str): string format of SQL query SELECT *.
    Return:
        rows (list): list of tuples for each row of the database.
    '''

    # Call create_connection() and assign it to a variable.
    con = create_connection(db_file)
    # Create a cursor object.
    cur = con.cursor()

    # Call the execute() method to perform SQL.
    # Select all rows and columns.
    cur.execute(query)
    # Call fetchall() to fetch all the rows.
    rows = cur.fetchall()

    # Save (commit) changes.
    con.commit()
    # Close the connection.
    con.close()

    return rows


# Define a function to delete a contact.
def delete_contact(db_file, query):
    '''
    Function to delete a specific contact.
    Args:
        db_file (database): database file.
        query (str): string format of the SQL query DELETE.
    Return:
        message to confirm the removal.
    '''

    # Call create_connection().
    con = create_connection(db_file)
    # Create a cursor object.
    cur = con.cursor()

    # Call the execute() method to perform SQL.
    cur.execute(query)

    # Save (commit) changes.
    con.commit()
    # Close the connection.
    con.close()

    return 'Contact deleted successfully!'


def main():
    '''Main program.'''

    # Define a neatly heading for the CLI.
    LINE = '+' + '-' * 34 + '+'
    SPACE = ' ' * 9
    HEADING = '|' + SPACE + '+ ADDRESS BOOK +' + SPACE + '|'

    # Define a variable to store the path to the SQLite database.
    db_file = './contacts.db'
    # Initialize a query with empty string.
    query = ''

    # CONDITIONS TO EXECUTE THE SCRIPT WITH RIGHT OPTIONS;
    # sys.arg[1] corresponds to the defined options.

    # Check if the prompt contains right options.
    if len(sys.argv) != 2:
        print('\nUsage: ./abma.py [-a | -v | -s | -d]\n')
    else:
        option = sys.argv[1]
        table = """
        CREATE TABLE person (
            name TEXT NOT NULL,
            job CHAR(50),
            company CHAR(50),
            email CHAR(50),
            phone CHAR(50),
            address CHAR(50)
        );
        """

        if option == '-a':
            while True:
                print('Press ENTER to register a contact.')
                print("Enter 'q' to quit.")

                response = input()

                if response in ('q', 'Q'):
                    sys.exit(1)
                else:
                    name = input('Name > ').title()
                    job = input('Job > ')
                    company = input('Company > ')
                    email = input('Email > ')
                    phone = input('Phone > ')
                    address = input('Address > ')

                    # SQL query to INSERT data in the database.
                    query = f"""
                    INSERT INTO person
                    VALUES (
                        "{name}", "{job}", "{company}",
                        "{email}", "{phone}", "{address}"
                    );
                    """

                    # Check if the table exists into the DB.
                    check = check_table("person", db_file)
                    if check:
                        # Add data to the database.
                        results = add_contact(db_file, query)
                        print(results)
                    else:
                        # Call create_connection().
                        con = create_connection(db_file)
                        # Create a cursor object.
                        cur = con.cursor()

                        # Call the execute() method to create table person.
                        cur.execute(table)

                        # Save (commit) changes.
                        con.commit()
                        # Close the connection.
                        con.close()

                        # Add data to the database with the defined function.
                        results = add_contact(db_file, query)
                        print(results)

        elif option == '-v':
            # SELECT all the contents of the DB.
            query = f'SELECT * FROM person;'

            # Call view_db to SELECT the contents of the DBe.
            rows = view_db(db_file, query)

            if rows == []:
                print('\nThe database is empty.\n')
            else:
                if len(rows) > 1:
                    for i, data in enumerate(rows, start=1):
                        print(f'Contact {i}:')
                        print(f"{'; '.join(data)}")
                        print('-+-+-+-+-+-')
                else:
                    pass

        elif option == '-s':
            # SQL query to SELECT all the contents of the DB.
            query = f'SELECT * FROM person;'
            name = input('Enter a name to view its details:\n: ')
            # Call the function to view the contents of the DB.
            rows = view_db(db_file, query)
            found = []
            for row in rows:
                if name.title() in row[0]:
                    found.append(row)
                else:
                    continue

            if found:
                if len(found) > 1:
                    print('\n-+-+-+-+ Contacts found +-+-+-+-\n')
                    for index, data in enumerate(found, start=1):
                        print(f'{index} >')
                        print(f'Name: {data[0]}')
                        print(f'Job: {data[1]}')
                        print(f'Company: {data[2]}')
                        print(f'Email: {data[3]}')
                        print(f'Phone Number: {data[4]}')
                        print(f'Address: {data[5]}\n')
                    print('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
                else:
                    print('\n-+-+-+-+ Contact found +-+-+-+-\n')
                    print(f'Name: {found[0][0]}')
                    print(f'Job: {found[0][1]}')
                    print(f'Company: {found[0][2]}')
                    print(f'Email: {found[0][3]}')
                    print(f'Phone Number: {found[0][4]}')
                    print(f'Address: {found[0][5]}\n')
                    print('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
            else:
                print(f'No contact {name} in the database.')

        elif option == '-d':
            # SQL query to SELECT all the contents of the DB.
            query = f'SELECT * FROM person;'
            name = input('Enter the name to delete: ')

            # Call the function to view the contents of the DB.
            rows = view_db(db_file, query)
            found = []
            for row in rows:
                if name.title() in row[0]:
                    found.append(row)
                else:
                    continue

            if found:
                if len(found) > 1:
                    print(f'{len(found)} {name.title()} founded in the DB.\n')
                    my_dict = {}
                    for index, data in enumerate(found, start=1):
                        my_dict[index] = data[0]
                    for key, value in my_dict.items():
                        print(f'{key} - {value}')

                    number = int(input('Enter the number to delete > '))
                    if number in my_dict.keys():
                        name = my_dict[number]
                    else:
                        print('Invalid choice.')
                else:
                    name = found[0][0]
            else:
                print(f'No contact {name} in the database.')

            # Define a SQL query to DELETE a row in the DB.
            query = f"""
            DELETE FROM person WHERE name = "{name}";
            """

            results = delete_contact(db_file, query)
            print(results)

        else:
            args = sys.argv[1:]
            print(f"\nOptions '{' '.join(args)}' are not valid.\n")


# The standard boilerplate statement to call the main() function.
if __name__ == '__main__':
    main()
