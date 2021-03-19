from flask_wtf import FlaskForm
from wtforms import Form, StringField ,PasswordField ,SelectField ,validators,IntegerField,DateField,BooleanField,FloatField
from wtforms.fields.html5 import EmailField

class SignInForm(FlaskForm):
	UserName = StringField('帳號',[validators.DataRequired(),validators.Length(min=2,max=30)])
	Email = EmailField('Email',[validators.DataRequired(),validators.Email()])
	Password = PasswordField('密碼',[
		validators.DataRequired(),
		validators.EqualTo('Confirm',message='密碼必須一致')
	])
	Confirm = PasswordField('再次輸入密碼')

class LogInForm(FlaskForm):
	Email = StringField('輸入Email',[validators.DataRequired()])
	Password = PasswordField('輸入密碼',[validators.DataRequired()])

class InspectionForm(FlaskForm):
	CageClass = StringField('箱網編號',[validators.DataRequired()])
	Boat = StringField('船隻編號',[validators.DataRequired()])

class CageBuildForm(FlaskForm):
	CageClass = StringField('箱網類別',[validators.DataRequired()])
	BuildDate = DateField('箱網建置時間 ex: 2020/01/02 05:10',format='%Y/%m/%d %H:%M')

class CageForm(FlaskForm):
	CageClass = StringField('箱網類別',[validators.DataRequired()])
	FishClass = StringField('魚種',[validators.DataRequired()])
	Amount = IntegerField('數量',[validators.DataRequired()])