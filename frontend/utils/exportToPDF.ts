/**
 * PDF Export Utility
 * Export analysis results to PDF
 */

export interface PDFExportOptions {
  title: string
  content: Record<string, any>
  metadata?: {
    contractName?: string
    analysisDate?: string
    confidenceScore?: number
  }
}

/**
 * Export analysis to PDF
 * Note: This is a placeholder implementation
 * In production, you would use a library like jsPDF or pdfmake
 */
export async function exportAnalysisToPDF(options: PDFExportOptions): Promise<void> {
  const { title, content, metadata } = options

  // Create a formatted text version of the analysis
  let pdfContent = `${title}\n`
  pdfContent += `${'='.repeat(title.length)}\n\n`

  if (metadata) {
    if (metadata.contractName) {
      pdfContent += `Contract: ${metadata.contractName}\n`
    }
    if (metadata.analysisDate) {
      pdfContent += `Analysis Date: ${metadata.analysisDate}\n`
    }
    if (metadata.confidenceScore !== undefined) {
      pdfContent += `Confidence Score: ${Math.round(metadata.confidenceScore * 100)}%\n`
    }
    pdfContent += '\n'
  }

  // Format each section
  for (const [key, value] of Object.entries(content)) {
    const sectionTitle = formatSectionTitle(key)
    pdfContent += `\n${sectionTitle}\n`
    pdfContent += `${'-'.repeat(sectionTitle.length)}\n\n`

    if (Array.isArray(value)) {
      value.forEach((item, index) => {
        pdfContent += `${index + 1}. ${item}\n`
      })
    } else if (typeof value === 'object' && value !== null) {
      for (const [subKey, subValue] of Object.entries(value)) {
        pdfContent += `${formatKey(subKey)}: ${subValue}\n`
      }
    } else {
      pdfContent += `${value}\n`
    }
    pdfContent += '\n'
  }

  // Create a blob and download
  const blob = new Blob([pdfContent], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = url
  link.download = `${sanitizeFilename(title)}.txt`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  URL.revokeObjectURL(url)
}

function formatSectionTitle(key: string): string {
  return key
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function formatKey(key: string | number): string {
  if (typeof key === 'number') return `${key + 1}`

  return String(key)
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function sanitizeFilename(filename: string): string {
  return filename
    .replace(/[^a-z0-9]/gi, '_')
    .replace(/_+/g, '_')
    .toLowerCase()
}
