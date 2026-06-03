<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useData, useRouter } from 'vitepress'

const STORAGE_KEY = 'pysheeet-bookmark'

const { page } = useData()
const router = useRouter()
const saved = ref(null)
const isBookmarked = ref(false)
const toast = ref({ visible: false, message: '' })
let toastTimer = null

function showToast(msg) {
  clearTimeout(toastTimer)
  toast.value = { visible: true, message: msg }
  toastTimer = setTimeout(() => { toast.value.visible = false }, 2200)
}

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) { saved.value = null; isBookmarked.value = false; return }
    const data = JSON.parse(raw)
    saved.value = data
    isBookmarked.value = data && data.path === router.route.path
  } catch { saved.value = null; isBookmarked.value = false }
}

function toggle() {
  if (isBookmarked.value) {
    localStorage.removeItem(STORAGE_KEY)
    saved.value = null
    isBookmarked.value = false
    showToast('Bookmark removed')
  } else if (saved.value) {
    const label = saved.value.title + (saved.value.hash ? ' \u2192 ' + saved.value.hash : '')
    showToast('Navigating to: ' + label)
    router.go(saved.value.path + (saved.value.hash || ''))
  } else {
    const data = {
      path: router.route.path,
      hash: window.location.hash || null,
      title: page.value.title || document.title
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    saved.value = data
    isBookmarked.value = true
    const label = data.title + (data.hash ? ' \u2192 ' + data.hash : '')
    showToast('Bookmarked: ' + label)
  }
}

onMounted(() => {
  load()
  if (saved.value && saved.value.hash && saved.value.path === router.route.path) {
    nextTick(() => {
      const el = document.getElementById(saved.value.hash.slice(1))
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    })
  }
})

watch(() => router.route.path, () => {
  load()
  if (saved.value && saved.value.hash && saved.value.path === router.route.path) {
    nextTick(() => {
      const el = document.getElementById(saved.value.hash.slice(1))
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    })
  }
})
</script>

<template>
  <button
    class="bookmark-btn"
    :title="isBookmarked
      ? 'Remove bookmark'
      : saved
        ? 'Go to: ' + saved.title + (saved.hash ? ' \u2192 ' + saved.hash : '')
        : 'Bookmark this page (current section)'
    "
    @click="toggle"
  >
    <svg v-if="isBookmarked" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
      <path d="M5 2h14a1 1 0 0 1 1 1v19.143a.5.5 0 0 1-.766.424L12 18.03l-7.234 4.536A.5.5 0 0 1 4 22.143V3a1 1 0 0 1 1-1z"/>
    </svg>
    <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round">
      <path d="M5 2h14a1 1 0 0 1 1 1v19.143a.5.5 0 0 1-.766.424L12 18.03l-7.234 4.536A.5.5 0 0 1 4 22.143V3a1 1 0 0 1 1-1z"/>
    </svg>
  </button>
  <Transition name="toast">
    <div v-if="toast.visible" class="bookmark-toast">{{ toast.message }}</div>
  </Transition>
</template>

<style scoped>
.bookmark-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 6px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: color .2s, background-color .2s;
}
.bookmark-btn:hover {
  color: var(--vp-c-brand-1);
  background-color: var(--vp-c-default-soft);
}
.bookmark-btn svg {
  width: 20px;
  height: 20px;
}

.bookmark-toast {
  position: fixed;
  top: 12px;
  right: 64px;
  z-index: 999;
  padding: 8px 16px;
  border-radius: 8px;
  background: var(--vp-c-brand-1);
  color: #fff;
  font-size: 13px;
  line-height: 1.4;
  max-width: 320px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
  box-shadow: 0 4px 12px rgba(0,0,0,.2);
}

.toast-enter-active { transition: all .25s ease-out; }
.toast-leave-active { transition: all .2s ease-in; }
.toast-enter-from { opacity: 0; transform: translateY(-8px); }
.toast-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
