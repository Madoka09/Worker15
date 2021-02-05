from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Escriba la contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme la contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'fathers_last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'fathers_last_name', 'mothers_last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'fathers_last_name', 'mothers_last_name', 'is_verified', 'is_admin')
    list_filter = ('is_verified', 'is_admin', 'created_at', 'modified_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'fathers_last_name', 'mothers_last_name', 'gender', 'birthdate')}),
        ('Estatus', {'fields': ('is_admin', 'is_verified', 'is_active')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Usuarios', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'fathers_last_name'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(User, CustomUserAdmin)
#admin.site.unregister(Group)
