import copy
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/finance.py'
spec = importlib.util.spec_from_file_location('founder_finance', SCRIPT)
finance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finance)


def unit(**changes):
    result = {'name': 'customer-month', 'period': 'month', 'price': '100',
              'variable_costs': {'delivery': '20', 'fees': '3'},
              'fixed_costs_per_period': {'payroll': '3500', 'tools': '350'},
              'planned_units_per_period': 80, 'capacity_per_period': 120}
    result.update(changes)
    return result


def period(label, **changes):
    result = dict(label=label, receipts='0', operating_payments='0',
                  capital_payments='0', tax_payments='0', debt_payments='0',
                  financing_received='0')
    result.update(changes)
    return result


def saas(**changes):
    result = dict(period='month-2', starting_mrr='4000', new_mrr='1000',
                  expansion_mrr='400', contraction_mrr='200', churned_mrr='400')
    result.update(changes)
    return result


class FinanceTests(unittest.TestCase):
    def test_worked_unit_economics(self):
        result = finance.calculate({'currency': 'USD', 'unit': unit()})['unit']
        self.assertEqual(result['contribution_per_unit'], Decimal(77))
        self.assertEqual(result['break_even_units'], Decimal(50))
        self.assertEqual(result['planned_operating_profit'], Decimal(2310))

    def test_fractional_break_even_ceiling_and_capacity(self):
        result = finance.calculate({'currency': 'USD', 'unit': unit(
            price='10', variable_costs={'delivery': '3'},
            fixed_costs_per_period={'rent': '100'}, capacity_per_period=14,
            planned_units_per_period=15)})['unit']
        self.assertEqual(result['break_even_whole_units'], 15)
        self.assertGreater(result['break_even_units'], 14)
        self.assertEqual(len(result['warnings']), 2)

    def test_nonpositive_contribution_has_no_scalable_break_even(self):
        for price in ['23', '20']:
            result = finance.calculate({'currency': 'USD', 'unit': unit(price=price)})['unit']
            self.assertIsNone(result['break_even_units'])
            self.assertLess(result['planned_operating_profit'], 0)

    def test_zero_price_and_volume_do_not_divide_by_zero(self):
        result = finance.calculate({'currency': 'USD', 'unit': unit(
            price=0, variable_costs={}, fixed_costs_per_period={},
            planned_units_per_period=0)})['unit']
        self.assertIsNone(result['contribution_margin_ratio'])
        self.assertIsNone(result['planned_operating_margin_ratio'])
        self.assertEqual(result['break_even_whole_units'], 0)

    def test_exact_decimal_inputs(self):
        result = finance.calculate({'currency': 'USD', 'unit': unit(
            price='0.30', variable_costs={'fee': '0.10'},
            fixed_costs_per_period={}, planned_units_per_period=3)})['unit']
        self.assertEqual(result['planned_operating_profit'], Decimal('0.60'))

    def test_cash_all_categories_and_reserve(self):
        data = {'currency': 'USD', 'cash': {'opening_cash': '100',
            'minimum_reserve': '20', 'periods': [period('one', receipts='30',
                operating_payments='80', capital_payments='10', tax_payments='5',
                debt_payments='15', financing_received='20'),
                period('two', operating_payments='70')]}}
        result = finance.calculate(data)['cash']
        self.assertEqual(result['periods'][0]['ending_cash'], Decimal(40))
        self.assertEqual(result['ending_cash'], Decimal(-30))
        self.assertEqual(result['additional_opening_cash_to_meet_reserve'], Decimal(50))
        self.assertEqual(result['additional_opening_cash_to_meet_reserve_without_listed_financing'], Decimal(70))
        self.assertEqual(result['first_negative_period_end'], 'two')

    def test_opening_cash_itself_must_meet_reserve(self):
        result = finance.calculate({'currency': 'USD', 'cash': {
            'opening_cash': '0', 'minimum_reserve': '100',
            'periods': [period('one', financing_received='1000')]}})['cash']
        self.assertEqual(result['minimum_endpoint_cash'], Decimal(0))
        self.assertEqual(result['additional_opening_cash_to_meet_reserve'], Decimal(100))

    def test_gross_and_net_retention_exclude_new_business(self):
        result = finance.calculate({'currency': 'USD', 'saas': saas()})['saas']
        result_more_new = finance.calculate({'currency': 'USD', 'saas': saas(new_mrr='9000')})['saas']
        self.assertEqual(result['ending_mrr'], Decimal(4800))
        self.assertEqual(result['gross_revenue_retention_ratio'], Decimal('0.85'))
        self.assertEqual(result['net_revenue_retention_ratio'], Decimal('0.95'))
        self.assertEqual(result['net_revenue_retention_ratio'], result_more_new['net_revenue_retention_ratio'])

    def test_empty_starting_cohort(self):
        result = finance.calculate({'currency': 'USD', 'saas': saas(
            starting_mrr=0, new_mrr=100, expansion_mrr=0,
            contraction_mrr=0, churned_mrr=0)})['saas']
        self.assertEqual(result['ending_mrr'], Decimal(100))
        self.assertIsNone(result['gross_revenue_retention_ratio'])
        self.assertIsNone(result['net_mrr_growth_ratio'])

    def test_invalid_finance_inputs(self):
        bad = [
            {'currency': 'USD'},
            {'currency': 'USD', 'units': unit()},
            {'currency': 'USD', 'unit': unit(price=True)},
            {'currency': 'USD', 'unit': unit(price='NaN')},
            {'currency': 'USD', 'unit': unit(price='Infinity')},
            {'currency': 'USD', 'unit': unit(price='-1')},
            {'currency': 'USD', 'unit': unit(variable_costs={'x': None})},
            {'currency': 'USD', 'unit': unit(unknown=0)},
            {'currency': 'USD', 'saas': saas(churned_mrr='4001')},
            {'currency': 'USD', 'saas': saas(starting_mrr=0, expansion_mrr=1, contraction_mrr=0, churned_mrr=0)},
            {'currency': 'USD', 'cash': {'opening_cash': 0, 'minimum_reserve': 0, 'periods': []}},
            {'currency': 'USD', 'cash': {'opening_cash': 0, 'minimum_reserve': 0, 'periods': [period('a'), period('a')]}},
        ]
        missing = {'currency': 'USD', 'unit': unit()}
        del missing['unit']['price']
        bad.append(missing)
        for value in bad:
            with self.subTest(value=value), self.assertRaises(finance.InputError):
                finance.calculate(value)

    def test_cli_validates_json_and_never_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'numbers.json'
            path.write_text(json.dumps({'currency': 'USD', 'unit': unit()}))
            before = path.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['unit']['planned_operating_profit'], '2310')
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(temp).iterdir()), [path])
            for invalid in ['{"currency":"USD","currency":"EUR"}',
                            '{"currency":"USD","unit":{"price":NaN}}', '{invalid']:
                path.write_text(invalid)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
