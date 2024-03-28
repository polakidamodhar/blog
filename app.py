from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='system',database='blog')
with mysql.connector.connect(host='localhost',user='root',password='system',database='blog'):
     cursor=mydb.cursor(buffered=True)
     cursor.execute('create table if not exists registrationform(Username varchar(50) primary key,Mobile varchar(20) unique,Email varchar(50),Address varchar(50),Password varchar(30))')
     cursor.execute('create table if not exists posts(id int primary key auto_increment,title varchar (255),content text,date_posted datetime DEFAULT CURRENT_TIMESTAMP,slug varchar(255),poster_id varchar(50))')
app=Flask(__name__)
app.secret_key='my scretkey is too secret'
@app.route('/')
def home():
    return render_template('homepage.html')
@app.route('/reg',methods=['GET','POST'])
def register():
    if request.method=='POST':
        Username=request.form['Username']
        Mobile=request.form['Mobile']
        Email=request.form['Email']
        Address=request.form['Address']
        Password=request.form['Password']
        cursor=mydb.cursor(buffered=True) 
        cursor.execute('insert into registrationform values(%s,%s,%s,%s,%s)',[Username,Mobile,Email,Address,Password])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def posts():
    if request.method=='POST':
        id=request.form['id']
        title=request.form['title']
        content=request.form['content']
        date_posted=request.form['date_posted']
        slug=request.form['slug']
        poster_id=request.form['poster_id']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into posts values(%s,%s,%s,%s,%s,%s)',[id,title,content,date_posted,slug,poster_id])
        mydb.commit()
        cursor.close()
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registrationform where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('home'))
        else:
            return 'INVALID USERNAME AND PASSWORD'
    return render_template('login.html')
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/addposts',methods=['GET','POST'])
def addposts():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('INSERT INTO posts(title,content,slug) VALUES(%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')
@app.route('/viewpost')
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    # PRINT(posts)
    print(posts)
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    if request.method=='POST':
        title=request.form["title"]
        content=request.form['slug']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',(id,))
        post=cursor.fetchone()
        cursor.execute('delete from posts where id=%s',(id,))
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewpost'))
@app.route('/delete_post/<int:id>',methods=['GET','POST'])
app.run()