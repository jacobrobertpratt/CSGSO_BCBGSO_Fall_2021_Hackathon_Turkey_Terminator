from typing import List, Union

from .gui import Display


class BackableDisplay(Display):
    def __init__(self, title: str, choices: List[str]):
        super().__init__(title, choices)
        self.choices.append('Back')
        self.omap['back'] = True


class CEDDisplay(BackableDisplay):
    def __init__(self, title: str, item_name: str, normal_choices: List[str]):
        super().__init__(title, normal_choices + [
            'Add {}'.format(item_name),
            'Edit {}'.format(item_name),
            'Delete {}'.format(item_name)
        ])
        self.item_name = item_name.lower()
        self.omap['add {}'.format(self.item_name)] = self.create
        self.omap['edit {}'.format(self.item_name)] = self.edit
        self.omap['delete {}'.format(self.item_name)] = self.delete

    def create(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

    def process(self) -> Union[object, bool]:
        c = super().process()
        if c is True:
            return True
        elif isinstance(c, Display):
            return c
        elif callable(c):
            c()
        return False
