from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20, message='Username must be between 4 and 20 characters')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class HabitForm(FlaskForm):
    name = StringField('Habit Name', validators=[
        DataRequired(),
        Length(min=1, max=100, message='Habit name must be between 1 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500, message='Description cannot exceed 500 characters')
    ])
    category = SelectField('Category', choices=[
        ('health', 'Health & Fitness'),
        ('productivity', 'Productivity'),
        ('learning', 'Learning & Skills'),
        ('mindfulness', 'Mindfulness'),
        ('social', 'Social'),
        ('creativity', 'Creativity'),
        ('finance', 'Finance'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    color = SelectField('Color', choices=[
        ('#007bff', 'Blue'),
        ('#28a745', 'Green'),
        ('#dc3545', 'Red'),
        ('#ffc107', 'Yellow'),
        ('#6f42c1', 'Purple'),
        ('#fd7e14', 'Orange'),
        ('#20c997', 'Teal'),
        ('#e83e8c', 'Pink')
    ], default='#007bff')
    is_public = BooleanField('Share with friends')
    submit = SubmitField('Create Habit')

class EditHabitForm(FlaskForm):
    name = StringField('Habit Name', validators=[
        DataRequired(),
        Length(min=1, max=100, message='Habit name must be between 1 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500, message='Description cannot exceed 500 characters')
    ])
    category = SelectField('Category', choices=[
        ('health', 'Health & Fitness'),
        ('productivity', 'Productivity'),
        ('learning', 'Learning & Skills'),
        ('mindfulness', 'Mindfulness'),
        ('social', 'Social'),
        ('creativity', 'Creativity'),
        ('finance', 'Finance'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    color = SelectField('Color', choices=[
        ('#007bff', 'Blue'),
        ('#28a745', 'Green'),
        ('#dc3545', 'Red'),
        ('#ffc107', 'Yellow'),
        ('#6f42c1', 'Purple'),
        ('#fd7e14', 'Orange'),
        ('#20c997', 'Teal'),
        ('#e83e8c', 'Pink')
    ])
    is_public = BooleanField('Share with friends')
    submit = SubmitField('Update Habit')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20, message='Username must be between 4 and 20 characters')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[
        Optional(),
        Length(max=300, message='Bio cannot exceed 300 characters')
    ])
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class HabitEntryForm(FlaskForm):
    notes = TextAreaField('Notes', validators=[
        Optional(),
        Length(max=200, message='Notes cannot exceed 200 characters')
    ])
    submit = SubmitField('Save Notes')

class FriendRequestForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20, message='Username must be between 4 and 20 characters')
    ])
    submit = SubmitField('Send Friend Request')