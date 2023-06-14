import pyodbc

server = 'LAPTOP-MU3HMVU8\SQLEXPRESS'
database = 'ims1'
driver = '{SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};trusted_connection=yes'

conn = pyodbc.connect(connection_string)

cn = conn.cursor()

#cn.execute("INSERT INTO CUSTOMER(CUSTOMER_NAME,CUSTOMER_ADDR,CUSTOMER_MAIL) VALUES('MADHAV','HYD','KVM@GMAIL.COM')")
# conn.commit()

# cn.execute("select * from customer")

# print(cn.fetchall())

conn = pyodbc.connect(connection_string)
cn = conn.cursor()

'''customer_name = 'chinna'
customer_addr = 'thp'
customer_mail = 'chinna@gmail.com'''


#cn.execute(f"insert into customer(customer_name,customer_addr,customer_mail)values('{customer_name}','{customer_addr}','{customer_mail}')")
#conn.commit()

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

######################################################   SHOW CUSTOMERS ##################################################################

@app.route("/show customers")
def customer_show(): 
    cn = conn.cursor()
    cn.execute("select * from customer")
    data = []
    for i in cn.fetchall():
        customer = {}
        customer['customer_id'] = i[0]
        customer['customer_name'] = i[1]
        customer['customer_addr'] = i[2]
        customer['customer_mail'] = i[3]
        data.append(customer)

    return render_template('showcoustomers.html',data=data)

########################################################   SHOW ORDERS ##############################################################
 
@app.route("/show orders")
def orders_show(): 
    cn = conn.cursor()
    cn.execute("select * from orders")
    data = []
    for i in cn.fetchall():
        orders = {}
        orders['ORDERS_ID'] = i[0]
        orders['PRODUCT_ID'] = i[1]
        orders['CUSTOMER_ID'] = i[2]
        orders['QUANTITY'] = i[3]
        data.append(orders)
    print(data)
    return render_template('showorders.html',data=data)

##################################################   SHOW SUPPLIER   ####################################################################

@app.route("/show supplier")
def show_supplier(): 
    cn = conn.cursor()
    cn.execute("select * from supplier")
    data = []
    for i in cn.fetchall():
        supplier = {}
        supplier['SUPPLIER_ID'] = i[0]
        supplier['SUPPLIER_NAME'] = i[1]
        supplier['SUPPLIER_ADDR'] = i[2]
        supplier['SUPPLIER_MAIL'] = i[3]
        
        data.append(supplier)
    print(data)
    return render_template('showsupplier.html',data=data)

#####################################################   SHOW PRODUCT   ################################################################

@app.route("/show product")
def product_show(): 
    cn = conn.cursor()
    cn.execute("select * from product")
    data = []
    for i in cn.fetchall():
        product = {}
        product['PRODUCT_ID'] = i[0]
        product['PRODUCT_NAME'] = i[1]
        product['PRICE'] = i[2]
        product['STOCK'] = i[3]
        product['SUPPLIER_ID'] = i[4]
        data.append(product)
    print(data)
    return render_template('showproduct.html',data=data)

################################################   ADD ORDERS    ########################################################################

@app.route("/add-orders",methods=['GET','POST'])
def addorders():
    if request.method=='POST':
        cn=conn.cursor()
        productid=request.form.get('productid')
        customerid=request.form.get('customerid')
        quantity=request.form.get('quantity')
        cn.execute(f"insert into orders(product_id,customer_id,quantity) values('{productid}','{customerid}','{quantity}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addorders.html')

################################################   ADD CUSTOMERS    ########################################################################


@app.route("/add-customer",methods=['GET','POST'])
def addcustomer():
    if request.method=='POST':
        cn=conn.cursor()
        customername=request.form.get('name')
        customeraddr=request.form.get('address')
        customeremail=request.form.get('email')
        cn.execute(f"insert into customer(customer_name,customer_addr,customer_email) values('{customername}','{customeraddr}','{customeremail}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addcustomer.html')
    
################################################   ADD SUPPLIER    ########################################################################


@app.route("/add-supplier",methods=['GET','POST'])
def addsupplier():
    if request.method=='POST':
        cn=conn.cursor()
        suppliername=request.form.get('name')
        supplieraddr=request.form.get('address')
        supplieremail=request.form.get('email')
        cn.execute(f"insert into supplier(supplier_name,supplier_addr,supplier_email) values('{suppliername}','{supplieraddr}','{supplieremail}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addsupplier.html')


################################################   ADD PRODUCT    ########################################################################

@app.route("/add product",methods=['GET','POST'])
def addproduct():
    if request.method=='POST':
        cn=conn.cursor()
        productname=request.form.get('name')
        price=request.form.get('price')
        stock=request.form.get('stock')
        supplierid=request.form.get('id')
        cn.execute(f"insert into product(product_name,price,stock,supplier_id) values('{productname}','{price}','{stock}','{supplierid}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addproduct.html')

################################################   UPDATE CUSTOMER    ########################################################################

@app.route("/update-customer", methods=['GET','POST'])
def updatecustomer():    
    if request.method=='POST':
        cn=conn.cursor()
        customerid=request.form.get('customerid')
        change=request.form.get('change')
        print(customerid)
        print(change)
        newvalue = request.form.get('newvalue')
        cn.execute(f"update customer set {change} = '{newvalue}' where customer_id = '{customerid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updatecustomer.html')



################################################   UPDATE ORDERS    ########################################################################

@app.route("/update-orders", methods=['GET','POST'])
def updateorders():    
    if request.method=='POST':
        cn=conn.cursor()
        ordersid=request.form.get('ordersid')
        change=request.form.get('change')
        print(ordersid)
        print(change)
        newvalue = request.form.get('newvalue')
        cn.execute(f"update orders set {change} = '{newvalue}' where orders_id = '{ordersid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updateorders.html')


################################################   UPDATE PRODUCT    ########################################################################

@app.route("/update-product", methods=['GET','POST'])
def updateproduct():    
    if request.method=='POST':
        cn=conn.cursor()
        productid=request.form.get('productid')
        change=request.form.get('change')
        print(productid)
        print(change)
        newvalue = request.form.get('newvalue')
        cn.execute(f"update product set {change} = '{newvalue}' where product_id = '{productid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updateproduct.html')
    

################################################   UPDATE SUPPLIERS    ########################################################################

@app.route("/update-supplier", methods=['GET','POST'])
def updatesupplier():    
    if request.method=='POST':
        cn=conn.cursor()
        supplierid=request.form.get('supplierid')
        change=request.form.get('change')
        print(supplierid)
        print(change)
        newvalue = request.form.get('newvalue')
        cn.execute(f"update supplier set {change} = '{newvalue}' where supplier_id = '{supplierid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updatesupplier.html')

if __name__ == '__main__':
    app.run()






