<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal">
      <div class="row" style="justify-content: space-between; align-items: baseline;">
        <div>
          <div style="font-size: 18px; font-weight: 650;">{{ item.habit.name }}</div>
          <small>
            Due at {{ new Date(item.due_at).toLocaleString() }}
            <span v-if="item.is_overdue" style="color: var(--bad);">(overdue)</span>
          </small>
        </div>
        <button class="btn" @click="$emit('close')">Close</button>
      </div>

      <div style="height: 12px"></div>

      <div class="row">
        <button class="btn good" @click="setStatus('done')">Done</button>
        <button class="btn bad" @click="setStatus('not_done')">Not done</button>
      </div>

      <div style="height: 12px"></div>

      <div v-if="status" class="card" style="background: rgba(255,255,255,0.04)">
        <div v-if="status === 'not_done'" class="field">
          <label>Why not?</label>
          <textarea v-model="reason" rows="3" placeholder="Be honest, be kind." />
        </div>

        <div class="field">
          <label>Comment (optional)</label>
          <textarea v-model="comment" rows="3" placeholder="Anything to remember?" />
        </div>

        <div class="row" style="justify-content: flex-end;">
          <button class="btn primary" :disabled="saving" @click="submit">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  item: { type: Object, required: true }
})

const emit = defineEmits(['close', 'recorded'])

const status = ref(null)
const reason = ref('')
const comment = ref('')
const saving = ref(false)

function setStatus(v) {
  status.value = v
}

async function submit() {
  saving.value = true
  try {
    emit('recorded', {
      habitId: props.item.habit.id,
      payload: {
        due_at: props.item.due_at,
        status: status.value,
        reason: status.value === 'not_done' ? reason.value || null : null,
        comment: comment.value || null
      }
    })
    emit('close')
  } finally {
    saving.value = false
  }
}
</script>
