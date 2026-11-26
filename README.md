# Plug Shelf

A local, static catalogue of the Omarchy shell plugins Shaun built. It looks and behaves like a small workbench index: filter the shelf, inspect a plugin, copy the install command.

No build step, no server code, no accounts, no API keys. The whole folder can be uploaded to any static host as-is.

## Open it now

The editable copy runs locally on port 8902 on this machine. The exact laptop, WiFi and Tailscale addresses are recorded in the project note in Obsidian. The read-only public build has no edit controls.

- Live site: https://plug-shelf.vercel.app
- Source: https://github.com/a77lic7ion/plug-shelf

## Edit a plugin

1. Click **Edit shelf** in the top right. The button turns accent-coloured and the cards get dashed borders.
2. Click any card (or its **Edit** button). The inspector opens on the **Edit** tab.
3. Change the **Description** or **Install command**. Changes save in this browser as you type.
4. Under **Screenshots**:
   - **Replace** changes the image on that row.
   - **Remove** deletes that image.
   - **Add screenshots** adds as many as you like. Each gets a caption box you can rename.
   - Images are resized to 1200px and saved as JPEG inside the browser, to stop big files filling browser storage.
5. Click **Preview** to see exactly what visitors will see, including the copyable code block for the install command.
6. Click **Reset this plugin** to throw away your changes for that one plugin only.

Edits stay in this browser until you export them. That is intentional: nothing is sent anywhere.

## Publish your edits

1. Click **Export** in the top right. A file called `edits.json` is downloaded.
2. Copy that file into this project folder, replacing the existing `edits.json` (currently just `{}`).
3. Reload the page. Everyone who opens the site now sees your changes.

If your browser still shows the old version, your local edits are taking priority. Use **Reset this plugin** for the affected plugin, or clear this site's storage in the browser. Published changes in `edits.json` are the source of truth for visitors.

## Public build

`build-live.py` generates `live/`: the same site with **Edit shelf** and **Export** removed, three screenshots held back, and no local edit controls. The held-back captures are Server Kill (internal addresses), the GW2 API key settings panel, and a stray browser-tab screenshot. That folder is what Vercel serves. The editable copy stays on this machine with all original and added images.

To host: upload the generated `live/` folder to any static host, or import the repo into Vercel, which runs the build script and serves `live/`. No configuration or secrets are needed.

## Files

- `index.html` — the editable local site: markup, styles, plugin data and edit logic
- `DESIGN.md` — the token spec and design rationale (lints clean with `@google/design.md`)
- `edits.json` — published overrides, one entry per plugin slug
- `assets/` — screenshots shipped with the first version
- `build-live.py` — regenerates the read-only public build
- `live/` — generated public build; do not hand-edit

## Keyboard

- `/` focuses the search box
- `Esc` closes the inspector
- `Enter` opens the focused card
