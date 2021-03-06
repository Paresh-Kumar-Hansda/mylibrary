from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Language, Book, BookInstance, Borrower, Librarian

#inline author
class BookInline(admin.TabularInline):
    model=Book
    extra=0
#admin.site.register(Book)

#admin.site.register(Author)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines=[BookInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
admin.site.register([Borrower,Librarian])
admin.site.register(Genre)
admin.site.register(Language)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0
'''#bookadminainline
class BookAdminInline(admin.TabularInline):
    model=Book
    extra=0
'''




#admin.site.register(BookInstance)
# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'display_language')
    inlines = [BooksInstanceInline]
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=('book', 'status','borrower', 'due_back', 'id')
    actions=None
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
    def save_model(self, request, obj, form, change):
        if not obj.librarian:
            obj.librarian = request.user.librarian
            obj.save()

        else:
            obj.issuer=request.user.librarian
            obj.save()
    # inlines=[BookAdminInline]
