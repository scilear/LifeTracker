<template>
  <div class="card">
    <div class="row" style="justify-content: space-between;">
      <div>
        <div style="font-size: 18px; font-weight: 650;">{{ habit?.name || 'Habit' }}</div>
        <small>{{ habit ? scheduleLabel(habit) : '' }}</small>
      </div>
      <div class="row">
        <RouterLink class="btn" to="/">Back</RouterLink>
        <RouterLink v-if="habit" class="btn" :to="`/habits/${habit.id}/edit`">Edit</RouterLink>
      </div>
    </div>

    <div style="height: 14px"></div>

    <div class="grid">
      <div class="card" style="background: rgba(255,255,255,0.04)">
        <div style="font-weight: 650;">Tags</div>
        <div class="row" style="margin-top: 10px;">
          <span v-for="t in habit?.tags || []" :key="t" class="tag">{{ t }}</span>
          <small v-if="(habit?.tags || []).length === 0">No tags.</small>
        </div>
      </div>

      <div class="card" style="background: rgba(255,255,255,0.04)">
        <div style="font-weight: 650;">History</div>
        <div style="height: 10px"></div>
        <div v-if="records.length === 0">
          <small>No records yet.</small>
        </div>
        <div v-else style="display: grid; gap: 10px;">
          <div v-for="r in records" :key="r.id" class="card" style="background: rgba(0,0,0,0.12);">
            <div class="row" style="justify-content: space-between;">
              <small>Due {{ new Date(r.due_at).toLocaleString() }}</small>
              <span :style="{ color: r.status === 'done' ? 'var(--good)' : 'var(--bad)' }">
                {{ r.status === 'done' ? 'Done' : 'Not done' }}
              </span>
            </div>
            <div v-if="r.reason" style="margin-top: 8px; color: var(--muted);">Reason: {{ r.reason }}</div>
            <div v-if="r.comment" style="margin-top: 8px; color: var(--muted);">Comment: {{ r.comment }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getHabit, listRecords } from '../api/habits'

const props = defineProps({ id: { type: [String, Number], required: true } })

const habit = ref(null)
const records = ref([])

function scheduleLabel(h) {
  if (h.schedule_type === 'daily') return `Daily · ${h.time_of_day}`
  if (h.schedule_type === 'weekly') return `Weekly · ${h.time_of_day}`
  if (h.schedule_type === 'monthly') return `Monthly · ${h.time_of_day}`
  return `${h.schedule_type} · ${h.time_of_day}`
}

async function load() {
  habit.value = await getHabit(props.id)
  records.value = await listRecords(props.id)
}

onMounted(load)
</script>
