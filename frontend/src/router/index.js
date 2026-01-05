import { createRouter, createWebHistory } from 'vue-router'

import HabitsView from '../views/HabitsView.vue'
import HabitEditView from '../views/HabitEditView.vue'
import HabitDetailView from '../views/HabitDetailView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  { path: '/', name: 'habits', component: HabitsView },
  { path: '/habits/new', name: 'habit-new', component: HabitEditView },
  { path: '/habits/:id', name: 'habit-detail', component: HabitDetailView, props: true },
  { path: '/habits/:id/edit', name: 'habit-edit', component: HabitEditView, props: true },
  { path: '/settings', name: 'settings', component: SettingsView }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
