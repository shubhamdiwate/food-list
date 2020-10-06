import sqlite3

conn=sqlite3.connect('foodbotdb.sqlite')
cur=conn.cursor()

def admin_func(message,admin_name):
    msg=message
    admin_name=admin_name
    if msg.startswith('add user'):
        msg=msg.split()
        l=len(msg)
        if l!=4:
            return ('NULL')
        try:
            user_name=msg[2]
            user_no=msg[3]
            #check if user is already registered
            try:
                n=cur.execute("SELECT name FROM users WHERE no='"+user_no+"'")
                for i in n:
                    n=i[0]
                reply="soryy "+n+" is already registered "
                return(reply)
            except:
                pass
            #add the user in users table and foodlist table
            cur.execute('''INSERT INTO users (name,no,payed,total_amount) VALUES(?,?,'n',0)''',(user_name,user_no,))
            cur.execute('INSERT INTO foodlist (no) VALUES (?)',(user_no,))
            reply='registered user successfully'
            #  here add LOGIC to make all foodlist values zero for this no
            try:
                cur.execute('SELECT fname FROM fprice')
                fname=cur.fetchall()
                for f in fname:
                    item=f[0]
                    cur.execute('UPDATE foodlist SET '+item+"=0 WHERE no='"+user_no+"'")
                    conn.commit()
            except:
                pass
        except:
            reply='sorry user cant be registered.. invalid credentials!'
        return(reply)
    elif msg.startswith('add food'):
        msg=msg.split()
        l=len(msg)
        if l!=4:
            return ('NULL')
        food_name=msg[2]
        food_price=msg[3]
        
        try:
            #check if food is already avail
            try:
                fp=cur.execute("SELECT price FROM fprice WHERE fname='"+food_name+"'")
                for ff in fp:
                    fp=ff[0]
                reply=food_name+' is already in menu price at Rs'+fp
                return(reply)
            except:
                pass
            #enter the food in tables fprice and foodlist
            cur.execute('''INSERT INTO fprice (fname,price) VALUES (?,?) ''',(food_name,food_price))
            cur.execute('ALTER TABLE foodlist ADD '+ food_name+' INT')
            conn.commit()
            reply=food_name+' added successfully'
            #logic to make that food qty zero for all users 
            try:
                cur.execute("SELECT no FROM users ")
                numbers=cur.fetchall()
                for n in numbers:
                    num=n[0]
                    cur.execute("UPDATE foodlist SET "+food_name+"=0 WHERE no='"+num+"'")
                    conn.commit()
            except:
                pass
        except:
            reply='food cannot be added.. invalid credentials!'
        return(reply)

    else:
        return ('NULL')