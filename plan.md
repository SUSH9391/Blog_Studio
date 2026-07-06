# UI/UX Enhancement Plan for Blog Studio

## Goals
- Improve visual appeal with a refreshed color scheme.
- Enhance layout and responsiveness for better readability on various screen sizes.
- Refine UI components (cards, buttons, inputs) with subtle interactions and modern touches.
- Add a featured post section to highlight notable content on the home page.

## Changes

### 1. Color Scheme & Theme (main.css)
- Update `--color-bg-body` to a softer off-white (`#F8F9FA`).
- Update `--color-bg-content` to keep pure white (`#FFFFFF`).
- Update `--color-accent` to a vibrant indigo (`#4F46E5`) with adjusted hover (`#4338CA`).
- Update `--color-upvote`/`--color-downvote` for better visibility.
- Dark mode:
  - Adjust `--color-bg-body` to `#0F172A` (dark blue-gray).
  - Adjust `--color-bg-content` to `#1E293B`.
  - Adjust `--color-accent` to `#6366F1` (lighter indigo).
  - Improve text contrast for readability.

### 2. Layout & Responsiveness (main.css)
- Increase max-width of `.reddit-layout` from `1050px` to `1200px`.
- Adjust `.reddit-main` max-width from `640px` to `720px`.
- Adjust `.reddit-sidebar` width from `312px` to `300px` and margin-left to `20px`.
- Update spacing variables: `--spacing-nav-height` to `56px` for slightly taller navbar on larger screens.
- Adjust media query breakpoint for sidebar to `min-width: 1200px` (optional) or keep at `992px`.
- Improve mobile padding: reduce horizontal padding on `.reddit-layout` to `12px` on small screens.

### 3. Component Enhancements (main.css)
- **.reddit-card**:
  - Add `transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.15s ease;`.
  - On hover: `transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-color: var(--color-border-hover);`.
- **Buttons** (`.btn-reddit`, `.btn-reddit-outline`):
  - Add `box-shadow: 0 2px 4px rgba(0,0,0,0.1);`.
  - On hover: increase shadow and transform scale slightly.
  - `.btn-reddit`: change background to linear gradient (to bottom right, from `--color-accent` to a slightly darker shade).
- **Inputs** (`.form-control`):
  - Add subtle `box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);` on normal state.
  - On focus: enhance box-shadow and adjust border-color to `--color-accent`.
- **Avatars** (`.card-avatar`):
  - Add `border: 2px solid transparent;`.
  - On hover: `border-color: var(--color-accent);` and `transform: scale(1.05);`.
- **Action Bar** (`.action-btn`):
  - Increase padding and add hover background transition.

### 4. New Featured Post Section (home.html)
- Insert a section just below the site header (inside `<main>` but before the `reddit-layout` container) to display a featured post.
- The featured post will be styled as a larger card with a background accent, perhaps using a new class `.featured-post`.
- CSS for `.featured-post`:
  - Background: `var(--color-bg-hover)` or a soft gradient.
  - Padding: increased.
  - Title size: larger.
  - Maybe include a banner image placeholder.
- The section will be conditionally rendered if a featured post is passed from the view (we can modify the home view later, but for now we can static test with a placeholder or use the first post as featured).
- For simplicity, we can use the first post in the list as featured and display it prominently, then list the rest.

### 5. HTML Adjustments
- In `home.html`, extend the template to include a featured post block.
- Modify the loop to skip the featured post if we are using the first post as featured.
- Ensure the featured post section is responsive.

### 6. Additional Tweaks
- Update the navbar brand font size and spacing for better balance.
- Slightly increase font sizes for headings and body for improved readability.
- Add subtle focus outlines for accessibility (already covered by Bootstrap but we can customize).
- Ensure dark mode toggles correctly with new colors.

## Implementation Steps
1. Backup original main.css and home.html (optional).
2. Edit main.css with the variable changes and new component styles.
3. Edit home.html to add featured post section and adjust loops.
4. Test changes locally to ensure no breaking of existing functionality.
5. Verify responsiveness via browser dev tools.

## Files to Modify
- `static/css/main.css`
- `templates/home.html`
- Possibly `templates/layout.html` (for navbar tweaks)
- Possibly `static/js/utils.js` if needed for new interactions (unlikely)

## Notes
- Ensure all changes maintain backward compatibility and do not break existing JS interactions.
- Keep CSS custom properties consistent for easy theming.