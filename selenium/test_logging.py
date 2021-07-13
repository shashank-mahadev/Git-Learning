import logging

def test_loggingDemo():

    logger = logging.getLogger(__name__)

    fileHandler = logging.FileHandler("logfile.log") # which file to log, wher to log
    formatter=logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s" ) # loging format
    fileHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)  # filehandler object, add the log format

    logger.setLevel(logging.DEBUG)
    logger.debug("A debug level logs are logged")
    logger.info("A info level logs are logged ")
    logger.warning("A warning level logs are logged")
    logger.error("A error level logs are logged, ")
    logger.critical("critical error")



