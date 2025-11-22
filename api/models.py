from django.db import models
from django.contrib.auth.models import User

import random
class UserProfile(models.Model):
	django_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	user_id = models.BigIntegerField(unique=True, editable=False, blank=True, null=True)
	ref = models.CharField(max_length=155, blank=True, null=True)
	click_id = models.CharField(max_length=255, blank=True, null=True, help_text="ClickID Chatterfy")
	email = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=255)
	deposit = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
	country = models.CharField(max_length=255, blank=True, null=True)
	nombre = models.CharField(max_length=100, blank=True, null=True)
	apellido = models.CharField(max_length=100, blank=True, null=True)
	cumpleanos = models.DateField(blank=True, null=True)
	sexo = models.CharField(max_length=10, choices=[('masculino', 'masculino'), ('femenino', 'femenino')], blank=True, null=True)
	ciudad = models.CharField(max_length=255, blank=True, null=True)
	direccion = models.CharField(max_length=255, blank=True, null=True)
	numero_de_telefono = models.CharField(max_length=20, blank=True, null=True)
	bonificaciones = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	registration_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=[('active', 'active'), ('banned', 'banned')], default='active')
	positions_mine = models.CharField(max_length=255, blank=True, null=True)
	col_deposit = models.CharField(max_length=25, default='0')
	user_status = models.CharField(max_length=25, default='Not activated')
	stage = models.CharField(max_length=10, choices=[('normal', 'normal'), ('verif', 'verif'), ('verif2', 'verif2'), ('supp', 'supp'), ('meet', 'meet')], default='normal')
	stage_balance = models.DecimalField(max_digits=19, decimal_places=2, default=120.00)
	verification_start_date = models.DateTimeField(blank=True, null=True)
	chicken_trap_coefficient = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	first_bonus_used = models.BooleanField(default=False, help_text="Indica si el usuario ya utilizó su primer bono")
	email_verified = models.BooleanField(default=False, help_text="Indica si el email del usuario está verificado")
	email_verification_token = models.CharField(max_length=255, blank=True, null=True, help_text="Token para verificación de email")


	def save(self, *args, **kwargs):
		if not self.user_id:
			# Generate sequential user_id starting from 17958522
			# Get the maximum user_id and add 1
			max_user = UserProfile.objects.aggregate(models.Max('user_id'))
			max_id = max_user['user_id__max']
			
			if max_id is None or max_id < 17958522:
				# If no users exist or max_id is less than starting value, start from 17958522
				self.user_id = 17958522
			else:
				# Otherwise, increment by 1
				self.user_id = max_id + 1
		super().save(*args, **kwargs)

	def __str__(self):
		return self.email


class Country(models.Model):
	name = models.CharField(max_length=100, unique=True)
	currency = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.name} ({self.currency})"



class PaymentMethod(models.Model):
	alt = models.CharField(max_length=50, blank=True, null=True)
	src = models.ImageField(upload_to='payment_methods/', blank=True, null=True)
	label = models.CharField(max_length=100)
	numero_de_cuenta = models.CharField(max_length=100, blank=True, null=True)
	nombre = models.CharField(max_length=100, blank=True, null=True)
	banco = models.CharField(max_length=100, blank=True, null=True)
	ci = models.CharField(max_length=50, blank=True, null=True)
	cryptoId = models.CharField(max_length=50, blank=True, null=True)
	cuit = models.CharField(max_length=50, blank=True, null=True)
	cbu = models.CharField(max_length=50, blank=True, null=True)
	nro = models.CharField(max_length=50, blank=True, null=True)
	sinpe = models.CharField(max_length=50, blank=True, null=True)
	bac = models.CharField(max_length=50, blank=True, null=True)
	cta = models.CharField(max_length=50, blank=True, null=True)
	cedula = models.CharField(max_length=50, blank=True, null=True)
	IBAN = models.CharField(max_length=50, blank=True, null=True)
	Identificacion = models.CharField(max_length=50, blank=True, null=True)
	Rut = models.CharField(max_length=50, blank=True, null=True)
	qr = models.CharField(max_length=255, blank=True, null=True)
	status = models.CharField(max_length=20, blank=True, null=True)
	is_universal = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.label} ({self.numero_de_cuenta})"


class CountryPaymentMethod(models.Model):
	country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='payment_methods')
	payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='countries')

	def __str__(self):
		return f"{self.country.name} - {self.payment_method.label}"

class Transaction(models.Model):
	user_id = models.CharField(max_length=255)
	transacciones_data = models.DateTimeField()
	transacciones_monto = models.DecimalField(max_digits=15, decimal_places=2)
	estado = models.CharField(max_length=20, default='esperando')
	transaccion_number = models.CharField(max_length=20, blank=True, null=True)
	order_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID заказа от платежной системы")
	metodo_de_pago = models.CharField(max_length=50, blank=True, null=True)
	amount_usd = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
	stage_processed = models.BooleanField(default=False)
	currency = models.CharField(max_length=3, default='USD')
	exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1.0)
	created_at = models.DateTimeField(auto_now_add=True)
	# Поля для Telegram
	file_name = models.CharField(max_length=255, blank=True, null=True, help_text="Имя файла чека")
	chat_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID чата Telegram")
	message_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID сообщения в Telegram")
	processed_by = models.CharField(max_length=255, blank=True, null=True, help_text="Кто обработал платеж")
	processed_at = models.DateTimeField(blank=True, null=True, help_text="Когда был обработан")
	notes = models.TextField(blank=True, null=True, help_text="Заметки по платежу")

	def __str__(self):
		return f"{self.user_id} - {self.transaccion_number}"


class HistorialPagos(models.Model):
	user_id = models.CharField(max_length=255)
	transacciones_data = models.DateTimeField()
	transacciones_monto = models.DecimalField(max_digits=15, decimal_places=2)
	estado = models.CharField(max_length=20, default='esperando', blank=True, null=True)
	transaccion_number = models.CharField(max_length=20, blank=True, null=True)
	metodo_de_pago = models.CharField(max_length=50, blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	cuenta_corriente = models.CharField(max_length=50, blank=True, null=True)
	numero_de_cuenta = models.CharField(max_length=30, blank=True, null=True)
	tipo_de_documento = models.CharField(max_length=30, blank=True, null=True)
	numero_documento = models.CharField(max_length=30, blank=True, null=True)
	banco = models.CharField(max_length=30, blank=True, null=True)

	def __str__(self):
		return f"{self.user_id} - {self.transaccion_number}"


