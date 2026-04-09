from etl.current.run_current_pipeline import run_current_pipeline
from etl.shared.build_portfolio_snapshot import main as build_snapshot
from utils.formatter import print_header


def main():
    print_header("CRYPTO PORTFOLIO PROJECT START")

    run_current_pipeline()
    build_snapshot()

    print_header("CRYPTO PORTFOLIO PROJECT FINISHED")


if __name__ == "__main__":
    main()