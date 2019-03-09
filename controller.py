"""
Base controller for the application.
There will be one controller per page/view.
Each controller will implement a view method which will be in
charge of returning a string.
"""
from framework.utils import errors
from framework.forms.form import Form

class Controller(object):

    # The form to use. Default form does nothing and expects nothing.
    form = Form
    # defines if the subclass of this controller will handle validation.
    self_validating = False

    def __init__(self):
        """Declare class attributes."""
        self.request = None
        self.response = None
        self.form = None

    def __call__(self, request, response):
        """Call the controller instance."""
        self.request = request
        self.response = response

        # Order of operations for controller

        # Middleware
        # TODO write middleware

        # Form handling
        self.form = self._form_setup()
        if not self.__class__.self_validating and not self.form.validate():
            self.form_invalid()
        self.form.extract()

        # View handling
        return self.view()

    def _form_setup(self):
        """
        For initialising and setting up a form.
        """
        form = self.__class__.form()
        form.request = self.request
        return form

    def form_invalid(self):
        """What to do if the form is invalid."""

    def view(self):
        """
        This should be in charge of handling generating the view.
        If not implemented then throws http 500 error.
        """
        errors.abort(
            500,
            'Unimplemented view method in: ' +\
            self.__class__.__name__
        )