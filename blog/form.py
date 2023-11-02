from django import forms

class CommentForm(forms.Form):

    user_name = forms.CharField(label="Name", max_length=120)
    user_email = forms.EmailField(label="Email")
    text = forms.CharField(label="Your Comment", max_length=100)



