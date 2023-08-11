import logging


logging.basicConfig(
    filename="logs.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    1/0
except Exception as e:
    logging.info(e, exc_info=True)

try:
    1/0
except ZeroDivisionError as e:
    logging.error(e, exc_info=True)
