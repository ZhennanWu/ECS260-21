from analysis.identifier_name import analyze_names, extract_all_identifier_names, get_added_identifier_names, naming_style_sum, naming_style_default
from pydriller.domain.commit import ModificationType, ModifiedFile
import ast
import tokenize
import io

# To write better source file analysis: https://pydriller.readthedocs.io/en/latest/modifiedfile.html

def line_contains_comment(line):
    try:
        return any(toktype == tokenize.COMMENT
                      for toktype, tok, start, end, line in tokenize.generate_tokens(io.StringIO(line[1]).readline))
    except Exception:
        return False
def analyze_src(modified_src_file: ModifiedFile):
    # if modified_src_file.change_type == ModificationType.RENAME:
    #     return {
    #         'value': 0.01,  # Rename is not valuable
    #         'added_lines_py': 0,
    #         'deleted_lines_py': 0,
    #     }

    # This includes in-line comments that comes after normal code
    all_added_lines_with_comments = list(filter(
        line_contains_comment,
                      modified_src_file.diff_parsed['added']
    ))
    added_pure_comment_lines = list(filter(
        lambda x: x[1].lstrip().startswith('#'),
        modified_src_file.diff_parsed['added']
    ))
    deleted_pure_comment_lines = list(filter(
        lambda x: x[1].lstrip().startswith('#'),
        modified_src_file.diff_parsed['deleted']
    ))

    old_identifier_names = extract_all_identifier_names(
        modified_src_file.source_code_before)
    new_identifier_names = extract_all_identifier_names(
        modified_src_file.source_code)
    added_names = get_added_identifier_names(
        old_identifier_names, new_identifier_names)
    var_names_style_stat = analyze_names(added_names['var_names'])
    fun_names_style_stat = analyze_names(added_names['fun_names'])
    class_names_style_stat = analyze_names(added_names['class_names'])
    return {
        'value': modified_src_file.added_lines * 0.1 + modified_src_file.deleted_lines * 0.01,
        'added_lines_py': modified_src_file.added_lines,
        'deleted_lines_py': modified_src_file.deleted_lines,
        'added_functions': len(added_names['fun_names']),
        'added_classes': len(added_names['class_names']),
        'added_comment': len(all_added_lines_with_comments),
        'added_code_lines': modified_src_file.added_lines - len(added_pure_comment_lines),
        'deleted_code_lines': modified_src_file.deleted_lines - len(deleted_pure_comment_lines),
        'var_names_style_stat': var_names_style_stat,
        'fun_names_style_stat': fun_names_style_stat,
        'class_names_style_stat': class_names_style_stat,
    }


py_source_stat_combiner = dict(
    value=('value', 'sum'),
    added_lines_py=('added_lines_py', 'sum'),
    deleted_lines_py=('deleted_lines_py', 'sum'),
    added_functions=('added_functions', 'sum'),
    added_classes=('added_classes', 'sum'),
    added_comment=('added_comment', 'sum'),
    added_code_lines=('added_code_lines', 'sum'),
    deleted_code_lines=('deleted_code_lines', 'sum'),
    var_names_style_stat=('var_names_style_stat', naming_style_sum),
    fun_names_style_stat=('fun_names_style_stat', naming_style_sum),
    class_names_style_stat=('class_names_style_stat', naming_style_sum),
)

py_source_stat_columns = [
    'value',
    'added_lines_py',
    'deleted_lines_py',
    'added_functions',
    'added_classes',
    'added_comment',
    'added_code_lines',
    'deleted_code_lines',
    'var_names_style_stat',
    'fun_names_style_stat',
    'class_names_style_stat',
]

py_source_stat_default = {
    'value': 0,
    'added_lines_py': 0,
    'deleted_lines_py': 0,
    'added_functions': 0,
    'added_classes': 0,
    'added_comment': 0,
    'added_code_lines': 0,
    'added_code_lines': 0,
    'var_names_style_stat': naming_style_default,
    'fun_names_style_stat': naming_style_default,
    'class_names_style_stat': naming_style_default,
}