from mindsdb_sql.parser.ast.base import ASTNode
from mindsdb_sql.utils import indent


class Union(ASTNode):

    def __init__(self,
                 left,
                 right,
                 unique=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = left
        self.right = right
        self.unique = unique

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        ind1 = indent(level+1)

        left_str = f'\n{ind1}left=\n{self.left.to_tree(level=level + 2)},'
        right_str = f'\n{ind1}right=\n{self.right.to_tree(level=level + 2)},'

        out_str = f'{ind}Union(unique={repr(self.unique)},' \
                  f'{left_str}' \
                  f'{right_str}' \
                  f'\n{ind})'
        return out_str

    def maybe_add_alias(self, some_str):
        if self.alias:
            return f'({some_str}) AS {self.alias}'
        elif self.parentheses:
            return f'({some_str})'
        else:
            return some_str

    def to_string(self, *args, **kwargs):
        left_str = str(self.left)
        right_str = str(self.right)
        keyword = 'UNION' if self.unique else 'UNION ALL'
        out_str = f"""{left_str}\n{keyword}\n{right_str}"""

        return self.maybe_add_alias(out_str)
