import os
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class DirectoryContentSelector(Selector):

    ### CLASS VARIABLES ###

    storehouse_filesystem_paths = []

    space_delimited_lowercase_target_name = 'file'

    ### PUBLIC METHODS ###

    def list_items(self):
        from experimental.tools.scoremanagertools.proxies.DirectoryProxy \
            import DirectoryProxy
        result = []
        for directory_path in self.storehouse_filesystem_paths:
            directory_proxy = DirectoryProxy(
                filesystem_path=directory_path,
                session=self.session)
            result.extend(
                directory_proxy.list_directory(public_entries_only=True))
            if hasattr(self, 'forbidden_directory_entries'):
                for forbidden_directory_entry in \
                    self.forbidden_directory_entries:
                    if forbidden_directory_entry in result:
                        result.remove(forbidden_directory_entry)
        return result
