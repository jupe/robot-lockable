*** Settings ***
Library    Remote    http://127.0.0.1:8270

*** Test Cases ***
first:
    ${resource1}    lock    hostname=localhost
    ${resource2}    lock    hostname=localhost
    Log             ${resource1}
    Log             ${resource2}
    unlock          ${resource1}
    unlock          ${resource2}
