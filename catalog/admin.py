from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)


#Change how Models display in admin interface

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

admin.site.register(Author,AuthorAdmin)

 
@admin.register(Book)   #same as "admin.site.register"
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

@admin.register(BookInstance)   #same as "admin.site.register"
class BookInstanceAdmin(admin.ModelAdmin):
    pass

