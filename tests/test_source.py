import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from collect import normalize,amount
class SourceTests(unittest.TestCase):
 def test_cumulative_values_are_not_incremental_amendments(self):
  r={'owner_org':'x','reference_number':'1','owner_org_title':'X','procurement_id':'N/A','vendor_name':'A','contract_date':'2026-01-01','instrument_type':'A','original_value':'100','amendment_value':'20','contract_value':'120'};v=normalize([r])[0];self.assertEqual(v['amount'],20);self.assertEqual(v['reported_contract_value'],120);self.assertIsNone(v['group_key'])
 def test_missing_amount_is_not_zero(self):self.assertIsNone(amount(''));self.assertEqual(amount('0'),0)
