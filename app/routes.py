from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.forms import ApplicationForm, LoginForm
from app.models import Vendor, User
from app.vendor_dict import vendor_dict

import os

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    # gets directory of folder holding images and passes it to index
    image_names= os.listdir("./app/static/carousel")
    vendors = Vendor.query.order_by(Vendor.boothNum)
    
    # for vendor in vendors
    #   Find booth_[booth_num]
    #   Update booth_name and status
    return render_template('index.html', image_name = image_names, vendors = vendors, vendor_dict = vendor_dict)

@app.route('/application', methods=['GET', 'POST'])
def application():
    form = ApplicationForm()
        
    if form.validate_on_submit():
        v = Vendor(name = form.name.data, business = form.business.data, address = form.address.data, 
                   citystatezip = form.citystatezip.data, email = form.email.data, phoneNum = form.phoneNum.data, desc = form.desc.data, 
                   boothNum = form.boothNum.data, boothLoc = form.boothLoc.data, tableNum = form.tableNum.data, date = form.date.data, status="pendingApproval")
        db.session.add(v)
        db.session.commit()
        session['name'] = str(v.name)
        session['business'] = str(v.business)
        session['address'] = str(v.address)
        session['citystatezip'] = str(v.citystatezip)
        session['email'] = str(v.email)
        session['phoneNum'] = str(v.phoneNum)
        session['desc'] = str(v.desc)
        session['boothNum'] = str(v.boothNum)
        session['boothLoc'] = str(v.boothLoc)
        session['tableNum'] = str(v.tableNum)
        session['date'] = str(v.date)
        return redirect('/confirmation')
    return render_template('application.html', form=form)

@app.route('/confirmation')
def confirmation():
    # Retrieve the data stored in the session variable
    name = session.get('name')
    business = session.get('business')
    address = session.get('address')
    citystatezip = session.get('citystatezip')
    email = session.get('email')
    phoneNum = session.get('phoneNum')
    desc = session.get('desc')
    boothNum = session.get('boothNum')
    boothLoc = session.get('boothLoc')
    tableNum = session.get('tableNum')
    date = session.get('date')

    return render_template('confirmation.html', name=name, business=business, address=address, citystatezip=citystatezip, email=email, phoneNum=phoneNum,
                           desc=desc, boothNum=boothNum, boothLoc=boothLoc, tableNum=tableNum, date=date)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')