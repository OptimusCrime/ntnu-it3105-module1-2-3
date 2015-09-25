#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy

from module3.node import Node

# Read all lines in the file while stripping the ending newline
lines = [line.rstrip('\n') for line in open('module3/grams/example.txt')]
rows_and_columns = map(int, lines[0].split(' '))

# Get row specs
row_specs = []
for line in lines[1:rows_and_columns[1] + 1]:
    row_specs.append(map(int, line.split(' ')))

# Get column specs
column_specs = []
for line in lines[rows_and_columns[0] + 2:]:
    column_specs.append(map(int, line.split(' ')))

def row_has_space(size, specs):
    return row_max_expand(size, specs) >= size

def row_max_expand(size, specs):
    used = 0
    for spec in specs:
        used += spec['length'] + spec['space']
    return size - used

def calcolate_row_specs(size, index, specs):
    new_specs = copy.deepcopy(specs)

    combination = []

    for i in range(row_max_expand(size, new_specs)):
        # Get a copy of the specs
        new_specs = copy.deepcopy(new_specs)

        # Increase the space with one
        new_specs[index]['space'] += 1

        # Add to list
        combination.append(new_specs)

        # Reccurssive call on all other specs
        for j in range(len(specs)):
            if j != index:
                reccurrsive_row_specs = calcolate_row_specs(size, j, new_specs)
                if len(reccurrsive_row_specs) > 0:
                    combination.extend(reccurrsive_row_specs)

    return combination


def combination_to_representation(size, combinations):
    representation = []

    for combination in combinations:
        new_line = [0] * size
        current_index = 0
        for spec in combination:
            current_index += spec['space']
            for j in range( spec['length']):
                new_line[current_index] = 1
                current_index += 1
        representation.append(new_line)
    return representation


# Trying to calculate rows
def calculate_rows(size, specs):
    initial_specs = []
    for i in range(len(specs)):
        if i == 0:
            initial_specs.append({'length': specs[i], 'space': 0})
        else:
            initial_specs.append({'length': specs[i], 'space': 1})

    #print initial_specs
    #print combination_to_representation(size, [initial_specs])

    specs_combinations = copy.deepcopy([initial_specs])
    for i in range(len(initial_specs)):
        #print 'expand = ' + str(i)
        new_row = calcolate_row_specs(size, i, initial_specs)
        #print new_row
        if len(new_row) > 0:
            specs_combinations.extend(new_row)
    #print ' '
    #print 'Calculated this: '
    specs_representation = combination_to_representation(size, specs_combinations)
    #for representation in specs_representation:
    #    print representation
    #    print ' '
    return specs_combinations

for i in range(len(row_specs)):
    # Get the total row
    calculated_rows = calculate_rows(rows_and_columns[0], row_specs[i])
    print calculated_rows

    # Find the number of variables in this row
    variable_nums = len(calculated_rows[0])

    nodes = []
    for i in range(variable_nums):
        nodes.append(set())


    # Loop all calculated rows
    for j in range(len(calculated_rows)):

        #print calculated_rows[j]
        offset = 0

        # Loop individual start in the current calculated
        for k in range(len(calculated_rows[j])):
            #print offset + calculated_rows[j][k]['space']
            #print '--'
            nodes[k].add(offset + calculated_rows[j][k]['space'])

            offset += calculated_rows[j][k]['space'] + calculated_rows[j][k]['length']

    print nodes
    print ' '

#
