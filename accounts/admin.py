from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, RegistrationForm, UserCreationForm, UserChangeForm
from .models import CustomUser,  User1
from django.utils.html import format_html


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    change_list_template = "admin/accounts/change.html"

    def edit(self, instance):
        return format_html('<a href = "/admin/accounts/customuser/{0}/change/" class="changelink">Edit </a>',
                           instance.pk)

    list_display = ('email', 'username', 'phone', 'date_of_birth', 'is_staff', 'is_superuser', 'edit', 'test_res')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('username', 'phone', 'date_of_birth')}),

    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('username', 'phone', 'date_of_birth')}),

    )

    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.site_header = "IPASSIO ADMIN"

admin.site.register(CustomUser, CustomUserAdmin)


class Useradmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User1

    def edit(self, instance):
        return format_html('<a href = "/admin/accounts/user/{0}/change/" class="changelink">Edit </a>',
                           instance.pk)

    list_display = ('email', 'username', 'phone', 'gender', 'date_of_birth', 'is_staff', 'edit',)
    list_filter = ('gender',)
    fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'date_of_birth','gender', 'picture')}),

    )
    add_fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'password1', 'password2')}),
        ('Personal info', {'fields': ('email', 'phone', 'date_of_birth','gender', 'picture')}),

    )

    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.site_header = "IPASSIO ADMIN"

admin.site.register(User1, Useradmin)
