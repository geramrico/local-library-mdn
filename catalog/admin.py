from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.

# admin.site.register(Book), se quita porque se agrego abajo con el decorador @admn.register
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)


#Change how Models display in admin interface

#Edicion "en linea" de registros asociados xxx
class BookInline(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    #Mostar en tabla en panel de admin
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    #Para cambiar como se visualiza un campo de info en la vista de editar   
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    inlines = [BookInline]

#Edicion "en linea" de registros asociados xxx
class BookInstanceInline(admin.TabularInline):
    model = BookInstance


 
@admin.register(Book)   #same as "admin.site.register"
class BookAdmin(admin.ModelAdmin):
    #Mostrar en panel de admin
    list_display = ('title', 'author', 'display_genre')

    #Edicion "en linea" de registros asociados xxx
    inlines = [BookInstanceInline]


@admin.register(BookInstance)   #same as "admin.site.register"
class BookInstanceAdmin(admin.ModelAdmin):
     #Agrega la opcion de filtrar para buscar
    list_filter = ('status','due_back') 

    #Agrupa en el formulario de BookInstance
    fieldsets = (
    (None, {
            'fields': ('book', 'imprint', 'id')
    }),
    ('Availability', {
        'fields': ('status', 'due_back')
    }),
    )

    list_display = ('book', 'status','due_back','id')