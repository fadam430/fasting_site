# Test Documentation (QA)

**Purpose:** Single-source QA reference that consolidates automated tests, manual acceptance testing (user stories), validation checks, and test run/CI guidance.

**Audience:** QA / Test Engineers, Developers, and Release Managers

---

## 1) Executive summary ✅

- Latest automated run: **2026-02-01** (local run)
- Test scope: `fastblog` unit tests (auth & review flows) and project manual acceptance tests (user stories)
- Result: **Automated:** 5 tests run — 5 passed (0 failed)
- Manual (high-level): multiple user-story acceptance checks reported **Pass** (see user-story summary below)
- Accessibility: `aria-labelledby` warnings resolved (added `role="region"`); heading-order / multiple H1 warnings remain recommended to address before public release.

---

## 2) Quick test matrix (automated)

| Test case (method) | Purpose | Last result | Notes |
|---|---:|---:|---|
| `RegistrationRedirectTests.test_register_redirects_to_allauth_signup` | Legacy register → allauth signup | **PASS** | 302 redirect verified |
| `AuthPagesTests.test_login_page_loads` | Login page presence & field check | **PASS** | 200 + password field present |
| `AuthPagesTests.test_signup_creates_user` | Signup creates user record | **PASS** | User created after POST |
| `AuthFlowTests.test_login_and_logout_flow` | Login & immediate logout behavior | **PASS** | Session auth & logout cleared |
| `AuthFlowTests.test_add_review_requires_login` | Add-review protected | **PASS** | Anonymous POST redirected to login |

---

## 3) User-story acceptance summary (manual tests)

- Registration & Account flows: **Pass** — registration, login, password-reset flows validated. (See `TESTINGcrip.md` details.)
- Profile & Premium flows: **Pass** — profile access, premium upgrade prompts, and Stripe checkout flow behavior tested.
- Game/Battle/Codex/Leaderboard: **Pass** — creation, battle mechanics, leaderboard entry, and codex CRUD flows validated manually.

> Note: `TESTINGcrip.md` contains exhaustive, per-user-story walkthroughs and outcomes (many marked **Pass**). I integrated key acceptance results above; for full transcripts see `TESTINGcrip.md`.

---

## 3.a) User-story manual tests — detailed (4 key scenarios)

Below are four extensive, step-by-step manual test cases derived from the user-story acceptance test set in. Each is written so a QA engineer can follow it end-to-end, record the result, and capture evidence.

### Test A — User Story: Register → Login (Account lifecycle)

**Summary / purpose:** Verify new user registration, immediate login behavior, profile access, and sign-out.

**Acceptance criteria:** A site visitor can register, be created in the DB, sign in (no email verification required for the current config), access the profile, and sign out.

**Preconditions:**
- Local dev server running (DEBUG=True or accessible test environment).
- `EMAIL_BACKEND` is set to console (dev default) or test email capture available.
- No test user exists with the chosen test email.

**Test data:**
- Full name: Test User
- Email: test.user+qa@example.com
- Password: Secur3P@ssw0rd

**Steps:**
1. Navigate to `/accounts/signup/`.
2. Fill the registration form with the test data and submit.
3. Verify a successful redirect (e.g., to `LOGIN_REDIRECT_URL` or account page) and a success message.
4. Confirm a new user record exists in the database (Django admin or `python manage.py shell` query: `User.objects.filter(email='test.user+qa@example.com')`).
5. Attempt to login via `/accounts/login/` using email and password (or appropriate username depending on setup).
6. Verify login succeeds and session is authenticated (e.g., navbar shows username, `request.user.is_authenticated` true via a test page).
7. Visit the Profile page and confirm the user's info is displayed.
8. Click Logout (or visit `/accounts/logout/`) and confirm the session is ended and navbar shows login/register links.

**Expected results:**
- POST to signup creates a user and responds with redirect/success response.
- Login works immediately (no verification required under current `ACCOUNT_EMAIL_VERIFICATION='none'`).
- Profile page loads and shows created user.
- Logout clears auth session.

**Post-checks / cleanup:**
- Remove the test user (Django admin or shell) or leave in a test DB that is reset.

**Edge cases:**
- Try to register with an already used email and assert the form shows an error.
- Attempt registration with weak passwords and confirm validation messages.

**Result (to fill):** PASS / FAIL — Notes: __

---

### Test B — User Story: Password reset flow (in development with console email backend)

**Summary / purpose:** Ensure password-reset request, token delivery via console, and password change flow works end-to-end.

**Acceptance criteria:** A user can request a password reset, receive a token via the configured email backend (console for dev), set a new password, and login with the new password.

**Preconditions:**
- A known user exists (test.user+qa@example.com) with a valid password.
- Dev server logs console email output to terminal (or captured logs).

**Test data:**
- Email: test.user+qa@example.com
- New password: NewSecur3P@ss

**Steps:**
1. Visit `/accounts/password/reset/` and submit the registered email address.
2. Confirm the response indicates a reset email has been sent.
3. In the server console, locate the reset URL (the `password/reset/` email body printed to console) and copy the link (tokenized URL).
4. Visit the reset link in the browser.
5. Enter and confirm the new password and submit the form.
6. After success redirect, attempt to login with the new password.
7. Verify login succeeds and the session is authenticated.

**Expected results:**
- A tokenized reset link appears in the console output.
- The reset page accepts a new password and completes password change.
- The user can login using the new password.

**Edge cases / checks:**
- Attempt to reuse an expired/used token and confirm the expected error.
- Submit a non-registered email and confirm the form handles it without user enumeration (same generic message shown).

**Result (to fill):** PASS / FAIL — Notes: __

---

### Test C — User Story: Add Review (protected + submission) — (Auth required)

**Summary / purpose:** Verify that the review/add endpoint requires authentication, that logged-in users can submit reviews, and that the newly created review appears in the appropriate listing.

**Acceptance criteria:** Anonymous users attempting to POST are redirected to login; authenticated users can POST valid review data and see the created review in the listing.

**Preconditions:**
- A valid existing fasting plan or review target exists to attach the review to.
- Test user is registered and can log in.

**Test data:**
- Title: QA Review Title
- Rating: 4
- Body: "This is an automated QA review entry."

**Steps:**
1. As an anonymous user, attempt to POST to `/fasting/review/add/<plan_id>/` (or the project's review-add URL) with review data.
2. Confirm response redirects to `/accounts/login/?next=...` (or equivalent) and that POST is not permitted.
3. Log in as test user.
4. Visit the add-review form and submit the review with the test data.
5. Verify after submit the response redirects to the review listing or plan detail page where the review is visible.
6. On the listing, verify the review text, title, author, and rating are presented correctly.
7. Optionally, test editing/deleting the review if user permissions allow it.

**Expected results:**
- Anonymous POSTs are redirected to login.
- Authenticated review submissions succeed and appear in the list with correct metadata.

**Edge cases:**
- Submit with invalid data (missing body/rating) and confirm validation errors on the form.
- Submit a review with excessively long content and confirm either truncation or server-side validation prevents DB errors.

**Result (to fill):** PASS / FAIL — Notes: __

---

### Test D — User Story: View Fasting Plan & Weekday Accordion (display & accessibility)

**Summary / purpose:** Verify the fasting plan listing and per-plan weekday accordion display including accessibility attributes and review visibility.

**Acceptance criteria:** Fasting plans are listed on `/fasting/`; each plan shows title, author and duration; weekday sections expand/collapse correctly; collapsible panels include `role="region"` and `aria-labelledby` attributes; reviews (if present) are displayed and add-review controls respect auth rules.

**Preconditions:**
- At least one `Fasting_Plan` exists with non-empty weekday text (can be created via Django admin or fixtures).
- Optional: at least one `Reviews` entry exists for the plan to verify review display.

**Test data:**
- Plan title: "QA Test Fasting Plan"
- Weekday content: text present for Monday..Friday

**Steps:**
1. Visit `/fasting/` and locate the fasting plan card with the test title.
2. Verify the card displays the plan title, author username, and duration (e.g., "18-hours").
3. Inspect the weekday accordion headings — ensure each weekday header is present and has `data-bs-target`/`data-bs-toggle` attributes as expected.
4. Click a weekday header (e.g., Monday) to expand — confirm the weekday text becomes visible and is readable.
5. Inspect the expanded collapse container and confirm it has `role="region"` and `aria-labelledby` attributes correctly set.
6. If reviews exist, verify each review shows reviewer username, rating, and comment. Confirm review order (newest first).
7. As anonymous user, attempt to POST to `/fasting/review/add/` with `plan_id`, `rating`, and `comment` and verify you are redirected to the login page (`/accounts/login/?next=...`).
8. Log in as a test user, submit a review via the add-review form (or POST) and confirm the new review appears on the fasting list page.

**Expected results:**
- Plan card and metadata render correctly.
- Accordion expand/collapse works; expanded containers include `role="region"` and `aria-labelledby` (accessibility pass).
- Reviews present and correctly attributed; unauthenticated users are redirected when attempting to POST; authenticated users can submit reviews and see them appear.

**Edge cases:**
- Long weekday text should wrap without overflow; extremely long comments should not break layout.
- Missing weekday content should show a friendly placeholder or be absent without throwing errors.

**Result (to fill):** PASS / FAIL — Notes: __

---

If these tests look good, I can:
- Scaffold a `manual-test-results.md` prefilled with these four scenarios and `To be verified` rows for the recommended resolutions/browsers matrix, or
- Run the steps locally for one scenario and pre-fill the results as an example. Tell me which you prefer and I'll proceed.

## 4) Manual testing (responsive & cross-browser) 🧭

**Goal:** Verify UI & flows across common resolutions and browsers. Use the checklist below for each row in the table and record `PASS/FAIL` with short notes + screenshot.

### Recommended resolutions & browsers matrix

| Resolution (px) | Chrome | Firefox | Edge | Safari | Notes |
|---:|:---:|:---:|:---:|:---:|---|
| 1920 × 1080 | To be verified | To be verified | To be verified | To be verified | Desktop layout & navbar |
| 1366 × 768 | To be verified | To be verified | To be verified | To be verified | Laptop view |
| 1024 × 768 | To be verified | To be verified | To be verified | To be verified | Card wrapping + grid |
| 768 × 1024 | To be verified | To be verified | To be verified | To be verified | Tablet portrait; accordion |
| 412 × 915 | To be verified | To be verified | To be verified | To be verified | Large mobile |
| 390 × 844 | To be verified | To be verified | To be verified | To be verified | iPhone 12/13 viewport |
| 360 × 800 | To be verified | To be verified | To be verified | To be verified | Small mobile |

**Manual checklist (high-value items):**
- Home page renders (hero & cards), no overflow/overlap.
- Navbar: links work, single active link rule, hamburger menu functioning.
- Auth flows: login, signup, password reset operate and show expected messages.
- Review/add: access restriction for anonymous, submission for logged-in users.
- Accordion behavior: expand/collapse works; `role="region"` present.
- Headings: single H1 page-level; card headings H2/H3.
- Forms: keyboard accessible; focus visible; touch inputs work.

**Record keeping:**
- Capture a screenshot per test (resolution+browser). Add a one-line note for failures.
- Option: I can scaffold `manual-test-results.md` (table + screenshot links) or a CSV to collect results. Say "scaffold" and I'll add it.

---

## 5) Error handling & interface tests ⚠️

- 404/500 pages: ensure custom `404.html` and `500.html` are shown appropriately.
- External links open in new tab where expected (e.g., GitHub link in How To).
- Visual regression: scan for broken images, CTA overlap, or text clipping.
- Focus & keyboard navigation: verify important elements are reachable and actionable by keyboard.

---

## 6) Significant issues & status

| Issue | Description | Status | Recommended action |
|---|---:|---:|---|
| Heading-level warnings | Multiple H1s in `templates/fastblog/home.html` | **Open** | Change card headings to H2/H3 (or wrap in sections) and re-run W3C validator |
| Sites framework crash | Missing Site record caused 500 on login/admin (earlier) | **Resolved** | Keep `SITE_ID = 1` and document DB Site creation in README |
| aria-labelledby warnings | Accordion aria warnings | **Resolved** | `role="region"` added to collapsible containers |

---

## 7) How to run (minimal snippets)

- Run all fastblog tests:

```bash
python manage.py test fastblog
```

- Run a single test:

```bash
python manage.py test fastblog.tests.AuthPagesTests.test_login_page_loads
```

- To run with detailed output:

```bash
python manage.py test fastblog --verbosity=2
```

---

## 8) CI & automation suggestions 🤖

- Add GitHub Actions workflow to run Django tests on push/PR (migrate -> test).
- Add Playwright (recommended) for cross-browser automation: create 2–4 smoke tests (home load, login, signup, add-review redirect) and run them on Chromium, WebKit, and Firefox in CI.

If you want, I can:
- Add `.github/workflows/tests.yml` to run Django tests, and/or
- Add Playwright setup + sample tests and a GitHub Actions job to run them.

---

## 9) Acceptance criteria (QA)

- Automated: 100% of `fastblog` unit tests pass on CI.
- Manual: All user-story acceptance tests show **Pass** in `manual-test-results.md` for supported browsers/resolutions.
- Accessibility: No `aria-labelledby` errors and heading-order warnings resolved before public release.

---

## 10) Next actions (pick one)

1. **Scaffold manual results** (`manual-test-results.md`) and pre-fill with `To be verified` rows for your QA team. ✅
2. **Create CI workflow** for Django tests and add status badge to `README.md`. ✅
3. **Implement Playwright tests** + CI job for cross-browser checks. ✅
4. **Fix headings** in `templates/fastblog/home.html` and re-run the W3C validator. ✅

Tell me which you'd like me to do (choose any combination). I can implement the change and open a short PR for review.
