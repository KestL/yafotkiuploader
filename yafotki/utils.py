'''
Required params for optparse
Example:

    parser = OptionParser(option_list=[
        Option("-v", action="count", dest="verbose"),
        Option("-f", "--file", required=1)])
    (options, args) = parser.parse_args()
'''

import optparse

class Option (optparse.Option):
    ATTRS = optparse.Option.ATTRS + ['required']

    def _check_required (self):
        if self.required and not self.takes_value():
            raise OptionError(
                "required flag set for option that doesn't take a value",
                 self)

    # Make sure _check_required() is called from the constructor!
    CHECK_METHODS = optparse.Option.CHECK_METHODS + [_check_required]

    def process (self, opt, value, values, parser):
        optparse.Option.process(self, opt, value, values, parser)
        parser.option_seen[self] = 1
        if self.dest == 'help':
            parser.show_help = True


class OptionParser (optparse.OptionParser):

    def _init_parsing_state (self):
        optparse.OptionParser._init_parsing_state(self)
        self.option_seen = {}
        self.show_help = False

    def check_values (self, values, args):
        for option in self.option_list:
            if (isinstance(option, Option) and
                option.required and
                not self.option_seen.has_key(option) and
                not self.show_help):
                self.error("%s not supplied" % option)
        return (values, args)


