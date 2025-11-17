*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  pallo
    Set Password  pallo123
    Set Password_Confirmation  pallo123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  p
    Set Password  pallo123
    Set Password_Confirmation  pallo123
    Click Button  Register
    Register Should Fail With Message  Username too short

Register With Valid Username And Too Short Password
    Set Username  pallo123
    Set Password  p
    Set Password_Confirmation  p
    Click Button  Register
    Register Should Fail With Message  Password too short

Register With Valid Username And Invalid Password
    Set Username  pallo123
    Set Password  pallopallo
    Set Password_Confirmation  pallopallo
    Click Button  Register
    Register Should Fail With Message  Password needs to contain symbols

Register With Nonmatching Password And Password Confirmation
    Set Username  pallo123
    Set Password  pallo123
    Set Password_Confirmation  pallo456
    Click Button  Register
    Register Should Fail With Message  Passwords aren't matching

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  pallo123
    Set Password_Confirmation  pallo123
    Click Button  Register
    Register Should Fail With Message  User with username kalle already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password_Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page