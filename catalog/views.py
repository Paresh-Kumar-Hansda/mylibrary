from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import Book, Author, BookInstance, Genre, Borrower, Librarian
from django.contrib.auth.mixins import UserPassesTestMixin


from django.contrib.auth import login
#from django.shortcuts import redirect, render
from django.urls import reverse
from catalog.forms import CustomUserCreationForm


from django.http import HttpResponseRedirect
#from django.shortcuts import render

from .forms import BookAddForm

def newbook(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BookAddForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookAddForm()

    return render(request, 'catalog/newbook.html', {'form': form})




"""
def dashboard(request):
    return render(request, "users/dashboard.html")
"""
def register(request):
    if request.method == "GET":
        return render(
            request, "catalog/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))



#pdf.js
def pdf(request):
    return render(request, 'catalog/simple.html')



def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    #num_instances_borrowed=BookInstance.objects.filter(borrower=request.user.borrower).filter(status__exact='o').count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_genre=Genre.objects.count()
    #session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        #'num_instances_borrowed': num_instances_borrowed,
        'num_authors': num_authors,
        'num_genre':num_genre,
        'num_visits': num_visits,
    
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BorrowerListView(UserPassesTestMixin,generic.ListView):
    model = Borrower
    def test_func(self):
        return self.request.user.is_staff

class BorrowerDetailView(UserPassesTestMixin,generic.DetailView):
    model = Borrower
    def test_func(self):
        return self.request.user.is_staff

class LibrarianListView(UserPassesTestMixin,generic.ListView):
    model = Librarian
    def test_func(self):
        return self.request.user.is_staff
class LibrarianDetailView(UserPassesTestMixin,generic.DetailView):
    model = Librarian
    template_name ='catalog/librarian_detail.html'
    def test_func(self):
        return self.request.user.is_staff

class BookListView(generic.ListView):
    model = Book
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='math')[:5] # Get 5 books containing the title war
    #template_name = 'books/book_list.html def get_queryset is added funtion
    '''
    def get_queryset(self):
        return Book.objects.filter(title__icontains='jhar')[:5] 
    '''
    #new function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
#author listview
class AuthorListView(generic.ListView):
    model = Author
    #context_object_name = 'my_book_list'   # your own name for the list as a template va>
    #queryset = Book.objects.filter(title__icontains='math')[:5] # Get 5 books containing>
    #template_name = 'books/book_list.html def get_queryset is added funtion
    '''
    def get_queryset(self):
        return Book.objects.filter(title__icontains='jhar')[:5]
    '''
    #new function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context




#bookdetail view
class BookDetailView(generic.DetailView):
    model = Book
'''
def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'catalog/book_detail.html', context={'book': book})
'''
class AuthorDetailView(generic.DetailView):
    model = Author

#login required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


#borrowed list
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    #borrowr=BookInstance.objects.filter(id=1)
    #name = Borrower.objects.filter(id__in=borrowr.borrower)
    """Generic class-based view listing books on loan to current user."""
    #model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    #paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user.borrower).filter(status__exact='o').order_by('due_back')
        #return name
#from django.contrib.auth.mixins import UserPassesTestMixin
class LoanedBooksByLibrarianListView(UserPassesTestMixin,generic.ListView):
    model = BookInstance
    #borrowr=BookInstance.objects.filter(id=1)
    #name = Borrower.objects.filter(id__in=borrowr.borrower)
    """Generic class-based view listing books on loan to current user."""
    #model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_librarian.html'
    #paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(librarian=self.request.user.librarian)
        #return name
    def test_func(self):
        return self.request.user.is_staff





    """
#all borrowed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower'] = self.objects.borrower_set.all()
        return context
    """
#from django.contrib.auth.decorators import user_passes_test
#from django.contrib.auth.mixins import UserPassesTestMixin
#@user_passes_test(lambda user: user.is_staff)
class LoanedBooksListView(UserPassesTestMixin,generic.ListView):
    #"""Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    #paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')
    def test_func(self):
        return self.request.user.is_superuser
#form


import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm,BookAddForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            #return HttpResponseRedirect(reverse('all-borrowed') )
            return HttpResponseRedirect('/')
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
"""
from .forms import BorrowerForm
#from .forms import MovieForm
from django.contrib import messages




def new(request):
    if request.method == "POST":
        borrower_form = BorrowerForm(request.POST, request.FILES)
        if borrower_form.is_valid():
            borrower_form.save()
            messages.success(request, ('New borrower was successfully added!'))
        else:
            messages.error(request, 'Error saving form')
        return redirect("catalog:new") 
    borrower_form = BorrowerForm()
    borrowers = Borrower.objects.all()
    return render(request=request, template_name="catalog/new.html", context={'borrower_form':borrower_form, 'borrowers':borrowers})

"""
