# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from core.choices import *
from location.models import City, State
from plans.models import PlanCareer 
from collections import deque
from django.utils import timezone


#################################################################################################
# Tabela de Usuários dados padrões login, pass, email, etc
#################################################################################################
class User(AbstractUser):
    is_operator = models.BooleanField(default=False, verbose_name="É Operador ?")
    is_affiliate = models.BooleanField(default=False, verbose_name="É Afiliado ?")
    image_profile = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name="Foto de Perfil"
    )

    class Meta:
        db_table = 'tb_User'
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
    def __str__(self):
        return self.username



# #################################################################################################
# Tabela Detalhes de Usuarios do tipo Operador: endereço, telefone, etc
# #################################################################################################
class OperationsManager(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="Operador")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Login desse Operador")
    cpf_cnpj = models.CharField(max_length=20, unique=True, verbose_name="CPF/CNPJ")
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], verbose_name="Sexo")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    marital_status = models.CharField(max_length=20, choices=[('single', 'Solteiro(a)'), ('married', 'Casado(a)'), ('divorced', 'Divorciado(a)')], verbose_name="Estado Civil")
    id_document_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número do Documento de Identidade")
    id_document_issuer = models.CharField(max_length=20, blank=True, null=True, verbose_name="Órgão Emissor do Documento")
    
    city_lookup = models.ForeignKey('location.City', on_delete=models.SET_NULL, null=True, blank=True)
    city_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    state_abbr = models.CharField(max_length=2, blank=True, null=True, verbose_name="UF")
    
    cep = models.CharField(max_length=8, blank=True, null=True, verbose_name="CEP")
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name="Endereço")
    number = models.CharField(max_length=8, blank=True, null=True, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    district = models.CharField(max_length=300, blank=True, null=True, verbose_name="Bairro")
    phone = models.CharField(max_length=14, blank=True, null=True, verbose_name="Telefone")
    comment = models.TextField(blank=True, null=True, verbose_name="Comentário")
    user_permission_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Permissão do Usuário")
    stt_record = models.BooleanField(default=True, verbose_name="Ativo")
    dtt_record = models.DateTimeField(auto_now_add=True, verbose_name="Data Cadastro")
    dtt_update = models.DateTimeField(auto_now=True, verbose_name="Data Atualização")

    class Meta:
        db_table = 'tb_OperationsManager'
        verbose_name = "Gerente de Operação"
        verbose_name_plural = "Gerente de Operações"

    def __str__(self):
        return self.username



# #################################################################################################
# Tabela de Detalhes de Usuarios do tipo Afiliado: endereço, plano, carreira, etc
#################################################################################################
class Affiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Login desse Afiliado")

    original_indicator = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, 
        blank=True, related_name='referrals', verbose_name="Indicador")
    
    person_type = models.CharField(
        max_length=2,
        choices=[('pf', 'PF'), ('pj', 'PJ')] # TO DO: levar pro dicionario de choices.py depois
    , verbose_name="Pessoa")

    cpf_cnpj = models.CharField(max_length=20, unique=True, verbose_name="CPF/CNPJ")
    cep = models.CharField(max_length=8, blank=True, null=True, verbose_name="CEP")
    
    city_lookup = models.ForeignKey('location.City', on_delete=models.SET_NULL, null=True, blank=True)
    city_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    state_abbr = models.CharField(max_length=2, blank=True, null=True , verbose_name="UF")
        
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name="Endereço")
    number = models.CharField(max_length=8, blank=True, null=True, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    district = models.CharField(max_length=300, blank=True, null=True, verbose_name="Bairro")
    phone = models.CharField(max_length=14, blank=True, null=True, verbose_name="Telefone")

    plan = models.ForeignKey('plans.Plan', on_delete=models.PROTECT, verbose_name="Plano de Adesão")

     # FK - Conecta com PlanCareer
    previous_career = models.ForeignKey(
        'plans.PlanCareer',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='previous_affiliates',
        verbose_name="Carreira Anterior")

    current_career = models.ForeignKey(
        'plans.PlanCareer',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='current_affiliates',
        verbose_name="Carreira Atual")

    dtt_previous_career = models.DateTimeField(blank=True, null=True, verbose_name="Data Carreira Anterior")
    dtt_current_career = models.DateTimeField(blank=True, null=True, verbose_name="Data Carreira Atual")

    is_root = models.BooleanField(default=False, verbose_name="É Raiz na Rede ? ")
    stt_record = models.BooleanField(default=True, verbose_name="Ativo")
    is_in_network = models.BooleanField(default=True, verbose_name="Está na Rede ?")
    accept_lgpd = models.BooleanField(default=False, verbose_name="Aceita LGPD")
    comment = models.TextField(blank=True, null=True, verbose_name="Comentário")
    dtt_payment_received = models.DateTimeField(blank=True, null=True, verbose_name="Data Recebimento Pagamento")

    dtt_record = models.DateTimeField(auto_now_add=True, verbose_name="Data Cadastro")
    dtt_update = models.DateTimeField(auto_now=True, verbose_name="Data Atualização")
 
    class Meta:
        db_table = 'tb_Affiliate'
        verbose_name = "Afiliado"
        verbose_name_plural = "Afiliados"

    def __str__(self):
        return f'{self.user.username} ({self.cpf_cnpj})'

    # #################################################################################################
    # Métodos para verificar e atualizar plano de carreira do afiliado 
    # #################################################################################################
    def verificar_plano_de_carreira(self):
        print(f"\nAFILIADO: {self.user.username} ###########")

        planos = PlanCareer.objects.filter(stt_record=True).order_by('required_points')
        carreira_atual = self.current_career.required_points if self.current_career else 0

        for plano in planos:
            if carreira_atual >= plano.required_points:
                continue

            diretos = list(self.get_indicados_diretos_efetivados())
            qtd_diretos = len(diretos)
            if qtd_diretos < plano.required_directs:
                faltam = plano.required_directs - qtd_diretos
                print(f"Faltam {faltam} diretos para estágio {plano.stage_name}")
                break

            vendas_diretas = sum(1 for d in diretos if d.comprou_usina())
            if vendas_diretas < plano.required_direct_sales:
                faltam = plano.required_direct_sales - vendas_diretas
                print(f"Faltam {faltam} vendas diretas para estágio {plano.stage_name}")
                break

            pontos_equipe = 0
            fila = deque([(d, 1) for d in diretos])
            while fila:
                dist, nivel = fila.popleft()
                total = dist.get_total_pontos_acumulados_consolidados()
                pontos_equipe += min(total, plano.max_pml_per_line)
                if nivel < 5:
                    for net in dist.get_indicados_diretos_efetivados():
                        fila.append((net, nivel + 1))

            print(f"Pontos de equipe (PML={plano.max_pml_per_line}): {pontos_equipe}")
            if pontos_equipe < plano.required_points:
                faltam = plano.required_points - pontos_equipe
                print(f"Faltam {faltam} pontos para estágio {plano.stage_name}")
                break

            print(f"Parabéns! Qualificado para {plano.stage_name} — Prêmio: {plano.reward_description}")

            self.previous_career = self.current_career
            self.current_career = plano
            self.dtt_previous_career = self.dtt_current_career
            self.dtt_current_career = timezone.now()
            self.save(update_fields=['previous_career', 'current_career', 'dtt_previous_career', 'dtt_current_career'])
            break




