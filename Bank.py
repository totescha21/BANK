import decimal
import datetime
import mysql.connector
from tabulate import tabulate
 
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

#\u001b[34m - Blue
#\u001b[0m - Reset
#\u001b[31m - Red
 
#initializing database
s=mysql.connector.connect(host="localhost",user="root",passwd="20042006") #making a connection
if(s.is_connected()):
   print("\n\u001b[32mSQL connected!!!\u001b[0m \n")
c=s.cursor()
c.execute("CREATE DATABASE IF NOT EXISTS Bank;")
c.execute("USE Bank;")
c.execute("CREATE TABLE IF NOT EXISTS Accounts(Accno INT PRIMARY KEY, CustID VARCHAR(10), Balance DECIMAL(25,4), Branch INT, DWL DECIMAL(25,4), Withdrawn DECIMAL(25,4));")
c.execute("CREATE TABLE IF NOT EXISTS Transactions(TID INT PRIMARY KEY,Ttype INT,Acc1 INT,Acc2 INT,Val DECIMAL(25,4),Date DATE);")
c.execute("CREATE TABLE IF NOT EXISTS Customers(Custid VARCHAR(10) PRIMARY KEY,Name VARCHAR(30),Address VARCHAR(50),Email VARCHAR(40),Phoneno VARCHAR(12));")
 
 
 
 
def inputf(a):
   """Handles colour coding for input.""" 
   w=input('\u001b[34m'+a+'\u001b[0m')
   print('\u001b[31m',end="")
   return w
 
def Formatall():
   """Formats the existing data in the database"""
   c.execute("DELETE FROM Accounts;")
   c.execute("DELETE FROM Transactions;")
   c.execute("DELETE FROM Customers;")
   return
 
class Bank:
   def __init__(self,accounts={},customers={},transactions=[],nextAcc=1,nextBranch=2,nextTrans=1,date=datetime.datetime.date(datetime.datetime.now())):
       """Used to create an object of the class Bank"""
       self.Acc=accounts
       self.Cust=customers
       self.Trans=transactions
       self.nextAcc=nextAcc
       self.nextBranch=nextBranch
       self.nextTrans=nextTrans
       self.date=date
 
   class Accounts:
       def __init__(self,accno,CustID,balance,branch,dwl,withdrawn=0):
           """Used to create an object of the subclass Accounts"""
           self.accno=accno
           self.CustID=CustID
           self.balance=balance
           self.branch=branch
           self.dwl=dwl
           self.withdrawn=withdrawn
       def printFullDetails(aSelf,self):
           """Prints full details of an account"""
           print("Account Details:-")
           print("    Account Number: {0} \n    Account Balance: {1} \n    Branch Number: {2} \n    Daily withdrawing Limit: {3}".format(aSelf.accno,aSelf.balance,aSelf.branch,aSelf.dwl))
           self.Cust[aSelf.CustID].printDetails()
 
   class Transactions:
       def __init__(self,tid,ttype,acc1,acc2,val,date):
           """Used to create an object of the subclass Transactions"""
           self.tid=tid
           self.ttype=ttype
           self.acc1=acc1
           self.acc2=acc2
           self.val=val
           self.date=date
 
   class Customers:
       def __init__(self,custid, name, address, email, phoneno):
           """Used to create an object of the subclass Customers"""
           self.custid=custid
           self.name = name
           self.address = address
           self.email = email
           self.phone_number = phoneno
       def printDetails(Self):
           """Prints customer particulars like Name, Address, etc."""
           print("Customer Details:-\n    name: {0} \n    address: {1} \n    email: {2} \n    Phone Number: {3} \n    PersonID: {4}".format(Self.name,Self.address,Self.email,Self.phone_number,Self.custid))
       def printFullDetails(cSelf,self):
           """Prints customer particulars, all the accounts in a tabular format and the total balance"""
           cSelf.printDetails()
           self.tabulateAcc(self.getCustomerAccnos(cSelf.custid))
 
 
   def printFullDetails(self):
       """Prints full details of the bank(Branches, Accounts, Balance, etc.)"""
       print("Number of Branches: ",self.nextBranch-1)
       Bank.seg()
       res=Bank.dec('0.0')
       for i in range(1,self.nextBranch):
           self.branch_PrintFullDetails(i)
           res+=self.accountsBalance(self.getBranchAccnos(i))
           Bank.seg()
       print("Total Balance of the Bank: ",res)
 
   def dec(a):
       """Returns decimal of a string"""
       return decimal.Decimal(str(a))
 
   def seg():
       """Creates a separator between different sections of output"""
       print('\u001b[0m'+"-----------------------------------------------------------------------------------------------"+'\u001b[31m')
  
 
   def tabulateAcc(self,accnos):
       """Displays details of accounts in accnos in tabular format and displays total balance"""
       print("All Account Details:- ")
       l=[[self.Acc[x].accno,self.Acc[x].branch,str(self.Acc[x].balance)] for x in accnos]
       print(tabulate(l,headers=["Account Number","Branch Number","Balance"],tablefmt="psql",floatfmt=".3f"))
       print("Total Balance:",self.accountsBalance(accnos))
  
   def getBranchAccnos(self,bno):
       """Retrieves a list of account numbers of a particular branch from the database"""
       c.execute("SELECT Accno from Accounts WHERE branch={};".format(bno))
       return [x[0] for x in c.fetchall()]
  
   def getCustomerAccnos(self,cno):
       """Retrieves a list of account numbers of a particular customer from the database"""
       c.execute("SELECT Accno from Accounts WHERE CustID={};".format(cno))
       return [x[0] for x in c.fetchall()]
 
  
   def branch_PrintFullDetails(self,bno):
       """Prints full details of a branch"""
       print("Branch Number: ",bno)
       self.tabulateAcc(self.getBranchAccnos(bno))
 
   def accountsBalance(self,accnos):
       """Returns sum of account balance of accounts in accnos"""
       tbal=Bank.dec('0.0')
       tbal+=sum([self.Acc[x].balance for x in accnos])
       return tbal
 
   def getTtype(ttype):
       """Returns type of transaction"""
       if(ttype==0):
           return "Credit"
       elif(ttype==1):
           return "Debit"
       elif(ttype==2):
           return "Transfer"
 
   def printTrans(self,translist):
       """Prints transactions in a tabular format from translist"""
       l=[[self.Trans[x].tid,Bank.getTtype(self.Trans[x].ttype),self.Trans[x].acc1,self.Trans[x].acc2,self.Trans[x].val,self.Trans[x].date] for x in translist]
       print(tabulate(l,headers=["TID","Type","AccountNo.1(from)","AccountNo.2(To)","Value","Date"],tablefmt="psql"))
 
   def createAccount(self):
       """Used to create account"""
       flag=inputf("Have you created an Account before?(y/n): ")
       while(flag!='y' and flag!='n'):
           flag=inputf("Please enter a valid input. Do you already have an Account(y/n): ")
       if(flag=='y'):
 
           custid=inputf("Enter your PersonID: ")
           if(custid in self.Cust):
               pass
           else:
               print("You don't have an account. Please restart")
               return
       else:
           custid=inputf("Enter PersonID: ")
           if(custid in self.Cust):
               print("You have already made an account before. Please start again")
               return
           name=inputf("Enter name: ")
           address=inputf("Enter Home address: ")
           email=inputf("Enter email: ")
           pnumber=inputf("Enter Phone Number: ")
           self.Cust[custid]=Bank.Customers(custid,name,address,email,pnumber)
           c.execute("INSERT INTO Customers VALUES('{}','{}','{}','{}','{}');".format(custid,name,address,email,pnumber))
 
       bal=Bank.dec(inputf("Enter your initial Balance: "))
       bran=int(inputf("Enter BranchNo.: "))
       while(bran>=self.nextBranch or bran<1):
           bran=int(inputf("Please enter a Valid Branch Number"))
       dwl=Bank.dec(inputf("Enter Daily withdrawal limit for the Account: "))
       self.Acc[self.nextAcc]=Bank.Accounts(self.nextAcc,custid,bal,bran,dwl)
       c.execute("INSERT INTO Accounts VALUES({},'{}',{},{},{},0.0);".format(self.nextAcc,custid,str(bal),bran,str(dwl)))
       self.Acc[self.nextAcc].printFullDetails(self)
       self.nextAcc+=1
       print("Account Created!!")
       return
 
   def closeAccount(self):
       """Used to close account"""
       Accno=int(inputf("Please input your Account Number: "))
       if(Accno in self.Acc):
           del self.Acc[Accno]
           c.execute("DELETE FROM Accounts WHERE Accno={}".format(Accno))
           print("Your account has been deleted. Please take your money.")
       else:
           print("Account does not exist")
 
   def credit(self,accno,val):
       """Used to credit val to account number - accno """
       self.Acc[accno].balance+=val
       c.execute("UPDATE Accounts SET Balance=Balance+{} WHERE Accno={}".format(str(val),accno))
       return 1
 
   def debit(self,accno,val):
       """Used to debit val from account number - accno """
       if(self.Acc[accno].balance-val<0):
           print("Sorry the account does not have that balance")
           return 0
       self.Acc[accno].balance-=val
       c.execute("UPDATE Accounts SET Balance=Balance-{} WHERE Accno={}".format(str(val),accno))
       return 1
 
   def ask(self,ttype):
       """Helper function for credit/debit operations"""
       accno=int(inputf("Enter Account Number: "))
       if(accno not in self.Acc):
           print("Account does not exist")
           return
       val=Bank.dec(inputf("Enter amount: "))
       if(ttype==0):
           res=self.credit(accno,val)
           if(res):
               self.Trans[self.nextTrans]=(Bank.Transactions(self.nextTrans,0,accno,None,val,self.date))
               c.execute("INSERT INTO Transactions VALUES({},{},{},NULL,{},'{}');".format(self.nextTrans,0,accno,str(val),str(self.date)))
               self.nextTrans+=1
               print("Value Credited")
               print("Account Balance:",self.Acc[accno].balance)
       elif(ttype==1):
           if(self.Acc[accno].withdrawn+val<=self.Acc[accno].dwl):
               res=self.debit(accno,val)
               if(res):
                   self.Trans[self.nextTrans]=(Bank.Transactions(self.nextTrans,1,accno,None,val,self.date))
                   c.execute("INSERT INTO Transactions VALUES({},{},{},NULL,{},'{}');".format(self.nextTrans,1,accno,str(val),str(self.date)))
                   self.nextTrans+=1
                   print("Value Debited")
                   print("Account Balance:",self.Acc[accno].balance)
                   self.Acc[accno].withdrawn+=val
                   c.execute("UPDATE Accounts SET Withdrawn=Withdrawn+{} WHERE Accno={}".format(str(val),accno))
           else:
               print("Cannot proceed. Exceeding daily withdrawal limit")
  
   def makeTransaction(self):
       """Used to make transactions"""
       accno1=int(inputf("Transaction from Account Number: "))
       if(accno1 not in self.Acc):
           print("Account does not exist")
           return
       accno2=int(inputf("Transaction to Account Number: "))
       if(accno2 not in self.Acc):
           print("Account does not exist")
           return
       val=Bank.dec(inputf("Enter amount: "))
       res1=self.debit(accno1,val)
       if(res1):
           res2=self.credit(accno2,val)
           if(res2):
               print("Transaction Successful")
               self.Trans[self.nextTrans]=(Bank.Transactions(self.nextTrans,2,accno1,accno2,val,self.date))
               c.execute("INSERT INTO Transactions VALUES({},{},{},{},{},'{}');".format(self.nextTrans,2,accno1,accno2,str(val),self.date))
               self.nextTrans+=1
       else:
           print("Transaction can't be proceeded")
           print("Error: {0} Not enough account balance".format(accno1))
 
   def getTransactionReport(self):
       """Used for getting transaction report in a given date range"""
       print("Press\n    1 for Customer\n    2 for Branch\n    3 for Bank")
       choice=inputf("Enter choice: ")
       while(not(choice=='1' or choice=='2' or choice=='3')):
           choice=inputf("Please enter a valid choice: ")
       date_input1=inputf("Enter lower date(YYYY-MM-DD): ")
       year, month, day = map(int, date_input1.split('-'))
       date1 = datetime.date(year, month, day)
 
       date_input2=inputf("Enter upper date(YYYY-MM-DD): ")
       year, month, day = map(int, date_input2.split('-'))
       date2 = datetime.date(year, month, day)
       l=[]
       if(date2<date1):
           print("Invalid range")
           return
       if(choice=='1'):
           custid=inputf("Enter custid: ")
           if(custid not in self.Cust):
               print("Customer doesn't have an account")
               return
           c.execute("SELECT DISTINCT(TID) FROM Transactions T,Accounts A WHERE (T.acc1=A.Accno OR T.acc2=A.Accno) AND A.CustID={0} AND T.date BETWEEN '{1}' AND '{2}';".format(custid,date_input1,date_input2))
           print("Transaction Report for Customer {0} for the date range - {1} to {2}".format(custid,date_input1,date_input2))
           l=[x[0] for x in c.fetchall()]
       elif(choice=='2'):
           branchno=int(inputf("Enter Branchno: "))
           if(branchno>=self.nextBranch):
               print("Branch Does not exist")
               return
           c.execute("SELECT DISTINCT(TID) FROM Transactions T,Accounts A WHERE (T.Acc1=A.Accno OR T.Acc2=A.Accno) AND (A.branch={0}) AND (T.date BETWEEN '{1}' AND '{2}');".format(branchno,date_input1,date_input2))
           print("Transaction Report for Branch {0} for the date range - {1} to {2}: ".format(branchno,date_input1,date_input2))
           l=[x[0] for x in c.fetchall()]
       elif(choice=='3'):
           c.execute("SELECT DISTINCT(TID) FROM Transactions WHERE date BETWEEN '{0}' AND '{1}';".format(date_input1,date_input2))
           print("Transaction Report for the Bank for the date range - {0} to {1}: ".format(date_input1,date_input2))
           l=[x[0] for x in c.fetchall()]
       self.printTrans(l)
          
 
 
   def run(self):
       """Helper function to run the bank"""
       while(1):
           s.commit()
           print()
           print('\u001b[31m',end="")
           Bank.seg()
           print('\u001b[32m',end="")
           print(r"""
 ________   ________   ________    ___  __
|\   __  \ |\   __  \ |\   ___  \ |\  \|\  \
\ \  \|\ /_\ \  \|\  \\ \  \\ \  \\ \  \/  /|_
 \ \   __  \\ \   __  \\ \  \\ \  \\ \   ___  \
  \ \  \|\  \\ \  \ \  \\ \  \\ \  \\ \  \\ \  \
   \ \_______\\ \__\ \__\\ \__\\ \__\\ \__\\ \__\
    \|_______| \|__|\|__| \|__| \|__| \|__| \|__|
 
""")
 
           print('\u001b[31m',end="")
           Bank.seg()






           print('''Welcome to the Bank Menu. Press
           1  - Create Account
           2  - Close Account
           3  - Deposit Money
           4  - Withdraw Money
           5  - Make Transfer from one account to another
           6  - Create Branch
           7  - Get Transaction report for a date range(Customer/Branch/Bank)
           8  - Get Account Details
           9  - Get Customer Details
           10 - Get Branch Details
           11 - Get Bank Details
           12 - Roll the next date
           0  - exit ''')
           choice=inputf("Enter your Choice: ")
           Bank.seg()
           if(choice=='1'):
               self.createAccount()
           elif(choice=='2'):
               self.closeAccount()
           elif(choice=='3'):
               self.ask(0)
           elif(choice=='4'):
               self.ask(1)
           elif(choice=='5'):
               self.makeTransaction()
           elif(choice=='6'):
               print("New Branch Created!!")
               print("New Branch Number:",self.nextBranch)
               self.nextBranch+=1
           elif(choice=='7'):
               self.getTransactionReport()
           elif(choice=='8'):
               accno=int(inputf("Enter Account Number: "))
               if(accno not in self.Acc):
                   print("Account does not exist")
               else:
                   self.Acc[accno].printFullDetails(self)
           elif(choice=='9'):
               custid=inputf("Enter PersonID: ")
               if(custid not in self.Cust):
                   print("You don't have an account in the Bank yet.")
               else:
                   self.Cust[custid].printFullDetails(self)
           elif(choice=='10'):
               branchno=int(inputf("Enter Branch Number: "))
               if(branchno >= self.nextBranch or branchno < 1):
                   print("Branch Does not exist")
               else:
                   self.branch_PrintFullDetails(branchno)
           elif(choice=='11'):
               self.printFullDetails()
           elif(choice=='12'):
               self.date=self.date+datetime.timedelta(days=1)
               for i in self.Acc:
                   self.Acc[i].withdrawn=Bank.dec('0.0')
                   c.execute("UPDATE Accounts SET Withdrawn=0.0 WHERE Accno={}".format(i))
                  
               print("Date changed!!")
               print("Current Date:",self.date)
           elif(choice=='0'):
               print("Thank You for Banking with Us !!!")
               s.commit()
               s.close()
               print('\u001b[0m')
               break
           else:
               print("Please enter a valid option")


           inputf("Press any key to continue. ")
          
 
 
 
if __name__ == '__main__':
   ch=inputf("Do you want to use existing data?(y/n) ")
   while(ch!='y' and ch!='n'):
       ch=inputf("Please enter a valid choice. Do you want to use existing data?(y/n) ")
   if(ch=='n'):
       Formatall()
  
   c.execute("SELECT Accno,CustID,Balance,Branch,DWL,Withdrawn FROM Accounts;")
   data=c.fetchall()
   Acc={}
   for i in data:
       Acc[i[0]]=Bank.Accounts(i[0],i[1],i[2],i[3],i[4],i[5])
  
   c.execute("SELECT TID,Ttype,Acc1,Acc2,Val,date FROM Transactions;")
   data=c.fetchall()
   Trans={}
   for i in data:
       Trans[i[0]]=Bank.Transactions(i[0],i[1],i[2],i[3],i[4],i[5])
  
   c.execute("SELECT Custid,Name,Address,Email,Phoneno FROM Customers;")
   data=c.fetchall()
   Cust={}
   for i in data:
       Cust[i[0]]=Bank.Customers(i[0],i[1],i[2],i[3],i[4])
  
   c.execute("SELECT MAX(Branch) FROM Accounts;")
   nBranch=c.fetchall()[0][0]
   if(not nBranch):
       nBranch=1
   nBranch+=1
   bank=Bank(Acc,Cust,Trans,len(Acc)+1,nBranch,len(Trans)+1)
   bank.run()
