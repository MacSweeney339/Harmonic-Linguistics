class Wiki_Urls(object):

    def __init__(self):
        self._get_urls()

    def _get_urls(self):
        # read in url files
        key_array = []
        with open('artist_group_wiki.txt') as f:
            for line in f:
                key_array.append(line.replace('\n',''))
        # turn list into dict
        key_dict = {}
        for item in key_array:
            key, value = item.split(',')
            setattr(self, key, value)
