import argparse

from port.adapter.resource.crawl import crawl_resource


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", default="scroll", type=str)
    parser.add_argument("seed_url", default=r"", type=str)
    parser.add_argument("regex_to_save", default="", type=str)
    parser.add_argument("--more_selector", default="", type=str)
    args = parser.parse_args()

    algorithm = args.algorithm
    seed_url = args.seed_url
    regex_to_save = args.regex_to_save
    more_selector = args.more_selector

    crawl_resource.crawl(algorithm,
                         seed_url=seed_url,
                         detail_url_regex=regex_to_save,
                         regex_to_save=regex_to_save,
                         more_selector=more_selector)
