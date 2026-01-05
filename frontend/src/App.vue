<template>
  <div class="container">
    <div class="nav">
      <div class="row" style="gap: 12px;">
        <div class="pill">
          <span class="brand">LifeTracker</span>
          <small>habits, gently enforced</small>
        </div>
      </div>
      <div class="row">
        <RouterLink class="btn" to="/">Habits</RouterLink>
        <RouterLink class="btn" to="/settings">Settings</RouterLink>
        <RouterLink class="btn primary" to="/habits/new">+ New</RouterLink>
      </div>
    </div>

    <RouterView @refresh-due="refreshDue" />

    <DuePrompt
      v-if="duePromptOpen"
      :item="currentDue"
      @close="duePromptOpen = false"
      @recorded="onRecorded"
    />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { getDue, upsertRecord } from './api/habits'
import DuePrompt from './components/DuePrompt.vue'

const dueItems = ref([])
const duePromptOpen = ref(false)
const currentIndex = ref(0)

const currentDue = computed(() => dueItems.value[currentIndex.value] || null)

async function refreshDue() {
  try {
    const items = await getDue(60)
    dueItems.value = items

    if (items.length > 0) {
      currentIndex.value = 0
      duePromptOpen.value = true

      if (Notification && Notification.permission === 'granted') {
        const first = items[0]
        new Notification(`Due: ${first.habit.name}`, {
          body: `Record now (${new Date(first.due_at).toLocaleString()})`
        })
      }
    }
  } catch (e) {
    // silent in UI; dev console is enough for MVP
    console.error(e)
  }
}

async function onRecorded({ habitId, payload }) {
  await upsertRecord(habitId, payload)
  await refreshDue()
}

let timer = null
onMounted(async () => {
  await refreshDue()
  timer = setInterval(refreshDue, 60_000)
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>
