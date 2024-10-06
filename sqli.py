#
# Finnegan McCarthy
# CS 121
# SQL injection example
#
# Code released under the Do What the Fuck You Want to Public License
#         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#                     Version 2, December 2004 
#
#  Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 
#
#  Everyone is permitted to copy and distribute verbatim or modified 
#  copies of this license document, and changing it is allowed as long 
#  as the name is changed. 
#
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#   0. You just DO WHAT THE FUCK YOU WANT TO.
#


import sqlite3


def main():
    db = sqlite3.connect(":memory:")  # declare this shit in memory because ugh, db files
    # create some data to work with
    data = (
        {"name": "david", "title": "manager 1", "dir_report": "steve", "pay_grade": "mg1-y14", "reports_to": "bob"},
        {"name": "steve", "title": "worker drone 3", "dir_report": "n/a", "pay_grade": "wd3-y1", "reports_to": "david"},
    )
    # put it in
    cur = db.execute(
        "CREATE TABLE real_users(name, title, dir_report, pay_grade, reports_to)"
    )
    cur.executemany(
        "INSERT INTO real_users VALUES(:name, :title, :dir_report, :pay_grade, :reports_to)",
        data
    )

    malicious_injection = "'OR TRUE; --" # INJECT!

    # This is dangerous. Doing this is literally how SQL injection happens
    bad_query = "SELECT * FROM real_users WHERE name = '%s" % malicious_injection

    # This is the right way to do this.
    inop_query = "SELECT * FROM real_users WHERE name = ?"

    # get our demo results
    test_results = cur.execute("SELECT * FROM real_users")
    print(test_results.fetchall())
    mal_results = cur.execute(bad_query) # oh shit we just dumped the whole table
    inop_results = cur.execute(inop_query, (malicious_injection,)) # nothing will happen

    # stdout
    print("### MALICIOUS RESULTS BEGIN ###")
    print(mal_results.fetchall())
    print("### MALICIOUS RESULTS END ###")
    print("### INOP RESULTS BEGIN ###")
    print(inop_results.fetchall())
    print("### INOP RESULTS END ###")


if __name__ == "__main__":
    main()
