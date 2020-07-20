import logging

logger = logging.getLogger(__name__)

class StatelessValidation():
    @staticmethod
    def validate(request):
        logger.debug("StatelessValidation.validate")
        # do stateless validation
        # assert request.append != "", "cannot append empty value"
        pass
