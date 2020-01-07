from django import forms
from User.models import Person,Rationcard
from Distributor.models import Distributor

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
class DateInput(forms.DateInput):
    input_type='date'
 
class PersonForm1(forms.Form):    

    sex=(('MALE','MALE'),
         ('FEMALE','FEMALE'),
         ('OTHER','OTHER'))

    First_name=forms.CharField(max_length=100,required=True)
    Middle_name=forms.CharField(max_length=100,required=True)
    Last_name=forms.CharField(max_length=100,required=True)
    aadhar=forms.CharField(max_length=16,required=True)
    finger=forms.IntegerField()
    sex=forms.CharField(widget=forms.Select(choices=sex))
    age=forms.IntegerField()
    DOB=forms.DateField(widget=DateInput)
    photo=forms.ImageField()
 


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
       
            Row(
                Column('First_name', css_class='form-group col-md-4 '),
                Column('Middle_name', css_class='form-group col-md-4 '),
                Column('Last_name', css_class='form-group col-md-4 '),
                css_class='form-row'
            ),
            
            Row(
                Column('sex', css_class='form-group col-md-4 mb-0'),
                Column('age', css_class='form-group col-md-4 mb-0'),
                Column('DOB', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             
            
                Row(
                Column('aadhar', css_class='form-group col-md-4 mb-0'),
                Column('finger', css_class='form-group col-md-4 mb-0'),
                Column('photo', css_class='form-group col-md-4 mb-0'),
 
                css_class='form-row'
            ),

                          

            Submit('submit', 'Register')
        )



