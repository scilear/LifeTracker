<template>
  <div class="card">
    <div class="row" style="justify-content: space-between;">
      <div>
        <div style="font-size: 18px; font-weight: 650;">Habits</div>
        <small>Clean history, clear intent.</small>
      </div>
      <button class="btn" @click="load">Refresh</button>
    </div>

    <div style="height: 14px"></div>

    <div class="grid">
      <div v-for="h in habits" :key="h.id" class="card" style="background: rgba(255,255,255,0.04)">
        <div class="row" style="justify-content: space-between; align-items: baseline;">
          <RouterLink :to="`/habits/${h.id}`" style="font-weight: 650;">
            {{ h.name }}
          </RouterLink>
          <small>{{ scheduleLabel(h) }}</small>
        </div>

        <div v-if="h.description" style="margin-top: 8px; color: var(--muted);">
          {{ h.description }}
        </div>

        <div class="row" style="margin-top: 10px;">
          <span v-for="t in h.tags" :key="t" class="tag">{{ t }}</span>
        </div>

        <div class="row" style="justify-content: flex-end; margin-top: 12px;">
          <RouterLink class="btn" :to="`/habits/${h.id}/edit`">Edit</RouterLink>
        </div>
      </div>

      <div v-if="habits.length === 0" class="card" style="background: rgba(255,255,255,0.04)">
        <small>No habits yet. Create one to start tracking.</small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { listHabits } from '../api/habits'

const habits = ref([])

function scheduleLabel(h) {
  if (h.schedule_type === 'daily') return `Daily · ${h.time_of_day}`
  if (h.schedule_type === 'weekly') return `Weekly · ${h.time_of_day}`
  if (h.schedule_type === 'monthly') return `Monthly · ${h.time_of_day}`
  return `${h.schedule_type} · ${h.time_of_day}`
}

async function load() {
  habits.value = await listHabits()
}

onMounted(load)
</script>
