import sqlite3

conn=sqlite3.connect('foodbotdb.sqlite')
cur=conn.cursor()




choice=input("1.add user\t2.add food\nchoice:")
if choice=='1':
    count=int(input('how many users u wanna enter?'))
    while count>0:
        user_name=input('name-')
        phone_no=input('ph no-')
        cur.execute('''INSERT INTO users (name,no,payed,total_amount)VALUES(?,?,'n',0)''',(user_name,phone_no,))
        cur.execute('INSERT INTO foodlist (no) VALUES (?)',(phone_no,))
        #  here add LOGIC to make all foodlist values zero for this no
        try:
            cur.execute('SELECT fname FROM fprice')
            fname=cur.fetchall()
            for f in fname:
                item=f[0]
                cur.execute('UPDATE foodlist SET '+item+"=0 WHERE no='"+phone_no+"'")
                conn.commit()
        except:
            pass

        conn.commit()
        count=count-1
        
elif choice=='2':
    fname=input('enter food name-')
    mrp=input('enter price-')
    cur.execute('''INSERT INTO fprice (fname,price) VALUES (?,?) ''',(fname,mrp))
    try:
        cur.execute('ALTER TABLE foodlist ADD '+ fname+' INT')
        conn.commit()
        #logic to make that food qty zero for all users 
        try:
            cur.execute("SELECT no FROM users ")
            numbers=cur.fetchall()
            for n in numbers:
                num=n[0]
                cur.execute("UPDATE foodlist SET "+fname+"=0 WHERE no='"+num+"'")
                conn.commit()
        except:
            pass
    except:
        print(fname+' already in foodlist')   
else:
       print('invalid choice!')