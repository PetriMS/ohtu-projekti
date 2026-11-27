*** Settings ***
Library           robot_library.py
Suite Teardown    Stop Application
Test Setup        Clear References

*** Test Cases ***
Add Book Through The Form
    Add Book    robot-story-book    Test Author    Test Book
    Book Should Be Stored And Visible    robot-story-book    Test Book

Delete Selected Book
    Add Book    robot-delete-book    Test Author    Book To Delete
    Select Book    robot-delete-book
    Delete Selected Book
    Book Should Be Deleted    robot-delete-book
