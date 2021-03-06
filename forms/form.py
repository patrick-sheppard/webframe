"""Base forms and form utilities."""

import os
import html
import secrets
import filetype

class Form(object):
    """Base Form."""

    def __init__(self):
        """Setup attributes."""
        self.request = None
        self.params = {}
        self.valid = False
        self.errors = {}

    def sanitize(self, _input):
        """
        Sanitize input with default sanitization.
        Can be extended, though make sure to call parent
        if not extending complete functionality.

        returns dictionary containing sanitized input.
        """
        sanitized = {}
        for key, inp in _input.items():
            try:
                key = html.escape(key).strip()
            except AttributeError:
                pass
            # try:
            #     inp = html.escape(inp).strip()
            # except (AttributeError, TypeError):
            #     pass

            sanitized[key] = inp
        
        return sanitized

    def rules(self):
        return {}

    def validate(self):
        # Sanitize first and set params from request
        self.params = self.sanitize(self.request.allInput())

        # Get rules
        rules = self.rules()
        for name, validator_list in rules.items():
            for validator in validator_list:
                msg = validator(name, self)
                if msg is not None:
                    self.errors.setdefault(name, []).append(msg)

        # False if length of errors > 0
        return not len(self.errors)

    def extract(self):
        """Extract the values from the form."""
        pass

    def has(self, name):
        """Check if the form has an input."""
        try:
            if self.input(name) is None:
                return False
        except KeyError:
            return False

        return True

    def input(self, name):
        """
        Helper method to get the input.
        Returns None if the input is blank.

        Only works after validation has been called (or during validation).
        """
        try:
            _input = self.params[name]
            try:
                _input = _input.strip()
            except AttributeError:
                pass
            if _input == '':
                return None
            return _input
        except KeyError:
            return None

    def has_file(self, name):
        """
        Check if the file was uploaded.
        Files behave differently to normal inputs and the has() function
        will return true no matter if the file was uploaded or not.
        """
        return bool(self.input(name).__class__.__name__ == 'cgi_FieldStorage')

    def store_file(self, name, location, filename=None, extension=None):
        """
        Store an uploaded file with input "name" to a location.
        If extension is None it will try to find the correct extension.
        If filename is None it will generate a random name.
        Returns filename.
        """
        f = self.input(name)
        if filename is None:
            filename = secrets.token_hex(16)
        if extension is None:
            _type = filetype.guess(f.value)
            if _type is not None:
                extension = _type.extension
        path = os.path.join(location, f'{filename}.{extension}')
        if not os.path.exists(location) or not os.path.isdir(location):
            os.mkdir(location)
        
        with open(path, 'wb') as _file:
            _file.write(f.value)

        return path
