"""Inject the logo masks (extracted from the MACAI manual) into the viewer template."""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
logos = json.loads(pathlib.Path(sys.argv[1]).read_text())
html = (here / 'macai_cart.template.html').read_text().replace('/*__LOGOS__*/null', json.dumps(logos))
(here.parent / 'macai_cart.html').write_text(html)
print('wrote', here.parent / 'macai_cart.html', len(html))
