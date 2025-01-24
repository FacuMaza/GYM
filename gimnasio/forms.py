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



class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['tipo_usuario', 'usuario', 'contrasena'] # Asegúrate que 'usuario' y 'contrasena' estén incluidos
        widgets = {
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
             'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


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


class AsignarMensualidadForm(forms.Form):
    socio = forms.ModelChoiceField(queryset=Socio.objects.all(), label="Socio", widget=forms.TextInput(attrs={'readonly':'readonly'}))
    tipo_mensualidad_display = forms.CharField(label="Tipo de Mensualidad Actual", required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    tipo_mensualidad = forms.ModelChoiceField(queryset=TipoMensualidad.objects.all(), label="Seleccionar Nueva Mensualidad", required=False, widget=forms.HiddenInput())
    metodo_pago = forms.ChoiceField(choices=[
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta_credito', 'Tarjeta de Crédito')
    ], label="Método de Pago")
    monto = forms.FloatField(label="Monto Recibido")

    def clean(self):
        cleaned_data = super().clean()
        tipo_mensualidad = cleaned_data.get('tipo_mensualidad')
        
        if tipo_mensualidad:
           
          return cleaned_data
        else:
          # Si no hay una nueva mensualidad seleccionada, usa la existente del socio
            socio = cleaned_data.get('socio')
            if socio and socio.tipo_mensualidad:
              cleaned_data['tipo_mensualidad'] = socio.tipo_mensualidad
              return cleaned_data
            else:
              self.add_error('tipo_mensualidad', 'Debe Seleccionar una Mensualidad.')
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
        widget=forms.TextInput(attrs={'readonly': True}),
        initial=0
    ) 
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

        if producto and cantidad:
            if cantidad > producto.cantidad:
                 raise ValidationError(
                     f'No hay suficiente stock para este producto. Hay {producto.cantidad} disponibles.'
                 )

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
    



## SELECCIONAR GYM DENTRO DEL DIARIO

class SeleccionGimnasioForm(forms.Form):
    gimnasio = forms.ModelChoiceField(queryset=Gimnasio.objects.all(), label="Seleccionar Gimnasio")