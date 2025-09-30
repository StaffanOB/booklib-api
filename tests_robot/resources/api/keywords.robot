*** Settings ***
Library           RequestsLibrary
Resource          ./variables.robot
Resource          ./auth_keywords.robot
Resource          ./books_keywords.robot


*** Keywords ***
Setup User
    Register User
    Login User

Cleanup User
    Delete User
