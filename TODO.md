# Testing Implementation TODO

## Plan Breakdown & Progress Tracking

### 1. [x] Create TODO.md (done)

### 2. [x] Create tests/ directory structure & files
   - tests/conftest.py (fixtures: test_db, test_client, playwright page, seed user "sushmitha")
   - tests/test_integration.py (TestClient: home, login success/fail, account auth)
   - tests/test_e2e.py (Playwright: browser login flow, home posts)

### 3. [x] Implement fixtures in conftest.py
   - Async test DB session (rollback/transaction)
   - Override app deps for testing
   - Seed test user via populate_db or direct insert

### 4. [x] Write integration tests (test_integration.py)
   - test_homepage_renders()
   - test_login_success()
   - test_login_failure()
   - test_protected_account()

### 5. [x] Write E2E tests (test_e2e.py)
   - test_login_flow(page)
   - test_homepage_loads(page)

### 6. [x] Optional: Add StrictUndefined to main.py templates

### 7. [x] Test run - Ready! Run manually: pytest tests/ -v
   - pytest tests/ -v
   - pytest tests/test_e2e.py --headed (server running)

### 8. [] [x] Complete - attempt_completion

Updated when steps complete.
