<template>
  <div class="card">
    <div class="row" style="justify-content: space-between;">
      <div>
        <div style="font-size: 18px; font-weight: 650;">{{ isEdit ? 'Edit habit' : 'New habit' }}</div>
        <small>Define schedule, tags, and time.</small>
      </div>
      <RouterLink class="btn" to="/">Back</RouterLink>
    </div>

    <div style="height: 14px"></div>

    <div class="card" style="background: rgba(255,255,255,0.04)">
      <div class="field">
        <label>Name</label>
        <input v-model="form.name" placeholder="e.g., Journal" />
      </div>

      <div class="field">
        <label>Description</label>
        <textarea v-model="form.description" rows="2" placeholder="Optional" />
      </div>

      <div class="field">
        <label>Tags (comma-separated)</label>
        <input v-model="tagsText" placeholder="health, work" />
      </div>

      <div class="row">
        <div class="field" style="flex: 1; min-width: 220px;">
          <label>Schedule</label>
          <select v-model="form.schedule_type">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly (select weekdays)</option>
            <option value="monthly">Monthly (day of month)</option>
          </select>
        </div>

        <div class="field" style="flex: 1; min-width: 220px;">
          <label>Time</label>
          <input v-model="form.time_of_day" placeholder="HH:MM" />
        </div>
      </div>

      <div v-if="form.schedule_type === 'weekly'" class="field">
        <label>Weekdays</label>
        <div class="row">
          <label v-for="(d, idx) in weekdays" :key="idx" class="pill" style="cursor: pointer;">
            <input type="checkbox" :value="idx" v-model="form.days_of_week" />
            <span>{{ d }}</span>
          </label>
        </div>
      </div>

      <div v-if="form.schedule_type === 'monthly'" class="field">
        <label>Day of month</label>
        <input type="number" min="1" max="31" v-model.number="form.day_of_month" />
      </div>

      <div class="row" style="justify-content: flex-end;">
        <button class="btn primary" :disabled="saving" @click="save">Save</button>
      </div>

      <div v-if="error" style="margin-top: 10px; color: var(--bad);">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createHabit, getHabit, updateHabit } from '../api/habits'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => Boolean(route.params.id))
const saving = ref(false)
const error = ref('')

const weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const form = reactive({
  name: '',
  description: '',
  tags: [],
  schedule_type: 'daily',
  time_of_day: '20:00',
  days_of_week: [],
  day_of_month: null,
  is_active: true
})

const tagsText = ref('')

function syncTagsFromText() {
  const tags = tagsText.value
    .split(',')
    .map(s => s.trim())
    .filter(Boolean)
  form.tags = tags
}

async function load() {
  if (!isEdit.value) return
  const h = await getHabit(route.params.id)
  form.name = h.name
  form.description = h.description || ''
  form.tags = h.tags || []
  tagsText.value = (h.tags || []).join(', ')
  form.schedule_type = h.schedule_type
  form.time_of_day = h.time_of_day
  form.days_of_week = h.days_of_week || []
  form.day_of_month = h.day_of_month
  form.is_active = h.is_active
}

async function save() {
  saving.value = true
  error.value = ''
  try {
    syncTagsFromText()

    const payload = {
      name: form.name,
      description: form.description || null,
      tags: form.tags,
      schedule_type: form.schedule_type,
      time_of_day: form.time_of_day,
      days_of_week: form.schedule_type === 'weekly' ? form.days_of_week : null,
      day_of_month: form.schedule_type === 'monthly' ? form.day_of_month : null,
      is_active: true
    }

    if (isEdit.value) {
      await updateHabit(route.params.id, payload)
    } else {
      await createHabit(payload)
    }

    router.push('/')
  } catch (e) {
    error.value = String(e.message || e)
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
