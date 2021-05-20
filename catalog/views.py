from django.shortcuts import render
from catalog.models import Book,Author,BookInstance,Genre
from django.views import generic
from django.contrib.auth.decorators import login_required  #Part8
from django.contrib.auth.mixins import LoginRequiredMixin #Part8
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.


@login_required    #Part8
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    #Challenges
    num_genres = Genre.objects.all().count()

    num_potter = Book.objects.filter(title__icontains='potter').count()

    #Part7
    #Session example to tell user times in the home page.
    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1



    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_potter': num_potter,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        
        return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10



class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        try:
            author = Author.objects.get(pk=primary_key)
        except Author.DoesNotExist:
            raise Http404('Book does not exist')
        
        return render(request, 'catalog/author_detail.html', context={'author': author})



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# All borrowed books for librarians to see
class AllLoansBooksViewForLibrarians(PermissionRequiredMixin,generic.ListView):

    permission_required = 'catalog.can_mark_returned'

    """Generic class-based view listing books on loan, for the librarian to see."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_loaned_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')