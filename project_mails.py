import gmail
email='xxxxxxxxxxxxx@gmail.com'  #Mention Your gmail id
app_pass='xxxxxxxxxxxx'          #Mention app pass of same gmail account
def send_mail_for_openacn(to_mail,uacno,uname,upass,udate):
        con=gmail.GMail(email,app_pass)
        sub='Account Opened with ABC Bank'

        body=f"""Dear {uname},
        Your account has been opened successfully with ABC Bank and details are
    ACN={uacno}
    Pass={upass}
    Open Date = {udate}

    Kindly change your password when you login first time
    Thanks
    ABC Bank
    Noida
    """
        msg=gmail.Message(to=to_mail,subject=sub,text=body)
        con.send(msg)
        
def send_otp(to_mail,uname,uopt):
        con=gmail.GMail(email,app_pass)
        sub='OTP for Password recovery'
        body=f"""Dear {uname},
        Your OTP to get password = {uopt}

    Kindly Verify this OTP to application
    Thanks
    ABC Bank
    Noida
    """
        msg=gmail.Message(to=to_mail,subject=sub,text=body)
        con.send(msg)
        