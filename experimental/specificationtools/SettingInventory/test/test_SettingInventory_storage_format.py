from abjad.tools import *
from experimental import specificationtools
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification
from experimental.specificationtools import SettingInventory


def test_SettingInventory_storage_format_01():
    '''Disk format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    score_specification.interpret()

    setting_inventory_1 = segment.settings

    storage_format = setting_inventory_1.storage_format

    r'''
    specificationtools.SettingInventory([
        specificationtools.Setting(
            specificationtools.ContextSelection(
                'Grouped Rhythmic Staves Score',
                timespan=specificationtools.Timespan(
                    start=specificationtools.TemporalCursor(
                        anchor=specificationtools.ScoreObjectIndicator(
                            segment='1'
                            ),
                        edge=Left
                        ),
                    stop=specificationtools.TemporalCursor(
                        anchor=specificationtools.ScoreObjectIndicator(
                            segment='1'
                            ),
                        edge=Right
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False,
            fresh=True
            )
        ])
    '''

    assert storage_format == "specificationtools.SettingInventory([\n\tspecificationtools.Setting(\n\t\tspecificationtools.ContextSelection(\n\t\t\t'Grouped Rhythmic Staves Score',\n\t\t\ttimespan=specificationtools.Timespan(\n\t\t\t\tstart=specificationtools.TemporalCursor(\n\t\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Left\n\t\t\t\t\t),\n\t\t\t\tstop=specificationtools.TemporalCursor(\n\t\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Right\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False,\n\t\tfresh=True\n\t\t)\n\t])"

    setting_inventory_2 = eval(storage_format)

    assert isinstance(setting_inventory_1, SettingInventory)
    assert isinstance(setting_inventory_2, SettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
