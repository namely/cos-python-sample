class StatelessValidation():
    @staticmethod
    def validate(request):
        # do stateless validation
        assert request.append != "", "cannot append empty value"
