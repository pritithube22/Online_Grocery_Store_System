from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from fpdf import FPDF
from datetime import datetime


app=Flask(__name__)

app.secret_key='komal'
date=datetime.now()


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='password'
app.config['MYSQL_DB']='project3'

mysql=MySQL(app)

@app.route('/',methods=['POST','GET'])
def home():    
    data=''
    cursor=mysql.connection.cursor()
    cursor.execute('select * from project3.category')
    data=cursor.fetchall()

    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM vegetable WHERE veg_id<11 ")
    rows=cursor.fetchall()

    return render_template('index.html',data=data)

@app.route('/index2',methods=['POST','GET'])
def home2():    
    data=''
    cursor=mysql.connection.cursor()
    cursor.execute('select * from project3.category')
    data=cursor.fetchall()

    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM vegetable WHERE veg_id<11 ")
    rows=cursor.fetchall()

    return render_template('index2.html',data=data,fname=session['fname'],lname=session['lname'])

@app.route('/login1.html',methods=['POST','GET'])
def login1():
    msg =' '
    if request.method=='POST' and 'email' in request.form and 'password' in request.form :
        session['email'] = request.form['email']
        session['password']=request.form['password']

        email=session['email']
        password=session['password']

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user WHERE email=%s  AND password=%s',(email,password,))
        user=cursor.fetchone()
        
        if user:
            session['loggedin']=True
            session['userid']=user['userid']
            session['fname']=user['fname']
            session['lname']=user['lname']
            session['email'] = user['email']
            msg='Logged sucessfully'
            return redirect(url_for('home2'))
            
        else:
            msg='Enter Correct Email /Password ' 

        # userid=session['userid']   

    return render_template('login1.html',msg=msg)   

@app.route('/register1.html', methods =['GET', 'POST'])
def register1():
    msg=''
    if request.method=='POST' and 'fname' in request.form and 'lname' in request.form and 'email' in request.form  and 'password' in request.form :
        session['fname']=request.form['fname']
        session['lname']=request.form['lname']
        session['email'] = request.form['email']
        session['password']=request.form['password']

        fname=session['fname']
        lname=session['lname']        
        email=session['email']
        password=session['password']


        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s ',(email,))
        account = cursor.fetchone()
        if account:
            msg='Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Invalid email address !'
        elif not fname or not lname or not password or not email:
            msg='Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL,%s,%s,%s,%s)', (fname,lname,email, password, ))
            mysql.connection.commit()
            msg='You have successfully registered !'
            return redirect(url_for('login1'))
    elif request.method == 'POST':
        msg= 'Please fill out the form !'
    return render_template('register1.html',msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login1'))


@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/about2.html')
def about2():
    return render_template('about2.html',fname=session['fname'],lname=session['lname'])
    
@app.route('/blog.html')
def blog():
    return render_template('blog.html')
        
@app.route('/blog-single.html')
def blogsingle():
    return render_template('blog-single.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# @app.route('/contact2.html')
# def contact2():
#     return render_template('contact.html',fname=session['fname'],lname=session['lname'])

@app.route('/final_bill')
def final_bill():
    return render_template('final_bill.html')

@app.route('/products',methods=['POST','GET'])
def products():
    rows=''
    if request.method=='POST':
        cat_name=request.form['cat_name']

        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM vegetable WHERE cat_name=%s",(cat_name,))
        rows=cursor.fetchall()
        # print(rows[1][2])

    return render_template('products.html',products=rows)

@app.route('/products2',methods=['POST','GET'])
def products2():
    rows=''
    if request.method=='POST':
        cat_name=request.form['cat_name']

        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM vegetable WHERE cat_name=%s",(cat_name,))
        rows=cursor.fetchall()
        # print(rows[1][2])

    return render_template('products2.html',products=rows,fname=session['fname'],lname=session['lname'])


@app.route('/add', methods=['POST'])
def add_product_to_cart():
    if 'loggedin' in session :  
      #cursor = None
      if request.method == 'POST' and 'quantity' in request.form and 'code' in request.form:
        session['_quantity'] = int(request.form['quantity'])
        _quantity=session['_quantity']

        _code = request.form['code']
      # validate the received values
      #if _quantity and _code and request.method == 'POST':
        cursor = mysql.connection.cursor()
        #return str(_code)
        cursor.execute("SELECT * FROM vegetable WHERE code=%s",( _code,))
        row = cursor.fetchone()
        #return str(row)
        
        itemArray = { row[4] : {'veg_name' : row[3], 'code' : row[4], 'quantity' : _quantity, 'rate' : row[6], 'image' : row[8], 'total_price': _quantity * row[6]}}
        
        all_total_price = 0
        all_total_quantity = 0

        
        session.modified = True
        if 'cart_item' in session:
          if row[4] in session['cart_item']:
           for key, value in session['cart_item'].items():
            if row[4] == key:
             old_quantity = session['cart_item'][key]['quantity']
             total_quantity = old_quantity + _quantity
             session['cart_item'][key]['quantity'] = total_quantity
             session['cart_item'][key]['total_price'] = total_quantity * row[6]
             print(session['cart_item'][key]['veg_name'])

          else:
           session['cart_item'] = array_merge(session['cart_item'], itemArray)
           # print(session['cart_item'][key]['veg_name'])

     
          for key, value in session['cart_item'].items():
           individual_quantity = int(session['cart_item'][key]['quantity'])
           individual_price = float(session['cart_item'][key]['total_price'])
           all_total_quantity = all_total_quantity + individual_quantity
           all_total_price = all_total_price + individual_price
           print(session['cart_item'][key]['veg_name'])

        else:
          session['cart_item'] = itemArray
          all_total_quantity = all_total_quantity + _quantity
          all_total_price = all_total_price + _quantity * row[6]

        
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price

        session['rate']=row[6]
        rate=session['rate']

        session['veg_name']=row[3]
        veg_name=session['veg_name']



        # session['overall_price']=overall_price
        # session['dilivery_charge']=dilivery_charge


        
        return redirect(url_for('.home2'))
      else:
        return 'Error while adding item to cart'	# finally :

    else:
        return redirect(url_for('login1'))

@app.route('/empty')
def empty_cart():
 try:
  session.clear()
  return redirect(url_for('.cart'))
 except Exception as e:
  print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
 try:
  all_total_price = 0
  all_total_quantity = 0
  session.modified = True
   
  for item in session['cart_item'].items():
   if item[0] == code:    
    session['cart_item'].pop(item[0], None)
    if 'cart_item' in session:
     for key, value in session['cart_item'].items():
      individual_quantity = int(session['cart_item'][key]['quantity'])
      individual_price = float(session['cart_item'][key]['total_price'])
      all_total_quantity = all_total_quantity + individual_quantity
      all_total_price = all_total_price + individual_price
    break
   
  if all_total_quantity == 0:
   session.clear()
  else:
   session['all_total_quantity'] = all_total_quantity
   session['all_total_price'] = all_total_price
   
  return redirect(url_for('.cart'))
 except Exception as e:
  print(e)
   
def array_merge( first_array , second_array ):
 if isinstance( first_array , list ) and isinstance( second_array , list ):
  return first_array + second_array
 elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
  return dict( list( first_array.items() ) + list( second_array.items() ) )
 elif isinstance( first_array , set ) and isinstance( second_array , set ):
  return first_array.union( second_array )
 return False

@app.route('/cart.html')
def cart():
    # if 'loggedin' in session :
        
    
    # else:
    #     return redirect(url_for('login1'))
    return render_template('cart.html')



@app.route('/checkout',methods =['GET', 'POST'])
def checkout():
    if 'loggedin' in session :
        data=''
        msg=''
        msg1=''
        msg2=''
        msg3=''

        dilivery_charge=''
        overall_price=''
        session.modified = True
        if request.method=='POST' and 'customer' in request.form and 'address' in request.form and 'city' in request.form and 'pin' in request.form and 'state' in request.form and 'country' in request.form and 'mobile' in request.form and 'email' in request.form :
            address=request.form['address']
            city=request.form['city']
            pin=request.form['pin']
            # if pin>416000 and pin<416550:
            #     msg='Successfull'

            # else:
            #     msg='Enter valid pin'

                
            state=request.form['state']
            country=request.form['country']
            mobile=request.form['mobile']

            print('hii')

            cursor=mysql.connection.cursor()
            cursor.execute('SELECT * FROM customer_master WHERE email=%s ',(session['email'],))
            data = cursor.fetchone()
            if not data:                
                cursor=mysql.connection.cursor()
                cursor.execute('INSERT INTO  project3.customer_master(userid,fname,lname,address,city,pin,state,country,mobile,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(session['userid'],session['fname'],session['lname'],address,city,pin,state,country,mobile,session['email']))
                mysql.connection.commit()
                msg='Record added successfully  !'

           


        # if request.method =='POST' and 'order' in request.form and 'orderdate' in request.form and 'ordertime' in request.form:
        #     session['orderdate']=request.form['orderdate']
        #     session['orderid']=request.form['orderid']
        #     session['ordertime']=request.form['ordertime']

        #     orderdate=session['orderdate']

        if request.method=='POST' and  'orderdate' in request.form and 'ordertime' in request.form :
            print('hello')
            session['orderdate']=request.form['orderdate']
            session['ordertime']=request.form['ordertime']
            # _code = request.form['code']
            # session['orderid']=request.form['orderid']

            orderdate=session['orderdate']
            ordertime=session['ordertime']
            # orderid=session['orderid']
            # fname=request.form['fname']
            # lname=request.form['lname']

            # print('hii')
            

            dilivery_charge=0
            overall_price=0
            if session['all_total_price']<150:
                dilivery_charge=(session['all_total_price']*10)/100
                overall_price=session['all_total_price']+dilivery_charge
            else:
                overall_price=session['all_total_price']



            cursor=mysql.connection.cursor()
            cursor.execute('INSERT INTO  project3.order1(orderid,orderdate,ordertime,userid,fname,lname,all_total_price,dilivery_charge,overall_price) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s)',(orderdate,ordertime,session['userid'],session['fname'],session['lname'],session['all_total_price'],dilivery_charge,overall_price))
            mysql.connection.commit()
            msg1='Order placed successfully  !'
            # return redirect(url_for('login1'))

            # cursor = mysql.connection.cursor()
            # #return str(_code)
            # # cursor.execute("SELECT * FROM vegetable WHERE code=%s",( _code,))
            # # row = cursor.fetchone()
            # cursor.execute("SELECT * FROM order1 WHERE userid=%s ORDER BY orderid DESC LIMIT 1",( session['userid'],))
            # order = cursor.fetchone()
            # mysql.connection.commit()
            # cursor=mysql.connection.cursor()
            # cursor.execute('INSERT INTO  project3.orderdetail(orderid,cat_id,veg_id,veg_name,rate,quantity,total_price) VALUES (%s,%s,%s,%s,%s,%s,%s)',(order[0],session['cat_id'],session['veg_id'],session['veg_name'],session['quantity'],session['rate'],session['total_price']))
            # mysql.connection.commit()
            # msg2='order added successfully  !'

    else:
        return redirect(url_for('login1'))



    return render_template('checkout.html',msg=msg,msg1=msg1,msg2=msg2,msg3=msg3,data=data,userid=session['userid'],email=session['email'],all_total_quantity=session['all_total_quantity'] ,all_total_price=session['all_total_price'],fname=session['fname'],lname=session['lname'],password=session['password'],dilivery_charge=dilivery_charge,overall_price=overall_price)



    #         dilivery_charge=0
    #         if session['all_total_price']<200:
    #             dilivery_charge=(session['all_total_price']*10)/100

    #         else:
    #             overall_price=session['all_total_price']+dilivery_charge

    #         # session['overall_price']=overall_price
    #         # session['dilivery_charge']=dilivery_charge

    #         cursor=mysql.connection.cursor()
    #         cursor.execute('INSERT INTO  project3.order1(orderid,orderdate,ordertime,userid,fname,lname,all_total_price,dilivery_charge,overall_price) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s)',(orderdate,ordertime,session['userid'],session['fname'],session['lname'],session['all_total_price'],dilivery_charge,overall_price))
    #         mysql.connection.commit()
    #         msg='Category added successfully  !'

    # else:
    #     return redirect(url_for('login1'))


    # return render_template('checkout.html',data=data,userid=session['userid'],email=session['email'],all_total_quantity=session['all_total_quantity'] ,all_total_price=session['all_total_price'],fname=session['fname'],lname=session['lname'],password=session['password'] )
# -------------------------------------------------------------------------ADMIN------------------------------------------------------------------------


@app.route('/dash')
def dash():
    if 'loggedin' in session :
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user')
        data = cursor.fetchall()
        c=0
        for i in data:
            c=c+1
        cursor.close()

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM project3.vegetable ;')
        data=cursor.fetchall()
        c1=0
        for i in data:
            c1=c1+1
        cursor.close()

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM project3.category ;')
        data=cursor.fetchall()
        c2=0
        for i in data:
            c2=c2+1
        cursor.close()

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM project3.customer_master ;')
        data=cursor.fetchall()
        c3=0
        for i in data:
            c3=c3+1
        cursor.close()

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM project3.order1 where orderid>5 ;')
        data=cursor.fetchall()
        c4=0
        for i in data:
            c4=c4+1
        cursor.close()

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM project3.order1 where orderid<6 ;')
        data=cursor.fetchall()
        c5=0
        for i in data:
            c5=c5+1
        cursor.close()

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM project3.feedback;')
        data=cursor.fetchall()
        c6=0
        for i in data:
            c6=c6+1
        cursor.close()



    else:
        return redirect(url_for('admin'))

    return render_template('adminindex.html',c=c,c1=c1,c2=c2,c3=c3,c4=c4,c5=c5,c6=c6)   


@app.route('/admin', methods =['GET', 'POST'])
def admin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM project3.adminlogin WHERE username = % s AND password = % s', (username, password ))
        data = cursor.fetchone()
        if data:
            session['loggedin'] = True
            session['username'] = data['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('dash'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('adminlogin.html', msg = msg)

@app.route('/data',methods=['POST','GET'])
def data():
    
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM project3.user ;')
    data = cursor.fetchall()
    cursor.close()
    return render_template('data.html',user=data)




@app.route('/customer_master',methods=['POST','GET'])     
def customer_master():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM project3.customer_master ;')
    data=cursor.fetchall()
    cursor.close()
    return render_template('customer_master.html',data=data)

@app.route('/order_master',methods=['POST','GET'])     
def order_master():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM project3.order1 where orderid>5;')
    data=cursor.fetchall()
    cursor.close()
    return render_template('order_master.html',data=data)

@app.route('/order',methods=['POST','GET'])     
def order():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM project3.order1 where orderid<6;')
    data=cursor.fetchall()
    cursor.close()
    return render_template('order.html',data=data)

@app.route('/feedback',methods=['POST','GET'])     
def feedback():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM project3.feedback;')
    data=cursor.fetchall()
    cursor.close()
    return render_template('feedback.html',data=data)



   

@app.route('/greet1',methods=['POST','GET'])
def greet1():
    msg =' '
    if request.method=='POST' and 'cat_id' in request.form :
        cat_id=request.form['cat_id']
        #print(cat_id)

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM project3.category WHERE cat_id=%s ',(cat_id,))
        user=cursor.fetchall()
        user=user[0][1]
        print(user)
        session['user']=user
        return jsonify(message7=f'{user}')
    return ' ',400







@app.route('/contact2.html', methods=['GET', 'POST'])
def contact2():
    if request.method=='POST' and 'fname' in request.form and 'lname' in request.form and 'feedback' in request.form:
        session['fname']=request.form['fname']
        session['lname']=request.form['lname']
        session['feedback'] = request.form['feedback']

        fname=session['fname']
        lname=session['lname']        
        feedback=session['feedback']


        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO feedback VALUES (NULL,%s,%s,%s)', (fname,lname,feedback, ))
        mysql.connection.commit()
        msg='You have successfully registered !'
        return redirect(url_for('contact2'))
    elif request.method == 'POST':
        msg= 'Please fill out the form !'
    return render_template('contact2.html',fname=session['fname'],lname=session['lname'])














@app.route('/category.html',methods=['POST','GET'])     
def category():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM project3.category ;')
    data=cursor.fetchall()
    cursor.close()
    return render_template('Category2.html',data=data)



@app.route('/add_category',methods=['GET','POST'])
def add_category():
    msg = ''
    cat_name=''
    if request.method=='POST' :
        cat_name=request.form['cat_name']
        # cat_id=request.form['cat_id']
        image = request.form['image']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO project3.category VALUES (NULL,%s,%s)', (cat_name,image,))
        mysql.connection.commit()
        msg='Category added successfully  !'
    else:
        msg='Unable to add Category'
    return redirect (url_for('category'))


@app.route('/edit_category', methods = ['POST', 'GET'])
def edit_category():
    if request.method == 'POST':
        cat_id=request.form['cat_id']
        cat_name=request.form['cat_name']
        image=request.form['image']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE project3.category SET project3.category.cat_name=%s,project3.category.image=%s WHERE cat_id=%s", ( cat_name,image,cat_id, ))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        cur.close()
    return redirect(url_for('category'))


@app.route('/delete_category/<int:cat_id>', methods = ['GET'])
def delete_category(cat_id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM project3.category WHERE cat_id=%s", (cat_id,))
    mysql.connection.commit()
    return redirect(url_for('category'))

@app.route('/product',methods=['POST','GET'])     
def product():
    data=''
    data1=''
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM project3.vegetable  ;')
    data=cursor.fetchall()
    cursor.execute("SELECT * FROM project3.category ;")
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('product.html',data=data, data1=data1)

@app.route('/add_product',methods=['GET','POST'])
def add_product():
    msg=''
    if request.method=='POST' :
        cat_id=request.form['cat_id']
        cat_name=request.form['cat_name']
        veg_name=request.form['veg_name']
        code=request.form['code']
        uom=request.form['uom']
        rate=request.form['rate']
        stock=request.form['stock']
        image = request.form['image']

        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO project3.vegetable VALUES (%s,%s,NULL,%s,%s,%s,%s,%s,%s)', (cat_id, cat_name,veg_name,code,uom,rate,stock,image,))
        mysql.connection.commit()
        msg='Product added successfully  !'
    else:
        msg='Unable to add Product'
    return redirect(url_for('product',msg=msg,data=data))  

@app.route('/edit_product', methods = ['POST', 'GET'])
def update_vegetable():
    if request.method == 'POST':
        cat_id=request.form['cat_id']
        cat_name=request.form['cat_name']
        veg_id=request.form['veg_id']
        veg_name=request.form['veg_name']
        code=request.form['code']
        uom=request.form['uom']
        rate=request.form['rate']
        stock=request.form['stock']
        image=request.form['image']


        cursor = mysql.connection.cursor()
        query='UPDATE project3.vegetable SET cat_id=%s,cat_name=%s,veg_name=%s,code=%s,uom=%s,rate=%s,stock=%s,image=%s WHERE veg_id = %s'
        cursor.execute(query,(cat_id,cat_name,veg_name,code,uom,rate,stock,image,veg_id, ))
        flash('collection Updated Successfully')
        mysql.connection.commit()
    return redirect(url_for('product'))


@app.route('/delete_product/<int:veg_id>', methods = ['GET'])
def delete_vegetable(veg_id):
    flash("Product has been updated Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM project3.vegetable WHERE veg_id=%s", (veg_id,))
    mysql.connection.commit()
    return redirect(url_for('product'))



# --------------------------------------------------------------------Reports----------------------------------------------------------------------------------------------

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/download/user_report/pdf')
def download_user_report():
    now=date.today()
    cursor = mysql.connection.cursor()
    
    cursor.execute("SELECT userid,fname,lname,email,password FROM project3.user")
    result = cursor.fetchall()
        
        
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin

    # pdf.image('logo2.jpg',160,5,50,50) 
    # pdf.ln(10)

    pdf.set_font('Arial','B',25.0) 
    pdf.cell(page_width, 0.0, "Freschery", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "2130 E Ward,Tarabai Park,", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "Pune - 416003", align='L')
    pdf.ln(20)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "---------------------------------------------------------------------------------------------------------------------------")
    pdf.ln(10)

        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, " Registerd User Report", align='C')
    pdf.ln(10)
    pdf.set_font('Times','B',12.0) 
    pdf.cell(page_width, 0.0, 'Date :- '+str(date.strftime("%d / %m / %y")), align='L')
    

    pdf.ln(10)


    pdf.set_font('Courier', '', 12)
        
    col_width = page_width/5
        
    pdf.ln(1)
        
    th = pdf.font_size
    i=1
    pdf.cell(20,th,"Sr.No",align='C',border=1)
    # pdf.cell(20,th,"User Id",border=1)
    pdf.cell(30,th,"First Name",border=1)
    pdf.cell(30,th,"Last Name",border=1)
    pdf.cell(70,th,"E mail",border=1)
    # pdf.cell(col_width,th,"Password",border=1)

    pdf.ln(th)
    for col in result:
        pdf.cell(20, th, str(i),align='C', border=1)
        # pdf.cell(20, th, str(col[0]), border=1)
        pdf.cell(30, th, col[1], border=1)
        pdf.cell(30, th, col[2], border=1)
        pdf.cell(70, th, col[3], border=1)
        # pdf.cell(col_width, th, col[4], border=1)

        i=i+1
        pdf.ln(th)
        
    pdf.ln(10)
         
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    cursor.close()
            
    return Response(pdf.output(dest='S').encode('latin_1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=user_report.pdf'})


@app.route('/download/category_report/pdf')
def download_category_report():
    now=date.today()
    cursor = mysql.connection.cursor()
    
    cursor.execute("SELECT  * FROM project3.category")
    result = cursor.fetchall()
        
        
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin

    # pdf.image('logo2.jpg',160,5,50,50) 
    # pdf.ln(10)

    pdf.set_font('Arial','B',25.0) 
    pdf.cell(page_width, 0.0, "Freschery", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "2130 E Ward,Tarabai Park,", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "Pune - 416003", align='L')
    pdf.ln(20)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "---------------------------------------------------------------------------------------------------------------------------")
    pdf.ln(10)
    
        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, "Category Report", align='C')
    pdf.ln(10)
    pdf.set_font('Times','B',12.0) 
    pdf.cell(page_width, 0.0, 'Date :- '+str(date.strftime("%d / %m / %y")), align='L')
        

    pdf.ln(10)


    pdf.set_font('Courier', '', 12)
            
    col_width = page_width/3
            
    pdf.ln(1)
            
    th = pdf.font_size
    i=1
    pdf.cell(20,th,"Sr.No",align='C',border=1)
    #pdf.cell(col_width,th,"Category Id",border=1,align='C')
    pdf.cell(col_width,th,"Category Name",border=1,align='C')
    pdf.ln(th)
    for col in result:
        pdf.cell(20, th, str(i),align='C', border=1)
        #pdf.cell(col_width, th, str(col[0]),align='C', border=1)
        pdf.cell(col_width, th, col[1], border=1,align='C')
        i=i+1
        pdf.ln(th)
            
    pdf.ln(10)
         
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    cursor.close()
                
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=category_report.pdf'})

@app.route('/download/veg_report/pdf')
def download_veg_report():
    now=date.today()
    cursor = mysql.connection.cursor()
    
    cursor.execute("SELECT * FROM project3.vegetable ORDER BY cat_id ASC;")
    result = cursor.fetchall()
        
        
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 4 * pdf.l_margin

    # pdf.image('logo2.jpg',160,5,50,50) 
    # pdf.ln(10)

    pdf.set_font('Arial','B',25.0) 
    pdf.cell(page_width, 0.0, "Freschery", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "2130 E Ward,Tarabai Park,", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "Pune - 416003", align='L')
    pdf.ln(20)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "---------------------------------------------------------------------------------------------------------------------------")
    pdf.ln(10)

        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, "Products Report", align='C')
    pdf.ln(10)
    pdf.set_font('Times','B',12.0) 
    pdf.cell(page_width, 0.0, 'Date :- '+str(date.strftime("%d / %m / %y")), align='L')
        

    pdf.ln(10)


    pdf.set_font('Courier', '', 12)
            
    col_width = page_width/8
            
    pdf.ln(1)
            
    th = pdf.font_size
    i=1
    pdf.cell(15,th,"Sr.No",align='C',border=1)
    #pdf.cell(17,th,"Cat Id",border=1,align='C')
    pdf.cell(22,th,"Cat Name",border=1,align='C')
    #pdf.cell(col_width,th,"Veg Id",border=1,align='C')
    pdf.cell(38,th,"Product Name",border=1,align='C')
    pdf.cell(30,th,"UOM",border=1,align='C')
    pdf.cell(col_width,th,"Rate",border=1,align='C')
    pdf.cell(col_width,th,"Stock",border=1,align='C')

    pdf.ln(th)
    for col in result:
        pdf.cell(15, th, str(i),align='C', border=1)
        #pdf.cell(17, th, str(col[0]),align='C', border=1)
        pdf.cell(22, th, col[1], border=1,align='C')
        #pdf.cell(col_width, th, str(col[2]),align='C', border=1)
        pdf.cell(38, th, col[3], border=1,align='C')
        pdf.cell(30, th, col[5], border=1,align='C')
        pdf.cell(col_width, th, str(col[6]),align='C', border=1)
        pdf.cell(col_width, th, str(col[7]),align='C', border=1)



        i=i+1
        pdf.ln(th)
            
    pdf.ln(10)
         
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    cursor.close()
                
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=product_report.pdf'})

@app.route('/cat_wise_prod_report.html')
def upload_form():
    cursor=mysql.connection.cursor()
    
    cursor.execute("SELECT * FROM project3.category ")
    data= cursor.fetchall()
    return render_template('cat_wise_veg_report.html',data=data)

@app.route('/download/cat_wise_prod_report/pdf',methods=['POST','GET'])
def download_cat_wise_veg_report():
    now=date.today()
    cursor = mysql.connection.cursor()

    if request.method == "POST" :
        session['cat_name']=request.form['cat_name']
        mcat_name=session['cat_name']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM project3.vegetable where cat_name=%s",(mcat_name,))
        result = cursor.fetchall()

    pdf = FPDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    # pdf.image('logo2.jpg',160,5,50,50) 
    # pdf.ln(10)

    pdf.set_font('Arial','B',25.0) 
    pdf.cell(page_width, 0.0, "Freschery", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "2130 E Ward,Tarabai Park,", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "Pune - 416003", align='L')
    pdf.ln(20)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "---------------------------------------------------------------------------------------------------------------------------")
    pdf.ln(10)
    
        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, "Category Wise Product Report", align='C')
    pdf.ln(10)
    pdf.set_font('Times','B',12.0) 
    pdf.cell(page_width, 0.0, 'Date :- '+str(date.strftime("%d / %m / %y")), align='L')
    

    pdf.ln(10)

    pdf.cell(page_width, 0.0, 'Category ID :- '+str(result[0][0]), align='L')

    pdf.ln(0)

    pdf.cell(page_width, 0.0, 'Category Name :- '+mcat_name , align='R')

    pdf.ln(10)



    pdf.set_font('Courier', '', 12)
        
    col_width = page_width/5
        
    pdf.ln(1)
        
    th = pdf.font_size
    i=1
    pdf.cell(20,th,"Sr.No",align='C',border=1)
    # pdf.cell(col_width,th,"Cat Id",border=1)
    # pdf.cell(col_width,th,"Cat Name",border=1)
   # pdf.cell(col_width,th,"Product Id",border=1)
    pdf.cell(col_width,th,"Product Name",border=1)
    pdf.cell(col_width,th,"Rate",border=1)
    pdf.cell(col_width,th,"Stock",border=1)

    pdf.ln(th)
    for col in result:
        pdf.cell(20, th, str(i),align='C', border=1)
        # pdf.cell(col_width, th, str(col[0]), border=1)
        # pdf.cell(col_width, th, col[1], border=1)
        #pdf.cell(col_width, th, str(col[2]), border=1)
        pdf.cell(col_width, th, col[3], border=1)
        pdf.cell(col_width, th, str(col[6]), border=1)
        pdf.cell(col_width, th, str(col[7]), border=1)


        i=i+1
        pdf.ln(th)
        
    pdf.ln(10)
         
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    cursor.close()
            
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=cat_wise_prod_report.pdf'})   

@app.route('/order_date_report.html')
def order_date_report():
    return render_template('order_date_report.html')


@app.route('/download/order_date_report/pdf',methods =['POST'])
def download_order_date_report():

    
    if request.method == "POST":
        from datetime import datetime
        fdate=request.form.get('fdate')
        tdate=request.form.get('tdate')
        
        print(type(fdate),tdate)
        fdate = datetime.strptime(fdate, '%Y-%m-%d')
        tdate = datetime.strptime(tdate, '%Y-%m-%d')
        print(type(fdate),tdate)
        now=date.today()
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM project3.order1 where str_to_date(orderdate,'%%Y-%%m-%%d')>=%s and str_to_date(orderdate,'%%Y-%%m-%%d')<=%s" ,(fdate,tdate,))
        result = cursor.fetchall()
        print(result)
        
        pdf = FPDF()
        pdf.add_page()
        
        page_width = pdf.w - 2 * pdf.l_margin

        # pdf.image('logo2.jpg',160,5,50,50) 
        # pdf.ln(10)

        pdf.set_font('Arial','B',25.0) 
        pdf.cell(page_width, 0.0, "Freschery", align='L')
        pdf.ln(8)

        pdf.set_font('Arial','',12.0) 
        pdf.cell(page_width, 0.0, "2130 E Ward,Tarabai Park,", align='L')
        pdf.ln(8)

        pdf.set_font('Arial','',12.0) 
        pdf.cell(page_width, 0.0, "Pune - 416003", align='L')
        pdf.ln(20)

        pdf.set_font('Arial','',12.0) 
        pdf.cell(page_width, 0.0, "---------------------------------------------------------------------------------------------------------------------------")
        pdf.ln(10)
        
        pdf.set_font('Times','B',14.0) 
        pdf.cell(page_width, 0.0, "Order Report", align='C')
        pdf.ln(10)
        pdf.set_font('Times','B',12.0) 
        pdf.cell(page_width, 0.0, 'Date :- '+str(date.strftime("%d / %m / %y")), align='L')
        pdf.ln(10)
        pdf.cell(page_width, 0.0, 'From :- '+str(fdate.strftime("%d / %m / %y"))+'  '+'To:-'+str(tdate.strftime("%d / %m / %y")),align='L') 
        pdf.ln(10)

        
        pdf.set_font('Courier', '', 12)
            
        col_width = page_width/7
            
        pdf.ln(1)
            
        th = pdf.font_size
        i=1
        pdf.cell(15,th,"Sr.No",align='C',border=1)
        pdf.cell(22,th,"Order id",align='C',border=1)
        #pdf.cell(20,th,"User Id",border=1)
        pdf.cell(col_width,th,"First Name",border=1)
        pdf.cell(col_width,th,"Last Name",border=1)
        pdf.cell(40,th,"Payable amount",border=1)
        pdf.cell(col_width,th,"Order Date",border=1)
        pdf.ln(th)
        for col in result:
            pdf.cell(15, th, str(i),align='C', border=1)
            pdf.cell(22, th, str(col[0]), border=1)
            #pdf.cell(20, th, str(col[3]), border=1)
            pdf.cell(col_width, th, str(col[4]),align='C', border=1)
            pdf.cell(col_width, th, str(col[5]),align='C', border=1)
            pdf.cell(40, th, str(col[8]), border=1)
            pdf.cell(col_width, th, str(col[1].strftime("%d/%m/%Y")), border=1)
            i=i+1
            pdf.ln(th)
            
        pdf.ln(10)

        pdf.set_font('Times','',10.0) 
        pdf.cell(page_width, 0.0, '- end of report -', align='C')
        cursor.close()
                
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=order_report.pdf'})

@app.route('/download/customer_master_report/pdf')
def download_customer_master_report():
    now=date.today()
    cursor = mysql.connection.cursor()
    
    cursor.execute("SELECT * FROM project3.customer_master ORDER BY userid ASC;")
    result = cursor.fetchall()
        
        
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 4 * pdf.l_margin

    # pdf.image('logo2.jpg',160,5,50,50) 
    # pdf.ln(10)

    pdf.set_font('Arial','B',25.0) 
    pdf.cell(page_width, 0.0, "Freschery", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "2130 E Ward,Tarabai Park,", align='L')
    pdf.ln(8)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "Pune - 416003", align='L')
    pdf.ln(20)

    pdf.set_font('Arial','',12.0) 
    pdf.cell(page_width, 0.0, "---------------------------------------------------------------------------------------------------------------------------")
    pdf.ln(10)

        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, "Customer master Report", align='C')
    pdf.ln(10)
    pdf.set_font('Times','B',12.0) 
    pdf.cell(page_width, 0.0, 'Date :- '+str(date.strftime("%d / %m / %y")), align='L')
        

    pdf.ln(10)


    pdf.set_font('Courier', '', 12)
            
    col_width = page_width/8
            
    pdf.ln(1)
            
    th = pdf.font_size
    i=1
    pdf.cell(15,th,"Sr.No",align='C',border=1)
    #pdf.cell(17,th,"UserId",border=1,align='C')
    pdf.cell(22,th,"FName",border=1,align='C')
    pdf.cell(col_width,th,"Lname ",border=1,align='C')
    pdf.cell(42,th,"address",border=1,align='C')
    pdf.cell(30,th,"city",border=1,align='C')
    pdf.cell(20,th,"pin",border=1,align='C')
    pdf.cell(35,th,"mobile",border=1,align='C')
    

    pdf.ln(th)
    for col in result:
        pdf.cell(15, th, str(i),align='C', border=1)
        #pdf.cell(17, th, str(col[9]),align='C', border=1)
        pdf.cell(22, th, col[0], border=1,align='C')
        pdf.cell(col_width, th, col[1],align='C', border=1)
        pdf.cell(42, th, col[2], border=1,align='C')
        pdf.cell(30, th, col[3], border=1,align='C')
        pdf.cell(20, th, str(col[4]),align='C', border=1)
        pdf.cell(35, th, str(col[7]),align='C', border=1)



        i=i+1
        pdf.ln(th)
            
    pdf.ln(10)
         
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    cursor.close()
                
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=customer_master_report.pdf'})