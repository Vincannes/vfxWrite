
class TemplateKeyName(object):
    NAME_PUBLISH = 'publish'
    NAME_WORK = 'work'

    def __init__(self, defaultTemplate='', work='', publish=''):
        if not defaultTemplate and (not work or not publish):
            raise ValueError("TemplateKeyName invalid argument constructor: empty")
        self.work = defaultTemplate or work
        self.publish = defaultTemplate or publish


class FieldsTemplate(object):

    def __init__(self, name, template, fields={}):
        self.name = name
        self.fields = fields
        self.template = template

    def get_key(self, key):
        return self.fields.get(key, None)


class FieldKey(object):

    def __init__(self, tank_id, label, values=None, preferencie=None, template=None, dependencies=None):
        self.tank_id = tank_id
        self.label = label
        self.values = values
        self.template = template
        self.preferencie = preferencie
        self.dependencies = dependencies

