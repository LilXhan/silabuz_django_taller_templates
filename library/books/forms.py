from django import forms 

class BookForm(forms.Form):
    title = forms.CharField(max_length=400, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    authors = forms.CharField(max_length=400)
    average_rating = forms.FloatField()
    isbn = forms.CharField(max_length=400)
    isbn13 = forms.CharField(max_length=400)
    language_code = forms.CharField(max_length=20)
    num_pages = forms.IntegerField()
    ratings_count = forms.IntegerField()
    text_reviews_count = forms.IntegerField()
    publication_date = forms.DateField()
    publisher = forms.CharField(max_length=400)