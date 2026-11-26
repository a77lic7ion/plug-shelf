---
version: alpha
name: Plug Shelf
description: A restrained, instrument-like catalogue for Shaun's Omarchy shell plugins.
colors:
  primary: "#0B0C0E"
  secondary: "#15181B"
  tertiary: "#E8875A"
  neutral: "#F1EDE6"
  on-primary: "#F1EDE6"
  on-tertiary: "#14100D"
  muted: "#9A9C99"
  line: "#2A2E32"
  signal: "#61D6FF"
  success: "#86D993"
  warning: "#E2C275"
typography:
  h1:
    fontFamily: Liberation Sans
    fontSize: 3.25rem
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.035em"
  h2:
    fontFamily: Liberation Sans
    fontSize: 1.75rem
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: Liberation Sans
    fontSize: 0.9375rem
    lineHeight: 1.55
  label-caps:
    fontFamily: "JetBrainsMono Nerd Font"
    fontSize: 0.6875rem
    fontWeight: 700
    letterSpacing: "0.12em"
  mono:
    fontFamily: "JetBrainsMono Nerd Font"
    fontSize: 0.8125rem
    lineHeight: 1.6
rounded:
  sm: 3px
  md: 6px
  lg: 12px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-ghost:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
    padding: 12px
  card:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
    padding: 16px
  badge:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.muted}"
    rounded: "{rounded.full}"
    padding: 4px
  inspector:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 24px
  card-border:
    backgroundColor: "{colors.line}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 0
  state-listed:
    backgroundColor: "{colors.success}"
    textColor: "{colors.primary}"
    rounded: "{rounded.full}"
    padding: 3px
  state-submitted:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.primary}"
    rounded: "{rounded.full}"
    padding: 3px
  accent-signal:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 0
---

## Overview

Plug Shelf is a personal registry for shell plugins: browsable, filterable, and
quiet. It takes the marketplace's command-first posture (copy the install, see
the state, move on) but rejects its masthead-and-carousel composition. The page
reads like a well-kept workbench index: numbered entries, hairline dividers,
monospace metadata, and one accent used only for action and focus.

Two accent modes share the same geometry. **Ember** uses the warm copper
tertiary token and sits closest to the Omarchy marketplace's warmth without
copying its orange. **Signal** uses the cyan token from the Hermarchy design
system already on this machine, for a cooler instrument-panel reading.

## Colors

- **Primary (#0B0C0E):** Near-black canvas and inspector backdrop.
- **Secondary (#15181B):** Raised surfaces: cards, filter rail, inspector.
- **Tertiary (#E8875A):** Sole interaction driver in Ember mode: focus rings,
  active filters, copy feedback. Never a background wash.
- **Signal (#61D6FF):** Alternate interaction driver in Signal mode.
- **Neutral (#F1EDE6):** Warm bone text, not pure white.
- **Muted (#9A9C99):** Metadata, captions, inactive labels.
- **Line (#2A2E32):** Hairline borders; structure without boxes.
- **Success (#86D993):** "Listed" state only. Warning amber is "submitted".

## Typography

Liberation Sans is the installed local stand-in for a neutral grotesque; no
web fonts are fetched. JetBrains Mono Nerd Font carries every label, command,
version and id, so the catalogue reads like a terminal index rather than a
marketing page. Display sizes are tight; body copy is ordinary and unstyled.

## Layout

Left-aligned masthead, then a two-column body: a narrow filter rail and the
entry grid. Cards use a 4px baseline and 3px corners. The detail view is an
inspector drawer, not a separate page: browsing context stays visible behind
it. Mobile collapses to one column and the drawer becomes full-width.

## Shapes

Nearly square. Hairline borders, no glow, no drop shadows on resting cards, no
glass. Corners at `sm` for controls and cards, `md` for the inspector only.

## Components

`button-primary` is the copy-install action on the selected entry; every other
button is `button-ghost`. `card` is one plugin entry with a top sample image or
a typographic placeholder. `badge` marks listed / submitted / local state.
`inspector` holds README content, screenshots and the install command.

## Do's and Don'ts

- **Do** keep every command in a real `<code>` block with a working copy button.
- **Do** show which plugins are local-only; never invent a public URL for them.
- **Don't** add a centered hero with three feature cards. This is an Explore
  surface: filters and entries are the composition.
- **Don't** use gradients, purple accents, emoji, or thick coloured card rails.
