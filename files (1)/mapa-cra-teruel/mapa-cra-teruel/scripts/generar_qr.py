"""Genera el QR.  Uso:  python scripts/generar_qr.py https://TU-USUARIO.github.io/mapa-cra-teruel/
Necesita:  pip install "qrcode[pil]" """
import sys
try:
    import qrcode
except ImportError:
    sys.exit('Falta la librería. Ejecuta: pip install "qrcode[pil]"')
if len(sys.argv) < 2: sys.exit(__doc__)
qrcode.make(sys.argv[1], box_size=14, border=4).save('qr-mapa-cra-teruel.png')
print('Guardado: qr-mapa-cra-teruel.png')
