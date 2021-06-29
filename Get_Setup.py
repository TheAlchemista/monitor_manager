import os


class Get_Setup:
    def __init__(self):
        self.raw = os.popen("dccmd -listmonitors").read()
        self.lines = self.get_lines()
        self.descriptions = self.get_descriptions()
        self.setup = self.get_setup()
        # pprint(self.raw)
        # pprint(self.monitor_descriptions)
        # pprint(self.descriptions)
        # pprint(self.setup)

    def get_lines(self):
        strings = str.split(self.raw, "\n")
        return [s for s in strings if s != '']

    def get_descriptions(self):
        return [self.lines[i:i+4] for i in range(0, len(self.lines), 4)]

    def get_setup(self):
        setup = []
        for des in self.descriptions:
            dic = {}
            for line in des:
                dic = self.parse_line(str.split(line, " "), dic)
            setup.append(dic)
        return setup

    """Parses information in line. Takes list of elements in line."""
    def parse_line(self, element_list, dic):
        if element_list[0] == "Monitor:" or element_list[0] == "Adapter:" or element_list[0] == "Device:":
            # Also removes ':' from arguments
            dic[element_list[0].replace(':', '')] = ' '.join(element_list[1:len(element_list)])
        # Last line
        else:    
            # State of the monitor (on or off)
            if element_list.__contains__('attached'):
                dic["State"] = "on"
            else:
                dic["State"] = "off"

            dic = self.extract_location(element_list, dic)
        
        return dic

    def extract_location(self, element_list, dic):
        # Location from top left corner of primary monitor (always last)
        if len(element_list) >= 5:
            location = element_list[len(element_list) - 1].replace('(','').replace(')', '').split(',')
            dic["x"] = int(location[0])
            dic["y"] = int(location[1])
        return dic
    
    # TODO extract rotation (apears o not be needed, because default is used)

