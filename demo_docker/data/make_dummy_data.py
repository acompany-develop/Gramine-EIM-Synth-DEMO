import random
from string import ascii_letters, digits

from pprint import pprint
import pandas as pd

COL_NAME_LETTERS = ascii_letters + digits + ".-_"
COL_NAME_LEN_LIMIT = 20

COL_VALUE_LETTERS = ascii_letters + digits + ".-_"
COL_VALUE_LEN_LIMIT = 5
ID_COL_VALUE_LEN_LIMIT = 64
NUM_UNIQUE_VALUES = 10

# Constants for the two CSV files
CSV1_NUM_RECORDS = 10000000
CSV1_NUM_COLS = 10

CSV2_NUM_RECORDS = 10000000
CSV2_NUM_COLS = 10

# matched CSV
NUM_RECORDS = 5000000
NUM_COLS = CSV1_NUM_COLS + CSV2_NUM_COLS


def main() -> None:
    # generate column names
    assert 0 < NUM_COLS < 100
    col_name_prefixes = [f"col{i:02d}_" for i in range(NUM_COLS)]
    random_str_len = COL_NAME_LEN_LIMIT - len(col_name_prefixes[0])
    col_names = []
    for i, prefix in enumerate(col_name_prefixes):
        random_str = "".join(
            random.choice(COL_NAME_LETTERS) for _ in range(random_str_len)
        )
        col_names.append(prefix + random_str)

    assert len(col_names) == NUM_COLS
    for col_name in col_names:
        assert len(col_name) <= COL_NAME_LEN_LIMIT
        assert all(ch in COL_NAME_LETTERS for ch in col_name)

    # generate values for each column
    all_values = []
    for i in range(NUM_COLS):
        while True:
            uniq_vals = [
                "".join(
                    random.choice(COL_VALUE_LETTERS) for _ in range(COL_VALUE_LEN_LIMIT)
                )
                for _ in range(NUM_UNIQUE_VALUES)
            ]
            if len(set(uniq_vals)) < NUM_UNIQUE_VALUES:
                continue
            has_appended = False
            while True:
                values = [random.choice(uniq_vals) for _ in range(max(CSV1_NUM_RECORDS, CSV2_NUM_RECORDS))]
                if len(set(values)) == NUM_UNIQUE_VALUES:
                    all_values.append(values)
                    has_appended = True
                    break
            if has_appended:
                break

    assert len(all_values) == NUM_COLS
    for values in all_values:
        assert len(values) == max(CSV1_NUM_RECORDS, CSV2_NUM_RECORDS)
        assert len(set(values)) == NUM_UNIQUE_VALUES
        assert all(len(value) == COL_VALUE_LEN_LIMIT for value in values)
        assert all(ch in COL_VALUE_LETTERS for value in values for ch in value)

    # split columns into two sets for CSV1 and CSV2
    csv1_columns = col_names[:CSV1_NUM_COLS]
    csv2_columns = col_names[CSV1_NUM_COLS:]

    matched_ids = ["".join(random.choice(COL_VALUE_LETTERS) for _ in range(ID_COL_VALUE_LEN_LIMIT)) for _ in range(NUM_RECORDS)]

    # Adjust lengths for CSV1 and CSV2
    csv1_values = {}
    csv1_values['id'] = matched_ids + ["".join(random.choice(COL_VALUE_LETTERS) for _ in range(ID_COL_VALUE_LEN_LIMIT)) for _ in range(CSV1_NUM_RECORDS - NUM_RECORDS)]
    csv1_values.update({name: all_values[i][:CSV1_NUM_RECORDS] for i, name in enumerate(csv1_columns)})
    # csv1_values['id']に、matched_idsを含む、CSV1_NUM_RECORDS個のIDを生成
    
    csv2_values = {}
    csv2_values['id'] = matched_ids + ["".join(random.choice(COL_VALUE_LETTERS) for _ in range(ID_COL_VALUE_LEN_LIMIT)) for _ in range(CSV2_NUM_RECORDS - NUM_RECORDS)]
    csv2_values.update({name: all_values[i + CSV1_NUM_COLS][:CSV2_NUM_RECORDS] for i, name in enumerate(csv2_columns)})

    # Ensure that the first column in both CSVs is the same for joining, but only NUM_RECORDS overlap
    join_column = ["".join(random.choice(COL_VALUE_LETTERS) for _ in range(COL_VALUE_LEN_LIMIT)) for _ in range(NUM_RECORDS)]
    
    # CSV1の最初の NUM_RECORDS 行と残りの行を異なるIDで埋める
    csv1_join_ids = join_column[:NUM_RECORDS] + ["".join(random.choice(COL_VALUE_LETTERS) for _ in range(COL_VALUE_LEN_LIMIT)) for _ in range(CSV1_NUM_RECORDS - NUM_RECORDS)]
    csv1_values[csv1_columns[0]] = csv1_join_ids

    # CSV2の最初の NUM_RECORDS 行と残りの行を異なるIDで埋める
    csv2_join_ids = join_column[:NUM_RECORDS] + ["".join(random.choice(COL_VALUE_LETTERS) for _ in range(COL_VALUE_LEN_LIMIT)) for _ in range(CSV2_NUM_RECORDS - NUM_RECORDS)]
    csv2_values[csv2_columns[0]] = csv2_join_ids

    # save csv files
    # print(len(csv1_values), [c for c in csv1_values], len(csv2_values), [c for c in csv2_values])
    print([(k, len(v)) for k, v in csv1_values.items()])
    pd.DataFrame(csv1_values).to_csv(f"{CSV1_NUM_RECORDS}_a.csv", index=False)
    pd.DataFrame(csv2_values).to_csv(f"{CSV1_NUM_RECORDS}_b.csv", index=False)


def test_csv_files() -> None:
    # 1. CSV1とCSV2を読み込む
    csv1 = pd.read_csv(f"{CSV1_NUM_RECORDS}_a.csv")
    csv2 = pd.read_csv(f"{CSV1_NUM_RECORDS}_b.csv")

    # 2. 行数と列数が一致しているかを確認
    assert len(csv1) == CSV1_NUM_RECORDS, f"CSV1の行数が一致しません: {len(csv1)}"
    assert len(csv2) == CSV2_NUM_RECORDS, f"CSV2の行数が一致しません: {len(csv2)}"
    assert len(csv1.columns) == CSV1_NUM_COLS+1, f"CSV1の列数が一致しません: {len(csv1.columns)}"
    assert len(csv2.columns) == (NUM_COLS - CSV1_NUM_COLS)+1, f"CSV2の列数が一致しません: {len(csv2.columns)}"

    # 3. CSV1とCSV2を共通列で結合し、行数を確認
    # 共通列のidは結合後に削除
    merged_df = pd.merge(csv1, csv2, on='id')

    # 4. ジョイン結果の行数と列数が一致しているか確認
    assert len(merged_df) == NUM_RECORDS, f"結合後の行数が一致しません: ({len(merged_df)},{NUM_RECORDS})"
    expected_columns = NUM_COLS
    assert len(merged_df.columns) == expected_columns+1, f"結合後の列数が一致しません: ({len(merged_df.columns)},{expected_columns})"

    print("すべてのテストが成功しました！")

if __name__ == "__main__":
    main()
    test_csv_files()
