from rest_framework import serializers
from .models import UserProfile, Country, Transaction, HistorialPagos
# Serializer for HistorialPagos
class HistorialPagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPagos
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'currency']

class UserRegisterSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user_id', 'email', 'password', 'country',
            'ref','click_id', 'nombre', 'apellido', 'cumpleanos', 'sexo', 'ciudad', 'direccion', 'numero_de_telefono'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'ref': {'required': False, 'allow_blank': True, 'allow_null': True},
            'click_id': {'required': False, 'allow_blank': True, 'allow_null': True},
            'nombre': {'required': False, 'allow_blank': True, 'allow_null': True},
            'apellido': {'required': False, 'allow_blank': True, 'allow_null': True},
            'cumpleanos': {'required': False, 'allow_null': True},
            'sexo': {'required': False, 'allow_blank': True, 'allow_null': True},
            'ciudad': {'required': False, 'allow_blank': True, 'allow_null': True},
            'direccion': {'required': False, 'allow_blank': True, 'allow_null': True},
            'numero_de_telefono': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def create(self, validated_data):
        # Hash the password before saving
        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



# Serializer for updating user profile (allow all fields except user_id and registration_date)
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user_id', 'registration_date']
        extra_kwargs = {
            'password': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def update(self, instance, validated_data):
        # If password is being updated, hash it
        password = validated_data.get('password', None)
        if password:
            from django.contrib.auth.hashers import make_password
            instance.password = make_password(password)
            validated_data.pop('password')
        return super().update(instance, validated_data)


# Serializer specifically for updating deposit field
class DepositUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['deposit']
    
    def validate_deposit(self, value):
        # Ensure deposit is not negative
        if value < 0:
            raise serializers.ValidationError("Deposit cannot be negative")
        return value


# Serializer for user lookup by user_id (read-only)
class UserLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user_id', 'email', 'deposit', 'country', 'ref', 'click_id',
            'nombre', 'apellido', 'cumpleanos', 'sexo', 'ciudad', 
            'direccion', 'numero_de_telefono', 'bonificaciones', 
            'registration_date', 'status', 'positions_mine', 
            'col_deposit', 'user_status', 'stage', 'stage_balance', 
            'verification_start_date', 'chicken_trap_coefficient', 
            'first_bonus_used'
        ]
        read_only_fields = [
            'user_id', 'email', 'deposit', 'country', 'ref', 'click_id',
            'nombre', 'apellido', 'cumpleanos', 'sexo', 'ciudad', 
            'direccion', 'numero_de_telefono', 'bonificaciones', 
            'registration_date', 'status', 'positions_mine', 
            'col_deposit', 'user_status', 'stage', 'stage_balance', 
            'verification_start_date', 'chicken_trap_coefficient', 
            'first_bonus_used'
        ]
