# I should be able to do this, but it's apparently broken.
# from vlermv.serializers import identity as text

class _serializer:
    '''
    Hack because vlermv insists on str type.
    '''
    @classmethod
    def dump(Class, obj, old_fp):
        error, response = obj
        if error:
            raise error
        with open(old_fp.name, 'w' + Class.b) as fp:
            fp.write(response)

    @classmethod
    def load(Class, old_fp):
        with open(old_fp.name, 'r' + Class.b) as fp:
            response = fp.read()
        return None, response

class text(_serializer):
    b = ''

class binary(_serializer):
    b = 'b'
