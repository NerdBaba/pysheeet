<script setup>
import { ref, onMounted, watch } from 'vue'
import { useData, useRouter } from 'vitepress'

const STORAGE_KEY = 'pysheeet-bookmark'

const { page } = useData()
const router = useRouter()
const savedPath = ref(null)
const savedTitle = ref(null)
const isBookmarked = ref(false)

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) { savedPath.value = null; savedTitle.value = null; isBookmarked.value = false; return }
    const data = JSON.parse(raw)
    savedPath.value = data.path || null
    savedTitle.value = data.title || null
    isBookmarked.value = data.path === router.route.path
  } catch { savedPath.value = null; savedTitle.value = null; isBookmarked.value = false }
}

function toggle() {
  if (isBookmarked.value) {
    localStorage.removeItem(STORAGE_KEY)
    savedPath.value = null
    savedTitle.value = null
    isBookmarked.value = false
  } else if (savedPath.value) {
    router.go(savedPath.value)
  } else {
    const data = { path: router.route.path, title: page.value.title || document.title }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    savedPath.value = data.path
    savedTitle.value = data.title
    isBookmarked.value = true
  }
}

onMounted(load)
watch(() => router.route.path, load)
</script>

<template>
  <button class="bookmark-btn" :title="isBookmarked ? 'Remove bookmark' : savedPath ? 'Go to: ' + savedTitle : 'Bookmark this page'" @click="toggle">
    <svg v-if="isBookmarked" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
      <path d="M5 2h14a1 1 0 0 1 1 1v19.143a.5.5 0 0 1-.766.424L12 18.03l-7.234 4.536A.5.5 0 0 1 4 22.143V3a1 1 0 0 1 1-1z"/>
    </svg>
    <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round">
      <path d="M5 2h14a1 1 0 0 1 1 1v19.143a.5.5 0 0 1-.766.424L12 18.03l-7.234 4.536A.5.5 0 0 1 4 22.143V3a1 1 0 0 1 1-1z"/>
    </svg>
  </button>
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
</style>
