from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox
import os,shutil
import time
from PIL import Image,ImageTk
import random
import project_tables
import sqlite3
import project_mails
from tkintertable import TableCanvas,TableModel
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry


def generate_captcha():
    captcha=[]
    for i in range(1):
        a=chr(random.randint(33,64))
        captcha.append(a)
        c=chr(random.randint(65,90))
        captcha.append(c)
        s=chr(random.randint(97,122))
        captcha.append(s)
        n=random.randint(0,9)
        captcha.append(str(n))        
    random.shuffle(captcha)
    captcha=' '.join(captcha)
    return captcha

def refresh_btn_func():
    captcha=generate_captcha()
    captcha_lbl.configure(text=captcha)

root=Tk()
combo=ttk.Combobox(root,state='readonly')
style=ttk.Style()
style.theme_use('default')
style.configure('TCombobox',
    foreground='black',
    background='white',
    fieldbackground='#FFFFFF',
    bordercolor='#B0BEC5',
    lightcolor='#E0E0E0',
    darkcolor='#E0E0E0',
    arrowcolor='black',
    borderwidth=2
)
style.configure('TButton',
    font=('Segoe UI', 12, 'bold'),
    foreground='white',
    background='#007ACC',
    padding=6,
    borderwidth=0,
    focusthickness=3,
    focuscolor='none'
)
style.map('TButton',
    background=[('active', '#005F99')],
    foreground=[('disabled', 'gray')],
    relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
)
root.state("zoomed")
root.configure(bg='#F2F7F2',highlightthickness=2,highlightbackground="black")
root.title("ABC bank")
bank_icon = ImageTk.PhotoImage(file="images/icon.jpg") 
root.iconphoto(False, bank_icon)

root.resizable(width = False,height = False)
title_lbl=Label(root,text="Bank Automation",bg='#F2F7F2', font=('Helvetica',60))
title_lbl.pack()

today_lbl=Label(root,text=time.strftime("%A,%d-%B-%Y"),bg='#F2F7F2', font=('Times New Roman',15,"bold"),fg='indigo')
today_lbl.pack(pady=10)

left_images=['images/logo_1.jpg','images/logo_4.jpg','images/logo_6.jpg','images/logo_7.jpg']
right_images=['images/logo_2.jpg','images/logo_5.jpg','images/logo_9.jpg','images/logo_8.jpg']
current_index=0
left_label=Label(root)
left_label.place(relx=0,rely=0)
right_label=Label(root)
right_label.place(relx=0.8,rely=0)

def logo_images():
    global left_images,right_images,current_index
    #LEFT IMAGE
    left_image_path=left_images[current_index]
    left_image_raw=Image.open(left_image_path)
    left_image_raw=left_image_raw.resize((300,150))
    left_img=ImageTk.PhotoImage(left_image_raw)
    left_label.config(image=left_img)
    left_label.image=left_img
    #RIGHT IMAGE
    right_image_path=right_images[current_index]
    right_image_raw=Image.open(right_image_path)
    right_image_raw=right_image_raw.resize((300,150))
    right_img=ImageTk.PhotoImage(right_image_raw)
    right_label.config(image=right_img)
    right_label.image=right_img
    current_index=(current_index + 1) % len(left_images)
    root.after(2000,logo_images)   
logo_images()

footer_lbl=Label(root,text="Developed by:Jagriti Nimiya",bg='#F2F7F2',fg='indigo',font=('Times New Roman',20,"bold"))
footer_lbl.pack(side='bottom',pady=7)
footer_lbl=Label(root,text="Project Guider:Mr Aditya Kumar",bg='#F2F7F2',fg='indigo',font=('Times New Roman',20,"bold"))
footer_lbl.pack(side='bottom',pady=7)

def main_screen():
    def forgot():
        frm.destroy()
        forgot_screen()
    def reset():
            user_combo.delete(0,"end")
            acn_entry.delete(0,"end")
            pass_entry.delete(0,"end")
            inputcap_entry.delete(0,"end")            
            user_combo.focus()
    def show_btn_func():
        if pass_entry.cget("show")== '':
            pass_entry.config(show='*')
            showpas_btn.config(text='show')
        else:
            pass_entry.config(show='')
            showpas_btn.config(text='hide')
    def login():
        uacn = acn_entry.get()
        upass=pass_entry.get()
        ucap=inputcap_entry.get()
        utype=user_combo.get()
        actual_cap=captcha_lbl.cget('text')
        actual_cap=actual_cap.replace(' ','')
        if utype=="Admin":
            if uacn=='0' and upass=='admin':
                if ucap==actual_cap:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login','Invalid captcha')
            else:
                messagebox.showerror('Login','Invalid Type/Account_No./password')
        elif utype=="User":
            if ucap==actual_cap:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                query='Select * from accounts where accounts_acno=? and accounts_pass=?'
                curobj.execute(query,(uacn,upass))
                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("User Login","Invalid account_no/password")
                else:
                    frm.destroy()
                    user_screen(uacn)
            else:
                messagebox.showerror('Login','Invalid captcha')
        else:
            messagebox.showerror("Login","Kindly Select Valid User Type")
    frm=Frame(root,highlightthickness=2,highlightbackground="gray")
    frm.configure(bg='lightyellow')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.7)

    user_lbl=Label(frm,text="User Type",bg='lightyellow',font=('Arial',20,'bold'))
    user_lbl.place(relx=.33,rely=.1)
    user_combo=Combobox(frm,values=['Admin','User','----------select----------'],font=('',20),state="readonly")
    user_combo.current(2)
    user_combo.place(relx=.48,rely=.1)

    acn_lbl=Label(frm,text="Account No.",bg='lightyellow',font=('Arial',20,'bold'))
    acn_lbl.place(relx=.33,rely=.2)
    acn_entry=Entry(frm,font=('Arial',20),bd=5,bg='lightgray')
    acn_entry.place(relx=.48,rely=.2)
    acn_entry.focus()

    pass_lbl=Label(frm,text="Password",bg='lightyellow',font=('Arial',20,'bold'))
    pass_lbl.place(relx=.33,rely=.3)
    pass_entry=Entry(frm,font=('Arial',20),bd=5,show='*',bg='lightgray')
    pass_entry.place(relx=.48,rely=.3)

    showpas_btn=Button(frm,text="Show 👁",command=show_btn_func,bg="gray",font=("Arial",10,"bold"))
    showpas_btn.place(relx=.69,rely=.3)

    global captcha_lbl
    captcha_lbl=Label(frm,text=generate_captcha(),bg='gray',font=('Arial',20,'bold'))
    captcha_lbl.place(relx=.48,rely=.4)

    img_3=Image.open("images/logo_3.jpg").resize((40,30))
    img_bitmap_3=ImageTk.PhotoImage(img_3)

    refresh_btn=Button(frm,image=img_bitmap_3,command=refresh_btn_func,bg="gray",bd=2)
    refresh_btn.image=img_bitmap_3
    refresh_btn.place(relx=.62,rely=.4)

    inputcap_lbl=Label(frm,text="Captcha",bg='lightyellow',font=('Arial',20,'bold'))
    inputcap_lbl.place(relx=.33,rely=.5)
    inputcap_entry=Entry(frm,font=('Arial',20),bd=5,bg='lightgray')
    inputcap_entry.place(relx=.48,rely=.5)

    login_btn=Button(frm,width=10,text="Login 🔓",bg="gray",font=("Arial",16,"bold"),bd="8",command=login)
    login_btn.place(relx=.48,rely=.6)

    reset_btn=Button(frm,width=10,text="Reset ♻",bg="gray",font=("Arial",16,"bold"),bd="8",command=reset)
    reset_btn.place(relx=.58,rely=.6)
    
    forgot_btn=Button(frm,width=22,text="Forgot Password ❓",bg="gray",font=("Arial",16,"bold"),bd="8",command=forgot)
    forgot_btn.place(relx=.48,rely=.75)

ifrm=None
def admin_screen():
    def open_acn():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        def open_acn_db():
            uname=name_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            uadhar=adhar_entry.get()
            upan=pan_entry.get()
            udob=dob_entry.get()
            uadd=add_entry.get()
            ugender=gender_combo.get()
            unomi=nomi_entry.get()
            ubal=0.0
            uopendate=datetime.now().strftime("%A, %d-%B-%Y")
            upass=generate_captcha().replace(' ','')

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?,?)'
            curobj.execute('insert into accounts(accounts_pass,accounts_Name,accounts_Mobile,accounts_Email,accounts_bal,accounts_Adhar,accounts_DOB,accounts_Address,accounts_Pan,accounts_Nominee,accounts_Gender,accounts_opendate) values(?,?,?,?,?,?,?,?,?,?,?,?)',(upass,uname,umob,uemail,ubal,uadhar,udob,uadd,upan,unomi,ugender,uopendate))
            conobj.commit()
            conobj.close()
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select max(accounts_acno) from accounts"
            curobj.execute(query)
            uacno=curobj.fetchone()[0]
            conobj.close()      
            try:
                project_mails.send_mail_for_openacn(uemail,uacno,uname,upass,uopendate)
                msg=f'Account opened with ACN {uacno} and mail sent to {uemail},Kindly check spam also'
                messagebox.showinfo('Open Account',msg)
            except Exception as msg:
                messagebox.showerror("Open Account",msg)
            


        def reset():
            name_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            add_entry.delete(0,"end")
            pan_entry.delete(0,"end")
            adhar_entry.delete(0,"end")
            dob_entry.delete(0,"end")
            nomi_entry.delete(0,"end")
            gender_combo.current(3)
            name_entry.focus()
        
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgrey')
        ifrm.place(relx=.22,rely=.03,relwidth=.75,relheight=.95)

        title_lbl=Label(ifrm,text="This is open account screen",bg="lightgray",font=('Arial',7,'bold'),bd=5,fg='black')
        title_lbl.pack()

        name_lbl=Label(ifrm,text="FULL Name",bg='lightgrey',font=('Arial',15,'bold'))
        name_lbl.place(relx=.03,rely=.03)
        name_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        name_entry.place(relx=.03,rely=.08)
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email ID",bg='lightgray',font=('Arial',15,'bold'))
        email_lbl.place(relx=.03,rely=.15)
        email_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        email_entry.place(relx=.03,rely=.2)

        mob_lbl=Label(ifrm,text="Mobile NO.",bg='lightgrey',font=('Arial',15,'bold'))
        mob_lbl.place(relx=.03,rely=.27)
        mob_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        mob_entry.place(relx=.03,rely=.32)

        adhar_lbl=Label(ifrm,text="Adhar No.",bg='lightgray',font=('Arial',15,'bold'))
        adhar_lbl.place(relx=.03,rely=.39)
        adhar_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        adhar_entry.place(relx=.03,rely=.44)

        pan_lbl=Label(ifrm,text="PAN No.",bg='lightgray',font=('Arial',15,'bold'))
        pan_lbl.place(relx=.03,rely=.51)
        pan_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        pan_entry.place(relx=.03,rely=.56)

        dob_lbl=Label(ifrm,text="DOB",bg='lightgray',font=('Arial',15,'bold'))
        dob_lbl.place(relx=.03,rely=.63)
        dob_entry = DateEntry(ifrm, font=('Arial',15), bd=5, bg='lightyellow', width=37, date_pattern='dd-mm-yyyy')
        dob_entry.place(relx=.03, rely=.68)

        add_lbl=Label(ifrm,text="Address",bg='lightgrey',font=('Arial',15,'bold'))
        add_lbl.place(relx=.03,rely=.75)
        add_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        add_entry.place(relx=.03,rely=.8)

        gender_lbl=Label(ifrm,text="Gender",bg='lightgrey',font=('Arial',15,'bold'))
        gender_lbl.place(relx=.03,rely=.87)
        gender_combo=Combobox(ifrm,values=['Male','Female','others','----------select----------'],font=('',15),state="readonly")
        gender_combo.current(3)
        gender_combo.place(relx=.03,rely=.92)

        nomi_lbl=Label(ifrm,text="Nominee Name",bg='lightgrey',font=('Arial',15,'bold'))
        nomi_lbl.place(relx=.55,rely=.03)
        nomi_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        nomi_entry.place(relx=.55,rely=.08)

        open_btn=Button(ifrm,width=20,text="Open Account",bg="gray",font=("Arial",16,"bold"),bd="8",command=open_acn_db)
        open_btn.place(relx=.74,rely=.75)

        reset_btn=Button(ifrm,width=20,command=reset,text="Reset Account ♻",bg="gray",font=("Arial",16,"bold"),bd="8")
        reset_btn.place(relx=.74,rely=.85)
        
    def delete_acn():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        def send_otp():
            uacn=int(acn_entry.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query='Select * from accounts where accounts_acno=? '
            curobj.execute(query,(uacn,))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Delete Account","Record Not Found")
            else:
                otp=str(random.randint(1000,9999))
                project_mails.send_otp(tup[3],tup[1],otp)
                messagebox.showinfo('Delete Account','OTP sent to registered mail id')
                otp_entry=Entry(ifrm,font=('Arial',20),bd=5,bg='lightyellow')
                otp_entry.place(relx=.4,rely=.6)
                def verify():
                    uotp=otp_entry.get()
                    if otp==uotp:
                        resp=messagebox.askyesno("Delete Account",f"Do you want to delete this account?")
                        if not resp:
                            ifrm.destroy()
                            admin_screen()
                            return
                        conobj=sqlite3.connect(database="bank.sqlite")
                        curobj=conobj.cursor()
                        query='delete from accounts where accounts_acno=? '
                        curobj.execute(query,(uacn,))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo("Delete Account","Account Deleted")
                        frm.destroy()
                        admin_screen()               
                    else:
                        messagebox.showerror("Delete Account","Incorrect OTP")
                    
                verify_btn=Button(ifrm,width=10,command=verify,text="Verify",bg="gray",font=("Arial",15,"bold"),bd="8")
                verify_btn.place(relx=.4,rely=.8)
                 
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.25,rely=.05,relwidth=.5,relheight=.8)

        title_lbl=Label(ifrm,text="This is delete account screen",bg="lightgray",font=('Arial',16,'bold'),bd=5,fg='black')
        title_lbl.pack()

        acn_lbl=Label(ifrm,text="Account No.",bg='lightgrey',font=('Arial',15,'bold'))
        acn_lbl.place(relx=.2,rely=.2)

        acn_entry=Entry(ifrm,font=('Arial',20),bd=5,bg='lightyellow')
        acn_entry.place(relx=.4,rely=.2)
        acn_entry.focus()

        otp_btn=Button(ifrm,width=10,command=send_otp,text="Send OTP",bg="gray",font=("Arial",16,"bold"),bd="8")
        otp_btn.place(relx=.4,rely=.4)
        
    def view_acn():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        def view_details():
            uacn=int(acn_entry.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query='Select * from accounts where accounts_acno=? '
            curobj.execute(query,(uacn,))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("View Account","Record Not Found")
            else:
                opendate = tup[11]if tup[11]else"Not Available"
                details=f"""user Name = {tup[1]}
                            Aval Bal = {tup[12]}
                            ACN Open Date = {opendate}
                            Email = {tup[3]}
                            Mob = {tup[4]} """
                messagebox.showinfo("view Account",details)#
             
                 
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.25,rely=.05,relwidth=.5,relheight=.8)

        title_lbl=Label(ifrm,text="This is view account screen",bg="lightgray",font=('Arial',16,'bold'),bd=5,fg='black')
        title_lbl.pack()

        acn_lbl=Label(ifrm,text="Account No.",bg='lightgrey',font=('Arial',15,'bold'))
        acn_lbl.place(relx=.2,rely=.2)

        acn_entry=Entry(ifrm,font=('Arial',20),bd=5,bg='lightyellow')
        acn_entry.place(relx=.4,rely=.2)
        acn_entry.focus()

        view_btn=Button(ifrm,width=10,command=view_details,text="view",bg="gray",font=("Arial",16,"bold"),bd="8")
        view_btn.place(relx=.4,rely=.4)
        
    def logout():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        resp=messagebox.askyesno("logout","Do you want to logout?")
        if resp:
            frm.destroy()
            main_screen()  
    frm=Frame(root,highlightthickness=2,highlightbackground="gray")
    frm.configure(bg='lightyellow')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.7) 

    wel_lbl=wel_lbl=Label(frm,text=f"Welcome,Admin",bg="lightyellow",font=('Arial',20),bd=5,fg='black')
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,width=22,text="logout",bg="gray",font=("Arial",16,"bold"),bd="8",command=logout)
    logout_btn.place(relx=0,rely=.60)

    open_btn=Button(frm,width=22,command=open_acn,text="Open Account",bg="gray",font=("Arial",16,"bold"),bd="8")
    open_btn.place(relx=0,rely=.15)

    delete_btn=Button(frm,width=22,text="Delete Account",bg="gray",font=("Arial",16,"bold"),bd="8",command=delete_acn)
    delete_btn.place(relx=0,rely=.30)

    view_btn=Button(frm,width=22,text="View Account",bg="gray",font=("Arial",16,"bold"),bd="8",command=view_acn)
    view_btn.place(relx=0,rely=.45)

def forgot_screen():
    def back():
        frm.destroy()
        main_screen()
    def reset():
            acn_entry.delete(0,"end")
            email_entry.delete(0,"end")
            inputcap_entry.delete(0,"end")       
            acn_entry.focus()
    def send_otp():
        uacn=int(acn_entry.get())
        uemail=email_entry.get()
        ucaptcha=inputcap_entry.get()
        if ucaptcha!=forgot_captcha.replace(' ',''):
            messagebox.showerror('Forgot password','Invalid captcha')
            return
        #authenticate acn & email
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query='Select * from accounts where accounts_acno=? and accounts_email=?'
        curobj.execute(query,(uacn,uemail))
        tup=curobj.fetchone()
        curobj.close()
        if tup==None:
            messagebox.showerror("Forgot Password","Record Not Found")
        else:
            otp=str(random.randint(1000,9999))
            project_mails.send_otp(uemail,tup[1],otp)
            messagebox.showinfo('Forgot pass','OTP sent to given/registered mail id')

            otp_entry=Entry(frm,font=('Arial',20),bd=5,bg='lightgray')
            otp_entry.place(relx=.48,rely=.71)
            def verify():
                uotp=otp_entry.get()
                if otp==uotp:
                    messagebox.showinfo("Forgot Password",f"Your Pass={tup[2]}")
                else:
                    messagebox.showerror("Forgot Pass","Incorrect OTP")
            verify_btn=Button(frm,width=10,command=verify,text="Verify",bg="gray",font=("Arial",16,"bold"),bd="8")
            verify_btn.place(relx=.48,rely=0.8)
    frm=Frame(root,highlightthickness=2,highlightbackground="gray")
    frm.configure(bg='lightyellow')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.7)

    back_btn=Button(frm,text="Back",bg="gray",font=("Arial",16,"bold"),bd="8",command=back)
    back_btn.place(relx=0.95,rely=0.9)

    acn_lbl=Label(frm,text="Account No.",bg='lightyellow',font=('Arial',20,'bold'))
    acn_lbl.place(relx=.33,rely=.2)
    acn_entry=Entry(frm,font=('Arial',20),bd=5,bg='lightgray')
    acn_entry.place(relx=.48,rely=.2)
    acn_entry.focus()

    email_lbl=Label(frm,text="Email",bg='lightyellow',font=('Arial',20,'bold'))
    email_lbl.place(relx=.33,rely=.3)
    email_entry=Entry(frm,font=('Arial',20),bd=5,bg='lightgray')
    email_entry.place(relx=.48,rely=.3)

    global captcha_lbl
    forgot_captcha=generate_captcha()
    captcha_lbl=Label(frm,text=forgot_captcha,bg='gray',font=('Arial',20,'bold'))
    captcha_lbl.place(relx=.48,rely=.4)

    img_3=Image.open("images/logo_3.jpg").resize((40,30))
    img_bitmap_3=ImageTk.PhotoImage(img_3)

    refresh_btn=Button(frm,image=img_bitmap_3,command=refresh_btn_func,bg="gray",bd=2)
    refresh_btn.image =img_bitmap_3
    refresh_btn.place(relx=.62,rely=.4)

    inputcap_lbl=Label(frm,text="Captcha",bg='lightyellow',font=('Arial',20,'bold'))
    inputcap_lbl.place(relx=.33,rely=.5)
    inputcap_entry=Entry(frm,font=('Arial',20),bd=5,bg='lightgray')
    inputcap_entry.place(relx=.48,rely=.5)

    otp_btn=Button(frm,width=10,command=send_otp,text="Send OTP",bg="gray",font=("Arial",16,"bold"),bd="8")
    otp_btn.place(relx=.48,rely=.6)

    reset_btn=Button(frm,width=10,text="Reset ♻",bg="gray",font=("Arial",16,"bold"),bd="8",command=reset)
    reset_btn.place(relx=.58,rely=.6)

def user_screen(uacn=None):
    def logout():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        resp=messagebox.askyesno("logout","Do you want to logout?")
        if resp:
            frm.destroy()
            main_screen()
    def update_btn_screen():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        def update_db():
            uname=name_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            uadd=add_entry.get()
            unomi=nomi_entry.get()
            upass=pass_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set accounts_name=?,accounts_email=?,accounts_mobile=?,accounts_address=?,accounts_nominee=?,accounts_pass=? where accounts_acno=?' 
            curobj.execute(query,(uname,uemail,umob,uadd,unomi,upass,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Details","profile Updated")
            frm.destroy()
            user_screen(uacn)
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.22,rely=.03,relwidth=.75,relheight=.95)

        title_lbl=Label(ifrm,text="This is Update Screen",bg="lightgray",font=('Arial',20,'bold'),bd=5,fg='Black')
        title_lbl.pack()
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query='Select * from accounts where accounts_acno=? '
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        name_lbl=Label(ifrm,text="FULL Name",bg='lightgray',font=('Arial',15,'bold'))
        name_lbl.place(relx=.03,rely=.03)
        name_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        name_entry.place(relx=.03,rely=.09)
        name_entry.insert(0,tup[1])
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email ID",bg='lightgray',font=('Arial',15,'bold'))
        email_lbl.place(relx=.03,rely=.15)
        email_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        email_entry.place(relx=.03,rely=.21)
        email_entry.insert(0,tup[3])

        mob_lbl=Label(ifrm,text="Mobile NO.",bg='lightgrey',font=('Arial',15,'bold'))
        mob_lbl.place(relx=.03,rely=.27)
        mob_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        mob_entry.place(relx=.03,rely=.33)
        mob_entry.insert(0,tup[4])

        add_lbl=Label(ifrm,text="Address",bg='lightgrey',font=('Arial',15,'bold'))
        add_lbl.place(relx=.03,rely=.39)
        add_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        add_entry.place(relx=.03,rely=.45)
        add_entry.insert(0,tup[8])

        nomi_lbl=Label(ifrm,text="Nominee Name",bg='lightgrey',font=('Arial',15,'bold'))
        nomi_lbl.place(relx=.03,rely=.51)
        nomi_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        nomi_entry.place(relx=.03,rely=.57)
        nomi_entry.insert(0,tup[10])

        pass_lbl=Label(ifrm,text="password",bg='lightgrey',font=('Arial',15,'bold'))
        pass_lbl.place(relx=.03,rely=.63)
        pass_entry=Entry(ifrm,font=('Arial',15),bd=5,bg='lightyellow',width=40)
        pass_entry.place(relx=.03,rely=.69)
        pass_entry.insert(0,tup[2])

        update_btn=Button(ifrm,width=22,text="Update",bg="gray",font=("Arial",18,"bold"),bd=8,command=update_db)
        update_btn.place(relx=.60,rely=.75)

    def deposit_btn_screen():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        def deposit():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='Bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()
            conobj=sqlite3.connect(database='Bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,)) 
            ubal=curobj.fetchone()[0]
            conobj.close()
            
            t=str(time.time())
            utxnid='txt'+t[:t.index('.')]
            conobj=sqlite3.connect(database='Bank.sqlite')
            curobj=conobj.cursor()
            query='insert into stmts values(?,?,?,?,?,?)'
            curobj.execute(query,(uacn,uamt,'CR',time.strftime("%d-%m-%Y-%r"),ubal,utxnid))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit",f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn)
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.22,rely=.03,relwidth=.75,relheight=.95)

        title_lbl=Label(ifrm,text="This is deposit Screen",bg="lightgray",font=('Arial',20,'bold'),bd=5,fg='Black')
        title_lbl.pack()

        amt_lbl=Label(ifrm,text="Amount",bg='lightgrey',font=('Arial',15,'bold'))
        amt_lbl.place(relx=.2,rely=.2)
        amt_entry=Entry(ifrm,font=('Arial',20),bd=5,bg='lightyellow')
        amt_entry.place(relx=.4,rely=.2)
        amt_entry.focus()

        dep_btn=Button(ifrm,width=10,command=deposit,text="Deposit",bg="gray",font=("Arial",16,"bold"),bd="8")
        dep_btn.place(relx=.4,rely=.4)

    def withdraw_btn_Screen():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        def withdraw():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='Bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()
            if ubal>=uamt:
                conobj=sqlite3.connect(database='Bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()

                t=str(time.time())
                utxnid='txt'+t[:t.index('.')]
                conobj=sqlite3.connect(database='Bank.sqlite')
                curobj=conobj.cursor()
                query='insert into stmts values(?,?,?,?,?,?)'
                curobj.execute(query,(uacn,uamt,'DR',time.strftime("%d-%m-%Y-%r"),ubal-uamt,utxnid))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("withdraw",f"{uamt} Amount withdrawn")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("withdraw","Insufficient bal {ubal}")
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.22,rely=.03,relwidth=.75,relheight=.95)

        title_lbl=Label(ifrm,text="This is withdraw Screen",bg="lightgray",font=('Arial',20,'bold'),bd=5,fg='Black')
        title_lbl.pack()

        amt_lbl=Label(ifrm,text="Amount",bg='lightgrey',font=('Arial',15,'bold'))
        amt_lbl.place(relx=.2,rely=.2)
        amt_entry=Entry(ifrm,font=('Arial',20),bd=5,bg='lightyellow')
        amt_entry.place(relx=.4,rely=.2)
        amt_entry.focus()

        dep_btn=Button(ifrm,width=10,command=withdraw,text="withdraw",bg="gray",font=("Arial",16,"bold"),bd="8")
        dep_btn.place(relx=.4,rely=.4)

    def check_btn_screen():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.22,rely=.03,relwidth=.75,relheight=.95)

        title_lbl=Label(ifrm,text="This is Details Screen",bg="lightgray",font=('Arial',20,'bold'),bd=5,fg='Black')
        title_lbl.pack()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query='Select * from accounts where accounts_acno=? '
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup is not None:
            opendate = tup[11]if tup[11]else"Not Available"
            Details=f''' Accounts No. = {tup[0]}

        Opening Date = {opendate}

            Availabale bal = {tup[12]}

                    Email ID = {tup[3]}

              Mobile No. = {tup[4]}'''
        else:
            Details="Account not Found!"
        details_lbl=Label(ifrm,text=Details,bg="lightgray",font=('Arial',12,'bold'),bd=5,fg='indigo')
        details_lbl.place(relx=.30,rely=.1)

    def transfer_btn_screen():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        def transfer():
            toacn=to_entry.get()
            uamt=float(amt_entry.get())

            conobj=sqlite3.connect(database='Bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(toacn,))
            to_tup=curobj.fetchone()
            conobj.close()

            if to_tup==None:
                messagebox.showerror("transfer","To ACN does not exist")
                return
            conobj=sqlite3.connect(database='Bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                conobj=sqlite3.connect(database='Bank.sqlite')
                curobj=conobj.cursor()
                query_deduct='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                query_credit='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
                curobj.execute(query_deduct,(uamt,uacn))
                curobj.execute(query_credit,(uamt,toacn))
                conobj.commit()
                conobj.close()

                t=str(time.time())
                utxnid1='txt_DR'+t[:t.index('.')]
                utxnid2='txt_CR'+t[:t.index('.')]
                conobj=sqlite3.connect(database='Bank.sqlite')
                curobj=conobj.cursor()
                query1='insert into stmts values(?,?,?,?,?,?)'
                query2='insert into stmts values(?,?,?,?,?,?)'
                curobj.execute(query1,(uacn,uamt,'DR',time.strftime("%d-%m-%Y-%r"),ubal-uamt,utxnid1))          
                curobj.execute(query2,(toacn,uamt,'CR',time.strftime("%d-%m-%Y-%r"),ubal+uamt,utxnid2))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{uamt} Amount Transferred")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Transfer","Insufficient bal {ubal}")
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.22,rely=.03,relwidth=.75,relheight=.95)

        title_lbl=Label(ifrm,text="This is Transfer Screen",bg="lightgray",font=('Arial',20,'bold'),bd=5,fg='Black')
        title_lbl.pack()

        to_lbl=Label(ifrm,text="TO ACN",bg='lightgrey',font=('Arial',15,'bold'))
        to_lbl.place(relx=.3,rely=.2)

        to_entry=Entry(ifrm,font=('Arial',20),bd=5,bg='lightyellow')
        to_entry.place(relx=.45,rely=.2)
        to_entry.focus()

        amt_lbl=Label(ifrm,text="Amount",bg='lightgrey',font=('Arial',15,'bold'))
        amt_lbl.place(relx=.3,rely=.4)

        amt_entry=Entry(ifrm,font=('Arial',20),bd=5,bg='lightyellow')
        amt_entry.place(relx=.45,rely=.4)
        
        tr_btn=Button(ifrm,width=10,command=transfer,text="Transfer",bg="gray",font=("Arial",16,"bold"),bd="8")
        tr_btn.place(relx=.45,rely=.6)

    def history_btn_screen():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='lightgray')
        ifrm.place(relx=.22,rely=.03,relwidth=.75,relheight=.95)

        title_lbl=Label(ifrm,font=('arial',20,'bold'),bd=5,bg='lightgray',text="This is Txn History screen",fg='Black')
        title_lbl.pack()
        # Create a Frame (Fix for NoneType error)
        frame = Frame(ifrm)
        frame.place(relx=.1,rely=.1,relwidth=.7)
        data={}
        i=1
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from stmts where stmts_acn=?",(uacn,))
        for tup in curobj:
            data[f"{i}"]= {"Txn Id": tup[5], "Txn Amt":tup[1], "Txn Date": tup[3],"Txn Type":tup[2],"Updated Bal":tup[4]}
            i+=1
        conobj.close()
        # Create Table Model
        model = TableModel()
        model.importDict(data)  # Load data into the model
        # Create Table Canvas inside Frame 
        table = TableCanvas(frame, model=model, editable=True)
        table.show()

    def getdetail():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query='Select * from accounts where accounts_acno=? '
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        return tup
    
    def update_picture():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
        img_folder=os.path.join(os.getcwd(),"images")
        path=filedialog.askopenfilename(initialdir=img_folder,title="Select an image",filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if not path:
            print("No file selected..")
            return
        try:
            filename=f"images/profile_{uacn}.jpg"
            if os.path.abspath(path)!=os.path.abspath(filename):
                shutil.copy(path,filename)

            profile_img=Image.open(f"images/profile_{uacn}.jpg").resize((210,180))
            profile_img_bitmap=ImageTk.PhotoImage(profile_img,master=root)
            profile_img_lbl.image=profile_img_bitmap
            profile_img_lbl.configure(image=profile_img_bitmap)
        except Exception as e:
            print("Error updating picture..",e)

    frm=Frame(root)
    frm.configure(bg='lightyellow')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.7)

    wel_lbl=Label(frm,text=f"Welcome,{getdetail()[1]}",bg="lightyellow",font=('Arial',12),bd=5,fg='indigo')
    wel_lbl.place(relx=0,rely=0) 

    logout_btn=Button(frm,width=22,text="Logout",bg="gray",font=("Arial",14,"bold"),bd=8,command=logout)
    logout_btn.place(relx=0,rely=.92)

    if os.path.exists(f'images/profile_{uacn}.jpg'):
        path=f"images/profile_{uacn}.jpg"
    else:
        path="images/default_profile.jpg"

    profile_img=Image.open(path).resize((250,200))
    profile_img_bitmap=ImageTk.PhotoImage(profile_img,master=root)
    profile_img_lbl=Label(frm,image=profile_img_bitmap)
    profile_img_lbl.image=profile_img_bitmap
    profile_img_lbl.place(relx=0.01,rely=0.05)

    update_pic_btn=Button(frm,width=22,text="Update picture",bg="gray",font=("Arial",14,"bold"),bd=8,command=update_picture)
    update_pic_btn.place(relx=0,rely=.36)

    check_btn=Button(frm,width=22,text="Check Details",bg="gray",font=("Arial",14,"bold"),bd=8,command=check_btn_screen)
    check_btn.place(relx=0,rely=.44)
    
    deposit_btn=Button(frm,width=22,text="Deposit",bg="gray",font=("Arial",14,"bold"),bd=8,command=deposit_btn_screen)
    deposit_btn.place(relx=0,rely=.52)

    withdraw_btn=Button(frm,width=22,text="Withdraw",bg="gray",font=("Arial",14,"bold"),bd=8,command=withdraw_btn_Screen)
    withdraw_btn.place(relx=0,rely=.60)

    transfer_btn=Button(frm,width=22,text="Transfer",bg="gray",font=("Arial",14,"bold"),bd=8,command=transfer_btn_screen)
    transfer_btn.place(relx=0,rely=.68)

    history_btn=Button(frm,width=22,text="History",bg="gray",font=("Arial",14,"bold"),bd=8,command=history_btn_screen)
    history_btn.place(relx=0,rely=.76)

    update_btn=Button(frm,width=22,text="Update",bg="gray",font=("Arial",14,"bold"),bd=8,command=update_btn_screen)
    update_btn.place(relx=0,rely=.84)

main_screen()
root.mainloop()

