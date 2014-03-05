from django.template import Context
from django.http.request import QueryDict

from achilles import blocks, actions


register = actions.Library('forms')


class Form(blocks.Block):
    """
    Form block, display a formulary
    """
    #: Template file
    template_name = 'achilles/form.html'

    initial = {}
    form_class = None

    def __init__(self, context=Context()):
        super(Form, self).__init__(context)

    def get_initial(self):
        return self.initial.copy()

    def get_form(self, form_data=None, *args, **kwargs):
        return self.form_class(data=form_data, **self.get_form_kwargs())

    def get_form_kwargs(self, form_data=None, *args, **kwargs):
        kwargs = {
            'initial': self.get_initial(),
        }
        if form_data:
            kwargs['data'] = form_data
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(Form, self).get_context_data(*args, **kwargs)
        context.update({
            'form': self.get_form(*args, **kwargs),
        })
        return context

    def form_valid(self, request, form):
        raise NotImplementedError("You should implement this method")

    def form_invalid(self, request, form):
        raise NotImplementedError("You should implement this method")


@register.action
def send(request, form, data):
    """
    Validate a form and call the proper callback Form.form_valid
    or Form.form_invalid

    :param request: Request object
    :param form: Form block name
    :param data: Serialized form data
    """
    block = blocks.get(form)
    data = QueryDict(data, encoding=request.encoding)
    form = block.get_form(form_data=data)

    if form.is_valid():
        block.form_valid(request, form)
    else:
        block.form_invalid(request, form)
