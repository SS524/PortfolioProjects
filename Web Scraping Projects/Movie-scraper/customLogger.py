import logging

logging.basicConfig(filename = "customLoggerCreation.log",
                    level = logging.INFO,filemode='w',
                    format = '%(asctime)s-%(levelname)s-%(filename)s-%(message)s')


class custom_logger_class:
    def __init__(self, filename, nameOfLogger):
        try:
            self.filename = filename
            self.nameOfLogger = nameOfLogger
            logging.info("Variables are initialized for creating custom logger")
        except Exception as e:
            logging.error(str(e))
    
    def create_custom_logger(self):
        try:
            logger = logging.getLogger(self.nameOfLogger)
            logger.setLevel(logging.INFO)
            logging.info("Custom logger level has been set")
            fileHandler = logging.FileHandler(self.filename)
            fileHandler.setLevel(logging.INFO)
            logging.info("Custom logger destination file has been declared")
            formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(message)s')
            fileHandler.setFormatter(formatter)
            logging.info("Custom logger formatting has been done")

            logger.addHandler(fileHandler)
            logging.info("Custom logger has been successfully created")
            return logger
        except Exception as e:
            logging.info(str(e))
    



