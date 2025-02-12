from django import forms
from django.forms import DateInput
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *



class SocioForm(forms.ModelForm):
    gimnasio = forms.ModelChoiceField(queryset=Gimnasio.objects.all(), empty_label="Seleccione un Gimnasio",widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Socio
        fields = ['nombre', 'apellido', 'dni','gimnasio', 'tipo_mensualidad', 'clases_restantes']  # Eliminamos el campo usuario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['tipousuario']
        widgets = {
            'tipousuario': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    tipo_usuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de Usuario"
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'tipo_usuario')  # Incluye los campos que quieras del modelo User
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),  # Asegura que la contraseña sea un campo de contraseña
        }

    def save(self, commit=True):
        # Guarda el usuario en auth_user
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)  # Hashea la contraseña usando el método de Django
        user.save()

        # Crea el usuario en tu modelo Usuario personalizado
        tipo_usuario = self.cleaned_data['tipo_usuario']
        usuario_custom = Usuario.objects.create(
            tipo_usuario=tipo_usuario,
            usuario=user.username,
            contrasena=user.password # El password ya viene hasheado desde UserCreationForm
        )

        return usuario_custom


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=255)
    contrasena = forms.CharField(widget=forms.PasswordInput)

class GimnasioForm(forms.ModelForm):
    class Meta:
        model = Gimnasio
        fields = ['direccion'] # Campos que quieres en el formulario
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),    }




class TipoMensualidadForm(forms.ModelForm):
    class Meta:
        model = TipoMensualidad
        fields = ['tipo', 'precio'] #Especifica qué campos del modelo se incluirán en el formulario
        widgets = { # Personaliza el aspecto de los campos del formulario
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'})
        }

from django import forms
from .models import Socio, TipoMensualidad

class AsignarMensualidadForm(forms.Form):
    socio = forms.CharField(
        label="Socio",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    tipo_mensualidad_display = forms.CharField(label="Tipo de Mensualidad Actual", required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    tipo_mensualidad = forms.ModelChoiceField(
        queryset=TipoMensualidad.objects.all(),
        label="Seleccionar Nueva Mensualidad",
        required=False,
        widget=forms.Select(),
        to_field_name='tipo',
        empty_label="Seleccione una mensualidad"
    )
    metodo_pago = forms.ChoiceField(choices=[
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta_credito', 'Tarjeta de Crédito')
    ], label="Método de Pago")
    monto = forms.FloatField(label="Monto Recibido")
    clases_restantes = forms.IntegerField(label="Clases Restantes", required=False, widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        initial_socio = kwargs.pop('initial_socio', None)
        initial_mensualidad = kwargs.pop('initial_mensualidad', None)
        super().__init__(*args, **kwargs)
        if initial_socio:
            self.initial['socio'] = f"{initial_socio.nombre} {initial_socio.apellido}"
            self.fields['socio'].widget.attrs['value'] = f"{initial_socio.nombre} {initial_socio.apellido}"
        if initial_mensualidad:
            self.initial['tipo_mensualidad'] = initial_mensualidad
            self.fields['tipo_mensualidad'].initial = initial_mensualidad
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_mensualidad_seleccionada = cleaned_data.get('tipo_mensualidad')
        socio_value = cleaned_data.get('socio')
        monto = cleaned_data.get('monto')
        clases_restantes = cleaned_data.get('clases_restantes')
        
        if socio_value:
            cleaned_data['socio'] =  self.initial['socio']
            try:
                socio_id = self.initial.get('socio_id')
                socio = Socio.objects.get(pk=socio_id)
                
                if socio.tipo_mensualidad:
                     # Si el socio ya tiene una mensualidad asignada
                     tipo_mensualidad_actual = socio.tipo_mensualidad
                     if not tipo_mensualidad_seleccionada:
                         # si no se selecciono una nueva mensualidad, uso la actual
                         cleaned_data['tipo_mensualidad'] = tipo_mensualidad_actual
                     
                     #Validacion del monto, tanto si selecciono una nueva mensualidad como si usa la misma
                     if monto is None:
                                  self.add_error('monto', 'Este campo es obligatorio al seleccionar una mensualidad')
                     elif cleaned_data['tipo_mensualidad'].precio != monto:
                                  self.add_error('monto', 'El monto recibido no coincide con el precio de la mensualidad seleccionada.')
                     #Validacion de clases restantes
                     if cleaned_data['tipo_mensualidad'].tipo != 'Pase Libre':
                           self.fields['clases_restantes'].required = True
                           if clases_restantes is None and self.fields['clases_restantes'].required:
                                self.add_error('clases_restantes', 'Este campo es obligatorio cuando la mensualidad no es Pase Libre.')
                     else:
                        self.fields['clases_restantes'].required = False
                        
                else:#Si el socio no tiene una mensualidad asignada
                     
                     if not tipo_mensualidad_seleccionada:
                          self.add_error('tipo_mensualidad', 'Debe Seleccionar una Mensualidad.')
                     elif tipo_mensualidad_seleccionada:
                           if monto is None:
                                  self.add_error('monto', 'Este campo es obligatorio al seleccionar una nueva mensualidad')
                           elif tipo_mensualidad_seleccionada.precio != monto:
                                  self.add_error('monto', 'El monto recibido no coincide con el precio de la mensualidad seleccionada.')
                           
                           if cleaned_data['tipo_mensualidad'].tipo != 'Pase Libre':
                              self.fields['clases_restantes'].required = True
                              if clases_restantes is None and self.fields['clases_restantes'].required:
                                self.add_error('clases_restantes', 'Este campo es obligatorio cuando la mensualidad no es Pase Libre.')
                           else:
                                 self.fields['clases_restantes'].required = False

            except Socio.DoesNotExist:
                 self.add_error('socio', 'Socio no encontrado')
        return cleaned_data

    
class SeleccionarFechaRenovacionForm(forms.Form):
    fecha_renovacion = forms.DateField(widget=DateInput(attrs={'type': 'date', 'min': str(date.today())}))


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'cantidad', 'gimnasio', 'precio']


class VentaForm(forms.ModelForm):
    total = forms.DecimalField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': True, 'id': 'id_total'}),
        initial=0
    )
    
    efectivo = forms.DecimalField(required=False, initial=0)
    transferencia = forms.DecimalField(required=False, initial=0)
    tarjeta_credito = forms.DecimalField(required=False, initial=0)

    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'efectivo', 'transferencia', 'tarjeta_credito']

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = self.producto_label_from_instance

    def producto_label_from_instance(self, obj):
       return f"{obj.descripcion} - ${obj.precio}"
    
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        efectivo = cleaned_data.get('efectivo') or 0
        transferencia = cleaned_data.get('transferencia') or 0
        tarjeta_credito = cleaned_data.get('tarjeta_credito') or 0
        total = self.data.get('total')
        
        if producto and cantidad:
            if cantidad > producto.cantidad:
                raise ValidationError(
                     f'No hay suficiente stock para este producto. Hay {producto.cantidad} disponibles.'
                )
        
        if total is not None:
          total = float(total)
          suma_pagos = float(efectivo) + float(transferencia) + float(tarjeta_credito)
          if suma_pagos != total:
            raise ValidationError("La suma de los pagos debe ser igual al total.")
           
        return cleaned_data

class ExtrasForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, widget=forms.RadioSelect, label='Tipo')
    fecha = forms.DateField(widget=forms.HiddenInput(), initial=timezone.now().date())
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        required=False,  # Puede que no siempre se asocie a un producto
        empty_label="--- Seleccionar Producto (Opcional) ---", #opcional un producto
        label="Producto (Opcional)"
    )

    class Meta:
        model = extras
        fields = ['descripcion', 'monto', 'gimnasio', 'tipo', 'producto']
        # eliminamos el widgets de fecha

    def clean(self):
        cleaned_data = super().clean()
        # Asignamos la fecha inicial si aún no está en el cleaned_data (en caso de que ya tenga un valor predefinido)
        if 'fecha' not in cleaned_data:
            cleaned_data['fecha'] = self.fields['fecha'].initial
        return cleaned_data
    


##historial de ingrso 
class HistorialIngresosForm(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha Inicio',
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today(),
        required = False,
    )
    fecha_fin = forms.DateField(
        label='Fecha Fin',
        widget=forms.DateInput(attrs={'type': 'date'}),
          initial=date.today(),
        required = False,
    )

## SELECCIONAR GYM DENTRO DEL DIARIO

class SeleccionGimnasioForm(forms.Form):
    gimnasio = forms.ModelChoiceField(queryset=Gimnasio.objects.all(), label="Seleccionar Gimnasio")