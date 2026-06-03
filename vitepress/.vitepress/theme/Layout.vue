<script setup>
import DefaultTheme from 'vitepress/theme'
import BookmarkButton from './BookmarkButton.vue'
</script>

<template>
  <DefaultTheme.Layout>
    <template #nav-bar-content-after>
      <BookmarkButton />
    </template>
  </DefaultTheme.Layout>
</template>

<style>
/* ── Logo dark mode ── */
.dark .VPImage.logo {
  filter: brightness(0) invert(1);
}

/* ── Sidebar beautification ── */

/* Reduce sidebar container padding */
.VPSidebar .nav {
  padding-left: 12px !important;
  padding-right: 8px !important;
}

/* Group headers: compact uppercase */
.VPSidebarItem.level-0 > .item > .text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .04em;
  text-transform: uppercase;
  color: var(--vp-c-text-2);
  padding: 4px 0;
}

/* Group spacing */
.VPSidebarItem.level-0 {
  margin-bottom: 2px;
}
.VPSidebarItem.level-0 + .VPSidebarItem.level-0 {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--vp-c-divider);
}

/* Items: subtle indent with left border */
.VPSidebarItem.level-1 {
  position: relative;
}
.VPSidebarItem.level-1 > .item {
  padding: 4px 12px 4px 20px;
  border-radius: 6px;
  margin: 0 2px;
  transition: background-color .15s;
}
.VPSidebarItem.level-1 > .item:hover {
  background: var(--vp-c-default-soft);
}
.VPSidebarItem.level-1.is-active > .item {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}
.VPSidebarItem.level-1.is-active > .item > .text {
  color: var(--vp-c-brand-1);
  font-weight: 600;
}

/* Active left accent bar */
.VPSidebarItem.level-1.is-active::before {
  content: '';
  position: absolute;
  left: 2px;
  top: 6px;
  bottom: 6px;
  width: 3px;
  border-radius: 2px;
  background: var(--vp-c-brand-1);
}

/* Caret styling */
.VPSidebarItem.level-0 > .item .caret {
  color: var(--vp-c-text-3);
  transition: transform .2s, color .2s;
}
.VPSidebarItem.level-0:not(.collapsed) > .item .caret .caret-icon {
  transform: rotate(90deg);
}

/* Home page logo */
.home-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 8px;
}
.home-logo svg {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  color: var(--vp-c-brand-1);
}
.home-logo h1 {
  margin: 0;
}
</style>
