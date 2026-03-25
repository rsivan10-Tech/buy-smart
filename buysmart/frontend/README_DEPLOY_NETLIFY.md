# Deploy Buy Smart frontend to Netlify

## 1. Local setup

From `frontend`:

```bash
npm install
npm run build
npm run dev
```

## 2. Configure Netlify (CLI or UI)

### CLI:

```bash
npm install -g netlify-cli
netlify login
netlify init
```

- build command: `npm run build`
- publish directory: `.next`
- set environment variable for local: `NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8005`

### Production env var

In Netlify site settings (or netlify.toml):

`NEXT_PUBLIC_BACKEND_URL=https://your-backend-host.example.com`

## 3. Deploy

```bash
netlify deploy --prod
```

## 4. API routing

If backend is local / ngrok, update front-end env to that URL and rebuild.

## 5. Optional: Netlify Functions proxy

- Add in `netlify.toml`:
  - `functions = "../backend"` (or separate functions directory)

## 6. Health check

- Frontend: `https://<netlify-url>/`
- Backend: `https://your-backend-host.example.com/api/welcome`
- Ensure CORS from frontend origin is allowed.
