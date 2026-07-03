<script setup>
import { RouterLink, RouterView } from 'vue-router'
import ChatWidget from './components/ChatWidget.vue'
</script>

<template>
  <header class="nav">
    <div class="nav-inner">
      <RouterLink to="/" class="nav-logo">🐾 펫미용샵 창업 컨설팅</RouterLink>
      <nav>
        <RouterLink to="/pre-open">사업장 오픈 전</RouterLink>
        <RouterLink to="/operations">미용샵 운영 관리</RouterLink>
        <RouterLink to="/marketing">마케팅 & 홍보</RouterLink>
        <RouterLink to="/finance">수익 & 재무 관리</RouterLink>
        <RouterLink to="/support">국가 창업 지원</RouterLink>
        <RouterLink to="/education">교육</RouterLink>
        <RouterLink to="/faq">FAQ</RouterLink>
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
</style>
