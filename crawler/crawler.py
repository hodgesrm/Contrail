import logging
from time import sleep

from crawler.providers.aws_ec2 import AmazonEC2

DEFAULT_CRAWL_PERIOD_S = 5

providers = []


def register_provider(instance):
    """
    Register a provider class with the crawler to ensure this provider is crawled.
    """
    providers.append(instance)


def load_providers() -> int:
    """
    Loads all modules in the `providers` directory.
    :return: The number of providers loaded.
    """
    # TODO Make this dynamically load all modules in providers/
    register_provider(AmazonEC2())
    return 1


def crawl(period: int = DEFAULT_CRAWL_PERIOD_S):
    """
    Runs the crawler until an interrupt is received.
    :param period: Number of seconds to wait between data requests.
    """
    logging.info("Starting crawler.")
    num_providers = load_providers()
    logging.info("Loaded {} providers.".format(num_providers))

    # Loop crawler until interrupted
    # TODO Ensure fairness between providers in this loop
    try:
        while True:
            for p in providers:
                p.crawl()
                sleep(period)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    crawl()