from common import ROOT,save,fetch,sha
import json,gzip,argparse,datetime,time,re,unicodedata,collections
from urllib.parse import urlencode
from decimal import Decimal,InvalidOperation
RESOURCE='fac950c0-00d5-4ec1-a4d3-9cbebf98a305'
FIELDS=['reference_number','owner_org','owner_org_title','procurement_id','vendor_name','contract_date','original_value','amendment_value','contract_value','instrument_type','reporting_period','description_en','commodity_type','solicitation_procedure','contract_period_start','delivery_date']
def vendor(value):return re.sub('[^a-z0-9]+',' ',''.join(c for c in unicodedata.normalize('NFKD',value.lower()) if not unicodedata.combining(c))).strip()
def amount(value):
 if value is None or str(value).strip()=='':return None
 try:n=float(Decimal(str(value).replace(',','')))
 except InvalidOperation:raise ValueError('Unrecognized monetary value')
 if not -1e13<n<1e13:raise ValueError('Amount outside expected range')
 return n

def normalize(raw):
 rows=[]
 for r in raw:
  name=r.get('vendor_name') or 'Not reported';contract=(r.get('procurement_id') or '').strip();valid=contract and contract.upper() not in ['N/A','NA','NONE','UNKNOWN','TBD','0','-']
  kind={'C':'Award','A':'Amendment','SOSA':'Standing offer / supply arrangement'}.get(r.get('instrument_type'),'Other / unspecified');department=(r.get('owner_org_title') or r['owner_org']).split(' | ')[0]
  row={'id':r['owner_org']+'|'+r['reference_number'],'vendor':name,'vendor_key':vendor(name),'department':department,'department_id':r['owner_org'],'contract':contract or 'Not reported','group_key':r['owner_org']+'|'+contract if valid else None,'date':r['contract_date'],'year':r['contract_date'][:4],'kind':kind,'amount':amount(r.get('original_value') if kind=='Award' else r.get('amendment_value') if kind=='Amendment' else r.get('contract_value')),'original_value':amount(r.get('original_value')),'amendment_value':amount(r.get('amendment_value')),'reported_contract_value':amount(r.get('contract_value')),'reporting_quarter':r.get('reporting_period'),'reference':r['reference_number'],'description':r.get('description_en'),'source_url':'https://search.open.canada.ca/contracts/?'+urlencode({'search_text':r['reference_number']})}
  rows.append(row)
 groups=collections.defaultdict(list)
 for r in rows:
  if r['group_key']:groups[r['group_key']].append(r)
 for r in rows:
  group=groups.get(r['group_key'],[]);vendors={v['vendor_key'] for v in group}
  r['link_status']='No usable procurement ID' if not group else 'Ambiguous: multiple normalized vendor names' if len(vendors)>1 else 'Potential link: same department and procurement ID'
  r['related_disclosures']=len(group)
 return rows

def main():
 p=argparse.ArgumentParser();p.add_argument('--seed',action='store_true');a=p.parse_args();end=datetime.date.today();start=end-datetime.timedelta(days=365)
 if a.seed:
  raw=json.load(gzip.open(ROOT/'.cache/contracts-12months.json.gz','rt'));meta=json.loads((ROOT/'.cache/contracts-12months-metadata.json').read_text());pages=meta['pages'];start=meta['start'];end=meta['end']
 else:
  raw=[];pages=[];offset=0
  while True:
   url='https://open.canada.ca/data/en/api/3/action/datastore_search?'+urlencode({'resource_id':RESOURCE,'limit':1000,'offset':offset,'sort':'contract_date desc, _id asc','fields':','.join(FIELDS)})
   response=fetch(url);d=json.loads(response)
   if not d.get('success'):raise ValueError('CKAN source returned failure')
   batch=d['result']['records'];pages.append({'url':url,'sha256':sha(response)})
   raw.extend(r for r in batch if start.isoformat()<=(r.get('contract_date') or '')<=end.isoformat())
   if not batch or (batch[-1].get('contract_date') or '')<start.isoformat():break
   offset+=len(batch)
   if offset>500000:raise ValueError('Unexpected cohort size; retain prior dataset')
   time.sleep(.3)
 rows=normalize(raw)
 save(rows,sources=[{'label':'Federal proactive contract disclosures','url':'https://open.canada.ca/data/en/dataset/d8f85d91-7dec-4fd1-8055-483b77225d8b'},{'label':'Source schema','url':'https://open.canada.ca/data/recombinant-published-schema/contracts.json'}],coverage=f'Complete returned contract-date cohort {start} through {end} · {len(rows):,} disclosures',warnings=['Unaudited disclosures. Repeated-award patterns are investigation leads, not allegations of contract splitting.','Amendments can retain the original award date; this date-selected cohort is not a complete amendment census. A row can leave the rolling date window without being deleted from the source.'],extra={'source_pages':pages,'window_start':str(start),'window_end':str(end)})
if __name__=='__main__':main()
