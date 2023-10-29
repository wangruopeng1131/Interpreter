grammar = {
    'S': [['statement'], ['$']],
    'primary_expression': [['id'], ['number'], ['(', 'or_expression', ')'], ['True'], ['False'], ['string'], ['samplings']],
    'comp_op': [['=='], ['≠'], ['>'], ['<'], ['≤'], ['≥']],
    'unary_op': [['abs'], ['round'], ['floor'], ['ceil'], ['trunc'], ['sin'], ['cos'], ['tan'],
                 ['arcsin'], ['arccos'], ['arctan'], ['pos'], ['neg']],
    'secondary_operator': [['*'], ['/'], ['%'], ['//']],
    'primary_operator': [['+'], ['-']],
    'third_operator': [['^'], ['log']],
    'func_primary': [['id'], ['number'], ['or_expression'], ['samplings'], ['(', 'or_expression', ')']],
    # 运算
    'func_expression': [['unary_op', '(', 'func_primary', ')'], ['primary_expression']],
    'power_expression': [['power_expression', 'third_operator', 'func_expression'], ['func_expression']],
    'term_expression': [['term_expression', 'secondary_operator', 'power_expression'], ['power_expression']],
    'expression': [['expression', 'primary_operator', 'term_expression'], ['term_expression']],
    'comparison': [['comparison', 'comp_op', 'expression'], ['expression']],
    'not_expression': [['not', 'not_expression'], ['comparison']],
    'and_expression': [['and_expression', 'and', 'not_expression'], ['not_expression']],
    'or_expression': [['or_expression', 'or', 'and_expression'], ['and_expression']],

    # 变量赋值
    'assignment_operator': [['='], ['+='], ['-='], ['*='], ['/='], ['%='], ['//=']],
    'assignment_expression': [['id', 'assignment_operator', 'or_expression']],

    # 集合运算
    'set_op': [['|'], ['&'], ['-'], ['×']],
    'atom': [['number'], ['string'], ['True'], ['False']],
    'atom_list': [[',', 'atom'], ['$']],
    'elements': [['[', 'atom', 'atom_list', ']']],
    'primary_set': [['set', '(', 'elements', ')'], ['id'], ['(', 'set_expression', ')']],
    'set_expression': [['set_expression', 'set_op', 'primary_set'], ['primary_set']],

    # 集合赋值
    'assignment_set': [['id', '=', 'set_expression']],

    # 集合采样
    'dist': [['discrete'], ['uniform'], ['gauss'], ['vonmises']],
    'samplings': [['dist', '(', 'assignment_set', ')']],
    # 'assignment_expression_profix': [[',', 'assignment_expression', 'assignment_expression_profix'], ['$']],
    # 'assignment_expression_list': [['assignment_expression', 'assignment_expression_profix']],

    'statement': [['assignment_expression'], ['selection_statement']],
    # 'expression_statement': [['assignment_expression', ';']],
    'selection_statement': [['if', '(', 'or_expression', ')', '{', 'statement', '}', 'elif_statement', 'else_statement']],
    'elif_statement': [['elif', '(', 'or_expression', ')', '{', 'statement', '}'], ['$']],
    'else_statement': [['else', '{', 'statement', '}'], ['$']]
    # 'jump_statement': [['break'], ['continue']],
    # 'iteration_statement': [['while', '(', 'expression', ')', '{', 'statement', '}']]
}


tree_rules = {
    'S': [['change'], ['end']],
    'primary_expression': [['change'], ['change'], ['drop', 'change', 'drop'], ['change'], ['change'], ['change'],
                           ['samplings']],
    'comp_op': [['change'], ['change'], ['change'], ['change'], ['change'], ['change']],
    'unary_op': [['change'], ['change'], ['change'], ['change'], ['change'], ['change'], ['change'], ['change'], ['change'],
                 ['change'], ['change'], ['change'], ['change']],
    'secondary_operator': [['change'], ['change'], ['change'], ['change']],
    'primary_operator': [['change'], ['change']],
    'third_operator': [['change'], ['change']],
    'func_primary': [['change'], ['change'], ['change'], ['change'], ['drop', 'change', 'drop']],
    'func_expression': [['un_op', 'drop', 'arg1', 'drop'], ['change']],
    'power_expression': [['arg1', 'op', 'arg2'], ['change']],
    'term_expression': [['arg1', 'op', 'arg2'], ['change']],
    'expression': [['arg1', 'op', 'arg2'], ['change']],
    'comparison': [['arg1', 'op', 'arg2'], ['change']],
    'not_expression': [['un_op', 'arg1'], ['change']],
    'and_expression': [['arg1', 'op', 'arg2'], ['change']],
    'or_expression': [['arg1', 'op', 'arg2'], ['change']],
    'assignment_operator': [['change'], ['change'], ['change'], ['change'], ['change'], ['change'], ['change']],
    'assignment_expression': [['arg1', 'op', 'arg2']],

    # 集合运算
    'set_op': [['change'], ['change'], ['change'], ['change']],
    'atom': [['change'], ['change'], ['change'], ['change']],
    'atom_list': [['drop', 'change'], ['$']],
    'elements': [['drop', 'change', 'change', 'drop']],
    'primary_set': [['set', 'drop', 'change', 'drop'], ['change'], ['drop', 'change', 'drop']],
    'set_expression': [['arg1', 'op', 'arg2'], ['change']],

    # 集合赋值
    'assignment_set': [['arg1', 'op', 'arg2']],

    # 集合采样
    'dist': [['change'], ['change'], ['change'], ['change']],
    'samplings': [['change', 'drop', 'change', 'drop']],
    # 'assignment_expression_profix': [[',', 'assignment_expression', 'assignment_expression_profix'], ['$']],
    # 'assignment_expression_list': [['assignment_expression', 'assignment_expression_profix']],

    'statement': [['change'], ['change']],
    # 'expression_statement': [['assignment_expression', ';']],
    'selection_statement': [
        ['if', 'drop', 'condition', 'drop', 'drop', 'body', 'drop', 'elif_statement', 'else_statement']],
    'elif_statement': [['elif', 'drop', 'condition', 'drop', 'drop', 'body', 'drop'], ['end']],
    'else_statement': [['else', 'drop', 'body', 'drop'], ['end']]
}

# grammar = {
#     'start': [['S'], ['$']],
#     'S': [['L', '=', 'R'], ['R']],
#     'L': [['*', 'R'], ['id']],
#     'R': [['L']]
# }
# grammar = {
#     'start': [['E'], ['$']],
#     'E': [['E', '+', 'T'], ['T']],
#     'T': [['T', '*', 'F'], ['F']],
#     'F': [['(', 'E', ')'], ['id'], ['number']]
# }