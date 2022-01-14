from django import forms


class ShareForm(forms.Form):

    message = forms.CharField(max_length = 3000, label = "Message(Optional)", required = False, widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Hey, Look at this course!',
        'rows':5,
    }))