import sqlite3
conobj=sqlite3.connect(database='bank.sqlite')
curobj=conobj.cursor()

table_1=('''create table if not exists accounts(
accounts_acno integer primary key autoincrement,
accounts_Name text,
accounts_pass text,
accounts_Email text,
accounts_Mobile text,
accounts_Adhar text,
accounts_Pan text,
accounts_DOB text,
accounts_Address text,
accounts_Gender text,
accounts_Nominee text,
accounts_opendate text,
accounts_bal float
)''')

table_2='''create table if not exists stmts(
stmts_acn integer,
stmts_amt float,
stmts_type text,
stmts_date text,
stmts_update_bal float,
stmts_txnid text primary key)
'''


try:
    curobj.execute(table_1)
    curobj.execute(table_2)
    print('table created')
except Exception as msg:
    print(msg)
conobj.close()














