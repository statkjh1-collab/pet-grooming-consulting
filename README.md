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

`backend/`에 FastAPI 백엔드가 있습니다. 예비창업패키지 준비 과정(체크리스트, 상권·입지, 상권 분석)을
관리하는 개인용 도구이며, 프론트엔드(Vercel 배포)와 별도로 [Render](https://render.com)에
Web Service + Postgres로 배포되어 있습니다.

### 로컬 개발

```sh
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

`backend/.env.example`을 참고해 `backend/.env`를 만들고 값을 채웁니다:
- `DATA_GO_KR_SERVICE_KEY` — 상권 분석 데이터 수집용
- `DATABASE_URL` — Render Postgres의 **External Database URL**. 비워두면 로컬 SQLite(`backend/startup.db`)로 자동 폴백

```sh
uvicorn main:app --reload --port 8000
```

프론트엔드에서는 평소처럼 `npm run dev`를 실행하면 `/startup` 메뉴에서 접근할 수 있습니다 (Vite가 `/api`
요청을 8000번 포트로 프록시합니다).

### 배포 (Render + Vercel)

- **백엔드(Render Web Service)**: 이 저장소의 `backend/`를 Root Directory로 지정, Python 런타임.
  Build Command `pip install -r requirements.txt`, Start Command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
  환경변수로 `DATA_GO_KR_SERVICE_KEY`, `DATABASE_URL`(Postgres의 **Internal** Database URL) 설정.
- **DB(Render Postgres)**: 별도 Postgres 인스턴스. 무료 플랜은 30일 후 만료되므로 장기 운영 시 유료 플랜 권장.
- **프론트엔드(Vercel)**: 환경변수 `VITE_API_BASE_URL`을 Render 웹서비스의 공개 URL(예: `https://pet-grooming-backend.onrender.com`)로 설정 — 로컬에서는 비워두면 Vite 프록시를 그대로 씀.
- 매달 상권 데이터를 갱신하는 `backend/fetch_market.py`는 로컬 스케줄 작업으로 실행되며, `DATABASE_URL`이
  설정되어 있으면 같은 Render Postgres에 스냅샷을 쌓아 운영 사이트와 데이터를 공유합니다.
