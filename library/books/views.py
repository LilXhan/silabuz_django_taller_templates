from django.shortcuts import render, redirect
from django.views.generic import ListView, View

from .models import Book
from .forms import BookForm
import urllib.request
import json

class CreateBook(View):
    def get(self, request):

        form = BookForm()

        context = {
            'form': form
        }

        return render(request, 'add.html', context)

    def post(self, request):

        form = BookForm(request.POST)
        if form.is_valid():
            print('hola')
            cleaned_data = form.cleaned_data
            b = Book.objects.create(**cleaned_data)
            b.save()
            
            return redirect('list-book')
    

class Index(View):
    def get(self, request):

        url = 'https://silabuzinc.github.io/books/books.json'
        data = urllib.request.urlopen(url)
        data = json.load(data)


        for book in data:
            book.pop('bookID')
            book.pop('FIELD13')
            
            book['authors'] = book['authors'][:400]

            try:
                book['num_pages'] = int(book['num_pages'])
            except:
                book['num_pages'] = 0

            try: 
                book['average_rating'] = float(book['average_rating'])
            except:
                book['average_rating'] = 0

            
            book['publication_date'] = book['publication_date'].split('/')

            if '/'.join(book['publication_date']) in ['11/31/2000', '6/31/1982']:
                date = '2023-01-16'
                book['publication_date'] = date
                b = Book.objects.create(**book)
                b.save()
                break

            if len(book['publication_date']) == 3:
                date = ''
                date += book['publication_date'][2] + '-'
                date += book['publication_date'][0] + '-'
                date += book['publication_date'][1]
            else:
                date = '2023-01-16' 

            book['publication_date'] = date

            b = Book.objects.create(**book)
            b.save()
        

class ListBook(ListView):
    template_name = 'book_list.html'
    model = Book
