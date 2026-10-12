#!/usr/bin/env python3
"""Offline founder arithmetic. See references/finance-inputs.md for semantics."""

import argparse
from decimal import Decimal, InvalidOperation, ROUND_CEILING, localcontext
import json
from pathlib import Path
import sys


class InputError(ValueError):
    pass


def fields(value, required, optional, path):
    if not isinstance(value, dict):
        raise InputError(f"{path}: expected an object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing:
        raise InputError(f"{path}: missing {', '.join(sorted(missing))}")
    if extra:
        raise InputError(f"{path}: unknown {', '.join(sorted(extra))}")


def text_value(value, path):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{path}: expected a nonempty string")
    return value


def number(value, path):
    if isinstance(value, bool) or not isinstance(value, (int, Decimal, str)):
        raise InputError(f"{path}: expected a finite nonnegative decimal")
    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError):
        raise InputError(f"{path}: expected a finite nonnegative decimal") from None
    if not result.is_finite() or result < 0:
        raise InputError(f"{path}: expected a finite nonnegative decimal")
    # Limit pathological inputs while retaining useful precision for currencies.
    if result != 0 and not -20 <= result.adjusted() <= 20:
        raise InputError(f"{path}: magnitude outside supported range")
    if len(result.as_tuple().digits) > 28:
        raise InputError(f"{path}: at most 28 significant input digits supported")
    return result


def cost_map(value, path):
    if not isinstance(value, dict):
        raise InputError(f"{path}: expected a named cost object; use {{}} for zero")
    total = Decimal(0)
    for name, amount in value.items():
        text_value(name, path + '.cost_name')
        total += number(amount, path + '.' + name)
    return total


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def unit_model(data):
    required = {'name', 'period', 'price', 'variable_costs',
                'fixed_costs_per_period', 'planned_units_per_period'}
    fields(data, required, {'capacity_per_period'}, 'unit')
    name = text_value(data['name'], 'unit.name')
    period = text_value(data['period'], 'unit.period')
    price = number(data['price'], 'unit.price')
    variable = cost_map(data['variable_costs'], 'unit.variable_costs')
    fixed = cost_map(data['fixed_costs_per_period'], 'unit.fixed_costs_per_period')
    volume = number(data['planned_units_per_period'], 'unit.planned_units_per_period')
    capacity = (number(data['capacity_per_period'], 'unit.capacity_per_period')
                if 'capacity_per_period' in data else None)
    contribution = price - variable
    revenue = price * volume
    profit = contribution * volume - fixed
    break_even = fixed / contribution if contribution > 0 else (
        Decimal(0) if fixed == 0 and contribution == 0 else None)
    warnings = []
    if contribution <= 0:
        warnings.append('No positive contribution from incremental units.')
    if capacity is not None and volume > capacity:
        warnings.append('Planned volume exceeds stated capacity.')
    if capacity is not None and break_even is not None and break_even > capacity:
        warnings.append('Break-even volume exceeds stated capacity.')
    if profit < 0:
        warnings.append('Operating loss at planned volume under the stated costs.')
    return {
        'name': name, 'period': period,
        'variable_cost_per_unit': variable, 'fixed_cost_per_period': fixed,
        'contribution_per_unit': contribution,
        'contribution_margin_ratio': ratio(contribution, price),
        'planned_revenue': revenue, 'planned_operating_profit': profit,
        'planned_operating_margin_ratio': ratio(profit, revenue),
        'break_even_units': break_even,
        'break_even_whole_units': (int(break_even.to_integral_value(rounding=ROUND_CEILING))
                                 if break_even is not None else None),
        'warnings': warnings,
    }


def cash_model(data):
    fields(data, {'opening_cash', 'minimum_reserve', 'periods'}, set(), 'cash')
    opening = number(data['opening_cash'], 'cash.opening_cash')
    reserve = number(data['minimum_reserve'], 'cash.minimum_reserve')
    periods = data['periods']
    if not isinstance(periods, list) or not periods:
        raise InputError('cash.periods: expected a nonempty ordered array')
    columns = {'receipts', 'operating_payments', 'capital_payments',
               'tax_payments', 'debt_payments', 'financing_received'}
    current = opening
    minimum = opening
    before_financing = opening
    minimum_before_financing = opening
    rows = []
    labels = set()
    first_negative = None
    for i, period in enumerate(periods):
        path = f'cash.periods[{i}]'
        fields(period, columns | {'label'}, set(), path)
        label = text_value(period['label'], path + '.label')
        if label in labels:
            raise InputError(path + ': duplicate period label')
        labels.add(label)
        amounts = {key: number(period[key], path + '.' + key) for key in columns}
        operating_net = amounts['receipts'] - amounts['operating_payments']
        before_net = (operating_net - amounts['capital_payments']
                      - amounts['tax_payments'] - amounts['debt_payments'])
        net = before_net + amounts['financing_received']
        start = current
        current += net
        before_financing += before_net
        minimum = min(minimum, current)
        minimum_before_financing = min(minimum_before_financing, before_financing)
        if current < 0 and first_negative is None:
            first_negative = label
        rows.append({'label': label, 'opening_cash': start,
                     'operating_net_cash': operating_net, 'net_cash_change': net,
                     'ending_cash': current,
                     'ending_cash_without_listed_financing': before_financing})
    return {
        'periods': rows, 'ending_cash': current,
        'minimum_endpoint_cash': minimum,
        'additional_opening_cash_to_meet_reserve': max(Decimal(0), reserve - minimum),
        'additional_opening_cash_to_meet_reserve_without_listed_financing':
            max(Decimal(0), reserve - minimum_before_financing),
        'first_negative_period_end': first_negative,
        'limitation': 'Period endpoints only; intra-period shortfalls are not modeled.',
    }


def saas_model(data):
    required = {'period', 'starting_mrr', 'new_mrr', 'expansion_mrr',
                'contraction_mrr', 'churned_mrr'}
    fields(data, required, set(), 'saas')
    period = text_value(data['period'], 'saas.period')
    values = {key: number(data[key], 'saas.' + key) for key in required - {'period'}}
    starting = values['starting_mrr']
    expansion = values['expansion_mrr']
    losses = values['contraction_mrr'] + values['churned_mrr']
    if losses > starting:
        raise InputError('saas: starting-cohort contraction plus churn exceeds starting MRR')
    if starting == 0 and expansion != 0:
        raise InputError('saas: expansion cannot belong to an empty starting cohort')
    retained = starting - losses
    end = retained + expansion + values['new_mrr']
    return {
        'period': period, 'ending_mrr': end,
        'gross_revenue_retention_ratio': ratio(retained, starting),
        'net_revenue_retention_ratio': ratio(retained + expansion, starting),
        'net_mrr_growth': end - starting,
        'net_mrr_growth_ratio': ratio(end - starting, starting),
        'limitation': 'Normalized recurring revenue bridge, not cash or recognized revenue.',
    }


def calculate(data):
    fields(data, {'currency'}, {'unit', 'cash', 'saas'}, 'input')
    currency = text_value(data['currency'], 'currency')
    if not any(key in data for key in ('unit', 'cash', 'saas')):
        raise InputError('input: provide at least one of unit, cash, saas')
    with localcontext() as context:
        context.prec = 64
        result = {'currency': currency}
        for key, function in [('unit', unit_model), ('cash', cash_model), ('saas', saas_model)]:
            if key in data:
                result[key] = function(data[key])
        return result


def decimal_json(value):
    if isinstance(value, Decimal):
        return format(value, 'f')
    raise TypeError(f'Unsupported JSON value: {type(value).__name__}')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f'JSON: duplicate key {key}')
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON document; no network or file writes')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'), parse_float=Decimal,
                          parse_constant=Decimal, object_pairs_hook=unique_object)
        result = calculate(data)
        print(json.dumps(result, default=decimal_json, indent=2, allow_nan=False))
    except (InputError, OSError, ValueError, UnicodeError) as error:
        print(f'Input error: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
