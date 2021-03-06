from flask import Flask, redirect, render_template, request
import pymysql
import datetime

app = Flask(__name__)

userid = {
    'id' : None,
    'email' : None,
    'passwd' : None,
    'storesid' : None
}
userinfo = [0, 0, 0] # seller, customer, delivery
menulist = [] # 메뉴 리스트


db_connector = {
    'host' : 'localhost',
    'port' :3306,
    'user' : 'root',
    'passwd':'mysqlroot', 
    'db' :'TP', 
    'charset' :'utf8'
}

@app.route("/")
def index():
    userid['email'] = None
    userid['passwd'] = None
    userid['id'] = None
    userinfo[0] = 0
    userinfo[1] = 0
    userinfo[2] = 0
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    passwd = request.form.get('pw')
    
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql = f"SELECT sellers_id FROM sellers WHERE passwd = '{passwd}' AND email = '{email}'"
    cur.execute(sql)
    seller = cur.fetchall()
    sql = f"SELECT customer_id FROM customers WHERE passwd = '{passwd}' AND email = '{email}'"
    cur.execute(sql)
    customer = cur.fetchall()
    sql = f"SELECT del_id FROM delivery WHERE passwd = '{passwd}' AND email = '{email}'"
    print(sql)
    cur.execute(sql)
    delivery = cur.fetchall() 
    
    if (not seller) and (not customer) and (not delivery):
        return render_template('error.html')
    if seller:
        userinfo[0] = 1
    if customer:
        userinfo[1] = 1
    if delivery:
        userinfo[2] = 1

    userid['email'] = email
    userid['passwd'] = passwd

    if seller :
        userid['id'] = seller[0]['sellers_id']
    elif customer :
        userid['id'] = customer[0]['customer_id']
    elif delivery :
        userid['id'] = delivery[0]['del_id']
    else :
        userid['id'] = None
    print(userinfo)
    conn.close()
    return redirect("/login/user")


# 로그인 성공
@app.route("/login/user", methods=['GET', 'POST'])
def user():
    """
    로그인 성공 페이지
    로그인에 성공한 사용자 정보(판매자, 구매자, 배달대행원)와 이름을 반환
    사용자 정보(판매자, 구매자, 배달대행원)에 맞는 로그인 성공 페이지를 보여주기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    print("here")
    print({userid['id']})
    sql =f"SELECT name1 FROM sellers WHERE sellers_id = '{userid['id']}'"
    cur.execute(sql)
    sname = cur.fetchall()
    sql = f"SELECT name1 FROM customers WHERE customer_id ='{userid['id']}'"
    cur.execute(sql)
    cname = cur.fetchall()
    sql = f"SELECT name1 FROM delivery WHERE del_id ='{userid['id']}'"
    cur.execute(sql)
    dname = cur.fetchall()

    if userinfo[0]==1:
        name = sname[0]['name1']
    elif userinfo[1]==1 :
        name = cname[0]['name1']
    elif userinfo[2]==1 :
        name = dname[0]['name1']
    else :
        name = None
        
    conn.close()
    return render_template("user.html", info=userinfo, k=name)
# ========== 판매자 ==========

# 판매자 개인 정보 변경
@app.route("/login/user/schange", methods=['GET', 'POST'])
def schange():
    """
    판매자 개인 정보 변경 페이지
    현재 비밀번호와 이름을 확인하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = f"SELECT name1 FROM sellers WHERE sellers_id = '{userid['id']}' "
    cur.execute(sql)
    seller = cur.fetchall()
    sname = seller[0]['name1']
    conn.close()
    return render_template("schange.html", info=userinfo, name=sname, passwd=userid['passwd'])

# 판매자 비밀번호 변경
@app.route("/login/user/schange/pw", methods=['GET', 'POST'])
def spw():
    """
    로그인한 판매자 비밀번호 변경
    """
    pwd = request.form.get('passwd')
    
    userid['passwd'] = pwd
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    sql = f"UPDATE sellers SET passwd = '{pwd}'  WHERE sellers_id = {userid['id']} "
    cur.execute(sql)
    conn.commit()
    
    conn.close()
    
    return redirect("/login/user")

# 판매자 이름 변경
@app.route("/login/user/schange/name", methods=['GET', 'POST'])
def schname():
    """
    로그인한 판매자 이름 변경
    """
    name = request.form.get('name')
    
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    sql = f"UPDATE sellers SET name1 = '{name}'  WHERE sellers_id = {userid['id']} "
    cur.execute(sql)
    conn.commit()
    
    conn.close()
    return redirect("/login/user")

# 소유중인 가게 리스트
@app.route("/login/user/seller", methods=['GET', 'POST'])
def seller():
    """
    소유중인 가게 리스트 페이지
    로그인한 판매자가 소유중인 가게 리스트를 보여주기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = f"SELECT * FROM stores WHERE seller_id ='{userid['id']}'"
    cur.execute(sql)
    seller = cur.fetchall()
    store = seller
    conn.close()
    
    return render_template("seller.html", info=userinfo, store=store)

# 가게 정보, 메뉴 정보, 현재 주문
@app.route("/login/user/seller/store", methods=['GET', 'POST'])
def store():
    sid = request.form.get('sid')

    if sid:
        userid["storesid"] = sid
    sid = userid["storesid"]
    """
    가게 정보, 메뉴 정보, 현재 주문 페이지
    가제 정보, 메뉴 정보, 현재 주문을 확인하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = f"SELECT * FROM stores WHERE store_id ='{userid['storesid']}'"
    cur.execute(sql)
    stores = cur.fetchall()
    store = stores[0]
    
    sql = f"SELECT * FROM menu WHERE store_id ='{userid['storesid']}'"
    cur.execute(sql)
    menu = cur.fetchall()
    
    
    sql = f"SELECT c.email , o.order_time, d.phone, p.pay_type FROM customers as c, orders as o, delivery as d, payment as p WHERE o.store_id ='{userid['storesid']}'"
    cur.execute(sql)
    order = cur.fetchall()
    
    conn.close()
    
    return render_template("store.html", info=userinfo, store=store, menu=menu, sid=sid, order=order)

# 메뉴 이름 변경
@app.route("/login/user/seller/store/menuchan", methods=['GET', 'POST'])
def menuchan():
    """
    메뉴 이름 변경
    해당 가게의 새로 입력 받은 메뉴 이름으로 변경하기 위함
    """
    menu = request.form.get('menu')
    sid = request.form.get('sid')
    newname = request.form.get('newname')
    
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql = f"UPDATE menu SET name1 = '{newname}' WHERE store_id ='{userid['storesid']}' AND name1 = '{menu}'"
    cur.execute(sql)
    
    conn.commit()
    conn.close()
    
    return redirect("/login/user/seller/store")

# 메뉴 삭제
@app.route("/login/user/seller/store/menudel", methods=['GET', 'POST'])
def menudel():
    sid = request.form.get('sid')
    menu = request.form.get('menu')
    """
    메뉴 삭제(현재 주문중인 메뉴는 삭제 불가)
    해당 가게의 메뉴를 삭제하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"DELETE FROM menu WHERE store_id ='{userid['storesid']}' AND name1 = '{menu}'"
    cur.execute(sql)
    
    conn.commit()
    conn.close()
    return redirect("/login/user/seller/store")

# 메뉴 추가
@app.route("/login/user/seller/store/menuadd", methods=['GET', 'POST'])
def menuadd():
    """
    메뉴 추가
    해당 가게의 새로 입력(메뉴명, 가격, 할인율) 받은 메뉴를 추가하기 위함
    """
    newmenuname = request.form.get('newmenuname')
    newmenuprice = request.form.get('newmenuprice')
    newmenuevent = request.form.get('newmenuevent')
    sid = request.form.get('sid')
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"SELECT max(menu_id) FROM menu"
    cur.execute(sql)
    last=cur.fetchall()
    lastmenuid = last[0]['max(menu_id)']
    newmenuid = lastmenuid + 1
    sql = f"INSERT INTO menu VALUES ('{newmenuid}', '{newmenuname}', '{newmenuprice}', '{newmenuevent}', '{sid}')"
    cur.execute(sql)
    
    conn.commit()
    conn.close()
    return redirect("/login/user/seller/store")

# 배달원 할당
@app.route("/login/user/seller/store/ordercheck", methods=['GET', 'POST'])
def ordercheck():
    orderinfo = request.form.get('orderinfo')
    """
    배달원 할당
    현재 주문에 대해 배달 가능한 배달대행원을 최대 5명까지 확인하기 위함(남은 횟수가 높은 순서로 확인)
    
    배달 가능한 배달대행원:
    1. 배달 가능한 지역(가게와 가까운 지역)
    2. 현재 배달 가능한 상태
    3. 남은 횟수가 0이 아닌 상태
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"SELECT * FROM delivery as d, stores as s WHERE d.address = s.address AND s.seller_id = {userid['id']} AND d.available=1 AND d.stock > 0 ORDER BY d.stock ASC LIMIT 5"
    cur.execute(sql)
    deli=cur.fetchall()
    
    conn.close()
    return render_template("ordercheck.html", info=userinfo, view=deli, orderinfo=orderinfo)

# 현재 주문에 배달원 ID 할당
@app.route("/login/user/seller/store/ordercheck/real", methods=['GET', 'POST'])
def orderreal():
    """
    현재 주문에 배달원 ID 할당
    현재 주문에 대해 배달대행원의 배달원 ID를 할당하기 위함
    """
    did = request.form.get('did')
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    
    sql = f"UPDATE orders SET del_id ={did} WHERE store_id={userid['storesid']}"
    cur.execute(sql)
    
    conn.commit()
    conn.close()
    return redirect("/login/user/seller/store")

# 주문 취소
@app.route("/login/user/seller/store/orderdel", methods=['GET', 'POST'])
def orderdel():
    """
    주문 취소
    현재 주문을 취소하기 위함
    """
    did = request.form.get('did')
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    
    sql = f"DELETE FROM orders WHERE del_id ={did} AND store_id={userid['storesid']}"
    cur.execute(sql)
    
    conn.commit()
    
    conn.close()
    return redirect("/login/user/seller/store")

# ========== 구매자 ==========

# 구매자 관리 화면
@app.route("/login/user/customer", methods=['GET', 'POST'])
def customer():
    """
    구매자 관리 화면 페이지
    현재 비밀번호와 이름과 주소를 확인하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = f"SELECT * FROM customers WHERE customer_id = '{userid['id']}' "
    cur.execute(sql)
    customer = cur.fetchall()
    customer = customer[0]
    conn.close()
    
    return render_template("customer.html", info=userinfo, customer=customer)

# 구매자 비밀번호 변경
@app.route("/login/user/customer/pw", methods = ['GET', 'POST'])
def cpw():
    """
    로그인한 구매자 비밀번호 변경
    """
    pwd = request.form.get('passwd')
    
    userid['passwd'] = pwd
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    
    sql = f"UPDATE customers SET passwd = '{pwd}'  WHERE customer_id = {userid['id']} "
    cur.execute(sql)
    conn.commit()
    
    conn.close()
    return redirect("/login/user")

# 구매자 이름 변경
@app.route("/login/user/customer/name", methods=['GET', 'POST'])
def cname():
    """
    로그인한 구매자 이름 변경
    """
    name = request.form.get('name')
    
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    
    sql = f"UPDATE customers SET name1 = '{name}'  WHERE customer_id = {userid['id']} "
    cur.execute(sql)
    conn.commit()
    
    conn.close()
    return redirect("/login/user")

# 구매자 주소 변경
@app.route("/login/user/customer/address", methods=['GET', 'POST'])
def addchan():
    """
    로그인한 구매자 주소 변경
    """
    addr = request.form.get('address')
    
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    
    sql = f"UPDATE customers SET address = '{addr}'  WHERE customer_id = {userid['id']} "
    cur.execute(sql)
    conn.commit()
    
    conn.close()
    return redirect("/login/user/customer")

# 구매자 구매화면
@app.route("/login/user/customer/buy", methods=['GET', 'POST'])
def buy():
    """
    구매화면 페이지
    로그인한 구매자의 주소로 가게 검색을 하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"SELECT address FROM customers WHERE customer_id = {userid['id']} "
    cur.execute(sql)
    caddress=cur.fetchall()
    
    conn.close()
    return render_template("buy.html", info=userinfo, cus_addr=caddress)

# 고객 기본 주소로 가게 검색
@app.route("/login/user/schange/consearch", methods=['GET', 'POST'])
def consearch():
    """
    고객 기본 주수로 가게 검색
    로그인한 구매자의 주소로 부터 가까운 가게 검색을 하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"SELECT * FROM stores as s, customers as c WHERE s.address = c.address"
    cur.execute(sql)
    store=cur.fetchall()
    
    conn.close()
    return render_template("storesearch.html", info=userinfo, store=store)

# 이름으로 가게 검색
@app.route("/login/user/schange/namesearch", methods=['GET', 'POST'])
def namesearch():
    """
    이름으로 가게 검색
    가게의 이름으로 검색하기 위함(부분 일치 가능)
    """
    name = request.form.get('name')
    
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"SELECT * FROM stores WHERE sname LIKE '%{name}%'"
    cur.execute(sql)
    store = cur.fetchall()
    
    conn.close()
    
    return render_template("storesearch.html", info=userinfo, store=store)

# 입력 주소로 가게 검색
@app.route("/login/user/schange/addresssearch", methods=['GET', 'POST'])
def addresssearch():
    """
    입력 주소로 가게 검색
    입력한 주소로 가게를 검색하기 위함(부분 일치 가능)
    """
    kaddr = request.form.get('keyaddr')
    
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"SELECT * FROM stores WHERE address LIKE '%{kaddr}%'"
    cur.execute(sql)
    store = cur.fetchall()
    
    conn.close()
    return render_template("storesearch.html", info=userinfo, store=store)

# 가게 정보, 메뉴 정보, 장바구니
@app.route("/login/user/customer/storebuy", methods=['GET', 'POST'])
def storebuy():
    buystoresid = request.form.get('storesid')
    o_menu = request.form.get('menu')
    o_num = request.form.get('num')
    o_sid = request.form.get('sid')

    if not buystoresid:
        buystoresid = o_sid
    if o_num and o_num != "0" :
        menulist.append([o_menu, o_num])

    """
    가게 정보, 메뉴 정보, 장바구니 페이지
    가게 정보 및 메뉴 정보를 확인하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql=f"SELECT * FROM stores WHERE store_id = {buystoresid}"
    cur.execute(sql)
    store=cur.fetchall()
    store=store[0]
    
    sql=f"SELECT * FROM menu WHERE store_id ={buystoresid}"
    cur.execute(sql)
    menu=cur.fetchall()
    
    conn.close()
    
    return render_template("order.html", info=userinfo, store=store, menu=menu, menulist=menulist, sid=buystoresid)

# 주문 메뉴 확인, 결제 수단
@app.route("/login/user/customer/storebuy/pay", methods = ['GET', 'POST'])
def pay():
    buystoresid = request.form.get('sid')
    if not menulist:
        return render_template("payerror.html")

    """
    결제 수단
    로그인한 구매자의 결제 수단 및 결제정보를 확인하여 원하는 방식으로 결제하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"SELECT * FROM payment WHERE customer_id = {userid['id']}"
    cur.execute(sql)
    payment = cur.fetchall()
    
    conn.close()
    return render_template("realpay.html", info=userinfo, sid=buystoresid, payment=payment, menulist=menulist)

# Order 및 Orderdetail
@app.route("/login/user/customer/storebuy/pay/done", methods=['GET', 'POST'])
def realpay():
    """
    구매자의 주문을 추가와 주문의 상세 내용을 추가하기 위함
    """
    del menulist[:]
    return redirect("/login/user/customer")
# 주문Order 화면
@app.route("/login/user/customer/order", methods=['GET', 'POST'])
def cusorder():
    """
    주문Order 화면
    주문한 가게 이름, 주문한 총 메뉴 수, 결제수단, 주문 시간, 배달 완료 여부를 확인하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql =f"SELECT sname as store_name, quantity as menu_count, pay_type, order_time, delivery_done FROM orders, orderdetail, stores, payment as p  WHERE p.customer_id ={userid['id']}"
    cur.execute(sql)
    od = cur.fetchall()
    
    conn.close()
    
    return render_template("payhistory.html", info=userinfo, order=od)

# ========== 배달대행원 ==========

# 현재 배송 중인 주문
@app.route("/login/user/delivery", methods=['GET', 'POST'])
def delivery():
    """
    현재 OOO님의 배송 중인 주문 페이지
    가게 이름, 주문자 이름, 주문자 전화번호, 배송지, 주문시간, 배송 완료 여부를 확인하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql=f"SELECT name1 FROM delivery WHERE del_id={userid['id']}"
    cur.execute(sql)
    deli = cur.fetchall()
    deli = deli[0]
    
    sql=f"SELECT sname, name1, c.phone, c.address, order_time, delivery_done FROM stores,customers as c, orders  WHERE del_id={userid['id']}"
    cur.execute(sql)
    oorder = cur.fetchall()
    
    conn.close()
    
    return render_template("delivery.html", info=userinfo, order=oorder, deli=deli)

# 배송 완료
@app.route("/login/user/delivery/deliverydone", methods = ['GET', 'POST'])
def deliverydone():
    """
    배송 완료
    배달대행원이 배달 완료 시 배달 완료 여부를 배달 완료로 갱신하기 위함
    """
    conn = pymysql.connect(**db_connector)
    cur = conn.cursor()
    
    sql = f"UPDATE orders SET delivery_done = 1 WHERE del_id ={userid['id']}"
    cur.execute(sql)
    
    conn.commit()
    conn.close()
    
    return redirect("/login/user/delivery")

if __name__ == '__main__':
    app.run(debug=True)
