*** Settings ***
Library     ${CURDIR}/../RobotLockable       lock_folder=.   resource_list_file=example/resource.json    hostname=hostname

*** Test Cases ***
first:
    ${resource}     lock    hostname=localhost
    ${resource}     lock    hostname=localhost
    Log     ${resource}
    sleep    10s
    unlock  ${resource}
