import main


def test_read_csv_reads_only_csv_and_skips_header(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "title,ctr,retention_rate\nVideo A,20.5,30\nVideo B,10,50\n",
        encoding="utf-8",
    )

    txt_file = tmp_path / "data.txt"
    txt_file.write_text("ignore me", encoding="utf-8")

    result = main.read_csv([str(txt_file), str(csv_file)])

    assert result == [["Video A", "20.5", "30"], ["Video B", "10", "50"]]


def test_read_csv_returns_empty_list_for_empty_csv(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    result = main.read_csv([str(csv_file)])

    assert result == []


def test_shortmetrics_from_row_converts_values():
    row = ["My video", "17.2", "35"]

    metric = main.ShortMetrics.from_row(row)

    assert metric.title == "My video"
    assert metric.ctr == 17.2
    assert metric.retention_rate == 35


def test_clickbait_report_prints_filtered_and_sorted_rows(tmp_path, capsys):
    csv_file = tmp_path / "stats.csv"
    csv_file.write_text(
        "title,ctr,retention_rate\n"
        "Bad CTR,14.9,20\n"
        "Bad retention,22.0,41\n"
        "Good second,16.0,40\n"
        "Good first,21.5,30\n",
        encoding="utf-8",
    )

    main.clickbait_report([str(csv_file)])

    output = capsys.readouterr().out

    assert "Good first" in output
    assert "Good second" in output
    assert "Bad CTR" not in output
    assert "Bad retention" not in output
    assert output.find("Good first") < output.find("Good second")


def test_main_prints_error_when_report_list_is_empty(capsys):
    main.main([], ["stats.csv"])

    output = capsys.readouterr().out.strip()
    assert output == "Report title not specified"


def test_main_prints_error_when_files_list_is_empty(capsys):
    main.main(["clickbait"], [])

    output = capsys.readouterr().out.strip()
    assert output == "Report title not specified"


def test_main_prints_error_for_unknown_report(capsys):
    main.main(["unknown"], ["stats.csv"])

    output = capsys.readouterr().out.strip()
    assert output == "Report 'unknown' not found"
