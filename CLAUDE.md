# CLAUDE.md

This file provides guidance for AI assistants working in this repository.

## Project Overview

Personal blog and portfolio site hosted on GitHub Pages at [ucpwang.github.io](http://ucpwang.github.io). The site has two distinct sections:

1. **Root-level blog** — Static HTML files with client-side Markdown rendering via Strapdown.js
2. **Portfolio site** (`jacobs_mac_house/`) — Full multi-page portfolio with Bootstrap Clean Blog theme

## Repository Structure

```
ucpwang.github.io/
├── index.html                    # Main landing page / blog index
├── README.md                     # Minimal project description
├── bower.json                    # Front-end dependency manifest
├── CLAUDE.md                     # This file
├── images/                       # Blog post images (PNG)
├── js/
│   ├── clean-blog.js             # Blog theme JS (~1057 lines)
│   └── clean-blog.min.js         # Minified version
├── jacobs_mac_house/             # Portfolio subdirectory (~36 MB)
│   ├── index.html                # Portfolio landing page
│   ├── about.html                # About page
│   ├── contact.html              # Contact page
│   ├── post.html                 # Blog post template
│   ├── css/                      # Compiled CSS (Bootstrap + Clean Blog theme)
│   ├── less/                     # LESS source files
│   │   ├── clean-blog.less       # Main theme LESS
│   │   ├── variables.less        # Theme variables
│   │   └── mixins.less           # LESS mixins
│   └── ...                       # AdminLTE, GreenSock, other vendor libs
└── 20YYMMDD_topic_name.*         # Blog posts (paired .md + .html files)
```

## Blog Post Convention

Blog posts follow a strict naming convention:

```
YYYYMMDD_topic_subtitle.md    # Markdown source
YYYYMMDD_topic_subtitle.html  # Rendered HTML wrapper
```

### How blog posts work

Each `.html` file wraps the Markdown in a `<textarea>` element that Strapdown.js renders client-side:

```html
<!DOCTYPE html>
<html>
<head>...</head>
<body>
<textarea theme="united">
# My Blog Post Title

Markdown content here...
</textarea>
<script src="http://strapdownjs.com/v/0.2/strapdown.js"></script>
</body>
</html>
```

The `.md` file contains the raw Markdown source.

**To add a new blog post:**
1. Create `YYYYMMDD_topic_name.md` with Markdown content
2. Create `YYYYMMDD_topic_name.html` using the Strapdown.js template above
3. Add a link entry to `index.html` in the blog listing section

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Hosting | GitHub Pages (static) |
| CSS Framework | Bootstrap 3.3.5 (CDN) |
| Blog Theme | StartBootstrap Clean Blog |
| CSS Preprocessor | LESS (source in `jacobs_mac_house/less/`) |
| Markdown Rendering | Strapdown.js (CDN, client-side) |
| Package Manager | Bower (front-end deps) |
| Icons | Font Awesome 4.1.0 |
| Fonts | Google Fonts (Lora, Open Sans) |

## Styling Conventions

- Primary color: `#0085a1` (teal) for links and accents
- Body text: `#404040` (dark gray)
- Body font: Lora (serif)
- Heading font: Open Sans (sans-serif)
- **Do not edit compiled CSS** in `jacobs_mac_house/css/` directly — edit the LESS sources in `jacobs_mac_house/less/` instead

### Theme Switcher

`index.html` includes a JavaScript snippet that randomly selects one of 7 Bootstrap CDN themes on page load:

- Cerulean, Cyborg, Journal, Simplex, Slate, Spacelab, United

## Development Workflow

### No build step at root level

The root-level blog requires no build process. HTML, CSS, and JS files are served directly by GitHub Pages.

### LESS compilation (portfolio section only)

The `jacobs_mac_house/` directory has a Grunt-based build (AdminLTE 2.3.0):

```bash
cd jacobs_mac_house
npm install     # install grunt and plugins
grunt           # compile LESS, minify CSS/JS, optimize images
grunt watch     # watch for changes
```

### Deploying

Push to `master` branch — GitHub Pages deploys automatically. There is no CI/CD pipeline.

```bash
git push origin master
```

## Branch Strategy

- `master` — production branch, auto-deployed to GitHub Pages
- Feature branches follow the pattern `<source>/description-suffix` (e.g., `claude/add-feature-XYZ`, `copilot/description`)

## Content Guidelines

- Blog posts are written in Korean or English (existing posts are in Korean)
- Images go in `/images/` directory
- Keep image sizes reasonable for web (existing images: 97 KB–363 KB)
- Avoid committing large binary files or vendor libraries unless necessary

## Key Files Reference

| File | Purpose |
|------|---------|
| `index.html` | Blog index — update this when adding new posts |
| `bower.json` | Front-end dependency manifest (Bootstrap, jQuery, etc.) |
| `js/clean-blog.js` | Main blog interactivity (navbar, smooth scroll, etc.) |
| `jacobs_mac_house/less/variables.less` | Theme color/font variables — edit to change visual style |

## What to Avoid

- Do not modify files inside `jacobs_mac_house/` vendor directories (`AdminLTE/`, `startbootstrap-clean-blog-gh-pages/`, etc.)
- Do not push directly to `master` when working on a feature — use a feature branch
- Do not add `node_modules/` or `bower_components/` to the repository (they are gitignored)
- The `jacobs_mac_house/` directory is ~36 MB — avoid adding more large assets
