---
version: alpha
name: NovaLink Landing Design System
---

## Overview

Design system for the NovaLink interactive landing page — a business automation and IoT platform. The page follows a conversion-first approach: deliver value through interactive demos before requesting contact information.

**Palette direction**: Black, white, and logo green (`#20E070`). High-contrast, modern, tech-forward.

## Colors

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#F8F9FA` | Main page background (light sections) |
| `--bg-dark` | `#000000` | Dark sections (hero, ROI output, testimonials, services photos, footer, CTA band, FAQ cta) |
| `--bg-card` | `#FFFFFF` | Card surfaces on light backgrounds |
| `--accent` | `#20E070` | Primary CTAs, highlights, metric numbers — matches logo green |
| `--accent-hover` | `#1cc060` | Button hover state |
| `--accent-glow` | `rgba(32,224,112,0.18)` | Radial glows, focus rings |
| `--text` | `#1A1A2E` | Primary body text |
| `--text-muted` | `#6B7280` | Secondary text, descriptions |
| `--border` | `#E5E7EB` | Card and section borders |
| `--border-light` | `#F3F4F6` | Subtle backgrounds (tab pills) |

Dark-mode overrides on dark sections use `color: #fff` and `rgba(255,255,255,x)` for muted text.

Nav bar uses `rgba(0,0,0,0.92)` background with white text. Mobile menu uses pure black background.

Green accent (`#20E070`) is used on black backgrounds for maximum contrast and legibility. White text on black; green used sparingly for metrics, CTAs, and highlights.

## Typography

| Token | Stack | Usage |
|---|---|---|
| Headings | `'Poppins', sans-serif` | All h1-h4, section labels, nav logo |
| Mono | `'JetBrains Mono', monospace` | Metric numbers, ROI values, counters |
| Body | `system-ui, -apple-system, sans-serif` | Paragraphs, form inputs, buttons |

- Minimum body size: 16px
- Heading weight: 700–800
- Letter-spacing on headings: `-0.02em` to `-0.03em`
- Section labels: 0.8rem, 600 weight, 0.08em letter-spacing, uppercase, accent color

## Rounded

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | `8px` | Buttons, small cards, inputs |
| `--radius` | `12px` | Cards, panels |
| `--radius-lg` | `20px` | Large containers, hero dashboard, testimonial cards |
| Full pill | `99px` | Badges, tab pills, chip metrics |

## Spacing

| Token | Value | Usage |
|---|---|---|
| Section gap | `clamp(48px, 8vw, 100px)` | Vertical spacing between sections |
| Container padding | `clamp(16px, 4vw, 40px)` | Horizontal padding within `.container` |
| Max content width | `1200px` | `.container` max-width |
| Nav height | `68px` | Fixed navigation bar |

## Assets

| Asset | Path | Usage |
|---|---|---|
| Logo PNG | `assets/images/nova-link-logotipo.png` | Nav bar and footer branding |
| Excel (Antes) | `assets/images/excel.jpg` | Before/after slider — before side (with red overlay) |
| Tablet Dashboard | `assets/images/tablet-dashboard.webp` | Before/after slider — after side (with green overlay) |
| IoT Photo | `assets/images/IOT.jpg` | Services photo card |
| Security Photo | `assets/images/security.jpg` | Services photo card |
| Software Dev & Cloud | `assets/images/softwaredev&cloud.jpg` | Services photo card |

## Components

### Buttons
- `.btn`: 13px 28px padding, 600 weight, 0.95rem, flex with gap
- `.btn-primary`: accent bg (`#20E070`), black text (contrast on green), green glow shadow, hover lifts 2px
- `.btn-outline`: transparent, white border, for dark backgrounds

### Cards
- Light: white bg, 1px border, 12px radius, hover elevates shadow and border turns accent green
- Dark: `rgba(255,255,255,0.04)` bg, subtle border, used in testimonials and ROI output

### Sliders
- Track: 8px height, rounded, `var(--border)` on light, `rgba(255,255,255,0.12)` on dark
- Thumb: 24px circle, accent color (`#20E070`), white border, green glow shadow

### Tabs
- Pill-shaped buttons, 99px radius
- Inactive: light gray bg, muted text
- Active: black bg, white text

### Navigation
- Fixed top, black background (`rgba(0,0,0,0.92)`) with backdrop blur
- Logo: `assets/images/nova-link-logotipo.png` — "Nova" in white, "Link" in `#20E070`
- Mobile: slide-in panel from right, pure black background
- Hamburger icon: white bars

### Service Photo Cards
- Three-column grid of photo cards for IoT, Security, and Software & Cloud
- 4:3 aspect ratio, black fallback background with gradient
- Images: `assets/images/IOT.jpg`, `assets/images/security.jpg`, `assets/images/softwaredev&cloud.jpg`
- Gradient overlay from bottom, green accent tag pill, white title, muted description
- Hover: image scales 1.05×
- Stack to single column on mobile

## Logo

The NovaLink logo is `assets/logo/novalink-logo.svg`:
- "Nova" in white (`#ffffff`)
- "Link" in green (`#20E070`)
- Font: Inter, 900 weight, 32px
- Used in nav bar and footer

## Interactive Features

- **ROI Calculator**: 3 range sliders with real-time computed output (animated transitions)
- **Before/After Slider**: Draggable comparison with mouse and touch support; "before" side in navy red tones, "after" side in dark green tones
- **Industry Tabs**: 5-tab panel switcher with fade animation
- **Testimonial Carousel**: Horizontal track with dot indicators and prev/next arrows
- **Animated Counters**: IntersectionObserver-triggered count-up on scroll
- **FAQ Accordion**: Expandable items with real-time search filter
- **Chatbot Widget**: Fixed bottom-right, keyword-matched replies, suggestion chips; green toggle button

## API Backend

The NovaLink Assistant is powered by a FastAPI backend at `/api/chat`:

- **POST /api/chat**: Receives `{message, session_id, step}` → returns `{session_id, bot_message, suggestions, step}`
- **GET /api/health**: Health check
- Session state is stored in-memory with UUID-based session IDs
- Leads are persisted to `/data/leads.json` as JSON array

### Conversation Flow

| Step | Action | Response |
|---|---|---|
| 0 | Init | Welcome + 14 industry options |
| 1 | Industry selected | Confirm + 12 process options |
| 2 | Processes selected | Confirm + 5 company size options |
| 3 | Size selected | Request email |
| 4 | Email received | Generate analysis, save lead, offer demo |

### LLM Integration

The `call_llm()` function in `api/main.py` is a placeholder ready for connection to DeepSeek, OpenAI, or any compatible API. Set environment variables `LLM_API_KEY` and `LLM_MODEL` when ready.

### Docker

- `novalink-api`: Python 3.12 FastAPI service on port 8000
- `novalink-web`: Nginx reverse proxy — `/api/*` → `novalink-api:8000`
- Leads persisted via Docker volume `novalink_data`

## Responsive Breakpoints

- `<= 640px`: Single column, stacked CTAs, collapsed dashboard grid, services photos stack, full-width chatbot
- `<= 840px`: Hamburger nav menu (slide-in from right, black background)
- `> 840px`: Full horizontal nav, multi-column grids, desktop chatbot window

## Motion

- Page-load reveals: staggered `fadeInUp` (0.6s, 0.1s delays)
- Hero glow: 6s pulse animation
- Floating nodes: 8s vertical float with staggered delays
- Hero lines: 10s horizontal scanning animation
- Tab panels: 0.35s fade with 8px upward slide
- Testimonial track: 0.5s cubic-bezier slide
- Chatbot messages: 0.3s fade-slide-in
- ROI numbers: 0.2s scale bounce on update
- Hover: 0.2–0.25s transitions on buttons and cards
- Photo cards: 0.5s image scale on hover
- All animations gated behind `@media (prefers-reduced-motion: reduce)`
