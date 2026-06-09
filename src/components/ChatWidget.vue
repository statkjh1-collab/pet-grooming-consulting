<script setup>
import { ref, nextTick } from 'vue'

const open = ref(false)
const input = ref('')
const loading = ref(false)
const messagesEl = ref(null)
const messages = ref([
  { role: 'assistant', content: '안녕하세요! 펫미용샵 창업 컨설턴트입니다 🐾\n궁금한 점을 무엇이든 물어보세요!' }
])

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  scrollBottom()

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: messages.value
          .filter(m => m.role !== 'assistant' || messages.value.indexOf(m) > 0)
          .map(m => ({ role: m.role, content: m.content }))
      })
    })
    const data = await res.json()
    messages.value.push({ role: 'assistant', content: data.text || data.error || '오류가 발생했습니다.' })
  } catch {
    messages.value.push({ role: 'assistant', content: '연결 오류가 발생했습니다. 잠시 후 다시 시도해주세요.' })
  } finally {
    loading.value = false
    scrollBottom()
  }
}

function scrollBottom() {
  nextTick(() => {
    if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  })
}

function onKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}
</script>

<template>
  <!-- 플로팅 버튼 -->
  <button class="chat-fab" @click="open = !open" :aria-label="open ? '닫기' : '채팅 열기'">
    <span v-if="!open">💬</span>
    <span v-else>✕</span>
  </button>

  <!-- 채팅창 -->
  <Transition name="chat">
    <div v-if="open" class="chat-window">
      <div class="chat-header">
        <span>🐾 창업 AI 상담</span>
        <button class="close-btn" @click="open = false">✕</button>
      </div>

      <div class="chat-messages" ref="messagesEl">
        <div
          v-for="(msg, i) in messages"
          :key="i"
          class="msg"
          :class="msg.role"
        >
          <div class="bubble">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="msg assistant">
          <div class="bubble loading">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <div class="chat-input-row">
        <textarea
          v-model="input"
          @keydown="onKeydown"
          placeholder="궁금한 점을 입력하세요..."
          rows="1"
          :disabled="loading"
        />
        <button class="send-btn" @click="send" :disabled="loading || !input.trim()">전송</button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.chat-fab {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #f59e0b;
  color: #fff;
  border: none;
  font-size: 1.4rem;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0,0,0,0.18);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, transform 0.15s;
}
.chat-fab:hover { background: #d97706; transform: scale(1.07); }

.chat-window {
  position: fixed;
  bottom: 5rem;
  right: 1.5rem;
  width: 340px;
  max-height: 520px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  display: flex;
  flex-direction: column;
  z-index: 999;
  overflow: hidden;
}

.chat-header {
  background: #f59e0b;
  color: #fff;
  padding: 0.85rem 1rem;
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.msg { display: flex; }
.msg.user { justify-content: flex-end; }
.msg.assistant { justify-content: flex-start; }

.bubble {
  max-width: 80%;
  padding: 0.6rem 0.9rem;
  border-radius: 12px;
  font-size: 0.875rem;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-word;
}
.user .bubble { background: #f59e0b; color: #fff; border-bottom-right-radius: 4px; }
.assistant .bubble { background: #f3f4f6; color: #111; border-bottom-left-radius: 4px; }

/* 로딩 점 애니메이션 */
.bubble.loading {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 0.75rem 1rem;
}
.bubble.loading span {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #9ca3af;
  animation: dot 1.2s infinite;
}
.bubble.loading span:nth-child(2) { animation-delay: 0.2s; }
.bubble.loading span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot { 0%,80%,100%{opacity:0.3;transform:scale(0.8)} 40%{opacity:1;transform:scale(1)} }

.chat-input-row {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem;
  border-top: 1px solid #e5e7eb;
}
textarea {
  flex: 1;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  resize: none;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s;
}
textarea:focus { border-color: #f59e0b; }
textarea:disabled { background: #f9fafb; }

.send-btn {
  background: #f59e0b;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 0.9rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
  white-space: nowrap;
}
.send-btn:hover:not(:disabled) { background: #d97706; }
.send-btn:disabled { background: #d1d5db; cursor: not-allowed; }

/* 트랜지션 */
.chat-enter-active, .chat-leave-active { transition: opacity 0.2s, transform 0.2s; }
.chat-enter-from, .chat-leave-to { opacity: 0; transform: translateY(12px) scale(0.97); }

@media (max-width: 400px) {
  .chat-window { width: calc(100vw - 2rem); right: 1rem; }
}
</style>
