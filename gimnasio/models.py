from django.db import models
from django.utils import timezone
from datetime import date

class TipoMensualidad(models.Model):
    tipo = models.CharField(max_length=255)  # Ejemplo de longitud máxima, ajústala según necesites
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Usando DecimalField para precios
    
    def __str__(self):
        return '%s %s  '%(self.tipo,self.precio)

    class Meta:
        db_table = 'TipoMensualidades'
        verbose_name = 'TipoMensualidad'
        verbose_name_plural = 'TipoMensualidades'


class Gimnasio(models.Model):

    direccion = models.CharField(max_length=255)
    
    def __str__(self):
        return '%s  '%(self.direccion)

    class Meta: 
        db_table = 'Gimnasios'
        verbose_name = 'Gimnasio'
        verbose_name_plural = 'Gimnasios'

class TipoUsuario(models.Model):
    tipousuario = models.CharField(max_length=255)

    def __str__(self):
        return '%s  '%(self.tipousuario)

    class Meta:
        db_table = 'TipoUsuarios'
        verbose_name = 'TipoUsuario'
        verbose_name_plural = 'TipoUsuarios'

class Usuario(models.Model):
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)  # Ej: "admin", "entrenador", "miembro"
    usuario = models.CharField(max_length=255, unique=True) # Nombre de usuario
    contrasena = models.CharField(max_length=255)  # Considera el hash de contraseñas

    def __str__(self):
        return '%s %s  '%(self.tipo_usuario,self.usuario)
    class Meta:
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Socio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Enlace a la tabla de usuarios
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=20)  # Asumiendo que el DNI es una cadena
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, related_name="socios",default=None)
    tipo_mensualidad = models.ForeignKey('TipoMensualidad', on_delete=models.SET_NULL, null=True, blank=True) # Relación con TipoMensualidad
    clases_restantes = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(null=True, blank=True) # Nuevo Campo
    
    def __str__(self):
        return '%s %s %s %s %s  '%(self.usuario,self.nombre,self.apellido,self.dni,self.gimnasio)
    class Meta:
        db_table = 'Socios'
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'

class Cuota(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    tipo_mensualidad = models.ForeignKey(TipoMensualidad, on_delete=models.CASCADE)
    precio = models.FloatField(null=True, blank=True)
    efectivo = models.FloatField(null=True, blank=True)
    fecha_inicio = models.DateField(default=date.today)
    transferencia = models.FloatField(null=True, blank=True)
    tarjeta_credito = models.FloatField(null=True, blank=True)
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, related_name="cuota",default=None)
    
    def __str__(self):
        return '%s %s %s %s %s %s %s '%(self.socio,self.tipo_mensualidad,self.precio,self.efectivo,self.transferencia,self.tarjeta_credito,self.gimnasio)
    class Meta:
        db_table = 'Cuotas'
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'

class Producto(models.Model):
    """Modelo para los productos disponibles para la venta en el gimnasio."""
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField()  # Stock del producto
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, related_name="producto",default=None)
    precio = models.FloatField(null=True, blank=True)
    
    
    def __str__(self):
        return '%s  %s %s  %s'%(self.descripcion,self.cantidad,self.gimnasio,self.precio)
    class Meta:
        db_table = 'Productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Venta(models.Model):
    """Modelo para los registros de ventas."""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    efectivo = models.FloatField(null=True, blank=True)
    transferencia = models.FloatField(null=True, blank=True)
    tarjeta_credito = models.FloatField(null=True, blank=True)
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, related_name="venta",default=None)
    
    def __str__(self):
        return '%s %s %s %s%s %s%s '%(self.producto,self.usuario,self.cantidad,self.gimnasio,self.efectivo,self.transferencia,self.tarjeta_credito)
    class Meta:
        db_table = 'Ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'


class ingresos(models.Model):
    descripcion = models.CharField(max_length=255)
    monto = models.FloatField(null=True, blank=True)
    tipo_ingreso = models.CharField(max_length=20)
    fecha = models.DateField()
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, related_name="ingresos",default=None)

    def __str__(self):
        return '%s%s%s%s%s '%(self.descripcion, self.monto , self.tipo_ingreso , self.fecha,self.gimnasio)
    
    class Meta:
        db_table = 'ingresos'
        verbose_name = 'ingreso'
        verbose_name_plural = 'ingresos'


class egreso(models.Model):
    descripcion = models.CharField(max_length=255)
    monto = models.FloatField(null=True, blank=True)
    tipo_ingreso = models.CharField(max_length=20)
    fecha = models.DateField()
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, related_name="egreso",default=None)

    def __str__(self):
        return '%s %s %s %s%s'%(self.descripcion, self.monto , self.tipo_ingreso , self.fecha,self.gimnasio)
    
    class Meta:
        db_table = 'egresos'
        verbose_name = 'egreso'
        verbose_name_plural = 'egresos'

class extras(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name="extras")  # Cambio aquí
    ingreso = models.ForeignKey(ingresos, on_delete=models.CASCADE, null=True, blank=True)
    egreso = models.ForeignKey(egreso, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    monto = models.FloatField(null=True, blank=True)
    fecha = models.DateField()
    hora = models.DateTimeField(default=timezone.now) # Agrega el campo hora
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, related_name="extras",default=None)

    def __str__(self):
        return '%s %s %s %s %s %s%s%s' % (self.ingreso, self.egreso, self.descripcion, self.monto, self.fecha,self.gimnasio,self.producto,self.hora)

    class Meta:
        db_table = 'extras'
        verbose_name = 'extra'
        verbose_name_plural = 'extras'


class BalanceDiario(models.Model):
    gimnasio = models.ForeignKey('Gimnasio', on_delete=models.CASCADE, related_name='balances')
    fecha = models.DateField(default=date.today)
    total_ingresos = models.FloatField(null=True, blank=True)
    total_egresos = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'Balance de {self.gimnasio.direccion} el {self.fecha}'

    class Meta:
        db_table = 'Balance Diarios'
        verbose_name = 'Balance Diario'
        verbose_name_plural = 'Balance Diarios'


class RegistroIngreso(models.Model):
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    dni_socio = models.CharField(max_length=20)
    clases_restantes_al_ingresar = models.PositiveIntegerField(null=True, blank=True)
    nombre_socio = models.CharField(max_length=100, null=True, blank=True) # Nuevo campo
    apellido_socio = models.CharField(max_length=100, null=True, blank=True) # Nuevo campo

    def __str__(self):
        return f"Ingreso de {self.nombre_socio} {self.apellido_socio} el {self.fecha_ingreso}"

    class Meta:
        db_table = 'Registro Ingresos'
        verbose_name = 'RegistroIngreso'
        verbose_name_plural = 'Registro Ingresos'

