<template>
  <div class="card">
    <div class="row" style="justify-content: space-between;">
      <div>
        <div style="font-size: 18px; font-weight: 650;">Settings</div>
        <small>Notifications are optional but helpful.</small>
      </div>
      <RouterLink class="btn" to="/">Back</RouterLink>
    </div>

    <div style="height: 14px"></div>

    <div class="card" style="background: rgba(255,255,255,0.04)">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div style="font-weight: 650;">Browser notifications</div>
          <small>Status: {{ statusLabel }}</small>
        </div>
        <button class="btn primary" @click="enable" :disabled="!canRequest">
          Enable notifications
        </button>
      </div>
      <div style="margin-top: 10px;">
        <small>
          Notifications work while this app is open and permission is granted.
        </small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const permission = ref(typeof Notification !== 'undefined' ? Notification.permission : 'unsupported')

const canRequest = computed(() => permission.value !== 'unsupported')

const statusLabel = computed(() => {
  if (permission.value === 'unsupported') return 'Not supported in this browser.'
  if (permission.value === 'granted') return 'Enabled'
  if (permission.value === 'denied') return 'Blocked'
  return 'Not enabled'
})

async function enable() {
  if (typeof Notification === 'undefined') return
  const res = await Notification.requestPermission()
  permission.value = res
}
</script>
