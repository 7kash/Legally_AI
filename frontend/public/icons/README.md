# PWA Icons

This directory contains the icons for the Progressive Web App (PWA) manifest.

## Current Status

- ✅ `icon.svg` - Source SVG icon (512x512)
- ⏳ `icon-192x192.png` - Needs to be generated
- ⏳ `icon-512x512.png` - Needs to be generated

## How to Generate PNG Icons

### Option 1: Using Online Tools

1. Open [Squoosh.app](https://squoosh.app/)
2. Upload `icon.svg`
3. Resize to 192x192, download as `icon-192x192.png`
4. Resize to 512x512, download as `icon-512x512.png`
5. Place both files in this directory

### Option 2: Using ImageMagick (Command Line)

```bash
# Install ImageMagick if not already installed
# macOS: brew install imagemagick
# Ubuntu: sudo apt-get install imagemagick

# Generate 192x192 icon
convert icon.svg -resize 192x192 icon-192x192.png

# Generate 512x512 icon
convert icon.svg -resize 512x512 icon-512x512.png
```

### Option 3: Using Node.js (Sharp)

```bash
# Install sharp
npm install --save-dev sharp sharp-cli

# Generate icons
npx sharp -i icon.svg -o icon-192x192.png resize 192 192
npx sharp -i icon.svg -o icon-512x512.png resize 512 512
```

### Option 4: Using Figma/Sketch/Adobe XD

1. Import `icon.svg` into your design tool
2. Export as PNG at 192x192px and 512x512px
3. Ensure resolution is 72 DPI minimum (144 DPI recommended for retina)

## Design Notes

The current icon features:
- **Primary color**: #0ea5e9 (sky-500 from Tailwind)
- **Icon**: Scale of justice with "LA" text
- **Style**: Modern, minimalist, professional
- **Format**: SVG (scalable vector)

## Customization

To customize the icon:

1. Edit `icon.svg` directly (it's just XML)
2. Or use a vector editor (Figma, Inkscape, Adobe Illustrator)
3. Keep dimensions at 512x512 for best quality
4. Regenerate PNG files after changes

## PWA Manifest

These icons are referenced in `/public/manifest.json`:

```json
{
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

Once PNG files are generated, the PWA will be fully functional for installation.

## Testing

After generating the icons:

1. Build the app: `npm run build`
2. Serve locally: `npm run preview`
3. Open Chrome DevTools > Application > Manifest
4. Verify icons are loading correctly
5. Test "Install App" functionality

---

**Created**: 2025-11-09
**Status**: SVG placeholder ready, PNG generation pending
