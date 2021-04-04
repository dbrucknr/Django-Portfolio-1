from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from users.forms import UserChangeForm, UserCreationForm

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ["username", "email"]
    list_filter = ["is_staff", "is_active", "is_superuser", "groups"]
    # filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'groups')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'groups')}
        ),
    )
    search_fields = ["username", "email"] 

admin.site.register(User, UserAdmin)