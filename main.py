import argparse
import dataclasses

import tabulate
import csv


def read_csv(files: list[str]) -> list[list[str]]:
    data = []

    for file in files:
        if not file.lower().endswith(".csv"):
            continue

        with open(file, "r", encoding='utf-8') as f:
            reader = csv.reader(f)

            if not reader:
                continue

            for i, row in enumerate(reader):
                if i == 0:
                    continue

                data.append(row)

    return data


@dataclasses.dataclass
class ShortMetrics:
    title: str
    ctr: float
    retention_rate: int

    @classmethod
    def from_row(cls, row: list[str]) -> "ShortMetrics":
        return cls(
            title=row[0],
            ctr=float(row[1]),
            retention_rate=int(row[2]),
        )


def clickbait_report(files: list[str]):
    files_data = [ShortMetrics.from_row(d) for d in read_csv(files)]

    data = list()
    for row in files_data:
        if row.ctr < 15:
            continue
        if row.retention_rate > 40:
            continue

        data.append(row)

    sorted_data = sorted(data, key=lambda x: x.ctr, reverse=True)
    print(
        tabulate.tabulate(
            sorted_data,
            headers='keys',
            tablefmt='grid',
        )
    )


ALL_REPORTS = {
    "clickbait": clickbait_report,
}


def main(report_list: list[str], files: list[str]):
    if not report_list:
        print("Report title not specified")
        return

    if not files:
        print("Report title not specified")
        return

    for report_name in report_list:
        if report_name not in ALL_REPORTS:
            print(f"Report '{report_name}' not found")
            continue

        report = ALL_REPORTS[report_name]
        report(files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", type=str, help="File names", nargs="+")
    parser.add_argument("--report", type=str, help="Report name", nargs="+")
    args = parser.parse_args()

    main(args.report, args.files)
