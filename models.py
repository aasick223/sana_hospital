from django.db import models
from django.db import connection
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
cursor = connection.cursor()
class medical(models.Model):
    def usertransactionhistorylist(accountnumber,startdate,enddate):
       
        cursor.execute("SELECT t.transactiondate,t.transactiontype,t.amount,u.id,u.name,sum(t.amount)OVER(PARTITION BY t.tabletid ORDER BY t.transactiondate) as currentbalance FROM transaction t join users u on t.userid = u.id where t.transactiondate BETWEEN %s AND %s AND u.accountnumber=%s ORDER BY t.transactiondate DESC",(startdate,enddate,accountnumber,))
        columns = [col[0] for col in cursor.description]
        transaction_list = [dict(zip(columns,row)) for row in cursor.fetchall()]
        return transaction_list
    

    def transactioninsert(accountnumber,name,amount,transactiontype):
            cursor.execute("SELECT * FROM transaction WHERE transactiondate IN (SELECT MAX(transactiondate) FROM transaction WHERE accountnumber = %s)",(accountnumber,))
            # ("select * from tabletstockmaster where tabletid=%s)",(tabletid,))
            transactionchklist = cursor.fetchall()
            transactionchklist_rc = len(transactionchklist)        
            if transactionchklist_rc > 0:
                alreadyamount = transactionchklist[0][4]
                if alreadyamount == 0 or transactiontype == 'deposit':
                    addamount = alreadyamount + int(amount)
                elif alreadyamount > int(amount)  or transactiontype == 'withdrawal':
                    addamount = alreadyamount - int(amount)
                elif alreadyamount == 0 or alreadyamount < int(amount)  or transactiontype == 'withdrawal':
                    addamount = alreadyamount
             
                cursor.execute("select id from users where accountnumber =%s",(accountnumber,))
                userslist = cursor.fetchall()
                userid = userslist[0][0]
           
                if (userid):
                    sql = "INSERT INTO transaction (userid,accountnumber,transactiontype,amount,transactiondate) VALUES (%s,%s,%s,%s,%s);"
                    val = (userid,accountnumber,transactiontype,addamount,now,)
                    cursor.execute(sql,val)
                    connection.commit()
                    
                    cursor.execute("update users set currentbalance =%s where accountnumber=%s",(addamount,accountnumber))
                    connection.commit()
                    return 1
                else:
                    return 0


            else:
                if transactiontype == 'deposit':
                    sql = "INSERT INTO users (accountnumber,name,currentbalance) VALUES (%s,%s,%s)"
                    val = (accountnumber,name,amount)
                    cursor.execute(sql,val)
                    connection.commit()
                    print("users insert successfully")
                    cursor.execute("select id from users where accountnumber=%s",(accountnumber,))
                    firstaclist = cursor.fetchall()
                    fisrtuserid = firstaclist[0][0]
                    if(fisrtuserid):
                            sql = "INSERT INTO transaction (userid,accountnumber,transactiontype,amount,transactiondate) VALUES (%s,%s,%s,%s,%s);"
                            val = (fisrtuserid,accountnumber,transactiontype,amount,now)
                            cursor.execute(sql,val)
                            connection.commit()
                            print("transaction insert successfully")
                            return 1
                else:
                    return 0


    def masterpatientlist():
        cursor.execute("select * from masterpatient")
        columns = [col[0] for col in cursor.description]
        masterpatient_list = [dict(zip(columns,row)) for row in cursor.fetchall()]        
            
        return masterpatient_list

    def masterpatientlistforcheckup_list():
        cursor.execute("select * from masterpatient")
        columns = [col[0] for col in cursor.description]
        masterpatient_list = [dict(zip(columns,row)) for row in cursor.fetchall()]        
            
        return masterpatient_list
    # SELECT tabletname,combinationname,category_name,pertabletmrp,MIN(expireddate) AS earliest_expiry FROM tabletstockmaster GROUP BY tabletname,combinationname,category_name,pertabletmrp

    def earliestexpiretabletlist():
        # cursor.execute("SELECT tabletname,combinationname,category_name,pertabletmrp FROM tabletstockmaster GROUP BY tabletname,combinationname,category_name")
        # cursor.execute("SELECT t.tabletname,t.combinationname,t.category_name,t.pertabletmrp FROM tabletstockmaster t JOIN ( SELECT tabletname, combinationname, category_name, MIN(STR_TO_DATE(expireddate,'%d-%m-%Y')) AS earliest_expiry FROM tabletstockmaster WHERE STR_TO_DATE(expireddate,'%d-%m-%Y') >= CURDATE() GROUP BY tabletname, combinationname, category_name ) x ON t.tabletname = x.tabletname AND t.combinationname = x.combinationname AND t.category_name = x.category_name AND STR_TO_DATE(t.expireddate,'%d-%m-%Y') = x.earliest_expiry ORDER BY earliest_expiry ASC;")

        # cursor.execute("SELECT t.tabletname,t.combinationname,t.category_name,t.pertabletmrp,t.tabletqty,t.expireddate FROM tabletstockmaster t")

        cursor.execute("SELECT tabletid,brandname, combinationname, categoryname, expireddate, tabletqty, pertabletmrp FROM tabletstockmaster WHERE tabletqty > 0 ORDER BY expireddate DESC;")

        
        
        result = []
        columns = [col[0] for col in cursor.description] 
        earliestexpiretabletlist_ar = [dict(zip(columns,row)) for row in cursor.fetchall()]

        print(type(earliestexpiretabletlist_ar),'earliestexpiretabletlist_ar')
        # for i in earliestexpiretabletlist:
        earliestexpiretabletlist = []
        for i in earliestexpiretabletlist_ar:
            my_float = float((i['pertabletmrp']))
            pertabletmrp = int(my_float)
            # pertabletmrp = (float(i['pertabletmrp']))
            # print(type(pertabletmrp),'pertabletmrp')
            my_float1 = float((i['tabletqty']))
            tabletqty = int(my_float1)
            earliestexpiretabletlist.append({
                           "tabletid": i['tabletid'],
                           "tabletname": i['brandname'],
                           "combinationname": i['combinationname'],  
                           "category_name": i['categoryname'],
                           "pertabletmrp": pertabletmrp,
                           "tabletqty" : tabletqty,
                           "expireddate" : i['expireddate']

                           })
        print(earliestexpiretabletlist,'earliestexpiretabletlist')

            
        return earliestexpiretabletlist


    def sanamedicallist():
        cursor.execute("select * from mf")
        columns = [col[0] for col in cursor.description]
        mf_list = [dict(zip(columns,row)) for row in cursor.fetchall()]

        cursor.execute("select * from pharma")
        columns = [col[0] for col in cursor.description]
        pharma_list = [dict(zip(columns,row)) for row in cursor.fetchall()]

        cursor.execute("select * from combination")
        columns = [col[0] for col in cursor.description]
        combination_list = [dict(zip(columns,row)) for row in cursor.fetchall()]

        cursor.execute("select * from tablet")
        columns = [col[0] for col in cursor.description]
        tablet_list = [dict(zip(columns,row)) for row in cursor.fetchall()]

        cursor.execute("select * from category")
        columns = [col[0] for col in cursor.description]
        category_list = [dict(zip(columns,row)) for row in cursor.fetchall()]

        return mf_list,pharma_list,combination_list,tablet_list,category_list
    def tabletlist():
       
        cursor.execute("SELECT * FROM tabletstockmaster")
        columns = [col[0] for col in cursor.description]
        tablet_list = [dict(zip(columns,row)) for row in cursor.fetchall()]
        
        return tablet_list

    def addtocartlist(tabletid):
        cursor.execute("select tabletid,tabletname,pertabletmrp from tabletstockmaster where tabletid=%s",(tabletid,))
        columns = [col[0] for col in cursor.description]
        addtocartlist = [dict(zip(columns,row)) for row in cursor.fetchall()]
    
        return addtocartlist

    def newoptioninsert(mfname,pharmaname,combinationname,tabletname,categoryname):
        # mf
        cursor.execute("select mfname from mf where mfname=%s",(mfname,))
        mflist = cursor.fetchall()
        mflist_length = len(mflist)

        # pharma
        cursor.execute("select pharmaname from pharma where pharmaname=%s",(pharmaname,))
        pharmalist = cursor.fetchall()
        pharmalist_length = len(pharmalist)

        # combination
        cursor.execute("select combinationname from combination where combinationname=%s",(combinationname,))
        combinationlist = cursor.fetchall()
        combinationlist_length = len(combinationlist)

        # tablet
        cursor.execute("select tabletname from tablet where tabletname=%s",(tabletname,))
        tabletlist = cursor.fetchall()
        tabletlist_length = len(tabletlist)

        # category
        cursor.execute("select categoryname from category where categoryname=%s",(categoryname,))
        categorylist = cursor.fetchall()
        categorylist_length = len(categorylist)


        if (mflist_length == 0 ):
            query = ("insert into mf(mfname) values(%s)")
            cursor.execute(query,(mfname,))
            connection.commit() 
            print("mf inserted successfully")
        else:
            pass

        if (pharmalist_length == 0 ):
            query = ("insert into pharma(pharmaname) values(%s)")
            cursor.execute(query,(pharmaname,))
            connection.commit() 
            print("pharma inserted successfully")
        else:
            pass

        if (combinationlist_length == 0 ):
            query = ("insert into combination(combinationname) values(%s)")
            cursor.execute(query,(combinationname,))
            connection.commit()
            print("combination inserted successfully")
        else:
            pass

        if (tabletlist_length == 0 ):
            query = ("insert into tablet(tabletname) values(%s)")
            cursor.execute(query,(tabletname,))
            connection.commit()
            print("tablet inserted successfully")
        else:
            pass

        if (categorylist_length == 0 ):
            query = ("insert into category(categoryname) values(%s)")
            cursor.execute(query,(categoryname,))
            connection.commit()
            print("category inserted successfully")
        else:
            pass

        

    # def newpharmaoptioninsert(pharmaname):
    #     cursor.execute("select pharma from mf where mfname=%s",(pharmaname,))
    #     pharma list = cursor.fetchall()
    #     mflist_length = len(mflist)
    #     if (mflist_length == 0 ):
    #         query = ("insert into pharma(pharmaname) values(%s)")
    #         cursor.execute(query,(pharmaname,))
    #         connection.commit() 
    #         print("mf inserted successfully")
    #     else:
    #         pass
    
    def newmasterpatientinsert(newpatientname,newpatientage,newpatientsex,newpatientcategory,newpatienthusband,newpatientcontact,newpatientoldfilenumber,newpatientconsultantfees,newpatientaddress,createddate):
        print(newpatientname,'newpatientname')
        print(newpatientage,'newpatientage')
        print(newpatientsex,'newpatientsex')
        print(newpatientcategory,'newpatientcategory')
        print(newpatienthusband,'newpatienthusband')
        print(newpatientcontact,'newpatientcontact')
        print(newpatientoldfilenumber,'newpatientoldfilenumber')
        print(newpatientconsultantfees,'newpatientconsultantfees')
        print(newpatientaddress,'newpatientaddress')

        cursor.execute("select * from masterpatient where oldfileno=%s",(newpatientoldfilenumber,))

        # tabletupdateselectlist = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        masterpatientlist = [dict(zip(columns,row)) for row in cursor.fetchall()]
        masterpatientlist_length = len(masterpatientlist)
        print(masterpatientlist_length,'masterpatientlist_length')
        if (masterpatientlist_length == 0):
            query = ("insert into masterpatient(patientname,age,husband_name,address,contactno,oldfileno,consultantfee,createddate,patientcategory,sex) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            cursor.execute(query,(newpatientname,newpatientage,newpatienthusband,newpatientaddress,newpatientcontact,newpatientoldfilenumber,newpatientconsultantfees, createddate,newpatientcategory,newpatientsex,))
            connection.commit()
        else:
          print("already exists")
            # for i in tabletupdateselectlist:
            #     tabletid = i['tabletid']
            #     update_mrp = int(i['mrp']) + int(totalstripmrp)
            #     update_rate =  int(i['rate']) + int(totalstriprate)
            #     update_totalnumberofstrip = int(i['totalnumberofstrip']) + int(totalnumberofstrip)
            #     update_tabletqty = int(i['tabletqty']) + int(tabletqty)
                
            #     cursor.execute("update tabletstockmaster set mrp =%s,rate=%s,totalnumberofstrip=%s,tabletqty=%s  where tabletid=%s",(update_mrp,update_rate,update_totalnumberofstrip,update_tabletqty,tabletid))
            #     connection.commit()
            #     print("updated successfully")




        
    def tablerstockmasterinsert(mfname,pharmaname,combinationname,tabletname,totalnumberofstrip,numberoftabletinperstrip,totalstriprate,tabletqty,totalstripmrp,pertabletmrp,pertabletrate,expireddate,perstriprate,perstripmrp,createddate,categoryname,perstripratepercentage,totalstriprateafterdiscount,pertabletrateafterdiscount,perstriprateafterdiscount,perstripdiscountamount,pertabletdiscountamount,totalstripdiscountamount):

        print(mfname,'mfname')
        print(pharmaname,'pharmaname')
        print(combinationname,'combinationname')
        print(tabletname,'tabletname')
        print(totalnumberofstrip,'totalnumberofstrip')
        print(numberoftabletinperstrip,'numberoftabletinperstrip')
        print(totalstriprate,'totalstriprate')
        print(tabletqty,'tabletqty')
        print(totalstripmrp,'totalstripmrp')
        print(pertabletmrp,'pertabletmrp')
        print(pertabletrate,'pertabletrate')
        print(expireddate,'expireddate')
        print(perstriprate,'perstriprate')
        print(perstripmrp,'perstripmrp')
        print(createddate,'createddate')
        print(perstripratepercentage,'perstripratepercentage')
        print(totalstriprateafterdiscount,'totalstriprateafterdiscount')
        print(pertabletrateafterdiscount,'pertabletrateafterdiscount')
        print(perstriprateafterdiscount,'perstriprateafterdiscount')
        print(perstripdiscountamount,'perstripdiscountamount')
        print(pertabletdiscountamount,'pertabletdiscountamount')
        print(totalstripdiscountamount,'totalstripdiscountamount')
        #  : perstripratepercentage ,
        #           : totalstriprateafterdiscount ,
        #          : pertabletrateafterdiscount ,
        #          : perstriprateafterdiscount ,
        #          : perstripdiscountamount ,
        #          : pertabletdiscountamount ,
        #          : totalstripdiscountamount ,

        
        # earliest date mysql query
        # SELECT mfname,pharmaname,combinationname,tabletname,categor_yname,MIN(expireddate) AS earliest_expiry FROM tabletstockmaster
        # GROUP BY mfname,pharmaname,combinationname,tabletname,category_name;

        cursor.execute("select * from tabletstockmaster where mfname=%s and pharmaname=%s and combinationname=%s and brandname=%s and perstriprate=%s and perstripmrp=%s and expireddate = %s and perstripratediscountpercentage=%s",(mfname,pharmaname,combinationname,tabletname,perstriprate,perstripmrp,expireddate,perstripratepercentage,))

        columns = [col[0] for col in cursor.description]
        tabletupdateselectlist = [dict(zip(columns,row)) for row in cursor.fetchall()]
        tabletupdateselectlist_length = len(tabletupdateselectlist)
        print(tabletupdateselectlist_length,'tabletupdateselectlist_length')
        print(tabletupdateselectlist,'tabletupdateselectlist')
        if (tabletupdateselectlist_length == 1):
            print("already exists")
            for i in tabletupdateselectlist:
                tabletid = i['tabletid']
                update_mrp = int(i['totalstripmrp']) + int(totalstripmrp)
                update_rate =  int(i['totalstriprate']) + int(totalstriprate)
                update_totalnumberofstrip = int(i['totalnumberofstrip']) + int(totalnumberofstrip)
                update_tabletqty = int(i['tabletqty']) + int(tabletqty)
                
                cursor.execute("update tabletstockmaster set totalstripmrp =%s,totalstriprate=%s,totalnumberofstrip=%s,tabletqty=%s  where tabletid=%s",(update_mrp,update_rate,update_totalnumberofstrip,update_tabletqty,tabletid))
                connection.commit()
                print("updated successfully")
        else:
            print("inserted successfully")  
            query = ("insert into tabletstockmaster(mfname,pharmaname,combinationname,brandname,totalnumberofstrip,numberoftabletinperstrip,totalstriprate,tabletqty,totalstripmrp,pertabletmrp,pertabletrate,expireddate,perstriprate,perstripmrp,categoryname,perstripratediscountpercentage,perstripafterdiscountrate,totalstripafterdiscountrate,pertabletafterdiscountrate,perstripratediscountamount,pertabletratediscountamount,totalstripratediscountamount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            cursor.execute(query,(mfname,pharmaname,combinationname,tabletname,totalnumberofstrip,numberoftabletinperstrip,totalstriprate, tabletqty,totalstripmrp,pertabletmrp,pertabletrate,expireddate,perstriprate,perstripmrp,categoryname,perstripratepercentage,perstriprateafterdiscount,totalstriprateafterdiscount,pertabletrateafterdiscount,perstripdiscountamount,pertabletdiscountamount,totalstripdiscountamount,))
            connection.commit()  

    def masterpatient_detail_for_tablet(id):
        cursor.execute("select * from masterpatient where patientid=%s",(id,))
        columns = [col[0] for col in cursor.description]
        single_patientdetail_for_tablet = [dict(zip(columns,row)) for row in cursor.fetchall()]
        return single_patientdetail_for_tablet


    def addtablet(tabletname,quantity,price,c_date):
        cursor.execute("select * from persons where tabletdetail=%s",(tabletname,))
        tabletcheck_rc = len(cursor.fetchall())
        
        if tabletcheck_rc == 0:
            sql = "INSERT INTO persons (tabletdetail, quantity,price,createddate) VALUES (%s, %s,%s,%s)"
            val = (tabletname, quantity,price,c_date)
            cursor.execute(sql,val)
            connection.commit()
            
            cursor.execute("select * from persons where tabletdetail=%s",(tabletname,))
            columns = [col[0] for col in cursor.description]
            medicalperson_list = [dict(zip(columns,row)) for row in cursor.fetchall()]
            return 1,medicalperson_list
        else:
            medicalperson_list = 0
            return 0,medicalperson_list

    def checkupdatelist(tabletid,edittabletname,editprice,editquantity):
        cursor.execute("select * from persons where userid !=%s and tabletdetail=%s",(tabletid,edittabletname,))
        updatechecklist_rc = len(cursor.fetchall())
        # print
        column = [x[0] for x in cursor.description]
        updatecheck_list = [dict(zip(columns,row)) for row in cursor.fetchall()]
        if updatechecklist_rc == 0:
            
            cursor.execute('update persons set tabletdetail=%s where userid =%s',(edittabletname,tabletid,))
            connection.commit()
            updatedstatus = 1
            return updatedstatus,updatecheck_list
        else:
            updatedstatus = 0
            updatecheck_list = 0
            return updatedstatus,updatecheck_list
            # return 0


    

          




