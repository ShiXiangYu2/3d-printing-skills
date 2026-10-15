"""Read-only validation of this case's assembly evidence; not physical certification."""
import json,sys
from pathlib import Path
def validate(r):
 assert r.get('physical_fit_verified') is False, 'No physical evidence for this case'
 assert len(r.get('tests',[]))==16, 'Missing path/rotation tests'
 assert all('collisions' in x and not x['collisions'] for x in r['tests']), 'Collision or missing result'
 assert len(r.get('topology',[]))==11
 assert all(x['components']==1 and x['nonmanifold_edges']==0 and x['volume']>0 for x in r['topology'])
 assert len(r.get('wheel_retention',[]))==6
 assert all(x['outward_0_8_mm_collision']>.001 for x in r['wheel_retention'])
 allowed={frozenset(['01_Chassis','02_CatArmor']):.31,frozenset(['02_CatArmor','04_FaceMask']):1.92}
 for x in r.get('static_intersections',[]):
  assert frozenset(x['pair']) in allowed and x['mm3']<=allowed[frozenset(x['pair'])], 'Unreviewed static interference'
 assert len(r.get('wheel_insertion_raw',[]))==6
 assert all(x.get('requires_elastic_snap') is True and len(x['samples'])==41 for x in r['wheel_insertion_raw'])
 return {'ok':True,'scope':'cat-v4 evidence completeness only','physical_fit_verified':False}
if __name__=='__main__':
 print(json.dumps(validate(json.loads(Path(sys.argv[1]).read_text(encoding='utf8')))))
