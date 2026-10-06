from pathlib import Path
root=Path(__file__).resolve().parent.parent
source=(root/'dist/index.html').read_text()
source=source.replace('/assets/style.css','/assets/premium-preview.css').replace('/assets/site.js','/assets/premium-preview.js')
source=source.replace('<title>İzmir Oto Çekiciniz | 7/24 Çekici ve Yol Yardım</title>','<title>Tasarım Önizlemesi | İzmir Oto Çekiciniz</title>')
source=source.replace('<meta name="theme-color" content="#101b29">','<meta name="theme-color" content="#050a16">')
source=source.replace('<body>','<body><div class="preview-note">Tasarım önizlemesi · Onayınızdan sonra tüm sayfalara uygulanacak.</div>')
source=source.replace('<button class="menu-button" aria-expanded="false" aria-controls="main-nav">Menü</button>','<button class="menu-button" aria-label="Menüyü aç" aria-expanded="false" aria-controls="main-nav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button><div class="menu-scrim" aria-hidden="true"></div>')
source=source.replace('id="main-nav" aria-label="Ana menü">','id="main-nav" aria-label="Ana menü"><div class="drawer-heading"><span>İZMİR OTO ÇEKİCİNİZ</span><button class="drawer-close" aria-label="Menüyü kapat"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button></div>')
source=source.replace('</nav></div></header>','<div class="drawer-contact"><small>7 gün, 24 saat iletişim</small><a class="btn" href="tel:+905366762866">0536 676 28 66</a><a class="btn secondary" href="https://wa.me/905366762866">WhatsApp ile yazın</a></div></nav></div></header>')
start=source.index('<section class="hero">');end=source.index('<div class="ribbon">',start)
old=source[start:end];copy_start=old.index('<span class="eyebrow">');copy_end=old.rfind('</div></section>');copy=old[copy_start:copy_end]
copy=copy.replace('Yolda kaldığınızda<br><em>yanınızdayız.</em>','İzmir’de oto çekici.<br><em>Yolun her anında yanınızda.</em>')
visual='<div class="hero-visual"><img class="hero-photo" src="/assets/hero.jpg" alt="İzmir oto çekici ve araç taşıma" width="1600" height="684" fetchpriority="high"><div class="hero-image-caption"><strong>7/24</strong><span>OTO ÇEKİCİ & YOL YARDIM<br>GAZİEMİR · MENDERES · İZMİR</span></div></div>'
source=source[:start]+'<section class="hero"><div class="wrap hero-shell"><div class="hero-copy">'+copy+'</div>'+visual+'</div></section>'+source[end:]
target=root/'dist/tasarim-onizleme';target.mkdir(exist_ok=True);(target/'index.html').write_text(source)
for src,dst in [('premium.css','premium-preview.css'),('premium.js','premium-preview.js')]:
 (root/'dist/assets'/dst).write_text((root/'design-preview'/src).read_text())
print('Tasarım önizlemesi hazır: /tasarim-onizleme/')
