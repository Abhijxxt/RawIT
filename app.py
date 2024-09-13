import random
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=100), unique=True, nullable=False)
    password = db.Column(db.String(length=20), nullable=False)
    user_image = db.Column(db.String(length=200), nullable=False)

class Issue(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=100), unique=True, nullable=False)
    issue = db.Column(db.String(length=200), nullable=False)
    description = db.Column(db.String(length=500), nullable=True)

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.String(length=100), unique=True ,nullable=False) 
    name = db.Column(db.String(length=100), nullable=False)
    image = db.Column(db.String(length=1000), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def HomePage():
    if request.method == 'GET':
        product_data = Product.query.all()
        # processed_data = list()
        # if len(product_data) != 0:
        #     processed_data = [
        #         product_data[random.randrange(0,len(product_data))],
        #         product_data[random.randrange(0,len(product_data))],
        #         product_data[random.randrange(0,len(product_data))],
        #         product_data[random.randrange(0,len(product_data))]
        #     ]
        return render_template('home.html', username='Username', userimage='', products=product_data[-4:])
    if request.method == 'POST':
        pass
        #Render template with user email use session in flask
@app.route('/login', methods=['GET','POST'])
def LoginPage():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        data = User.query.all()
        form_email = request.form['email']
        form_password = request.form['password']
        for row in data:
            if  form_email == row.email and form_password == row.password :
                # return redirect(url_for('.HomePage', username=row.email, userimage=row.user_image))
                product_data = Product.query.all()
                return render_template('home.html',username=row.email, userimage=row.user_image, products=product_data[-4:])

        return redirect('/false-login')
        
@app.route('/false-login')
def FalseLogin():
    return "There was an error logging you in. Maybe the password or email was wrong."

@app.route('/signup', methods=['POST','GET'])
def SignupPage():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        form_email = request.form['email']
        form_password = request.form['password']
        form_confirm_password = request.form['confirmpassword']
        if form_password == form_confirm_password:
            try:
                data = User.query.all();
                new_user_id = 0
                if len(data) > 0:
                    new_user_id = data[-1].id + 1
                else:
                    new_user_id = 1
                user_image_url = f'https://avatar.iran.liara.run/public/{new_user_id}'
                new_user = User(email=form_email, password=form_password, user_image=user_image_url)
                db.session.add(new_user)
                db.session.commit()
                # return redirect(url_for('.HomePage',username=form_email,userimage=user_image_url))
                product_data = Product.query.all()
                return render_template('home.html',username=form_email,userimage=user_image_url, products=product_data[-4:])
            
            except:
                return redirect('/false-signup-page')
                
        else:
            return redirect('/false-signup-page')

@app.route('/false-signup-page')
def FalseSignUp():
    return "There was an error signin you up. Maybe the email is already in use or the password didn't match."

@app.route('/contact-us', methods=['GET', 'POST'])
def ContactPage():
    if request.method == 'GET':
        return render_template('contact.html')
    if request.method == 'POST':
        form_email = request.form['email']
        form_issue = request.form['issue']
        form_description = request.form['description']
        loggedIssue = Issue(email=form_email, issue=form_issue, description=form_description)
        try:
            db.session.add(loggedIssue)
            db.session.commit()
        except:
            return "There was an error sending issue"
        return redirect('/')

@app.route('/about-us')
def AboutUsPage():
    return render_template('about.html')

@app.route('/products')
def ProductPage():
    data = Product.query.all()
    return render_template('products.html', products=data)

@app.route('/check-issues')
def IssuesPage():
    issue_data = Issue.query.all()
    return render_template('issues.html', issue = issue_data)

@app.route('/add-product', methods=['GET','POST'])
def AddProductPage():
    if request.method == 'POST':
        productID = request.form['id']
        product_name = request.form['name']
        product_image = request.form['image']
        product_price = request.form['price']
        product_quantity = request.form['quantity']
        print(product_name, product_price)
        try:
            product_db = Product(product_id=productID, name=product_name, image=product_image,price=product_price, quantity=product_quantity)
            db.session.add(product_db)
            db.session.commit()
            return redirect('/add-product')
        except:
            return "Error Adding Product"
    if request.method == 'GET':
        return render_template('addProduct.html')
    
@app.route('/estimator')
def EstimatorPage():
    return render_template('estimator.html')

@app.route('/helping-hand')
def HelpingHandPage():
    return render_template('helpinghand.html')

@app.route('/buy-page')
def BuyPage():
    return render_template('buypage.html')

@app.route('/consult')
def ConsultancyPage():
    return render_template('consultancy.html')

if __name__ == '__main__':
    app.run(debug=True)