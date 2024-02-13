from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

DB_USERNAME = 'muazrom'
DB_PASSWORD = 'wk8JeJEKtW2eBBJX'

DB_URI = f'mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@attendance.lmnvh79.mongodb.net/'
DB_CLIENT = pymongo.MongoClient(DB_URI)['attendance']




students_db = DB_CLIENT['students']
Staffs_db = DB_CLIENT['Staffs']
leaves_db = DB_CLIENT['leaves']
Lecturer_db =DB_CLIENT['Lecturer']

app = Flask(__name__)
app.secret_key = 'tu324y2h3i4n23jsgdf'


""""
CRUD - 
    Create - Insert (DONE)

    students_db.insert_one({})

    Read - Find (BELUM)

    students_db.find_one({})
    or
    students_db.find({})

    Update - Update (BELUM)



    Delete - Delete (BELUM)

        leaves_db.delete_one({})
"""

def get_user(matric_number):
    return students_db.find_one({
        'matric_number': matric_number
    })

def get_user(Username):
    return Staffs_db.find_one({
        'Username': Username
    })

def get_user(Nickname):
    return Lecturer_db.find_one({
        'Nickname' : Nickname
    })

@app.route('/approve_leave', methods=['POST'])
def approve_leave():
    leave_id = request.form['leave_id']

    leaves_db.update_one({
        '_id': ObjectId(leave_id)
    }, {
        '$set': {
            'status': 'Approved'
        }

    })

    return redirect(url_for('indexStaff'))

@app.route('/reject_leave', methods=['POST'])
def reject_leave():
    leave_id = request.form['leave_id']

    leaves_db.update_one({
        '_id': ObjectId(leave_id)
    }, {
        '$set': {
            'status': 'Rejected'
        }

    })

    return redirect(url_for('indexStaff'))


@app.route('/cancel_leave', methods=['POST'])
def cancel_leave():
    leave_id = request.form['leave_id']

    leaves_db.delete_one({
        '_id': ObjectId(leave_id)
    })

    return redirect(url_for('index'))

@app.route('/Lecturer')
def indexLecturer():
    if 'Nickname' in session:
        user = get_user(session['Nickname'])

        applied_leaves = leaves_db.find({
        })
        print(applied_leaves)
        return render_template('indexLecturer.html', user=user, applied_leaves=applied_leaves)
    else:
        return redirect(url_for('loginLecturer'))

@app.route('/Staff')
def indexStaff():
    if 'Username' in session:
        user = get_user(session['Username'])

        applied_leaves = leaves_db.find({
            'status': 'Pending'

        })

        print(applied_leaves)
        return render_template('indexstaff.html', user=user, applied_leaves=applied_leaves)
    else:
        return redirect(url_for('loginstaff'))

@app.route('/Student')
def index():
    if 'matric_number' in session:
        user = get_user(session['matric_number'])

        
        applied_leaves = leaves_db.find({
            'matric_number': session['matric_number'],
            'status': 'Pending'
        })

        approve_leaves = leaves_db.find({
            'matric_number': session['matric_number'],
            'status': 'Approved'

        })

        reject_leaves = leaves_db.find({
            'matric_number': session['matric_number'],
            'status': 'Rejected'

        })

        print(reject_leaves)
        print(approve_leaves)
        print(applied_leaves)
        return render_template('index.html', user=user, applied_leaves=applied_leaves, approve_leaves=approve_leaves, reject_leaves=reject_leaves)
    else:
        return redirect(url_for('login'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        msg = request.args.get('msg')

        if 'matric_number' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', msg=msg)
    
    elif request.method =='POST':
        matric_number = request.form['matric_number']
        password = request.form['password']

        """Check if user exists"""

        find_user = students_db.find_one({
            'matric_number': matric_number,
        })

        if find_user:
            if check_password_hash(find_user['password'], password):
                """Kalau Betul Password, Set Session (Login Allowed)"""
                session['matric_number'] = matric_number

                session['first_name'] = find_user['first_name']
                session['last_name'] = find_user['last_name']
                session['email'] = find_user['email']

                return redirect(url_for('index'))
            else:
                return redirect(url_for('login', msg='wpwd'))
        else:
            return redirect(url_for('login', msg='ne_matric'))
        

@app.route('/loginLecturer', methods=['GET', 'POST'])
def loginLecturer():

    if request.method == 'GET':
        msg = request.args.get('msg')

        if 'Nickname' in session:
            return redirect(url_for('indexLecturer'))
        else:
            return render_template('loginLecturer.html', msg=msg)
    
    elif request.method =='POST':
        Nickname = request.form['Nickname']
        password = request.form['password']

        """Check if user exists"""

        find_user = Lecturer_db.find_one({
            'Nickname': Nickname,
        })

        if find_user:
            if check_password_hash(find_user['password'], password):
                """Kalau Betul Password, Set Session (Login Allowed)"""
                session['Nickname'] = Nickname
                session['first_name'] = find_user['first_name']
                session['last_name'] = find_user['last_name']
                session['email'] = find_user['email']
                session['_id'] = str(find_user['_id'])

                return redirect(url_for('indexLecturer'))
            else:
                return redirect(url_for('loginLecturer', msg='wpwd'))
        else:
            return redirect(url_for('loginLecturer', msg='ne_Nickname'))
        

@app.route('/loginstaff', methods=['GET', 'POST'])
def loginstaff():

    if request.method == 'GET':
        msg = request.args.get('msg')

        if 'Username' in session:
            return redirect(url_for('indexStaff'))
        else:
            return render_template('loginstaff.html', msg=msg)
    
    elif request.method =='POST':
        Username = request.form['Username']
        password = request.form['password']

        """Check if user exists"""

        find_user = Staffs_db.find_one({
            'Username': Username,
        })

        if find_user:
            if check_password_hash(find_user['password'], password):
                """Kalau Betul Password, Set Session (Login Allowed)"""
                session['Username'] = Username
                session['first_name'] = find_user['first_name']
                session['last_name'] = find_user['last_name']
                session['email'] = find_user['email']

                return redirect(url_for('indexStaff'))
            else:
                return redirect(url_for('loginstaff', msg='wpwd'))
        else:
            return redirect(url_for('loginstaff', msg='ne_Username'))
        
@app.route('/register', methods = ['GET', 'POST'])
def register():

    if request.method == 'GET':

        if 'matric_number' in session:
            return redirect(url_for('index'))
        
        else:
            return render_template('register.html')
        
    elif request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        matric_number = request.form['matric_number']
        tutorial_class = request.form['tutorial_class']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        find_matric = students_db.find_one({
            'matric_number': matric_number
        })

        if find_matric:
            return redirect(url_for('register'), msg='mc_exists')
        
        else:

            students_db.insert_one({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'matric_number': matric_number,
                'tutorial_class': tutorial_class,
                'password': hashed_password
            })

            return redirect(url_for('login'))


@app.route('/registerstaff', methods = ['GET', 'POST'])
def registerstaff():

    if request.method == 'GET':

        if 'Username' in session:
            return redirect(url_for('indexstaff'))
        
        else:
            return render_template('registerstaff.html')
        
    elif request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        Username = request.form['Username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        find_Username = Staffs_db.find_one({
            'Username': Username
        })

        if find_Username:
            return redirect(url_for('registerstaff'), msg='mc_exists')
        
        else:

            Staffs_db.insert_one({
                'first_name': first_name,
                'last_name': last_name,
                'Username': Username,
                'email': email,
                'password': hashed_password
            })

            return redirect(url_for('loginstaff'))
        

@app.route('/registerLecturer', methods = ['GET', 'POST'])
def registerLecturer():

    if request.method == 'GET':

        if 'Nickname' in session:
            return redirect(url_for('indexLecturer'))
        
        else:
            return render_template('registerLecturer.html')
        
    elif request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        Nickname = request.form['Nickname']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        find_Username = Lecturer_db.find_one({
            'Nickname': Nickname
        })

        if find_Username:
            return redirect(url_for('registerLecturer'), msg='mc_exists')
        
        else:

            Lecturer_db.insert_one({
                'first_name': first_name,
                'last_name': last_name,
                'Nickname': Nickname,
                'email': email,
                'password': hashed_password,
                'tutorial_class':'none'
            })

            return redirect(url_for('loginLecturer'))

       
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/new_class', methods=['POST'])
def newclass():
    tutorial_class = request.form['tutorial_class']
    _id = session['_id']


    Lecturer_db.update_one({
        '_id': ObjectId(_id)
    },{ '$addToSet':{
        'tutorial_class':tutorial_class
    }
    })

    return redirect(url_for('indexLecturer'))



@app.route('/apply_leave', methods=['POST'])
def p_apply_leave():

    first_name = session['first_name']
    last_name = session['last_name']
    matric_number = session['matric_number']
    tutorial_class = request.form['tutorial_class']
    leaves_type = request.form['leaves_type']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    attachment = request.files['attachment']

    """Print Attachment Name"""

    print(attachment.filename)

    """Save Attachment"""

    attachment.save(f'static/attachments/{attachment.filename}')

    leaves_db.insert_one({
        'first_name': first_name,
        'last_name': last_name,
        'matric_number': matric_number,
        'leaves_type' : leaves_type,
        'start_date': start_date,
        'end_date': end_date,
        'tutorial_class': tutorial_class,
        'attachment':attachment.filename,
        'status': 'Pending',
        'approval_date': 'N/A'
    })

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

