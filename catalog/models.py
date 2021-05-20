from django.db import models
from django.urls import reverse #Part3 - generate URLs by reversing URL patterns
import uuid #Req. for unique book instances
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genre(models.Model):
    ''' Represents a book genre'''
    name = models.CharField(max_length = 200, help_text ='Enter a genre (e.g. Science Fiction')

    def __str__(self):
        '''String for representing the model object'''
        return self.name

class Book(models.Model):
    '''Model representing a book (not specific one)'''
    title = models.CharField(max_length = 200)

    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)

    summary = models.TextField(max_length=1000,help_text="Brief description of the book")

    isbn = models.CharField('ISBN',max_length=13,unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')

    language = models.ForeignKey('Language',null=True,on_delete=models.SET_NULL)

    '''representation of the object in human readable form'''
    def __str__(self):
        return self.title

    '''Returns URL to access a detail record for book'''
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        '''Func to display genre in admin'''
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    '''represents a specific copy of a book (that can be borrowed)'''
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='ID for this particular book across library')
    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices = LOAN_STATUS,
        blank=True,
        default = 'm',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    '''representation of the object in human readable form'''
    def __str__(self):
        return f'{self.id} ({self.book.title})'

    #Part8
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    '''Returns URL to access a detail record for book'''
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    name = models.CharField(max_length=200,help_text='Enter the book language')

    def __str__(self):
        return self.name