*** Settings ***
Library     ${CURDIR}/../RobotLockable       lock_folder=.   resource_list_file=${CURDIR}/resource.json    hostname=hostname

*** Test Cases ***
first:
    ${resource1}     lock    hostname=localhost
    ${resource2}     lock    hostname=localhost
    Log     ${resource1}
    Log     ${resource2}
    unlock  ${resource1}
    unlock  ${resource2}
