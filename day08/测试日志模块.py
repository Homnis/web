import logging

# 日志级别
# logging.debug("debug")
# logging.info("info")
# logging.warning("warning")
# logging.error("error")
# logging.fatal("fatal")

# logging.basicConfig(level=logging.DEBUG, filename="log.log")
# logging.debug("debug")
# logging.info("info")
# logging.warning("warning")
# logging.error("error")
# logging.fatal("fatal")

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("log.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.fatal("fatal")


logger2 = logging.getLogger(__file__)
logger2.setLevel(logging.WARN)

handler2 = logging.StreamHandler()
formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler2.setFormatter(formatter2)
logger2.addHandler(handler2)

logger2.debug("debug")
logger2.info("info")
logger2.warning("warning")
logger2.error("error")
logger2.fatal("fatal")