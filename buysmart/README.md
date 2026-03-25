# Buy Smart

פרויקט יוקרתי לקונים ישראלים של נכסים "על הנייר".

## עקרונות ליבה

- Architecture First: לא כותבים לוגיקה עד שיש ארכיטקטורה מודולרית וסקלאבילית.
- Modular Components: הפרדה ברורה בין UI, API ולוגיקה לעיבוד נתונים.
- Hebrew First (RTL): כל ה-UI ייבנה ב-RTL כברירת מחדל. מטרי וק"ש.
- Error Handling: לכל קריאת API טיפול מפורש בשגיאות, הודעות ידידותיות, degradation graceful.
- State Management: מקור אמת יחיד למדינת האפליקציה (input משתמש, פרויקט נוכחי).
- Third-Party Delegate: שימוש ב-API סטנדרטיים למשימות מורכבות (Auth, Payments, Google Maps, Floor Plan Processing).

## טכנולוגיות מועדפות

- Frontend: Next.js (React), Mantine (RTL), Tailwind (אופציונלי)
- State: Zustand
- Backend: FastAPI
- Database: PostgreSQL + PostGIS
- 3D/2D: Three.js / @react-three/fiber

## מבנה פרויקט

- /frontend
- /backend
- /docker

## איך להפעיל

1. הרץ `docker compose up -d` בתיקייה /docker.
2. frontend: `npm run dev` בתיקייה /frontend.
3. backend: `uvicorn main:app --host 0.0.0.0 --port 8000` בתיקייה /backend.

## מטרתו
תמיכה בקונים לא מומחים בנדל"ן בישראל בהדמיה, ניתוח ואופטימיזציה של הבית העתידי שלהם.
