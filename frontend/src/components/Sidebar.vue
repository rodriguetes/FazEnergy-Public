<template>
  <aside
    :class="[
      mini ? 'w-16' : 'w-52',
      'text-white flex flex-col justify-between bg-blue-600 h-full text-sm transition-all duration-300'
    ]"
  >
    <div>
      <!-- Logo -->
      <div class="flex items-center gap-2 p-[0.7rem] text-xl font-bold bg-[#1d4ed8]" :class="mini ? 'justify-center' : ''">
        <!-- Ícone do logo -->
      <Zap to="/dashboard" :class="['bg-white text-blue-600 flex items-center p-1 rounded-md w-6 h-6 hover:bg-white hover:text-blue-300', mini ? 'justify-center' : 'gap-2']"/>
        <span v-if="!mini">FazEnergy</span>
      </div>

      <nav class="px-2 space-y-5">
        <!-- Menu Principal -->
        <div class="mt-3">
          <h3 v-if="!mini" class="uppercase text-[10px] text-blue-200 mb-2 tracking-wider">Menu Principal</h3>
          <ul class="space-y-1">
            <li>
              <router-link
                to="/dashboard"
               :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']"
                active-class="bg-blue-800"
                title="Dashboard">
                <LayoutDashboard class="w-4 h-4" />
                <span v-if="!mini">Dashboard</span>
              </router-link>
            </li>
            <li>
              <router-link
                to="/preRegister"
                :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']"
                active-class="bg-blue-800"
                title="Cadastrar Afiliado"
              >
                <UserPlus class="w-4 h-4" />
                <span v-if="!mini">Cadastrar Afiliado</span>
              </router-link>
            </li>
            <li>
              <router-link
                to="/reports"
                :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']"
                active-class="bg-blue-800"
                title="Relatório Geral"
              >
                <FileText class="w-4 h-4" />
                <span v-if="!mini">Relatórios</span>
              </router-link>
            </li>
            <li v-if="isSuperUser">
              <router-link
                to="/settings"
                :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']"
                active-class="bg-blue-800"
                title="Configurações"
              >
                <Settings class="w-4 h-4" />
                <span v-if="!mini">Configurações</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Gerenciar Usuários -->
        <div>
          <h3 v-if="!mini" class="uppercase text-[10px] text-blue-200 mb-2 tracking-wider">Gerenciar Usuários</h3>
          <ul class="space-y-1">
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Usuários">
              <Users class="w-4 h-4" title="Usuários"/><span v-if="!mini">Usuários</span></a></li>
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Perfis">
              <User class="w-4 h-4" /><span v-if="!mini">Perfis</span></a></li>
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Grupos">
              <Link class="w-4 h-4" /><span v-if="!mini">Grupos</span></a></li>
          </ul>
        </div>

        <!-- Rede -->
        <div>
          <h3 v-if="!mini" class="uppercase text-[10px] text-blue-200 mb-2 tracking-wider">Rede</h3>
          <ul class="space-y-1">
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Diretos">
              <ArrowRight class="w-4 h-4" /><span v-if="!mini">Diretos</span></a></li>
            <li><a href="#" :class="['flex items-center p-4 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Equipe">
              <Users class="w-4 h-4" /><span v-if="!mini">Equipe</span></a></li>
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Árvore da Rede">
              <TreePine class="w-4 h-4" /><span v-if="!mini">Árvore da Rede</span></a></li>
          </ul>
        </div>

        <!-- Geral -->
        <div>
          <h3 v-if="!mini" class="uppercase text-[10px] text-blue-200 mb-2 tracking-wider">Geral</h3>
          <ul class="space-y-1">
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Materiais">
              <Book class="w-4 h-4" /><span v-if="!mini">Materiais</span></a></li>
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Suporte">
              <LifeBuoy class="w-4 h-4" /><span v-if="!mini">Suporte</span></a></li>
            <li><a href="#" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Plano de Carreira">
              <BarChart class="w-4 h-4" /><span v-if="!mini">Plano de Carreira</span></a></li>
            <li>
              <router-link to="/profile" :class="['flex items-center p-2 rounded hover:bg-blue-800', mini ? 'justify-center' : 'gap-2']" title="Meu Perfil">
                <UserCircle class="w-4 h-4" />
                <span v-if="!mini">Meu Perfil</span>
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
    </div>

    <!-- Rodapé -->
    <div class="p-4 border-t border-blue-700 text-[10px] text-blue-200 bg-[#1d4ed8] leading-tight">
      <div v-if="!mini">
        Versão: 18.1.5<br />
        <hr class="my-2 border-blue-500" />
        Copyright© 2025 - FazEnergy
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  mini: {
    type: Boolean,
    default: false
  }
})

import {
  Zap, LayoutDashboard, FileText, Settings, Users, User, Link,
  ArrowRight, TreePine, Book, LifeBuoy, BarChart, UserCircle, UserPlus
} from 'lucide-vue-next'

import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const isSuperUser = computed(() => auth.user?.is_superuser === true)
</script>
