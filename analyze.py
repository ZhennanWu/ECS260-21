from pydriller.domain.commit import ModificationType, ModifiedFile
# from pydriller import *
### To write better source file analysis: https://pydriller.readthedocs.io/en/latest/modifiedfile.html
def analyze_src(modified_src_file: ModifiedFile):
    if modified_src_file.change_type == ModificationType.RENAME:
        return {
            'value': 0,  # Rename is not valuable
            'added_lines_py': 0,
            'deleted_lines_py': 0,
        }
    return {
        'value': modified_src_file.added_lines * 0.1 + modified_src_file.deleted_lines * 0.01,
        'added_lines_py': modified_src_file.added_lines,
        'deleted_lines_py': modified_src_file.deleted_lines,
    }