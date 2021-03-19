from flask import Flask, render_template, request, redirect, url_for, session
from database import db_session, init_db
from sqlalchemy import desc
from models.member import Member
from models.cagebuild import Cagebuild
from models.inspection import Inspection
from models.cage import Cage
from models.form import SignInForm,LogInForm,InspectionForm,CageBuildForm,CageForm
import datetime
import os
import geoip2.database
from flask import jsonify

#app init
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.before_request
def make_session_permanet():
	session.permanet = True
	app.permanet_session_lifetime = datetime.timedelta(minutes=10)

@app.before_first_request
def init():
    init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#Router
	#Member
@app.route('/signin',methods=['GET','POST'])
def signin():
	form = SignInForm(request.form)
	if request.method == 'POST' and form.validate():
		member = Member(
			UserName = form.UserName.data,
			Email = form.Email.data,
			Password = form.Password.data
		)
		db_session.add(member)
		db_session.commit()
		return redirect(url_for('login'))
	return render_template('signin.html',form=form)

@app.route('/',methods = ['GET','POST'])
def login():
	form = LogInForm(request.form)
	error = None
	if request.method == 'POST' and form.validate():
		member = Member.query.filter(Member.Email == form.Email.data).first()
		if member:
			if member.Password == form.Password.data:
				session['Id'] = member.Id
				session['UserName'] = member.UserName
				return redirect('/index')
			else:
				member = None
		if not member:
			error = "帳號、密碼不正確"

	return render_template('login.html',form=form,error=error)

@app.route('/logout')
def logout():
	session.pop('Id',None)
	session.pop('UserName',None)
	return redirect('/')

@app.route('/index')
def index():
	return render_template('index.html')

	#CageBuild
@app.route('/cagebuild_create',methods=['GET','POST'])
def cagebuild_create():
	reader = geoip2.database.Reader('./GeoLite2-City_20190625/GeoLite2-City.mmdb')
	ip = request.remote_addr
	response = reader.city(ip)

	form = CageBuildForm(request.form)
	if 'UserName' in session:
		if request.method == 'POST' and form.validate():
			cagebuild = Cagebuild(
				CageClass = form.CageClass.data,
				BuildDate = form.BuildDate.data,
				FixDate = form.BuildDate.data,
				Lat = response.location.latitude,
				Lng = response.location.longitude
			)
			db_session.add(cagebuild)
			db_session.commit()
			return redirect(url_for('cage_build_list'))
		return render_template('cagebuild_create.html',form=form)
	return redirect(url_for('login'))

@app.route('/cage_build_list')
def cage_build_list():
	if 'UserName' in session:
		CageBuildList = Cagebuild.query.all()
		return render_template('cagebuild_list.html',buildlist=CageBuildList)
	return redirect(url_for('login'))

@app.route('/cage_update_time',methods=['GET'])
def cage_update_time():
	id = request.args.get('id')
	cagebuild = Cagebuild.query.filter(Cagebuild.Id == id).first()
	if cagebuild:
		cagebuild.FixDate = datetime.datetime.now()
		db_session.commit()
		return redirect(url_for('cage_build_list'))
	return redirect(url_for('error'))

	#Inspection
@app.route('/inspection_create',methods=['GET','POST'])
def inspection_create():
	form = InspectionForm(request.form)
	if 'UserName' in session:
		if request.method == 'POST' and form.validate():
			inspection = Inspection(
				CageClass = form.CageClass.data,
				Boat = form.Boat.data,
				EndTime = None,
				UserId = session['Id']
			)
			db_session.add(inspection)
			db_session.commit()
			return redirect(url_for('inspection_list'))
		return render_template('inspection_create.html',form=form)
	return redirect(url_for('login'))

@app.route('/inspection_list')
def inspection_list():
	if 'UserName' in session:
		inspectionList = Inspection.query.all()
		return render_template('inspection_list.html',inspectionlist=inspectionList)
	return redirect(url_for('login'))

@app.route('/inspection_update_time',methods=['GET'])
def inspection_update_time():
	id = request.args.get('id')
	boolean = request.args.get('boolean')
	inspection = Inspection.query.filter(Inspection.Id == id).first()
	if inspection:
		if boolean == None:
			inspection.EndTime = datetime.datetime.now()
		else:
			inspection.EndTime = datetime.datetime.now()
			inspection.FishStatus = strinbool(boolean)
		inspection.UserId = session['Id']
		db_session.commit()
		return redirect(url_for('inspection_list'))
	return redirect(url_for('error'))

	#CageFish
@app.route('/cagefish_create',methods=['GET','POST'])
def cagefish_create():
	form = CageForm(request.form)
	if 'UserName' in session:
		if request.method == 'POST' and form.validate():
			cagebuild = Cagebuild.query.filter(Cagebuild.CageClass == form.CageClass.data).first()
			cage = Cage(
				CageId = cagebuild.Id,
				FishClass = form.FishClass.data,
				Amount = form.Amount.data
			)
			db_session.add(cage)
			db_session.commit()
			return redirect(url_for('cagefish_list'))
		return render_template('cagefish_create.html',form=form)
	return redirect(url_for('login'))

@app.route('/cagefish_list')
def cagefish_list():
	if 'UserName' in session:
		cagelist = Cage.query.all()
		return render_template('cagefish_list.html',cagelist=cagelist)
	return redirect(url_for('login'))

@app.route('/cagefish_update_time',methods=['GET'])
def cagefish_update_time():
	id = request.args.get('id')
	boolean = request.args.get('boolean')
	cage = Cage.query.filter(Cage.Id == id).first()
	if cage:
		if boolean == None:
			cage.LastFeedTime = datetime.datetime.now()
		else:
			cage.LastFeedTime = datetime.datetime.now()
			cage.FishStatus = strinbool(boolean)
		db_session.commit()
		return redirect(url_for('cagefish_list'))
	return redirect(url_for('error'))

@app.route('/error')
def error():
	return render_template('error.html')

#Filter
def datetimeformat(value):
	return value.strftime('%Y-%m-%d %H:%M:%S')

def viewusername(value):
	member = Member.query.filter(Member.Id == value).first()
	return member.UserName

def strinbool(value):
	return value.lower() in ('1')

def viewcageclass(value):
	cagebuild = Cagebuild.query.filter(Cagebuild.Id == value).first()
	return cagebuild.CageClass

def trueorfalse(value):
	if value == True:
		boostr = '良好'
		return boostr
	else:
		boostr = '欠佳'
		return boostr

app.jinja_env.filters['datetime'] = datetimeformat
app.jinja_env.filters['viewusername'] = viewusername
app.jinja_env.filters['viewcageclass'] = viewcageclass
app.jinja_env.filters['trueorfalse'] = trueorfalse

#Run App
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run(
    	#host = '163.18.42.226',
    	host = '127.0.0.1',
    	port = 80,
    	debug = True
	)