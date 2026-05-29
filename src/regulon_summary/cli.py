import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Summarize TF-gene regulons from a TSV file."
    )

    parser.add_argument("input_file")
    parser.add_argument("output_file")

    parser.add_argument(
        "--min_genes",
        type=int,
        default=0,
    )

    parser.add_argument(
        "--type",
        choices=["all", "activador", "represor", "dual"],
        default="all",
    )

    parser.add_argument(
        "--format",
        choices=["summary", "sif"],
        default="summary",
    )

    parser.add_argument(
        "--top_n",
        type=int,
        default=10,
    )

    return parser.parse_args()
