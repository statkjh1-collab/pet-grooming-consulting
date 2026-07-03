<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import ChatWidget from './components/ChatWidget.vue'

const menuOpen = ref(false)
</script>

<template>
  <header class="nav">
    <div class="nav-inner">
      <RouterLink to="/" class="nav-logo" @click="menuOpen = false">🐾 펫미용샵 창업 컨설팅</RouterLink>
      <button class="hamburger" @click="menuOpen = !menuOpen" :aria-expanded="menuOpen" aria-label="메뉴 열기">
        <span></span><span></span><span></span>
      </button>
      <nav :class="{ open: menuOpen }">
        <RouterLink to="/education" @click="menuOpen = false">창업전 라이선스 준비</RouterLink>
        <RouterLink to="/pre-open" @click="menuOpen = false">사업장 오픈 전</RouterLink>
        <RouterLink to="/operations" @click="menuOpen = false">미용샵 운영 관리</RouterLink>
        <RouterLink to="/marketing" @click="menuOpen = false">마케팅 & 홍보</RouterLink>
        <RouterLink to="/finance" @click="menuOpen = false">수익 & 재무 관리</RouterLink>
        <RouterLink to="/support" @click="menuOpen = false">국가 창업 지원</RouterLink>
        <RouterLink to="/faq" @click="menuOpen = false">FAQ</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
  <ChatWidget />
</template>

<style>
*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f9fafb;
  color: #111;
}

#app { max-width: 100%; }

a { text-decoration: none; }
</style>

<style scoped>
.nav {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  gap: 1rem;
}

.nav-logo {
  font-size: 1.1rem;
  font-weight: 800;
  color: #111;
  white-space: nowrap;
}

nav {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

nav a {
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #374151;
  transition: background 0.15s;
}

nav a:hover,
nav a.router-link-active {
  background: #fef3c7;
  color: #d97706;
  font-weight: 600;
}

.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
}

.hamburger span {
  display: block;
  height: 2px;
  width: 100%;
  background: #111;
  border-radius: 2px;
  transition: transform 0.2s, opacity 0.2s;
}

@media (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  nav {
    display: none;
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    flex-direction: column;
    gap: 0;
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
    padding: 0.5rem 1.5rem 1rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
  }

  nav.open {
    display: flex;
  }

  nav a {
    padding: 0.75rem 0.5rem;
    border-radius: 0;
    border-bottom: 1px solid #f3f4f6;
  }
}
</style>
