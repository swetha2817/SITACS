from email import message
from os import access
import smtplib
from cryptography.fernet import Fernet
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from functools import wraps
import MySQLdb.cursors
from flask_mysqldb import MySQL
from io import BytesIO
import random
import os
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ai_cloud'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['UPLOAD_FILES'] = "static/files"
app.config["DOWNLOADS"] = "uploads"


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["upass"]
        cur = mysql.connection.cursor()
        cur.execute(
            "select * from reg where uname=%s and password=%s and status=True", (email, pwd))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = data["uname"]
            flash('Login Successfully', 'success')
            return redirect('home')
        else:
            flash(
                'Invalid Login / Admin Not Verified Your Account. Check Your Email, and Try Again', 'danger')
    return render_template("login.html")


@app.route('/downloadfile', methods=['POST', 'GET'])
def downloadfile():
    status = True
    if request.method == 'POST':
        filekey = request.form["filekey"]
        otp = request.form["otp"]
        cur = mysql.connection.cursor()
        cur.execute("select * from downloadrequest where username='" +
                    session["username"] + "' and fileaccesskey='" + filekey + "' and otp='" + otp + "'")
        data = cur.fetchone()
        if data:
            filename = data["filename"]
            cur.execute("update downloadrequest set status='" + "Downloaded" + "', otp='" + "" + "' where username='" +
                        session["username"] + "' and fileaccesskey='" + filekey + "'")
            mysql.connection.commit()
            cur.close()
            #shutil.copyfile("D:\\Iconix\\Projects\\2022\\Rani Anna\\project\\static\\files\\"+filename, "D:\\Iconix\\Projects\\2022\\Rani Anna\\project\\static\\downloads")
            flash('File Download Successfully', 'success')
            return send_from_directory(app.config["DOWNLOADS"], path=filename, as_attachment=True)
        else:
            flash('Invalid Key or OTP! Please Verify.', 'danger')
    return render_template("downloadfile.html")


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    status = True
    if request.method == 'POST':
        now = datetime.now()
        accesskey = os.urandom(12).hex()
        username = session["username"]
        filedec = request.form["filedec"]
        filename = request.files['uploadfile']

        if filename.filename != '':
            filepath = os.path.join(
                app.config['UPLOAD_FILES'], filename.filename)
            filepath1 = os.path.join(
                app.config['DOWNLOADS'], filename.filename + ".aes")
            filename.save(filepath)
            filename.save(filepath1)

            key1 = os.urandom(12).hex()
            buffersize = 64 * 1024

            f = Fernet(Fernet.generate_key())

            cur = mysql.connection.cursor()
            cur.execute("insert into upload(username, filename, filedec, filepath, fileaccesskey, datetime) values (%s,%s,%s,%s,%s,%s)",
                        (username, filename.filename, filedec, "static/files/" + filename.filename, accesskey, now))
            mysql.connection.commit()
            cur.close()

            flash('File Uploaded Successfully', 'success')
            return redirect('upload')
        else:
            flash('Error in File Upload! Try Again', 'danger')
    return render_template("upload.html")


@app.route('/viewfiles', methods=['POST', 'GET'])
def viewfiles():
    cur = mysql.connection.cursor()
    cur.execute("select * from upload where username='" +
                session["username"] + "'")
    data = cur.fetchall()
    return render_template("viewfiles.html", datas=data)


@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["upass"]
        if email == pwd == "Admin":
            flash('Login Successfully', 'success')
            return redirect('userslist')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("adminlogin.html")


@app.route('/userslist', methods=['POST', 'GET'])
def userslist():
    cur = mysql.connection.cursor()
    cur.execute("select * from reg where status=True")
    data = cur.fetchall()
    return render_template("userslist.html", datas=data)


@app.route('/waitinguserslist', methods=['POST', 'GET'])
def waitinguserslist():
    cur = mysql.connection.cursor()
    cur.execute("select * from reg where status=False")
    data = cur.fetchall()
    return render_template("waitinguserslist.html", datas=data)


@app.route('/<string:uname>/adminuserverify', methods=['POST', 'GET'])
def adminuserverify(uname):
    cur = mysql.connection.cursor()
    cur.execute("select * from reg where uname='" + uname + "'")
    data = cur.fetchone()
    email = data["email"]
    cur.execute("update reg set status=True where uname='" + uname + "'")
    mysql.connection.commit()
    cur.close()

    #mail_message = "Your Account is Verified!. Login and Access your Account"
    #server = smtplib.SMTP("smtp.gmail.com", 587)
    #server.starttls()
    #server.login("s.v.s.jeyalakshmi555@gmail.com", "JasLakshu@123")
    #server.sendmail("s.v.s.jeyalakshmi555@gmail.com", email, mail_message)

    flash('Verification Successfully. Information send to Users Registered Email.', 'success')
    return redirect(url_for('userslist'))


@app.route('/<string:fileaccesskey>/userdownloadrequest', methods=['POST', 'GET'])
def userdownloadrequest(fileaccesskey):
    cur = mysql.connection.cursor()
    cur.execute("select * from upload where username='" +
                session["username"] + "' and fileaccesskey = '" + fileaccesskey + "'")
    data = cur.fetchone()
    filename = data["filename"]
    cur.execute("insert into downloadrequest (username, filename, fileaccesskey, status, otp) values (%s,%s,%s,%s,%s)",
                (session["username"], filename, fileaccesskey, "Requested", ""))
    mysql.connection.commit()
    cur.close()
    flash('Your Request submitted Successfully. Information send to Users Registered Email.', 'success')
    return redirect(url_for('viewfilespyt'))


@app.route('/adminfileaccess', methods=['POST', 'GET'])
def adminfileaccess():
    cur = mysql.connection.cursor()
    cur.execute("select * from downloadrequest where status='" +
                "Requested" + "'")
    data = cur.fetchall()
    return render_template("adminfileaccess.html", datas=data)


@app.route('/<string:fileaccesskey>/adminfileaccesspersuc', methods=['POST', 'GET'])
def adminfileaccesspersuc(fileaccesskey):
    cur = mysql.connection.cursor()
    cur.execute(
        "select * from downloadrequest where fileaccesskey='" + fileaccesskey + "'")
    data1 = cur.fetchone()
    username = data1["username"]
    cur.execute("select * from reg where uname='" +
                username + "' and status=True")
    data = cur.fetchone()
    email = data["email"]
    otp = os.urandom(6).hex()
    cur.execute("update downloadrequest set status='" + "Done" + "', otp='" + otp + "' where username='" +
                username + "' and fileaccesskey='" + fileaccesskey + "'")
    mysql.connection.commit()
    cur.close()

    #mail_message = "Your download Request is Permitted!. Your File Access Key is " + \     fileaccesskey + " and OTP is " + otp + " . Login to download your file."
    #server = smtplib.SMTP("smtp.gmail.com", 587)
    #server.starttls()
    #server.login("s.v.s.jeyalakshmi555@gmail.com", "JasLakshu@123")
    #server.sendmail("s.v.s.jeyalakshmi555@gmail.com", email, mail_message)

    flash('Information send to Users Registered Email.', 'success')
    return redirect(url_for('adminfileaccess'))


@app.route('/<string:fileaccesskey>/adminfileaccessperdeny', methods=['POST', 'GET'])
def adminfileaccessperdeny(fileaccesskey):
    cur = mysql.connection.cursor()
    cur.execute(
        "select * from downloadrequest where fileaccesskey='" + fileaccesskey + "'")
    data1 = cur.fetchone()
    username = data1["username"]
    cur.execute("select * from reg where uname='" +
                username + "' and status=True")
    data = cur.fetchone()
    email = data["email"]
    cur.execute("update downloadrequest set status='" + "Deny" + "' where username='" +
                username + "' and fileaccesskey='" + fileaccesskey + "'")
    mysql.connection.commit()
    cur.close()

    #mail_message = "Your download Request is Not Permitted!. Thank You."
    #server = smtplib.SMTP("smtp.gmail.com", 587)
    #server.starttls()
    #server.login("s.v.s.jeyalakshmi555@gmail.com", "JasLakshu@123")
    #server.sendmail("s.v.s.jeyalakshmi555@gmail.com", email, mail_message)

    flash('Information send to Users Registered Email.', 'success')
    return redirect(url_for('adminfileaccess'))


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
    return wrap


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    status = False
    if request.method == 'POST':
        uname = request.form["uname"]
        pwd = request.form["upass"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        cname = request.form["cname"]
        coname = request.form["coname"]
        accesskey = request.form["acckesskey"]
        portno = request.form["port"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM reg WHERE uname LIKE %s", [uname])
        account = cursor.fetchone()
        if account:
            flash("Account already exists!", "danger")
        else:
            cur = mysql.connection.cursor()
            cur.execute("insert into reg(cloudname, cloudownername, accesskey, port, phone, email, uname, password, status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (cname, coname, accesskey, portno, mobile, email, uname, pwd, "False"))
            mysql.connection.commit()
            cur.close()
            flash('Registration Successfully. Admin Not Verified Your Account. Login after Verification notify to Your Registered Email.', 'success')
            return redirect('login')
    return render_template("reg.html", status=status)


@app.route("/home")
@is_logged_in
def home():
    return render_template('home.html')


@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
