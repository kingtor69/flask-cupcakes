from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, URLField
from wtforms.validators import InputRequired, URL, NumberRange

class AddCupcakeForm(FlaskForm):

    flavor = StringField("Flavor", validators=[InputRequired(message="A flavorless cupcake? Ew. Try again, please.")])
    size = StringField("Size", validators=[InputRequired(message="I'm assuming your cupcake exists, yeah? Please enter a size.")])
    rating = FloatField("Rating", validators=[InputRequired(message="Please enter a rating"), NumberRange(min=0, max=5.0, message="Please enter a rating from 0 to 5.")])
    image = URLField("Image", validators=[Optional(), URL(message="this should be a valid URL")])

