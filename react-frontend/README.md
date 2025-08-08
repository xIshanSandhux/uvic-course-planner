# UVic Course Planner — Frontend

A React + Tailwind single page app for planning UVic courses with an AI assistant. It collects student info, builds a term plan, checks prereqs, and chats with an AI to refine recommendations. Ships with a clean UI shell, a 3-step wizard, and a ChatGPT-style chat interface.

## Stack

- React 18, Vite
- React Router
- Tailwind CSS
- Axios for API calls
- js-cookie for lightweight session hints
- jsPDF for exporting plans
- Optional: Supabase (planned) for auth

## App flow

```
Landing → FS1 (Personal Info) → FS2 (Course Plan) → FS3 (Prereqs) → Chatbot → Dashboard
```

Routes:

- `/` Landing (public)
- `/dashboard` Dashboard (post-login)
- `/form` Step 1: Personal info
- `/form/plan` Step 2: Course plan
- `/courses` Step 3: Select completed prereqs
- `/chat` AI assistant

## Features

- Public and authed headers with a mobile sidebar
- Three-step progress tracker component
- Wizard state passed between steps via `navigate(..., { state })`
- AI chat pulls server state for course list, completed courses, and prereq eligibility
- PDF export and Save Plan actions
- Sticky app shell with header and footer

## Directory highlights

```
src/
  components/
    AppShell.jsx         # Shared layout wrapper
    Header.jsx           # Auth header with sidebar
    PublicHeader.jsx     # Public header for landing
    Footer.jsx
    ProgressTracker.jsx
    Sidebar.jsx
  pages/
    Landing.jsx
    Dashboard.jsx
    FS1PersonalInfo.jsx
    FS2CoursePlan.jsx
    FS3PrereqsCompleted.jsx
    Chatbot.jsx
  hooks/
    useAuth.js           # simple localStorage user check
    useScrollToTop.js    # scroll to top on mount
  App.jsx                # routes
```

## API contract (backend expected)

Base URL is configurable. The app currently calls `http://127.0.0.1:8000` and `http://localhost:8000`. Set a single base with an env var (see below).

Endpoints hit by the frontend:

- `POST /extract_courses` `{ major }` → `{ success, data: string[] }`
- `POST /course_list` `{ courses: string[] }` → `{ success }`
- `POST /courses_completed` `{ courses: string[] }` → `{ success }`
- `POST /courses_not_completed` (no body) → `{ success }`
- `POST /pre_req_check` (no body) → `{ success }`
- `GET /course_list` → `{ data: string[] }` used by Chatbot initial message
- `GET /courses_completed` → `{ data: string[] | string }`
- `GET /pre_req_check` → `{ data: string[] }`
- `POST /cohere/chat` `{ messages }` → Cohere response proxy
- `POST /save_plan` `{ user, messages }` → persists plan

> If your backend differs, update the axios calls in `FS2CoursePlan.jsx`, `FS3PrereqsCompleted.jsx`, and `Chatbot.jsx`.

## Quick start

1. **Install**

```bash
npm i
```

2. **Configure environment**

Create `.env.local` in the project root:

```bash
VITE_API_URL=http://127.0.0.1:8000
```

Optional auth placeholders:

```bash
# for future supabase auth
VITE_SUPABASE_URL=...
VITE_SUPABASE_ANON_KEY=...
```

3. **Run**

```bash
npm run dev
```

Vite prints the local URL.

## Configuration details

### API base URL

Replace hardcoded URLs with `import.meta.env.VITE_API_URL`. Example patch:

```js
// utils/api.js
export const API = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";
```

Then in pages:

```js
import { API } from "../utils/api";
await axios.post(`${API}/extract_courses`, { major });
```

Update in:

- `FS2CoursePlan.jsx`
- `FS3PrereqsCompleted.jsx`
- `Chatbot.jsx`

### Auth

Current `useAuth` reads `localStorage.user`. Logged-in header shows a sidebar if `isLoggedIn` is true.

Planned Supabase swap:

- Replace `useAuth` with a supabase session hook
- On login, set session and navigate to `/dashboard`
- Guard authed routes if needed

### Styling

- Tailwind config defines the palette:

```js
primary: "#F4D06F",
accent:  "#FF8811",
cyan:    "#9DD9D2",
offwhite:"#FFF8F0",
purple:  "#392F5A",
dark:    "#1a1a1a",
```

- Body background and text colors are set in `AppShell` and `Layout`.

### Accessibility and UX

- Headers are keyboard accessible
- Sidebar closes on Escape
- Inputs use high-contrast labels and focus rings
- ProgressTracker shows active and completed steps

## Common tasks

### Add a new step to the wizard

1. Create a new page in `src/pages/`
2. Add a route in `App.jsx`
3. Render `<ProgressTracker currentStep={n} />`
4. Pass accumulated state forward with `navigate('/next', { state: { ...prev, newField } })`

### Persist form state across refresh

- Option 1: store step state in `localStorage`
- Option 2: move wizard state to a context provider

### Change branding

- Update `logo` in `Header` and `PublicHeader`
- Adjust Tailwind colors in `tailwind.config.js`
- Update footer year text if needed

## Troubleshooting

- **Blank page on route change**  
  Ensure `AppShell` wraps each route element and `main` has padding top to avoid overlap with the fixed header.

- **Chatbot initial message empty**  
  Verify backend `/course_list`, `/courses_completed`, `/pre_req_check` return expected shapes.

- **CORS errors**  
  Allow `Vite dev server origin` in the backend CORS settings.

- **PDF export cut off**  
  The simple jsPDF export writes assistant messages only. For long chats, paginate lines or use a larger page size.

## Scripts

Add these to `package.json` if missing:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## Deployment

- Vercel or Netlify work out of the box
- Set `VITE_API_URL` in project environment settings to point at your backend
- If using Supabase later, set its URL and anon key as env vars too
