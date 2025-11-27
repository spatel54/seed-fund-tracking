# IWRC Fonts

## Montserrat Font Family

The official typeface for the Illinois Water Resources Center is **Montserrat**, a geometric sans-serif font designed by Julieta Ulanovsky.

## Available Weights

### Montserrat Regular
**File:** `Montserrat-Regular.ttf`
- **Size:** 323 KB
- **Weight:** 400 (Regular)
- **Use Cases:** Body text, paragraphs, descriptions, general content

### Montserrat Bold
**File:** `Montserrat-Bold.ttf`
- **Size:** 328 KB
- **Weight:** 700 (Bold)
- **Use Cases:** Headings, titles, emphasis, call-to-actions, labels

## Typography Guidelines

### Headings
- **H1:** Montserrat Bold, 32-48px
- **H2:** Montserrat Bold, 24-32px
- **H3:** Montserrat Bold, 20-24px
- **H4:** Montserrat SemiBold, 18-20px

### Body Text
- **Paragraphs:** Montserrat Regular, 14-16px
- **Small Text:** Montserrat Regular, 12-14px
- **Line Height:** 1.5-1.6 for optimal readability

### Color Pairings
- **Headings:** #258372 (Primary Teal) or #54595F (Text Gray)
- **Body Text:** #54595F (Text Gray)
- **Light Text:** #666666 or #555555

## Web Usage

### CSS Font-Face
```css
@font-face {
    font-family: 'Montserrat';
    src: url('assets/branding/fonts/Montserrat-Regular.ttf') format('truetype');
    font-weight: 400;
    font-style: normal;
}

@font-face {
    font-family: 'Montserrat';
    src: url('assets/branding/fonts/Montserrat-Bold.ttf') format('truetype');
    font-weight: 700;
    font-style: normal;
}
```

### Google Fonts Alternative
For web projects with CDN access:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap" rel="stylesheet">
```

## PDF/Print Usage

### Embedding in PDFs
- Always embed fonts in PDF reports
- Use TrueType (TTF) format
- Subset fonts if file size is a concern

### matplotlib/Python
```python
from matplotlib import font_manager

font_path = 'assets/branding/fonts/Montserrat-Regular.ttf'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Montserrat'
```

### ReportLab (PDF Generation)
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Montserrat', 'assets/branding/fonts/Montserrat-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Montserrat-Bold', 'assets/branding/fonts/Montserrat-Bold.ttf'))
```

## Font Characteristics

- **Style:** Geometric Sans-Serif
- **Character Set:** Latin Extended
- **Numerical:** Tabular and Proportional figures
- **Readability:** Excellent at all sizes
- **Professional:** Modern, clean, approachable

## License

Montserrat is licensed under the SIL Open Font License (OFL). Free for commercial and personal use.

## Questions?

For complete brand guidelines, see [IWRC_BRANDING_GUIDELINES.md](../IWRC_BRANDING_GUIDELINES.md).
