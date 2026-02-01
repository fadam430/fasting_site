# Tests

This file documents the unit tests in the project and how to run them.

Tests added (unit):

- `RegistrationRedirectTests.test_register_redirects_to_allauth_signup`
  - Verifies `/fasting/register/` redirects to `/accounts/signup/`.

- `AuthPagesTests.test_login_page_loads`
  - Verifies `/accounts/login/` returns 200 and contains the password field.

- `AuthPagesTests.test_signup_creates_user`
  - Posts to `/accounts/signup/` and asserts a new user is created.

Additional tests added:

- `AuthFlowTests.test_login_and_logout_flow`
  - Creates a user, logs in via `/accounts/login/`, asserts session auth, logs out via `/accounts/logout/` and confirms user is signed out.

- `AuthFlowTests.test_add_review_requires_login`
  - Posts to `/fasting/review/add/` as anonymous and verifies redirect to `/accounts/login/`.

How to run tests

- Run all `fastblog` tests:

```bash
python manage.py test fastblog
```

Notes

- Tests run with Django's test runner and use the test database; migrations are applied automatically for the test run.
- If you want these tests to run on CI, I can add a GitHub Actions workflow to run them on every push.
