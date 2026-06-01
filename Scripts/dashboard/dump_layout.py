import zipfile, json, os

pbix = os.path.join(os.path.dirname(__file__), "Dashboard Métricas P&C.pbix")
with zipfile.ZipFile(pbix, 'r') as z:
    with z.open('Report/Layout') as f:
        raw = f.read().decode('utf-16-le')
        data = json.loads(raw)
        for page in data.get('sections', []):
            pname = page.get('displayName')
            ordinal = page.get('ordinal')
            vis = page.get('visibility', 0)
            print("=== PAGE: " + str(pname) + " | ordinal: " + str(ordinal) + " | visible: " + str(vis))
            for v in page.get('visualContainers', []):
                cfg = json.loads(v.get('config','{}'))
                sv = cfg.get('singleVisual',{})
                vtype = sv.get('visualType','')
                title_obj = sv.get('vcObjects',{}).get('title',[{}])
                title_text = ''
                if title_obj:
                    tp = title_obj[0].get('properties',{}).get('text',{})
                    title_text = tp.get('expr',{}).get('Literal',{}).get('Value','')
                prj = sv.get('prototypeQuery',{}).get('Select',[])
                cols = [p.get('NativeReferenceName','') for p in prj]
                x = v.get('x'); y = v.get('y'); w = v.get('width'); h = v.get('height')
                print("  [" + vtype + "] title=" + repr(title_text) + " cols=" + str(cols) + " x=" + str(x) + " y=" + str(y) + " w=" + str(w) + " h=" + str(h))
