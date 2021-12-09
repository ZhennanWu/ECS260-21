import ast
from enum import Enum
from functools import reduce


def extract_all_identifier_names(source):
    if source== None:
        return {
        'var_names': [],
        'fun_names': [],
        'class_names': [],
    }
    try:
        root = ast.parse(source)
    except Exception:
        return {
            'var_names': [],
            'fun_names': [],
            'class_names': [],
        }

    var_names = sorted(
        node.id for node in ast.walk(root) if isinstance(
            node, ast.Name) and not isinstance(node.ctx, ast.Load)
    )
    fun_names = sorted(
        n.name for n in root.body if isinstance(n, ast.FunctionDef)
    )
    class_names = sorted(
        [n.name for n in root.body if isinstance(n, ast.ClassDef)]
    )
    return {
        'var_names': var_names,
        'fun_names': fun_names,
        'class_names': class_names,
    }


def get_added_identifier_names(old_names, new_names):
    return {
        'var_names': compare_get_addition_in_sorted_deduped(old_names["var_names"], new_names["var_names"]),
        'fun_names': compare_get_addition_in_sorted_deduped(old_names["fun_names"], new_names["fun_names"]),
        'class_names': compare_get_addition_in_sorted_deduped(old_names["class_names"], new_names["class_names"]),
    }


def compare_get_addition_in_sorted_deduped(old, new):
    i = 0
    j = 0
    old_len = len(old)
    new_len = len(new)
    res = []
    while i < old_len and j < new_len:
        if old[i] < new[j]:
            i += 1
        elif old[i] > new[j]:
            res.append(new[j])
            j += 1
        else:
            i += 1
            j += 1
    return res

# https://rust-lang.github.io/api-guidelines/naming.html
class NamingStyle(Enum):
    SingleChar, LowerCamel, UpperCamel, Screaming_Snake, Snake, UpperSnake, LowerCamelOrSnake, Unknown = range(
        8)
    # Screaming cannot be distinguished from Screaming Snake
    # LowerCamelOrSnake = Either LowerCamel or Snake or all Lower, we cannot tell


def analyze_names(names):
    stat = [0] * len(NamingStyle)
    for name in names:
        style = analyze_naming_style_for_identifier(name)
        stat[style.value] += 1
    return stat

def naming_style_sum(series):
    return reduce(lambda x, y: [xi + yi for xi, yi in zip(x, y)], series)

naming_style_default = [0] * len(NamingStyle)


def analyze_naming_style_for_identifier(name):
    if len(name) == 1:
        return NamingStyle.SingleChar
    name = name.strip('_')
    has_dash = '_' in name
    stripped_name = name.replace("_", "")
    is_all_lower = name.lower() == name
    is_all_upper = name.upper() == name
    if has_dash:
        if is_all_lower:
            return NamingStyle.Snake
        if is_all_upper:
            return NamingStyle.Screaming_Snake
        terms = name.split('_')
        if all(term[0].isupper() for term in terms):
            return NamingStyle.UpperSnake
    if not has_dash:
        if is_all_lower:
            return NamingStyle.LowerCamelOrSnake
        if is_all_upper:
            return NamingStyle.Screaming_Snake
        if name[0].islower():
            return NamingStyle.LowerCamel
        if name[0].isupper():
            return NamingStyle.UpperCamel
    return NamingStyle.Unknown
