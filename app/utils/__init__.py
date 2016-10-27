import re


class GlobList(list):
    def __contains__(self, ip_address):
        for pattern in self:
            if re.match(pattern, ip_address):
                return True
        return False
