*** Settings ***
Library     RobotLockable       lock_folder=.   resource_list_file=example/resource.json    hostname=hostname

*** Test Cases ***
first:
    ${resource}     lock    hostname=localhost
    unlock  ${resource}
