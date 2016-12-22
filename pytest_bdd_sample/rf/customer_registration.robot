*** Settings ***
Library  rf.Litecart
Library  Collections
Suite Setup     init fixtures
Suite Teardown  destroy fixtures


*** Test Cases ***
Customer Registration
    ${old_list}=    get customer ids
    ${customer}=    new valid customer
    register customer   ${customer}
    ${new_list}=    get customer ids
    list should contain sub list   ${new_list}  ${old_list}
    ${old_count}=   get length  ${old_list}
    ${new_count}=   get length  ${new_list}
    should be true  ${old_count} + 1 == ${new_count}