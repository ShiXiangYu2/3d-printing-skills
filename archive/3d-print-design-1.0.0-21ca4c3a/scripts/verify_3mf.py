"""Validate a native Bambu project against its actual sequential group G-code."""
import argparse,json,re,zipfile,xml.etree.ElementTree as E
def verify(path,printer):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None,'Broken ZIP'
  cfg=json.loads(z.read('Metadata/project_settings.config'));assert cfg['printer_model']==printer,'Wrong printer'
  assert cfg['print_sequence']=='by object','Not sequential by object'
  objects=E.fromstring(z.read('Metadata/model_settings.config')).findall('object');assert objects,'No group objects'
  for obj in objects:
   meta={m.get('key'):m.get('value') for m in obj.findall('metadata')};slot=meta.get('extruder','1')
   for part in obj.findall('part'):
    partmeta={m.get('key'):m.get('value') for m in part.findall('metadata')};assert partmeta.get('extruder',slot)==slot,'Group mixes colors'
  plates=E.fromstring(z.read('Metadata/slice_info.config')).findall('plate');assert len(plates)==1,'Not a single plate'
  meta={m.get('key'):m.get('value') for m in plates[0].findall('metadata')};assert meta['outside']=='false','Outside bed'
  warnings=[w.attrib for w in plates[0].findall('warning')]
  assert all(w['msg'] in ['not_support_traditional_timelapse','not_generate_timelapse'] for w in warnings),warnings
  code=z.read('Metadata/plate_1.gcode').decode();ids=re.findall(r'^; start printing object, unique label id: (\d+)',code,re.M);runs=[]
  for value in ids:
   if not runs or runs[-1]!=value:runs.append(value)
  assert len(runs)==len(objects) and len(set(runs))==len(runs),'Objects not continuously completed or missing G-code markers'
  tools=[int(n) for n in re.findall(r'^M620 S(\d+)A',code,re.M)]
  assert len(tools)==len(objects),'Unexpected material changes; inspect actual G-code'
  return {'ok':True,'printer':printer,'nozzle':cfg['nozzle_diameter'],'sequence':cfg['print_sequence'],'parts':sum(len(o.findall('part')) for o in objects),'group_runs':runs,'material_load_order':tools,'changes':len(tools)-1,'prediction_seconds':int(meta['prediction']),'weight_g':float(meta['weight']),'warnings':warnings,'physical_fit_verified':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('file');p.add_argument('--printer',required=True);a=p.parse_args();print(json.dumps(verify(a.file,a.printer),ensure_ascii=False,indent=2))
