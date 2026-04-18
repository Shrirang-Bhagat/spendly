# Spec: Login and Logout

## Overview
Implement session-based login and logout so registered users can authenticate with their email and password and maintain a logged-in state across requests. This step upgrades the existing stub `GET /login` route into a fully functional form that accepts a POST, validates credentials against the database, sets a server-side session on success, and provides a `/logout` route that clears the session. After this step, the app can distinguish between anonymous and authenticated users, which is the prerequisite for all protected routes in later steps.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (user rows exist in `users` table)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade it)
- `POST /login` — validate credentials, set session, redirect to dashboard or back to form — public
- `GET /logout` — clear session, redirect to `/login` — public (already exists as stub, upgrade it)

## Database changes
No new tables or columns.

A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — returns the matching `users` row as a `sqlite3.Row` (or `None` if not found). Used by the login route to look up the user and verify the password hash.

## Templates
- **Modify**: `templates/login.html`
  - Change the form `action` to `url_for('login')` with `method="post"`
  - Add `name` attributes to inputs: `email`, `password`
  - Add a block to display flash error messages (e.g. "Invalid email or password")
  - Keep all existing visual design
- **Modify**: `templates/base.html`
  - Update the navigation so a "Logout" link appears when the user is logged in, and "Login" / "Register" links appear when not logged in (use `session.get('user_id')` to decide)

## Files to change
- `app.py` — upgrade `login()` to handle `GET` and `POST`; upgrade `logout()` to clear session and redirect; import `session` and `check_password_hash` from werkzeug
- `database/db.py` — add `get_user_by_email()` helper
- `templates/login.html` — wire up form action/method and flash message display
- `templates/base.html` — conditionally show nav links based on session state

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security` (already installed) and Flask's built-in `session`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plaintext
- On successful login, store `session['user_id']` and `session['user_name']` — nothing else
- Use a generic error message "Invalid email or password" for both wrong-email and wrong-password cases — never reveal which field is wrong
- On any validation failure, re-render the login form with a flashed error — do not redirect
- On successful login, redirect to `url_for('dashboard')` (placeholder for now; fall back to `url_for('landing')` if dashboard does not yet exist)
- `logout()` must call `session.clear()` then redirect to `url_for('login')`
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid credentials sets `session['user_id']` and redirects away from the login page
- [ ] Submitting an unrecognised email re-renders the form with "Invalid email or password"
- [ ] Submitting a correct email but wrong password re-renders the form with "Invalid email or password"
- [ ] Submitting with any empty field re-renders the form with a validation error
- [ ] `GET /logout` clears the session and redirects to `/login`
- [ ] After logout, navigating to a session-protected URL does not show authenticated content
- [ ] The nav bar shows "Login" / "Register" when logged out and "Logout" when logged in
