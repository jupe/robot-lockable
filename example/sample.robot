*** Settings ***
Library     ${CURDIR}/../RobotLockable       lock_folder=.   resource_list_file=${CURDIR}/resource.json    hostname=hostname

*** Test Cases ***
first:
    ${resource}     lock    hostname=localhost
    ${resource}     lock    hostname=localhost
    Log     ${resource}
    unlock  ${resource}
