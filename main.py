import sqlite3

conn=sqlite3.connect('foodbotdb.sqlite')
cur=conn.cursor()

def checksecondword(st):
    m=st.split()
    c=len(m)
    if c!=3: 
        w='false'
    else: w=m[1]
    return w

def fetch_reply(msg,phone_no):
    #initialization
    no=str(phone_no)
    msg=msg.lower()
    msg=msg.rstrip()

    #check weather user is in record else respond sorry
    try:
        name=cur.execute("SELECT name FROM users WHERE no='"+no+"'")
        for n in name:
            name=n[0]
        name=name.lower()
    except:
        reply='sorry u r not registered with us contact to admin'
        return (reply)
    if msg=='menu':
        #set type as user
        #respond with the msg what would u like to eat..
        reply='what would u like to eat..?\nITEMS\t\tPRICE'
        rows=cur.execute('SELECT * FROM fprice')
        for row in rows:
            reply=reply+'\n'+row[0]+'\t\t'+str(row[1])
        reply=reply+'\nto order type following command (one order at a time)\norder <ordername> <qty>'
        return (reply)
    elif msg=='host':
        #check if previous host is nill or not
        #else set type as host

        try:
            hostname=cur.execute('SELECT name FROM host where id=0')
            for n in hostname:
                hostname=(n[0])
            if hostname!=None:
                reply=hostname+' is the current host please ask him/her to complete the order '
                return (reply)
            else:
                cur.execute("UPDATE host SET name='"+name+"', no='"+no+"' WHERE id=0 ")
                conn.commit()
                reply='you are host now'
                return (reply)

        except:
            cur.execute("UPDATE host SET name='"+name+"', no='"+no+"' WHERE id=0 ")
            conn.commit()
            reply='you are host now'
            return (reply)
        
        #LOGIC...msg
        #respond with great here r few commands..    
    else: 
        #check the type of user
        type='user'
        hostno=cur.execute('SELECT no FROM host WHERE id=0')
        for h in hostno:
            hostno=h[0]
        if no==hostno:
            type='host'

        #for host types
        if type=='host':
            if msg=='view food list':
                #fetch the list and make a msg..respond with the list
                total=0
                reply='FOOD LIST\nitem\t\tqty\trate\titem_price'
                cur.execute('SELECT fname,price FROM fprice')
                li=cur.fetchall()
                for l in li:
                    fname=l[0]
                    rate=l[1]
                    itemsum=0
                    cur.execute('SELECT '+fname+' FROM foodlist')
                    qty=cur.fetchall()
                    for q in qty:
                        f_qty=q[0]
                        itemsum=itemsum+int(f_qty)
                    net_item_price=float(rate)*itemsum
                    total=total+net_item_price
                    if net_item_price>0:
                        reply=reply+'\n'+fname+'\t\t'+str(itemsum)+'\t'+str(rate)+'\t'+str(net_item_price)
                reply=reply+'\n-----------------------\nTOTAL:'+str(total)
                return(reply)#exitpoint
            elif msg=='view food list order by name':
                #fetch the data and make the list
                #if has all foodlist table values 0 do not write in list
                #at last respond with the list
                reply='FOOD LIST (indivisually)\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                cur.execute('SELECT name,no,payed,total_amount FROM users')
                details=cur.fetchall()
                for d in details:
                    d_name=d[0]
                    d_no=d[1]
                    d_payed=d[2]
                    d_total=d[3]
                    if d_total>0:
                        reply=reply+'\nName:'+d_name+'  No:'+d_no+'\nITEM\tQTY\tprice\titemsum '
                        cur.execute("SELECT fname,price FROM fprice")
                        fname=cur.fetchall()
                        for f in fname:
                            item=f[0]
                            price=f[1]
                            qty=cur.execute("SELECT "+item+" FROM foodlist WHERE no='"+d_no+"'")
                            for l in qty:
                                qty=l[0]
                            itemsum=price*qty
                            if itemsum>0:
                                reply=reply+'\n'+str(item)+'\t'+str(qty)+'\t'+str(price)+'\t'+str(itemsum)
                        reply=reply+'\n---------------\nTOTAL='+str(d_total)+"\npayment status: "+d_payed+'\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                return(reply)#exitpoint              
            elif msg=='paid status list':
                #fetch data make the list & respond with list
                cur.execute('SELECT name,payed FROM users')
                obj=cur.fetchall()
                reply_up='PAYED STATUS LIST\nName\t\tPayment status'
                reply_down='\n--------------------------------'
                for o in obj:
                    o_name=o[0]
                    o_payed=o[1]
                    if(o_payed=='y'):
                        reply_up=reply_up+'\n'+o_name+'\t\t'+o_payed
                    else:
                        reply_down=reply_down+'\n'+o_name+'\t\t'+o_payed
                reply=reply_up+reply_down
                return(reply)#exitpoint      
            elif checksecondword(msg)=='paid':#(<name> payed y)
                #fetch the first word and match in data
                #update the data
                msg=msg.split()
                p_name=msg[0]
                ans=msg[2]
                try:
                    t_sum=cur.execute("SELECT total_amount,no FROM users WHERE name='"+p_name+"'")
                    for p in t_sum:
                        t_sum=p[0]
                        p_no=p[1]
                    if t_sum>0:
                        cur.execute("UPDATE users SET payed ='"+ans+"' WHERE no='"+p_no+"'")
                        conn.commit()
                        reply='noted boss :]'
                    else:
                        reply=p_name+' has not odered anything'
                except:
                    reply=p_name+' is not registered ..pls confirm the name'
                return(reply)#exitpoint
            elif msg.startswith('revise price'):#(revise price <item> <new price>)
                #update prices in the fprice table
                msg=msg.split()
                if len(msg)!=4:
                    reply='invalid format of command!'
                    return (reply)#exitpoint
                try:
                    item=msg[2]
                    new_price=float(msg[3])
                
                    pp=cur.execute("SELECT fname,price FROM fprice WHERE fname='"+item+"'")#to check food is in list or not
                    for p in pp:
                        pp=p[1]
                        pq=p[0]
                    
                    cur.execute('UPDATE fprice SET price ='+str(new_price)+" WHERE fname='"+pq+"'")
                    conn.commit()
                    #update total amount in users table for all users and all items
                    cur.execute('SELECT no FROM users')
                    numbers=cur.fetchall()
                    for n in numbers:
                        total_amount=0
                        num=n[0]#target phone no
                        cur.execute('SELECT fname,price FROM fprice')
                        foods=cur.fetchall()
                        for food in foods:
                            itemsum=0
                            fname=food[0]#target item
                            fprice=food[1]#target price
                            qty=cur.execute("SELECT "+fname+" FROM foodlist WHERE no='"+num+"'")
                            for q in qty:
                                qty=q[0]#target qty
                            itemsum=float(fprice)*int(qty)
                            total_amount=total_amount+itemsum
                        cur.execute("UPDATE users SET total_amount="+str(total_amount)+" WHERE no='"+str(num)+"'")
                        conn.commit()
                    #-------------------------------------------------------------------    
                    reply=item+"'s price revised from Rs"+str(pp)+' to Rs'+str(new_price)
                except:
                    reply='invalid credentials!'
                
                return (reply)#exitpoint
            elif msg=='order completed':
                #flush all the values to 0
                cur.execute('SELECT no FROM users')
                numbers=cur.fetchall()
                for n in numbers:
                    num=n[0]#target phone no
                    cur.execute('SELECT fname FROM fprice')
                    foods=cur.fetchall()
                    for food in foods:
                        fname=food[0]#target item
                        cur.execute("UPDATE foodlist SET "+fname+"=0 WHERE no='"+num+"'")
                    cur.execute("UPDATE users SET payed='n',total_amount=0.0 WHERE no='"+num+"'")
                    conn.commit()
                cur.execute('UPDATE host SET name=NULL,no=NULL WHERE id=0')
                conn.commit()
                reply='Order Completed...all values are flushed!'
                return (reply)#exitpoint
        #for user types
        elif type=='user' or type=='host':
            if msg=='order summary':
                #fetch order details make a message and send it
                reply='ORDER SUMMARY:\nITEM\t\tQTY\tprice\titemsum '
                cur.execute("SELECT fname,price FROM fprice")
                fname=cur.fetchall()
                for f in fname:
                    item=f[0]
                    price=f[1]
                    qty=cur.execute("SELECT "+item+" FROM foodlist WHERE no='"+no+"'")
                    for l in qty:
                        qty=l[0]
                    itemsum=price*qty
                    if itemsum>0:
                        reply=reply+'\n'+str(item)+'\t\t'+str(qty)+'\t'+str(price)+'\t'+str(itemsum)
                total=cur.execute("SELECT total_amount,payed FROM users WHERE no='"+no+"'")
                for t in total:
                    total=t[0]
                    payed=t[1]
                reply=reply+'\n---------------\nTOTAL='+str(total)+"\npayment status: "+payed
                return (reply)#exitpoint
            elif msg.startswith('order'):#(order <item> <qty>)
                #check the format and update the user orders
                array=msg.split()
                if len(array)!=3:
                    reply='invalid format of command!'
                    return (reply)#exitpoint
                item=array[1]
                qty=array[2]
                try:
                    cur.execute("UPDATE foodlist SET "+item+"="+item+"+"+qty+" WHERE no="+no)
                    conn.commit()
                    reply=item+' added:)'
                    #update the total amount
                    fp=cur.execute("SELECT price FROM fprice WHERE fname='"+item+"'")
                    for f in fp:
                        fp=f[0]
                    itemsum=float(fp)*int(qty)
                    cur.execute("UPDATE users SET total_amount=total_amount+"+str(itemsum)+" WHERE no='"+no+"'")
                    conn.commit()
                    return (reply)#exitpoint
                except:
                    reply='sorry '+item+' is not available in MENU or u have entered invalid credentials'
                    return (reply)#exitpoint      
            elif msg.startswith('remove item'):#(remove item <item>)
                #check the format,food and update the users order..
                array=msg.split()
                if len(array)!=3:
                    reply='invalid format of command!'
                    return (reply)#exitpoint
                item=array[2]
                try:
                    #setting total value
                    qty=cur.execute("SELECT "+item+" FROM foodlist WHERE no="+no)
                    for q in qty:
                        qty=q[0]
                    price=cur.execute("SELECT price FROM fprice WHERE fname='"+item+"'")
                    for p in price:
                        price=p[0]
                    sum=int(qty)*float(price)
                    cur.execute('UPDATE users SET total_amount=total_amount-'+str(sum)+"WHERE no='"+no+"'")
                    #updating foodlist table
                    cur.execute("UPDATE foodlist SET "+item+"=0 WHERE no="+no)
                    conn.commit()
                    reply=item+' removed from order!'
                    return (reply)#exitpoint
                except:
                    reply='sorry '+item+' is not available in ur order or u have entered invalid credentials'
                    return (reply)#exitpoint   
            #elif msg.startswith('add comments with'):to be developed
                #check format , set the comment with item and qty..also check qty<=qty in table   
            #extra commands
            
            else:
                #if msg=='hello':
                #   r={'hello','hola','yo geeky!','namaste','hey'}
                #   reply=(r)
                if msg=='!help':
                    reply="IMPORTANT COMMANDS: \n1.host -This command assigns you the host role if no one is hosting currently.\n2. menu -This command displays the current menu .\n3. order <item_name> <quantity> -This command is used to order food from the avail menu.\n4. remove item <item_name> -This command is used to remove that item from your order list.\n5. order summary -This command gives us our order summary (food,cost,payment stat,etc) \n\nHOST COMMANDS:\n1. view food list -This command displys the whole list to be ordered sorted by food items.\n2. view food list order by name-This command displays list of orders by indivisual person.\n3. paid status list-This command lists name of all users and their payment status.\n4. <user_name> paied <y/n> - This command helps host to mark the payed status of each user.\n5. revise price <item_name> <new_price> -This command helps the host to change prices of food items for acc to diff restaurants.\n6. order completed -This commands tells that all the orders are delivered and hence flushes all the data."
                elif msg=='astros' or msg=='define astros' or msg=='what is astros':
                    reply="Its a community of legends studying in SAE who are secretly planning to take over top 10 richest persons in the world by their epic inventions!"
                elif msg=='developer' or msg=='developed by' or msg.startswith('this bot is devloped by'):
                    reply="C'mon u already know that cool boi ;)\n.\n.\n yeah u got it ryt,its Shubham Diwate!"
                else:
                    reply='sorry this command is not found..press !help for commands'
                return(reply)#exitpoint

