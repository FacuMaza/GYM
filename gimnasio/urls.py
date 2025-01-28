from django.contrib import admin
from django.urls import path
from gimnasio import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.index, name= "index"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

##login



##SOCIOS
urlpatterns += [
    path('socios/', views.lista_socios, name='lista_socios'),
    path('socios/crear/', views.crear_socio, name='crear_socio'),
    path('socios/editar/<int:pk>/', views.editar_socio, name='editar_socio'),
    path('socios/eliminar/<int:pk>/', views.eliminar_socio, name='eliminar_socio'),
    path('socios/detalle/<int:pk>/', views.detalle_socio, name='detalle_socio')
]


##TIPOS DE USUARIOS
urlpatterns += [
    path('tipos-usuario/', views.tipo_usuario_list, name='tipo_usuario_list'),
    path('tipos-usuario/crear/', views.tipo_usuario_create, name='tipo_usuario_create'),
    path('tipos-usuario/editar/<int:pk>/', views.tipo_usuario_update, name='tipo_usuario_update'),
    path('tipos-usuario/eliminar/<int:pk>/', views.tipo_usuario_delete, name='tipo_usuario_delete'),
]

##USUARIOS

urlpatterns += [
    path('usuarios/crear/', views.usuario_create, name='usuario_create'),
    path('usuarios/lista/', views.usuario_list, name='usuario_list'),
    path('usuarios/editar/<int:pk>/', views.usuario_update, name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', views.usuario_delete, name='usuario_delete'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/<int:pk>/', views.password_reset_confirm, name='password_reset_confirm'),
]


## gym

urlpatterns += [
    path('gimnasios/', views.gimnasio_lista, name='gimnasio_lista'),
    path('gimnasios/crear/', views.gimnasio_crear, name='gimnasio_crear'),
    path('gimnasios/editar/<int:pk>/', views.gimnasio_editar, name='gimnasio_editar'),
    path('gimnasios/eliminar/<int:pk>/', views.gimnasio_eliminar, name='gimnasio_eliminar'),
    path('gimnasios/<int:pk>/', views.gimnasio_detalle, name='gimnasio_detalle'),
]


##tipo de mensualidad 
urlpatterns += [
    path('tipos/', views.lista_tipos_mensualidad, name='lista_tipos_mensualidad'),
    path('tipos/crear/', views.crear_tipo_mensualidad, name='crear_tipo_mensualidad'),
    path('tipos/editar/<int:pk>/', views.editar_tipo_mensualidad, name='editar_tipo_mensualidad'),
    path('tipos/eliminar/<int:pk>/', views.eliminar_tipo_mensualidad, name='eliminar_tipo_mensualidad'),
]


##cuotas

urlpatterns += [
    path('asignar_mensualidad/', views.asignar_mensualidad, name='asignar_mensualidad'),
    path('lista_cuotas/',views.lista_cuotas, name='lista_cuotas'),
    path('renovar_mensualidad/', views.renovar_mensualidad, name='renovar_mensualidad'),
    path('renovar_mensualidad_manual/', views.renovar_mensualidad_manual, name='renovar_mensualidad_manual'),
]

## productos y ventas

urlpatterns += [
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/crear/', views.producto_crear, name='producto_crear'),
    path('productos/editar/<int:pk>/', views.producto_editar, name='producto_editar'),
    path('producto_precio/<int:pk>/', views.producto_precio, name='producto_precio'),
    path('productos/eliminar/<int:pk>/', views.producto_eliminar, name='producto_eliminar'),
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/crear/', views.venta_crear, name='venta_crear'),
    
]


## EXTRAS

urlpatterns += [
    path('extras/', views.extras_list, name='extras_list'),
    path('extras/create/', views.extras_create, name='extras_create'),
    path('extras/<int:pk>/update/', views.extras_update, name='extras_update'),
    path('extras/<int:pk>/delete/', views.extras_delete, name='extras_delete'),
]


##caja diaria
urlpatterns += [
    path('balance/', views.balance_diario, name='balance_diario'),
    path('balance/<int:gimnasio_id>/', views.mostrar_balance, name='mostrar_balance'),
    path('historial/', views.historial_balances, name='historial_balances'),
]


##lista de ingresos 

urlpatterns += [
    path('listado-ingresos/', views.listado_ingresos_diarios, name='listado_ingresos'),
]


##api socios


urlpatterns += [
    path('api/socios/', views.api_socios, name='api_socios'),
]
