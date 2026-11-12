PS STEEL - WEB LOGO PACK (all PNGs have transparent background)

favicons/
  favicon.ico (16/32/48/64), favicon-16x16, favicon-32x32, favicon-48x48
  apple-touch-icon.png (180), android-chrome-192x192, android-chrome-512x512, mstile-150x150
  site.webmanifest, browserconfig.xml
  paste-in-head.html  -> copy these tags into your <head>
  (favicons use only the "PS" mark so they stay readable at small sizes)

logo/
  logo-full-2000/1000/512/256.png : complete logo (ring + PS + text), square canvas
  logo-full-tight-master.png      : full logo, tightly cropped, highest quality master
  logo-header-h40/h56/h80.png and @2x : full logo by height, for website header (use @2x with srcset)
  logo-mark-512/256/128/64.png    : PS mark only (no ring, no text)

Example header usage:
<img src="/logo/logo-header-h56.png" srcset="/logo/logo-header-h56@2x.png 2x" height="56" alt="PS Steel">

Note: logo artwork is dark/metallic, so it looks best on light backgrounds.
