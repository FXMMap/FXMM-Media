# FXMM · Plantillas de diseño

Plantillas para producir las piezas de redes de FXMM con el mismo diseño. Reglas de contenido y de cada red: Drive, carpeta "FXMM · Redes sociales (manual y registro)", doc "00 · LEEME" y "02 · Rol de cada red social FXMM".

Requisitos: Python 3 con Playwright (Chromium) y Pillow; ffmpeg para videos. Cada carpeta trae sus tipografías y logos; ejecutar los scripts desde dentro de su carpeta.

## carousel/ · Carruseles de Instagram (1080x1350)
- `lib.py` (+ `head.py`): base. `build(S, prefijo, idioma, navy=True/False)` genera las láminas y una hoja de revisión `<prefijo>_sheet.png`.
- Ejemplos: `c20_example.py` (claro, ES), `c24.py` (claro, EN), `c26.py` (navy, ES), `c30.py` (navy, EN), `c19.py` (post único navy).
- Helpers: `num()` (número + etiqueta), `candles()` (gráfico de velas con zona de interés).
- Regla: alternar azul/blanco post a post en el feed.

## reel/ · Reels verticales (1080x1920, 15 s + 2,5 s de cierre)
- `vv.html` contiene las escenas L, N y F (`?v=L`), tema navy con `&th=n`.
- `python3 render.py L n` renderiza los cuadros en `frLn/`; `keys.py`/`keysn.py` sacan cuadros clave.
- Video: `ffmpeg -framerate 30 -i frL/%05d.jpg ...`; mezcla con voz (María Pía, ElevenLabs oLubJSiUwnyPk50fJzYd, atempo 1.10, delay 400 ms) y música a 0,22 con fades. En Buffer, fijar portada con thumbnailOffset (~11000 ms).

## xcard/ · Cards de X (1600x900 aprox.)
- `python3 card3.py w5L.json D salida/` (D = claro, N = navy). El JSON mapea archivo -> [etiqueta, "Título <b>remate en azul.</b>"]. Depende de `card.py`.

## xvideo/ · Videos de X (1920x1080)
- `v.html` escenas A, B, C; `python3 render.py A`.

## linkedin/ · Posts de LinkedIn (1200x1500)
- `photoposts.py`: función `post(foto, recorte, línea1, línea2, nombre)`: franja navy con titular en dos colores + foto realista (ElevenLabs bytedance-seedream-5-pro, 16:9). Usa Inter y Poppins de `../fonts/`; ajustar rutas si hace falta.

## story/ · Historias de artículos de Substack (1080x1920)
- `st3.py`: navy, "NEW ON The Market Map" (Lora cursiva), portada del artículo, píldora blanca con el ícono oficial de Substack (`ss_icon.png`, sin modificar) y "Free newsletter, twice a week". Necesita la portada del artículo (de `../../substack/`) y Lora en `../fonts/`.

## substack_mock/ · Mockup de un artículo como se ve en Substack
- `build.py` (texto en HTML o Markdown + portada).

## fonts/ y brand/
- Poppins, JetBrains Mono, Inter, Lora. Kit de marca en `../brand/`.

Colores: navy #0D182E, azul #007DFF, acento #0060C7 (claro) / #62A5F4 (navy), crema #F7F6F2, gris #F4F6F9, verde #15875B, rojo #CC3A3F. Gráficos siempre en velas.
