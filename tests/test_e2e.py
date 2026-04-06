import pytest
from playwright.sync_api import Page, expect

# Note: Run with server at http://localhost:8000 (uvicorn main:app --reload)
# Assumes test user seeded or exists in DB

def test_login_flow(page: Page):
    page.goto("http://localhost:8000/login")
    
    # Fill login form
    page.fill('input[name="username"]', "sushmitha@example.com")  # adjust if username
    page.fill('input[name="password"]', "abc123@$")
    page.click('button[type="submit"]')
    
    # Wait for success and redirect (JS sets token, redirects to /)
    expect(page).to_have_url("http://localhost:8000/**")  # or /account if redirects there
    # Check token stored
    local_storage = page.evaluate("() => localStorage.getItem('access_token')")
    assert local_storage is not None

def test_homepage_ui(page: Page):
    page.goto("http://localhost:8000/")
    
    # Check posts render
    expect(page.locator('.reddit-card').first).to_be_visible()
    expect(page.locator('.vote-btn').first).to_be_visible()
    # Infinite scroll load more if present
    if page.locator('#loadMoreBtn').count() > 0:
        page.click('#loadMoreBtn')
        expect(page.locator('.reddit-card')).to_have_count(2)  # Adjust based on expected output

