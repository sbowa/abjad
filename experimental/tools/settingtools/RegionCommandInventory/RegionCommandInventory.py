import copy
from abjad.tools import sequencetools
from abjad.tools import timespantools
from abjad.tools.timespantools.TimespanInventory import TimespanInventory


class RegionCommandInventory(TimespanInventory):
    '''Region command inventory.

    Methods to do things region command collections.
    '''

    ### PUBLIC METHODS ###

    def sort_and_split_commands(self):
        '''Operate in place and return region command inventory.
        '''
        cooked_commands = []
        for raw_command in self[:]:
            command_was_delayed, command_was_split = False, False
            commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split = [], [], [], []
            for cooked_command in cooked_commands:
                if raw_command.timespan.contains_timespan_improperly(cooked_command):
                    commands_to_remove.append(cooked_command)
                elif raw_command.timespan.delays_timespan(cooked_command):
                    commands_to_delay.append(cooked_command)
                elif raw_command.timespan.curtails_timespan(cooked_command):
                    commands_to_curtail.append(cooked_command)
                elif raw_command.timespan.trisects_timespan(cooked_command):
                    commands_to_split.append(cooked_command)
            #print commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split
            for command_to_remove in commands_to_remove:
                cooked_commands.remove(command_to_remove)
            for command_to_curtail in commands_to_curtail:
                timespan = timespantools.Timespan(
                    command_to_curtail.timespan.start_offset, raw_command.timespan.start_offset)
                command_to_curtail._timespan = timespan
            for command_to_delay in commands_to_delay:
                timespan = timespantools.Timespan(
                    raw_command.timespan.stop_offset, command_to_delay.timespan.stop_offset)
                command_to_delay._timespan = timespan
                command_was_delayed = True
            # TODO: branch inside and implement a method to split while treating cyclic payload smartly.
            # or, alternatively, special-case for commands that cover the entire duration of score.
            for command_to_split in commands_to_split:
                left_command = command_to_split
                middle_command = raw_command
                right_command = copy.deepcopy(left_command)
                timespan = timespantools.Timespan(
                    left_command.timespan.start_offset, middle_command.timespan.start_offset)
                left_command._timespan = timespan
                timespan = timespantools.Timespan(
                    middle_command.timespan.stop_offset, right_command.timespan.stop_offset)
                right_command._timespan = timespan
                command_was_split = True
            if command_was_delayed:
                index = cooked_commands.index(cooked_command)
                cooked_commands.insert(index, raw_command)
            elif command_was_split:
                cooked_commands.append(middle_command)
                cooked_commands.append(right_command)
            else:
                cooked_commands.append(raw_command)
            cooked_commands.sort()
            #self._debug_values(cooked_commands, 'cooked')
        #self._debug_values(cooked_commands, 'cooked')
        self[:] = cooked_commands
        return self

    def supply_missing_commands(self, score_specification, voice_name, attribute):
        '''Operate in place and return region command inventory.
        '''
        assert self.is_sorted
        if not self and not score_specification.time_signatures:
            return self
        elif not self and score_specification.time_signatures:
            timespan = score_specification.timespan
            region_command = score_specification.make_default_region_command(
                voice_name, timespan, attribute)
            self[:] = [region_command]
            return self
        if not self.timespan.starts_when_timespan_starts(score_specification):
            timespans = score_specification.timespan - self.timespan
            timespan = timespans[0]
            region_command = score_specification.make_default_region_command(
                voice_name, timespan, attribute)
            self.insert(0, region_command)
        if not self.timespan.stops_when_timespan_stops(score_specification):
            timespans = score_specification.timespan - self.timespan
            timespan = timespans[-1]
            region_command = score_specification.make_default_region_command(
                voice_name, timespan, attribute)
            self.append(region_command)
        if len(self) == 1:
            return self
        result = []
        for left_region_command, right_region_command in \
            sequencetools.iterate_sequence_pairwise_strict(self):
            assert not left_region_command.timespan.starts_after_timespan_starts(right_region_command.timespan)
            result.append(left_region_command)
            if left_region_command.timespan.stops_before_timespan_starts(right_region_command.timespan):
                # TODO: implement timespan operations to create new timespan below
                start_offset = left_region_command.timespan.stop_offset 
                stop_offset = right_region_command.timespan.start_offset
                timespan = timespantools.Timespan(start_offset, stop_offset)
                region_command = score_specification.make_default_region_command(
                    voice_name, timespan, attribute)
                result.append(region_command)
        result.append(right_region_command)
        self[:] = sorted(result)
        return self

        # TODO: use this implementation instead of the longer one above
#        score_timespan = score_specification.timespan
#        self.append(score_timespan)
#        missing_regions = self.compute_logical_xor() 
#        for missing_region in missing_regions:
#            region_command = score_specification.make_default_region_command(
#                voice_name, missing_region, attribute)
#            self.append(region_command)
#        self.sort()
#        return self
