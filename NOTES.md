Change log — Project edits performed (summary)
Date: 2026-01-09

Summary
-------
This file records the source changes made during the current work session so you can review or commit them.

Edits (chronological)
- Fixed Bootstrap script tag in `templates/base.html` so JS bundle loads correctly (enabled collapse/Bootstrap JS).
- Implemented per-plan accordion collapse UI in `fastblog/templates/fastblog/fast_list.html` (weekday accordion items).
- Added Reviews display under each fasting plan (count, reviewer, date, numeric rating, comment).
- Created `fastblog/templatetags/review_tags.py` (filter `stars`) and registered templatetags package to render star ratings.
- Replaced invalid template slicing with the `stars` filter to avoid TemplateSyntaxError.
- Added per-plan collapsible review form (inline in each card) with `rating` (1-5) and `comment` fields.
- Implemented POST handler to save reviews:
  - `fastblog/views.py`: added `add_review` view (login required), validates rating, creates `Reviews` record.
  - `fastblog/urls.py`: added `review/add/` route (named `add_review`).
- Added model helper `Fasting_Plan.average_rating()` (was added but later reverted by user; confirm current state in `fastblog/models.py`).
- Added registration flow:
  - `fastblog/forms.py`: `RegistrationForm` (username, email, password + confirmation).
  - `fastblog/views.py`: `register` view (creates user and logs in).
  - `fastblog/urls.py`: `register/` route.
  - `fastblog/templates/fastblog/register.html`: registration page template.
  - Added `Register` link to navbar in `templates/base.html`.
- Added auth (login/logout):
  - `fastblog/urls.py`: `login/` and `logout/` routes using Django auth views.
  - `fastblog/templates/fastblog/login.html`: login template.
  - `fasting/settings.py`: set `LOGIN_REDIRECT_URL = 'home'`.
  - Navbar updated to show Login/Register when anonymous and Username + Logout when authenticated.
- Improved navbar spacing/layout:
  - `templates/base.html`: separated main nav items (left) from auth items (right) and added spacing for better mobile/desktop appearance.
- Review editing and deletion:
  - `fastblog/forms.py`: added `ReviewForm` for editing.
  - `fastblog/views.py`: added `edit_review` and `delete_review` views with ownership/staff checks.
  - `fastblog/urls.py`: added `review/edit/<int:pk>/` and `review/delete/<int:pk>/` routes.
  - `fastblog/templates/fastblog/review_edit.html`: edit form template.
  - `fastblog/templates/fastblog/fast_list.html`: shows Edit/Delete buttons for reviews when allowed; delete uses POST + CSRF and confirmation.

Notes & next steps
- Forms post to the current handlers; the review add/edit/delete flows require users to be logged in. Anonymous review behavior was intentionally restricted.
- Consider adding flash messages (success/error) and redirect anchors to return to the exact plan card after submit.
- If you want anonymous reviews, I can relax the reviewer FK constraints and adjust views.
- Confirm whether `Fasting_Plan.average_rating()` should be present — it was added earlier but later the file was reverted by the user; check `fastblog/models.py` current contents.

Files changed (high level)
- templates/base.html
- fastblog/templates/fastblog/fast_list.html
- fastblog/templatetags/review_tags.py
- fastblog/forms.py
- fastblog/views.py
- fastblog/urls.py
- fastblog/templates/fastblog/register.html
- fastblog/templates/fastblog/login.html
- fastblog/templates/fastblog/review_edit.html

If you want this note saved elsewhere or formatted differently, tell me where to put it.
