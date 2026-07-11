# pet-grooming-consulting

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## 창업 관리(Startup Tracker) 백엔드

`backend/`에 FastAPI + SQLite 백엔드가 있습니다. 예비창업패키지 준비 과정(체크리스트 등)을 로컬에서만
관리하는 개인용 도구이며, 배포되는 정적 사이트와는 별개로 로컬 개발 시에만 함께 띄웁니다.

```sh
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python seed.py                 # 최초 1회: 체크리스트 초기 데이터 주입 (uvicorn 실행 시 자동으로도 실행됨)
uvicorn main:app --reload --port 8000
```

프론트엔드에서는 평소처럼 `npm run dev`를 실행하면 `/startup` 메뉴에서 접근할 수 있습니다 (Vite가 `/api`
요청을 8000번 포트로 프록시합니다).
