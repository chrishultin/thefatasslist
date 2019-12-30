from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, IntegerField, DecimalField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class UpdateRestaurant(Form):
    orig_name = HiddenField('orig_name', validators=[DataRequired()])
    rest_name = StringField('name', validators=[DataRequired()])
    categories = TextAreaField('categories', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired()], places=0)
    ambiance = DecimalField('ambiance', validators=[DataRequired()], places=1)
    food = DecimalField('food', validators=[DataRequired()], places=1)
    consumed = TextAreaField('consumed', validators=[DataRequired()])
    commentary = TextAreaField('commentary', validators=[DataRequired()])
    vegangluten = BooleanField('vegangluten')
    honorablemention = BooleanField('honorablemention')
    champion = BooleanField('champion')
    location = StringField('location', validators=[DataRequired()])
    closed = BooleanField('closed')
    deleteField = SubmitField('Delete (CANNOT BE UNDONE)')
