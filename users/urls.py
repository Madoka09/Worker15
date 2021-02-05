""" Users urls """

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('usuarios', views.get_users, name="users"),
    path('agregar_usuario', views.add_user_view, name="add_user_view"),
    path('agregando_usuario', views.add_user_action, name="add_user_action"),
    path('ocultar_usuario', views.hide_user, name="hide_user"),
    path('gestion_usuarios', views.active_user, name="active_user"),
    path('perfil', views.profile, name="profile"),
    path('editar_usuario', views.edit_user_view, name="edit_user_view"),
    path('editando_usuario', views.edit_user_action, name="edit_user_action"),
    path('permisos', views.permissions, name="permissions"),
    path('agregar_grupo', views.create_group, name="create_group"),
    path('editar_grupo/<group>', views.edit_group, name="edit_group"),
    path('guardar_permisos', views.save_permissions_group, name="save_permissions"),
    path('agregar_usuario_grupo/<group>', views.add_user_group_page, name="add_user_group_page"),
    path('agregar_usuario_grupo_accion', views.add_user_group_action, name="add_user_group_action"),
    path('remover_usuario_grupo', views.remove_user_group, name="remove_user_group"),
    path('borrar_grupo', views.delete_group, name="delete_group"),

]
