# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Affiliate, OperationsManager
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.html import format_html


# #####################################################################################
# PAINEL ADMIN - MODELOS DE USUÁRIOS
# #####################################################################################
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('profile_image_tag', 'username', 'email', 'is_staff', 'is_superuser')
    readonly_fields = ('profile_image_tag',)
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {
            'fields': ('image_profile', 'profile_image_tag', 'first_name', 'last_name', 'email', 'is_active')
        }),
        ('Grupos', {
            'fields': ('groups',),
        }),
        ('Permissões', {
            'fields': ('is_staff', 'is_superuser', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'groups', 'is_staff', 'is_superuser'),
        }),
    )

    @admin.display(description="Criado em")
    def formatted_dtt_record(self, obj):
        return obj.dtt_record.strftime('%d/%m/%Y %H:%M')

    def profile_image_tag(self, obj):
        if obj.image_profile:
            return format_html('<img src="{}" style="width: 50px; height:50px;" />', obj.image_profile.url)
        return "-"
    profile_image_tag.short_description = 'Preview'


# #####################################################################################
# PAINEL ADMIN - MODELOS DE USUÁRIOS OPERADORES
# #####################################################################################
@admin.register(OperationsManager)
class OperationsManagerAdmin(admin.ModelAdmin):
    @admin.display(description="Criado em")
    def formatted_dtt_record(self, obj):
        return obj.dtt_record.strftime('%d/%m/%Y %H:%M')
    
    list_display = (
        'id','username', 'cpf_cnpj', 'gender', 'marital_status',
        'phone', 'city_name', 'state_abbr', 'stt_record', 'formatted_dtt_record'
    )
    list_filter = ('gender', 'marital_status','city_name', 'state_abbr', 'stt_record', 'dtt_record')
    search_fields = ('username', 'cpf_cnpj', 'phone')
    readonly_fields = ('dtt_record', 'dtt_update')


    autocomplete_fields = ['city_lookup']     # Campos para buscar na Location (opcional, usando raw_id_fields ou autocomplete_fields)

    # Campos a serem exibidos no formulário de edição separados em grupos (fieldsets)
    fieldsets = (
        ('User Info',           {'fields': ('user', 'cpf_cnpj', 'gender', 'birth_date', 'marital_status')}),
        ('Identity Document',   {'fields': ('id_document_number', 'id_document_issuer')}),
        ('Address',             {'fields': ('cep', 'city_lookup', 'address', 'number', 'complement', 'district')}),
        ('Contact',             {'fields': ('phone',)}),
        ('Other',               {'fields': ('comment', 'user_permission_type', 'stt_record')}),
        ('Timestamps',          {'fields': ('dtt_record', 'dtt_update')}),
    )
    ordering = ('-dtt_record',)

    # Filtro que exibe no campo o nome da cidade e estado em campo select 
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['city_lookup'].help_text = 'Busque a cidade — estado será salvo automaticamente'
        return form

    def save_model(self, request, obj, form, change):
        if obj.city_lookup:
            obj.city_name = obj.city_lookup.name
            obj.state_abbr = obj.city_lookup.state.uf
        else:
            obj.city_name = ''
            obj.state_abbr = ''
        if obj.user:
            obj.username = obj.user.username   
        super().save_model(request, obj, form, change)

        # Vincula o usuário ao grupo Operador se não estiver
        if obj.user:
            operator_group, _ = Group.objects.get_or_create(name='Operador')
            if not obj.user.groups.filter(name='Operador').exists():
                obj.user.groups.add(operator_group)    


# #####################################################################################
# PAINEL ADMIN - MODELOS DE USUÁRIOS AFILIADOS
# #####################################################################################
@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    # grid de exibição
    list_display = (
        'original_indicator', 'get_username', 'person_type', 'cpf_cnpj', 'plan', 
        'city_name', 
        'get_previous_career_name', 'get_current_career_name',
        'is_root', 'is_in_network', 'accept_lgpd',
        'formatted_dtt_record', 'formatted_dtt_update', 'stt_record'
    )
    list_filter = ('person_type', 'is_root', 'stt_record', 'is_in_network')
    search_fields = ('user__username', 'cpf_cnpj', 'phone')

    # Campos para buscar na Location (opcional, usando raw_id_fields ou autocomplete_fields)
    autocomplete_fields = ['city_lookup']

     # Campos a serem exibidos no formulário de edição separados em grupos (fieldsets)
    fieldsets = (
            ('Rede',                         {'fields': ('user', 'original_indicator', 'is_root', 'is_in_network')}), 
            ('Informações de Usuário',       {'fields': ('stt_record', 'person_type', 'cpf_cnpj')}),
            ('Plano e Carreira',             {'fields': ('plan', 'previous_career', 'current_career', 'dtt_previous_career', 'dtt_current_career')}),
            ('Contato e Endereço',           {'fields': ('phone', 'cep', 'city_lookup', 'address', 'number', 'complement', 'district')}),
            ('Outros',                       {'fields': ('comment','accept_lgpd')}),
        )

    # GRID: NOMES PERSONALIZADOS PARA GRID
    @admin.display(description="Cadastro")
    def formatted_dtt_record(self, obj):
        return obj.dtt_record.strftime('%d/%m/%Y %H:%M')
    
    @admin.display(description="Update")
    def formatted_dtt_update(self, obj):
        return obj.dtt_update.strftime('%d/%m/%Y %H:%M')   

    # Para exibir o username do User relacionado
    @admin.display(description='Usuário')
    def get_username(self, obj):
        return obj.user.username
    
    @admin.display(description='Cidade')
    def city_name(self, obj):
        return obj.city_lookup.name if obj.city_lookup else "-"
    
    @admin.display(description='Indicador')
    def original_indicator(self, obj):
        return obj.original_indicator.name
    
    @admin.display(description='Carreira Anterior')
    def get_previous_career_name(self, obj):
        return obj.previous_career.stage_name if obj.previous_career else "-"

    @admin.display(description='Carreira Atual')
    def get_current_career_name(self, obj):
        return obj.current_career.stage_name if obj.current_career else "-"
    
    @admin.display(description='É raiz?')
    def is_root(self, obj):
        return obj.is_root.capitalize()

    # Filtro que exibe no campo o nome da cidade e estado em campo select 
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['city_lookup'].help_text = 'Busque a cidade — estado será salvo automaticamente'
        return form
        
    # PERSISTENCIA
    def save_model(self, request, obj, form, change):
        # Preencher nome da cidade e sigla do estado
        if obj.city_lookup:
            obj.city_name = obj.city_lookup.name
            obj.state_abbr = obj.city_lookup.state.uf
        else:
            obj.city_name = ''
            obj.state_abbr = ''

        # Regra: não pode ter carreira atual sem carreira anterior
        if obj.current_career and not obj.previous_career:
            raise ValidationError("Não é permitido definir uma carreira atual sem definir uma carreira anterior.")

        super().save_model(request, obj, form, change)

        # Vincula o usuário ao grupo Afiliado se não estiver
        if obj.user:
            afiliado_group, _ = Group.objects.get_or_create(name='Afiliado')
            if not obj.user.groups.filter(name='Afiliado').exists():
                obj.user.groups.add(afiliado_group)
    
    
    


