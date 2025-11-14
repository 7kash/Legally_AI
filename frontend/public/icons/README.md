# PWA Icons

This directory contains the icons for the Progressive Web App (PWA) manifest.

## Generated Icons ✅

The PNG icons have been generated from the SVG source:
- ✅ `icon-192x192.png` - 192x192 PWA icon (3.0KB)
- ✅ `icon-512x512.png` - 512x512 PWA icon (8.8KB)

## Source

- `icon.svg` - Source SVG icon (512x512)

## Regenerate Icons

To regenerate the icons from the SVG source:

```bash
cd /home/user/Legally_AI/frontend
npm run icons
```

This runs the `scripts/generate-icons.mjs` script which uses sharp to convert the SVG to PNG at the required sizes.

## Manual Generation Methods

If you need to regenerate manually without the script:

### Method 1: Using Squoosh (Online)

1. Open [Squoosh.app](https://squoosh.app/)
2. Upload `icon.svg`
3. Resize to 192x192, download as `icon-192x192.png`
4. Resize to 512x512, download as `icon-512x512.png`
5. Place both files in this directory

### Method 2: Using ImageMagick (Command Line)

```bash
# Install ImageMagick if not already installed
# macOS: brew install imagemagick
# Ubuntu: sudo apt-get install imagemagick

# Generate 192x192 icon
convert icon.svg -resize 192x192 icon-192x192.png

# Generate 512x512 icon
convert icon.svg -resize 512x512 icon-512x512.png
```

### Method 3: Using Figma/Sketch/Adobe XD

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
4. Regenerate PNG files with `npm run icons`

## PWA Manifest

These icons are referenced in `nuxt.config.ts`:

```typescript
pwa: {
  manifest: {
    icons: [
      {
        src: '/icons/icon-192x192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icons/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  },
}
```

## Testing

After generating the icons:

1. Build the app: `npm run build`
2. Serve locally: `npm run preview`
3. Open Chrome DevTools > Application > Manifest
4. Verify icons are loading correctly
5. Test "Install App" functionality

---

**Created**: 2025-11-09
**Status**: ✅ Icons generated and ready for PWA
