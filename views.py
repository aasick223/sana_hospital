from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
#from json2excel import Json2Excel
import json
# import pandas as pd
# import requests
from ast import literal_eval
import phonenumbers
from phonenumbers import timezone
from phonenumbers import carrier
from email_validator import validate_email,exceptions_types
from sana.models import medical
from django.shortcuts import redirect
from datetime import date
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
# from datetime import datetime


@csrf_exempt
def tabletlist(request):
   tabletlist = medical.tabletlist()     
   # for i in tabletlist:
   #     i['']
   return render(request,'tabletlist.html',{'tabletlist':tabletlist})

@csrf_exempt
def Tablet_For_Patient(request):
   pass
   # mf_list,pharma_list,combination_list,tablet_list,category_list= medical.sanamedicallist()
   # return render(request,'tabletforpatient.html',{"combination_list":combination_list,"tablet_list":tablet_list,"category_list":category_list})
   
# @csrf_exempt
# def users(request):
#    accountnumber = request.POST['accountnumber']
#    startdate = request.POST['startdate']
#    enddate = request.POST['enddate']
#    transaction_list = medical.userwithdrawallist(accountnumber,startdate,enddate)
 
  
#    withdrawalcsvlist = pd.DataFrame(userwithdraw_list_ar) 
#    withdrawalcsvlist.to_csv("withdrawaluserlist.csv",index=False)
#    print("csvfilecreatedsuccessfully")
   
#    data = {"status":"success","userwithdraw_list_ar":userwithdraw_list_ar}
#    return JsonResponse(data,safe=False)


# def accountnumber(request):
#       return render(request,'accountnumber.html')
# def accounttransactionhistorylist(request):
#       accountnumber = request.POST['accountnumber']
#       startdate = request.POST['startdate']
#       enddate = request.POST['enddate']
#       transactionhistory_list = medical.usertransactionhistorylist(accountnumber,startdate,enddate)
#       context = {"transactionhistory_list":transactionhistory_list}
#       return render(request,'transactionhistorylist.html',context)

# def addtransaction(request):
#       return render(request,'addtransaction.html')

# def addtransactionvalidate(request):
#       accountnumber = request.POST['accountnumber']
#       name = request.POST['name']
#       amount = request.POST['amount']
#       transactiontype = request.POST['transactiontype']
#       insertdetail = medical.transactioninsert(accountnumber,name,amount,transactiontype)
#       if insertdetail == 1:
#          return redirect('accountnumber')
#       else:
#          return redirect('addtransaction')




def login(request):
      return render(request,'login.html')

def masterpatientadd(request):
     return render(request,'masterpatientadd.html')

def newlogin(request):
      if request.method == "POST":
         username = request.POST.get("username")
         password = request.POST.get("password")
         
         user = ['admin','masterstaff','medicalstaff']

         if username == 'admin' and password == 'admin@123':
               print("login successfully")
               return redirect("frontpage")   # redirect after login
         
         elif username == 'medicalstaff' and password == 'medicalstaff@123':
               # print("login successfully")
               return redirect("masterpatientlist")   

         elif username == 'masterstaff' and password == 'masterstaff@123':
               # print("login successfully")
               return redirect("masterpatientadd")
         else:
               print("error")
               messages.error(request, "Invalid username or password")

      return render(request, "newlogin.html")


def frontpage(request):
      return render(request,'frontpage.html')

def home(request):
         # enddate = request.POST['enddate']
         mf_list,pharma_list,combination_list,tablet_list,category_list= medical.sanamedicallist()
         # print(mf_list,'mf_list')
         # context = {"mf_list":mf_list}
         return render(request,"home.html",{"mf_list":mf_list,"pharma_list":pharma_list,"combination_list":combination_list,"tablet_list":tablet_list,"category_list":category_list})

def select_item_view(request):
   return render(request,"cart.html")


@csrf_exempt
def addtocart(request):
   tabletid = request.POST['tabletid']
   print(tabletid,'tabletid')
   addtocartlist = medical.addtocartlist(tabletid)
   data = {'status':'success','addtocartlist':addtocartlist}
   print(data,'data')
   return JsonResponse(data,safe=False)


@csrf_exempt
def masterpatientlist(request):
    
   masterpatient_list = medical.masterpatientlist()

   return render(request,"masterpatientlist.html",{"masterpatient_list":masterpatient_list})

@csrf_exempt
def add_newtablet_btn(request):
   if request.method == "POST":
      # masterpatient_list = medical.masterpatientlist()
      mf_list,pharma_list, combination_list,tablet_list,category_list= medical.sanamedicallist()
      data={"tablet_list":tablet_list,"combination_list":combination_list,"category_list":category_list}

      return JsonResponse(data,safe=False)


def patient_detail(request, id):
   
   single_patientdetail_for_tablet = medical.masterpatient_detail_for_tablet(id)
   # print(single_patientdetail_for_tablet,'single_patientdetail_for_tablet')
 
   mf_list,pharma_list,combination_list,tablet_list,category_list= medical.sanamedicallist()
   # return render(request,'tabletforpatient.html',{})

   earliertablet_list = medical.earliestexpiretabletlist()

   return render(request, "tabletforpatient.html", {"single_patientdetail_for_tablet": single_patientdetail_for_tablet,"combination_list":combination_list,"tablet_list":tablet_list,"category_list":category_list,"earliertablet_list":earliertablet_list})

@csrf_exempt
def appendratedetail(request) :
   # appendratedetail_tummy_id = request.POST['rowId']
   # masterpatient_list = medical.earliestexpiretabletlist()
   pass

   # return JsonResponse(data,safe=False)
@csrf_exempt
def newpatientadd(request):
   newpatientname = request.POST['newpatientname']
   newpatientage = request.POST['newpatientage']
   newpatientsex = request.POST['newpatientsex']
   newpatientcategory = request.POST['newpatientcategory']
   newpatienthusband = request.POST['newpatienthusband']
   newpatientcontact = request.POST['newpatientcontact']
   newpatientoldfilenumber = request.POST['newpatientoldfilenumber']
   newpatientconsultantfees = request.POST['newpatientconsultantfees']
   newpatientaddress = request.POST['newpatientaddress']

   

   now = datetime.now()
   createddate = now.strftime("%d-%m-%Y")

   medical.newmasterpatientinsert(newpatientname,newpatientage,newpatientsex,newpatientcategory,newpatienthusband,newpatientcontact,newpatientoldfilenumber,newpatientconsultantfees,newpatientaddress,createddate)
 
   data = {"status":"success","report":"inserted successfully"}
   print(data,'dada')
   return JsonResponse(data,safe=False)

@csrf_exempt
def masterpatientlistforcheckup(request):
    
   masterpatientlistforcheckup_list = medical.masterpatientlistforcheckup_list()

   return render(request,"masterpatientlistforcheckup_list.html",{"masterpatientlistforcheckup_list":masterpatientlistforcheckup_list})



   

@csrf_exempt
def tabletadd(request):
   mfname = request.POST['mfname']
   pharmaname = request.POST['pharmaname']
   combinationname = request.POST['combinationname']
   tabletname = request.POST['tabletname']
   totalnumberofstrip = request.POST['totalnumberofstrip']
   numberoftabletinperstrip = request.POST['numberoftabletinperstrip']
   totalstriprate = request.POST['totalstriprate']
   tabletqty = request.POST['tabletqty']
   totalstripmrp = request.POST['totalstripmrp']
   pertabletmrp = request.POST['pertabletmrp']
   pertabletrate = request.POST['pertabletrate']
   expireddate = request.POST['expireddate']
   perstriprate = request.POST['perstriprate']
   perstripmrp = request.POST['perstripmrp']
   categoryname = request.POST['categoryname']
   perstripratepercentage = request.POST['perstripratepercentage']
   print(perstripratepercentage,'perstripratepercentage')

   totalstriprateafterdiscount = request.POST['totalstriprateafterdiscount']
   pertabletrateafterdiscount = request.POST['pertabletrateafterdiscount']
   perstriprateafterdiscount = request.POST['perstriprateafterdiscount']
   perstripdiscountamount = request.POST['perstripdiscountamount']
   pertabletdiscountamount = request.POST['pertabletdiscountamount']
   totalstripdiscountamount = request.POST['totalstripdiscountamount']
   
   now = datetime.now()
   createddate = now.strftime("%d-%m-%Y")
   
   format_str_1 = "%Y-%m-%d"
   datetime_obj_1 = datetime.strptime(expireddate, format_str_1)
   expireddate =datetime_obj_1.strftime("%d-%m-%Y")

   if perstripratepercentage == '':
      print("strip percentage empty")
      totalstriprate = totalstriprate
   else:
      print("strip percentage here")
      totalstriprate = totalstriprateafterdiscount
   print(totalstriprate,'totalstriprate')
  
   medical.newoptioninsert(mfname,pharmaname,combinationname,tabletname,categoryname)

   medical.tablerstockmasterinsert(mfname,pharmaname,combinationname,tabletname,totalnumberofstrip,numberoftabletinperstrip,totalstriprate,tabletqty,totalstripmrp,pertabletmrp,pertabletrate,expireddate,perstriprate,perstripmrp,createddate,categoryname,perstripratepercentage,totalstriprateafterdiscount,pertabletrateafterdiscount,perstriprateafterdiscount,perstripdiscountamount,pertabletdiscountamount,totalstripdiscountamount)
 
   data = {"status":"success","report":"inserted successfully"}
   return JsonResponse(data,safe=False)

@csrf_exempt
def cartfinalsubmit(request):
    tableData = request.POST['tableData']
    totaltablet_rate = request.POST['totaltablet_rate']
    print(tableData,'tableData')
    print(totaltablet_rate,'totaltablet_rate')


  
@csrf_exempt
def updatetablet(request):
      tabletid = request.POST['tabletid']
      edittabletname = request.POST['edittabletname']
      editprice = request.POST['editprice']
      editquantity = request.POST['editquantity']
      #tabletid = request.POST['tabletid']
      print(tabletid,'tabletid')
      print(edittabletname,'edittabletname')
      print(editprice,'editprice')
      print(editquantity,'editquantity')

      #   print(tabletname,'tabletname')
      updatedstatus,updatecheck_list = medical.checkupdatelist(tabletid,edittabletname,editprice,editquantity)
      if updatedstatus == 0:
         data = {"status":"failed","tabletnamealready":"tabletname already exists"}
         return JsonResponse(data,safe=False)
      else:
        data = {"status":"success","updatedsuccessfully":"updated successfully"}
        return JsonResponse(data,safe=False)