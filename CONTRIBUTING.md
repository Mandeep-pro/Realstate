# Contributing to Realstate Repository

Thank you for your interest in contributing! This document outlines the workflow and guidelines for improving the project, especially the map feature.

## Getting Started
1. **Fork the repository** to your own GitHub account.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/Realstate.git
   cd Realstate
   ```
3. **Create a feature branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Example: `feature/improve-map-marker-colors`

## Map-Specific Updates
The interactive map lives in:
- `real_estate_predictor/templates/map.html` (Leaflet.js interface)
- `real_estate_predictor/geocoder.py` (city coordinates)
- `real_estate_predictor/app.py` (routes `/map` and `/api/properties-map`)

Common improvement ideas:
- Add a search box for cities or addresses
- Use a geocoding API to convert addresses to lat/long dynamically
- Add filters (price range, bedrooms) to the map
- Show property thumbnails or links in popups
- Cluster large datasets or enable heatmap layer

When updating map functionality:
1. Modify the above files or add new helpers.
2. Test locally by running `python real_estate_predictor/app.py` and visiting `http://127.0.0.1:5000/map`.
3. Make sure changes degrade gracefully if coordinate data is missing.

## General Contribution Workflow
1. Stage and commit your changes with clear messages:
   ```bash
   git add .
   git commit -m "feat: add search box to map interface"
   ```
2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
3. Open a **Pull Request** on the original repository:
   - Title should summarize the change (e.g. `feat(map): add city search filter`).
   - Describe what you changed and why.
   - Link any related issues if they exist.

## Coding Style & Quality
- Follow existing Python formatting (PEP 8).
- Keep HTML/CSS/JavaScript tidy; indent with 4 spaces.
- Add comments for non-obvious logic.

## Testing
- Manually test new UI elements in the browser.
- Ensure server API endpoints still work.
- Add automated tests if the project later includes a test suite.

## After Merge
Once your PR is reviewed and merged:
- Pull the latest changes into your fork:
  ```bash
  git checkout master
  git pull upstream master
  ```
- Delete your feature branch to keep things clean.

## Thank You
Your contributions help make the Realstate project better for everyone. Happy coding! 🚀