import os
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class ParameterSpecifierClassNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        forbidden_directory_entries = (
            'MusicSpecifier',
            'MusicContributionSpecifier',
            'ParameterSpecifier',
            'Specifier',
            )
        for directory_entry in os.listdir(
            self.configuration.built_in_specifiers_directory_path):
            if directory_entry.endswith('Specifier'):
                if not directory_entry in forbidden_directory_entries:
                    result.append(directory_entry)
        return result
