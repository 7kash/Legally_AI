/**
 * Generate PWA icons from SVG source
 * Run with: node scripts/generate-icons.mjs
 */

import { readFile, writeFile } from 'fs/promises'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import sharp from 'sharp'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const sizes = [
  { size: 192, name: 'icon-192x192.png' },
  { size: 512, name: 'icon-512x512.png' },
]

async function generateIcons() {
  const svgPath = join(__dirname, '../public/icons/icon.svg')
  const outputDir = join(__dirname, '../public/icons')

  console.log('Reading SVG file...')
  const svgBuffer = await readFile(svgPath)

  for (const { size, name } of sizes) {
    console.log(`Generating ${name}...`)

    try {
      await sharp(svgBuffer)
        .resize(size, size, {
          fit: 'contain',
          background: { r: 14, g: 165, b: 233, alpha: 1 }, // #0ea5e9
        })
        .png()
        .toFile(join(outputDir, name))

      console.log(`✅ Generated ${name}`)
    } catch (error) {
      console.error(`❌ Failed to generate ${name}:`, error.message)
    }
  }

  console.log('\n✅ All icons generated successfully!')
}

generateIcons().catch((error) => {
  console.error('Error generating icons:', error)
  process.exit(1)
})
