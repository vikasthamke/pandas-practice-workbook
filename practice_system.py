"""
practice_system.py
-------------------
Interactive hint/answer engine for the Pandas Practice Workbook.

Usage (inside the notebook):
    from practice_system import hint, answer
    hint(12)            # first-level hint for Task 12
    hint(12, level=2)   # second-level hint, where available
    answer(12)          # full solution, explanation, and reasoning for Task 12

This file intentionally holds ALL hint and solution content so the notebook
itself stays free of spoilers. Solutions are only ever shown when you
explicitly call answer(n) -- nothing here runs automatically.
"""

TASKS = {}


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

def _get_task(n):
    if n not in TASKS:
        valid = f"1-{max(TASKS)}" if TASKS else "none loaded"
        raise ValueError(
            f"There is no Task {n}. Valid task numbers are {valid}."
        )
    return TASKS[n]


def hint(n, level=1):
    """Print a hint for task n. Use level=2 for a more direct nudge, where available."""
    task = _get_task(n)
    hints = task["hints"]
    if level < 1 or level > len(hints):
        max_level = len(hints)
        raise ValueError(
            f"Task {n} only has hint level(s) 1-{max_level}. "
            f"You asked for level {level}."
        )
    bar = "-" * 60
    print(bar)
    print(f"Task {n} - Hint (level {level}/{len(hints)})")
    print(bar)
    print(hints[level - 1])
    if level < len(hints):
        print(f"\n(A more direct hint is available: hint({n}, level={level + 1}))")


def answer(n):
    """Print the full solution, its expected output, explanation, and key reasoning for task n."""
    task = _get_task(n)
    bar = "=" * 60
    print(bar)
    print(f"Task {n} - Solution: {task['title']}")
    print(bar)
    print("\n" + task["solution"].strip("\n") + "\n")
    print("-" * 60)
    output = task.get("output", "")
    if output.strip():
        print("Expected output:")
        print("-" * 60)
        print(output.rstrip("\n"))
    else:
        print("Expected output: (none -- this is a written reasoning question, not a code task.)")
    print("-" * 60)
    print("Explanation:")
    print(task["explanation"].strip())
    if task.get("reasoning"):
        print("\nKey reasoning:")
        print(task["reasoning"].strip())
    if task.get("alternative"):
        print("\nAlternative approach:")
        print(task["alternative"].strip())


def list_tasks(phase=None):
    """List task numbers and titles, optionally filtered by phase ('learning' or 'testing')."""
    for n in sorted(TASKS):
        t = TASKS[n]
        if phase and t["phase"] != phase:
            continue
        print(f"Task {n:>2} [{t['phase']:<8} | {t['difficulty']:<10}] {t['title']}")


def _validate():
    """Internal self-check: no gaps, no duplicates, every task has required fields."""
    nums = sorted(TASKS)
    required = {"phase", "title", "difficulty", "hints", "solution", "explanation"}
    problems = []
    for n in nums:
        missing = required - set(TASKS[n])
        if missing:
            problems.append(f"Task {n} missing fields: {missing}")
    expected = list(range(1, len(nums) + 1))
    if nums != expected:
        problems.append(f"Task numbering has gaps or duplicates: {nums}")
    if problems:
        raise AssertionError("\n".join(problems))
    return True


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 1 - Foundation
# ---------------------------------------------------------------------------

TASKS[1] = dict(
    phase="learning", difficulty="easy", title="Load the Dataset Files",
    hints=[
        "pd.read_csv() takes a file path and returns a DataFrame. You need four separate calls, "
        "one per file, and each result needs its own variable name.",
    ],
    solution='''
import pandas as pd

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")
order_items = pd.read_csv("data/order_items.csv")

for name, df in [("customers", customers), ("products", products),
                  ("orders", orders), ("order_items", order_items)]:
    print(name, df.shape)
''',
    explanation=(
        "pd.read_csv() infers column types automatically from the file, which is convenient but "
        "not always correct -- you'll fix a few of these guesses in later tasks (discount_pct, "
        "order_date, membership_tier). Keeping each table in its own variable is what makes the "
        "later merge/join tasks possible."
    ),
    reasoning=(
        "Loading everything up front, before any cleaning, mirrors how a real analysis starts: "
        "you inspect raw data before deciding what needs fixing."
    ),
)

TASKS[2] = dict(
    phase="learning", difficulty="easy", title="Series & DataFrame Recap",
    hints=[
        "pd.Series(list, name=...) builds a labeled 1-D array. pd.DataFrame(dict_of_lists) builds "
        "a 2-D table where each key becomes a column.",
    ],
    solution='''
import pandas as pd

prices = pd.Series([199.0, 449.0, 899.0], name="sample_price")
print(prices)

sample = pd.DataFrame({
    "product_name": ["Headphones", "Smartwatch", "Tablet"],
    "unit_price": [199.0, 449.0, 899.0],
})
print(sample)
''',
    explanation=(
        "A DataFrame is essentially a dict of aligned Series sharing one index. Every column you "
        "select out of a DataFrame (df['unit_price']) is a Series -- this is why Series and "
        "DataFrame operations feel so similar throughout the rest of the workbook."
    ),
)

TASKS[3] = dict(
    phase="learning", difficulty="easy", title="First Look at the Data",
    hints=[
        "You need six separate pieces of information about `customers`: the first rows, the last "
        "rows, a structural summary, the row/column count, the column dtypes, and the column names. "
        "There's a dedicated method or attribute for each.",
    ],
    solution='''
print(customers.head())
print(customers.tail())
customers.info()
print(customers.shape)
print(customers.dtypes)
print(customers.columns)
''',
    explanation=(
        ".head()/.tail() show actual rows so you can eyeball the data. .info() gives dtypes, "
        "non-null counts, and memory usage in one call -- usually the fastest way to spot a missing"
        "-value or wrong-dtype problem before you've written a single line of cleaning code."
    ),
    reasoning=(
        ".shape, .dtypes, and .columns are attributes (no parentheses), while .head(), .tail(), "
        "and .info() are methods -- a distinction that trips people up constantly in interviews."
    ),
)

TASKS[4] = dict(
    phase="learning", difficulty="easy", title="Renaming & Indexing",
    hints=[
        "rename(columns={...}) takes a mapping of old name to new name and returns a new "
        "DataFrame unless you pass inplace=True. set_index('col') moves a column into the row "
        "index; reset_index() moves it back out.",
    ],
    solution='''
renamed = customers.rename(columns={"first_name": "given_name", "last_name": "surname"})
print(renamed.columns)

by_order_id = orders.set_index("order_id")
print(by_order_id.head())

back_to_default = by_order_id.reset_index()
print(back_to_default.head())
''',
    explanation=(
        "rename() is non-destructive by default -- it hands back a copy, leaving the original "
        "DataFrame untouched, which is usually what you want in an exploratory notebook."
    ),
    reasoning=(
        "Setting a meaningful column as the index (like order_id) makes .loc[] lookups by that "
        "key much faster and more readable than filtering with a boolean mask every time."
    ),
)

TASKS[5] = dict(
    phase="learning", difficulty="easy", title="Selecting Columns and Rows",
    hints=[
        "df['col'] and df[['col1','col2']] select columns. df.loc[] selects by label (row index "
        "value and column name). df.iloc[] selects by integer position, regardless of what the "
        "labels actually are.",
    ],
    solution='''
print(orders["order_status"].head())
print(orders[["order_id", "order_status", "discount_pct"]].head())

print(orders.loc[0, "order_status"])
print(orders.loc[0:4, ["order_id", "order_status"]])

print(orders.iloc[0])
print(orders.iloc[0:5, 0:3])
''',
    explanation=(
        ".loc includes both endpoints of a slice (0:4 gives 5 rows) because it's label-based; "
        ".iloc excludes the stop position (0:5 gives 5 rows: positions 0-4) because it's "
        "position-based, matching normal Python slicing."
    ),
    reasoning=(
        "Mixing df['col'][df['other'] > 5] = x (chained indexing) instead of .loc is the single "
        "most common source of the SettingWithCopyWarning you'll debug later in Task 56."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 2 - Data Cleaning
# ---------------------------------------------------------------------------

TASKS[6] = dict(
    phase="learning", difficulty="easy", title="Finding and Handling Missing Data",
    hints=[
        "isna() (or notna()) gives you a boolean map of missing values; .sum() on that turns it "
        "into a per-column count. fillna() replaces missing values with something specific; "
        "dropna() removes rows/columns that contain them.",
    ],
    solution='''
print(customers.isna().sum())

cleaned = customers.copy()
cleaned["membership_tier"] = cleaned["membership_tier"].fillna("Bronze")
cleaned["email"] = cleaned["email"].fillna("unknown")

fully_known = customers.dropna(subset=["city"])
print(fully_known.shape, customers.shape)
''',
    explanation=(
        "There's no single correct way to handle missing data -- it depends on what the missing "
        "value means. Here, a missing membership_tier plausibly means the lowest/default tier, so "
        "fillna() with a value is reasonable. A missing city has no safe default, so dropping or "
        "flagging it is more honest than guessing."
    ),
    reasoning=(
        "Always run isna().sum() before choosing a strategy. Filling blindly with 0 or the mean "
        "can silently distort every downstream calculation -- you'll see exactly this problem "
        "in Task 61."
    ),
)

TASKS[7] = dict(
    phase="learning", difficulty="easy", title="Fixing Data Types",
    hints=[
        "astype() converts a column to a new dtype. Categorical columns with a limited set of "
        "repeated values (like membership_tier) benefit from astype('category'). A numeric column "
        "that contains missing values can't be plain int64 -- pandas has a nullable integer dtype "
        "for that: 'Int64' (capital I).",
    ],
    solution='''
df = customers.copy()
df["membership_tier"] = df["membership_tier"].astype("category")
print(df["membership_tier"].dtype)

orders_typed = orders.copy()
orders_typed["discount_pct"] = orders_typed["discount_pct"].astype("Int64")
print(orders_typed["discount_pct"].dtype)
print(orders_typed["discount_pct"].head(10))
''',
    explanation=(
        "Plain int64 cannot represent missing values (NaN is a float concept), so pandas silently "
        "upcasts a numeric column with any NaN to float64. The nullable 'Int64' dtype was added "
        "specifically to let you keep integer semantics while still allowing <NA>."
    ),
    reasoning=(
        "astype('category') doesn't just save memory -- it also makes groupby() and value_counts() "
        "faster on columns with a small number of repeated values, because comparisons happen on "
        "integer codes instead of full string objects."
    ),
)

TASKS[8] = dict(
    phase="learning", difficulty="easy", title="Correcting Inconsistent Values with replace()",
    hints=[
        "replace() takes a dictionary mapping old values to new values and works on an entire "
        "column at once -- pass it a dict where every key is a current order_status value.",
    ],
    solution='''
status_map = {
    "Completed": "Success",
    "Cancelled": "Failed",
    "Returned": "Refunded",
    "Pending": "In Progress",
}
orders["status_label"] = orders["order_status"].replace(status_map)
print(orders[["order_status", "status_label"]].drop_duplicates())
''',
    explanation=(
        "replace() does exact value substitution across the whole Series in one call, which is "
        "cleaner than writing an if/elif ladder or calling apply() with a custom function for a "
        "simple lookup like this."
    ),
    reasoning=(
        "replace() is for swapping known, exact values. For pattern-based text cleanup (case, "
        "whitespace, partial matches) the .str accessor in Task 14 is the right tool instead."
    ),
)

TASKS[9] = dict(
    phase="learning", difficulty="easy", title="Dropping Rows and Columns",
    hints=[
        "drop() removes rows by label (default axis=0) or columns when you pass axis=1 or "
        "columns=[...]. Neither happens in place unless you say so.",
    ],
    solution='''
no_shipping_city = orders.drop(columns=["shipping_city"])
print(no_shipping_city.columns)

first_three_gone = orders.drop(orders.index[:3])
print(len(first_three_gone), len(orders))
''',
    explanation=(
        "drop(columns=[...]) is the modern, explicit way to remove columns -- prefer it over "
        "drop('col', axis=1), which relies on remembering which axis number means 'columns'."
    ),
)

TASKS[10] = dict(
    phase="learning", difficulty="easy", title="Detecting and Removing Duplicate Records",
    hints=[
        "duplicated() flags rows that are exact repeats of an earlier row (keeping the first "
        "occurrence unflagged by default). drop_duplicates() removes them. Both accept a subset= "
        "argument if you only care about certain columns matching.",
    ],
    solution='''
print("Exact duplicate rows in customers:", customers.duplicated().sum())
customers_clean = customers.drop_duplicates()
print(customers_clean.shape, customers.shape)

print("Duplicate orders:", orders.duplicated().sum())
orders_clean = orders.drop_duplicates()
print(orders_clean.shape, orders.shape)
''',
    explanation=(
        "Both customers and orders were generated with a handful of exact duplicate rows mixed "
        "in, simulating a double-submitted form or a retry that wrote the same record twice -- a "
        "very common real-world data issue."
    ),
    reasoning=(
        "duplicated().sum() before you drop anything gives you a number to sanity-check against "
        "after -- always confirm row counts changed by exactly what you expected."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 3 - Selection & Filtering
# ---------------------------------------------------------------------------

TASKS[11] = dict(
    phase="learning", difficulty="easy", title="Conditional Selection with Boolean Indexing",
    hints=[
        "orders['order_status'] == 'Completed' produces a boolean Series the same length as "
        "orders. Passing that boolean Series inside orders[...] keeps only the True rows.",
    ],
    solution='''
completed = orders[orders["order_status"] == "Completed"]
print(completed.shape)
print(completed["order_status"].unique())
''',
    explanation=(
        "Under the hood, orders['order_status'] == 'Completed' is just elementwise comparison, "
        "producing True/False for every row. df[boolean_series] is pandas' core filtering "
        "mechanism -- almost everything else (query, loc with a condition) is built on this idea."
    ),
)

TASKS[12] = dict(
    phase="learning", difficulty="easy", title="Combining Multiple Filter Conditions",
    hints=[
        "Combine boolean Series with & (and), | (or), and ~ (not) -- not the Python keywords "
        "'and'/'or'. Each individual condition needs its own parentheses because of operator "
        "precedence.",
    ],
    solution='''
big_discount_completed = orders[
    (orders["order_status"] == "Completed") & (orders["discount_pct"] >= 20)
]
print(big_discount_completed.shape)

not_pending = orders[~(orders["order_status"] == "Pending")]
print(not_pending["order_status"].unique())

upi_or_card = orders[
    (orders["payment_method"] == "UPI") | (orders["payment_method"] == "Credit Card")
]
print(upi_or_card.shape)
''',
    explanation=(
        "Python's 'and'/'or' expect a single True/False value, but a comparison like "
        "orders['discount_pct'] >= 20 returns thousands of True/False values at once -- that's "
        "why pandas requires the bitwise operators &, |, ~, which work elementwise."
    ),
    reasoning=(
        "Forgetting the parentheses around each condition is the #1 cause of the confusing "
        "'The truth value of a Series is ambiguous' error."
    ),
)

TASKS[13] = dict(
    phase="learning", difficulty="easy", title="Filtering with query()",
    hints=[
        "query() takes a string expression using column names directly (no quotes, no df["
        "'...']). To reference a Python variable inside the string, prefix it with @.",
    ],
    solution='''
result = orders.query("order_status == 'Completed' and discount_pct >= 20")
print(result.shape)

threshold = 30
high_discount = orders.query("discount_pct >= @threshold")
print(high_discount.shape)
''',
    explanation=(
        "query() reads like a SQL WHERE clause, which many people find more readable once "
        "conditions stack up beyond two or three -- but it's evaluating a string, so typos in "
        "column names only surface at runtime, not at write time."
    ),
    alternative=(
        "orders[(orders['order_status'] == 'Completed') & (orders['discount_pct'] >= 20)] is "
        "equivalent boolean-indexing syntax; both are idiomatic, and the choice is mostly style."
    ),
)

TASKS[14] = dict(
    phase="learning", difficulty="medium", title="Cleaning and Inspecting Text Columns",
    hints=[
        "Every string method you'd normally call on a single Python string (strip, lower, "
        "contains, split, len) has a column-wide equivalent through the .str accessor, e.g. "
        "df['col'].str.strip().",
    ],
    solution='''
clean_city = customers["city"].str.strip().str.lower()
print(clean_city.value_counts())

has_at_symbol = customers["email"].str.contains("@", na=False)
print("Malformed emails:", (~has_at_symbol & customers["email"].notna()).sum())

email_domain = customers["email"].str.split("@").str[1]
print(email_domain.value_counts(dropna=True))
''',
    explanation=(
        "The .str accessor is null-safe by default -- calling .str.contains('@') on a Series "
        "with NaN entries returns NaN for those rows unless you pass na=False, which is why the "
        "malformed-email check explicitly handles that."
    ),
    reasoning=(
        "str.split('@').str[1] is a common two-step pattern: split() returns a Series of lists, "
        "and a second .str[index] pulls out one element from each list."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 4 - Sorting & Descriptive Statistics
# ---------------------------------------------------------------------------

TASKS[15] = dict(
    phase="learning", difficulty="easy", title="Sorting Data",
    hints=[
        "sort_values(by='col') sorts rows by a column's values; pass ascending=False to reverse "
        "it, and a list for by= to sort by multiple columns in order.",
    ],
    solution='''
by_price = products.sort_values(by="unit_price", ascending=False)
print(by_price[["product_name", "unit_price"]].head())

by_cat_then_price = products.sort_values(by=["category", "unit_price"])
print(by_cat_then_price[["category", "product_name", "unit_price"]].head())

print(orders.sort_index().head())
''',
    explanation=(
        "sort_values with a list in by= sorts hierarchically: rows are grouped by the first "
        "column, and within each group ordered by the second -- the same idea as ORDER BY col1, "
        "col2 in SQL."
    ),
)

TASKS[16] = dict(
    phase="learning", difficulty="easy", title="Descriptive Statistics",
    hints=[
        "mean(), median(), std(), min(), and max() each work on a single column or across an "
        "entire numeric DataFrame at once. describe() gives you all of the common ones together.",
    ],
    solution='''
print(products["unit_price"].mean())
print(products["unit_price"].median())
print(products["unit_price"].std())
print(products.describe())
''',
    explanation=(
        "The gap between mean and median for unit_price is a quick tell for skew -- a mean "
        "noticeably above the median usually means a handful of high-priced outliers (like the "
        "data-entry errors baked into this products table) are pulling the average up."
    ),
)

TASKS[17] = dict(
    phase="learning", difficulty="easy", title="Counting Category Frequencies",
    hints=[
        "value_counts() on a single column returns counts per unique value, sorted descending by "
        "default. Pass normalize=True to get proportions instead of raw counts.",
    ],
    solution='''
print(orders["order_status"].value_counts())
print(orders["order_status"].value_counts(normalize=True).round(3))
print(orders["payment_method"].value_counts(dropna=False))
''',
    explanation=(
        "value_counts(dropna=False) is worth using whenever you also want to see how many "
        "missing values there are, right alongside the real categories, instead of them silently "
        "disappearing from the count."
    ),
)

TASKS[18] = dict(
    phase="learning", difficulty="easy", title="Correlation and Covariance",
    hints=[
        "corr() and cov() work on a numeric DataFrame or between two specific Series, e.g. "
        "df['a'].corr(df['b']).",
    ],
    solution='''
numeric_orders = orders[["discount_pct"]].copy()
numeric_orders["quantity_total"] = order_items.groupby("order_id")["quantity"].sum().reindex(
    orders["order_id"]
).values

print(numeric_orders.corr())
print(numeric_orders["discount_pct"].cov(numeric_orders["quantity_total"]))
''',
    explanation=(
        "Correlation is a unitless number between -1 and 1 that describes linear association; "
        "covariance carries the units of both variables and is mostly useful as an intermediate "
        "quantity, which is why corr() is the one people actually report."
    ),
    reasoning=(
        "Correlation says nothing about causation, and it only captures linear relationships -- "
        "two variables can be strongly related in a curved way and still show near-zero "
        "correlation."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 5 - GroupBy & Aggregation
# ---------------------------------------------------------------------------

TASKS[19] = dict(
    phase="learning", difficulty="easy", title="Split-Apply-Combine: Basic Aggregation",
    hints=[
        "groupby('col') splits the DataFrame into groups sharing the same value in 'col'. "
        "Chain an aggregation like .mean() or .sum() on a specific column of the result.",
    ],
    solution='''
avg_price_by_category = products.groupby("category")["unit_price"].mean()
print(avg_price_by_category)

orders_per_status = orders.groupby("order_status")["order_id"].count()
print(orders_per_status)
''',
    explanation=(
        "groupby() itself is lazy -- it just remembers how to split the data. Nothing is "
        "actually computed until you chain an aggregation like .mean() or .count() on top of it."
    ),
    reasoning=(
        "This is the 'split -> apply -> combine' pattern: pandas splits rows into groups, "
        "applies your aggregation independently to each, then combines the results back into "
        "one Series or DataFrame indexed by the group keys."
    ),
)

TASKS[20] = dict(
    phase="learning", difficulty="medium", title="Multiple Aggregations with agg()",
    hints=[
        "agg() accepts a dictionary mapping column name to one or more aggregation functions "
        "(as a string like 'mean', or a list of strings for several at once on the same column).",
    ],
    solution='''
summary = products.groupby("category").agg(
    avg_price=("unit_price", "mean"),
    min_price=("unit_price", "min"),
    max_price=("unit_price", "max"),
    n_products=("product_id", "count"),
)
print(summary)
''',
    explanation=(
        "This is 'named aggregation' -- each keyword argument becomes a clean output column "
        "name, and its value is a (column, function) pair. It replaces the older nested-dict "
        "style, which produced awkward MultiIndex columns."
    ),
)

TASKS[21] = dict(
    phase="learning", difficulty="medium", title="GroupBy transform() vs apply()",
    hints=[
        "You want a value computed per group, but aligned back onto every original row -- that's "
        "exactly what groupby(...)[col].transform(func) is built for, unlike .agg() which "
        "collapses to one row per group.",
    ],
    solution='''
order_items["item_total"] = order_items["quantity"] * order_items["unit_price_at_purchase"]

order_total = order_items.groupby("order_id")["item_total"].transform("sum")
order_items["pct_of_order"] = (order_items["item_total"] / order_total * 100).round(2)

print(order_items[["order_id", "item_total", "pct_of_order"]].head(8))
print(len(order_items))  # unchanged row count confirms transform, not agg
''',
    explanation=(
        "transform('sum') computes the group sum but broadcasts it back to every row belonging "
        "to that group, so the output is the same length as the input -- ideal for 'this row's "
        "share of its group's total' calculations."
    ),
    reasoning=(
        "You could get the same result with groupby().apply(lambda g: g['item_total'] / "
        "g['item_total'].sum()), but transform() with a named function like 'sum' is faster "
        "because pandas can use a vectorized, C-level implementation instead of calling a Python "
        "function once per group."
    ),
)

TASKS[22] = dict(
    phase="learning", difficulty="medium", title="Pivot Tables for Cross-Tabular Summaries",
    hints=[
        "pivot_table(values=, index=, columns=, aggfunc=) reshapes long data into a grid: one "
        "row per index value, one column per columns value, cells filled by aggfunc.",
    ],
    solution='''
pivot = products.pivot_table(
    values="unit_price", index="category", columns="is_active", aggfunc="mean"
)
print(pivot.round(2))
''',
    explanation=(
        "pivot_table is essentially groupby(['category', 'is_active'])['unit_price'].mean() "
        "followed by unstack() -- it groups by two keys at once but lays the second key out "
        "across columns instead of stacking it into the row index."
    ),
)

TASKS[23] = dict(
    phase="learning", difficulty="easy", title="Crosstab: Frequency Cross-Tabulation",
    hints=[
        "pd.crosstab(index_series, columns_series) counts how often each combination occurs -- "
        "pass normalize='index' to see row-wise percentages instead of raw counts.",
    ],
    solution='''
ct = pd.crosstab(orders["order_status"], orders["payment_method"])
print(ct)

ct_pct = pd.crosstab(orders["order_status"], orders["payment_method"], normalize="index")
print(ct_pct.round(3))
''',
    explanation=(
        "crosstab() is pivot_table specialized for plain counting -- you hand it two (or more) "
        "Series directly rather than column names plus an aggfunc, and it defaults to aggfunc="
        "'count'."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 6 - Combining Data
# ---------------------------------------------------------------------------

TASKS[24] = dict(
    phase="learning", difficulty="easy", title="Stacking DataFrames with concat()",
    hints=[
        "pd.concat([df1, df2]) stacks DataFrames that share the same columns on top of each "
        "other. Pass ignore_index=True if you don't want the original row indices preserved.",
    ],
    solution='''
electronics = products[products["category"] == "Electronics"]
books = products[products["category"] == "Books"]

combined = pd.concat([electronics, books], ignore_index=True)
print(combined.shape, electronics.shape[0] + books.shape[0])
''',
    explanation=(
        "concat() is a row-wise (or, with axis=1, column-wise) stack -- it does not match rows "
        "on any key the way merge() does. It only lines columns up by name."
    ),
)

TASKS[25] = dict(
    phase="learning", difficulty="medium", title="SQL-Style Joins with merge()",
    hints=[
        "merge(left, right, on='key', how='inner'/'left'/'right'/'outer') matches rows where the "
        "key column agrees. Try the same merge with each how= value and compare the row counts.",
    ],
    solution='''
inner = pd.merge(orders, customers, on="customer_id", how="inner")
left = pd.merge(orders, customers, on="customer_id", how="left")
outer = pd.merge(orders, customers, on="customer_id", how="outer")

print("inner:", inner.shape[0])
print("left :", left.shape[0])
print("outer:", outer.shape[0])
''',
    explanation=(
        "inner keeps only customer_id values present in both tables, so it silently drops the "
        "orphan orders you saw in Task 6/26. left keeps every order regardless of whether a "
        "matching customer exists, filling unmatched customer columns with NaN. outer keeps "
        "every row from both sides."
    ),
    reasoning=(
        "how='inner' is the default. Using it without thinking is a common source of silently "
        "shrunk datasets -- always check row counts before and after a merge."
    ),
)

TASKS[26] = dict(
    phase="learning", difficulty="medium", title="Auditing Joins with indicator and validate",
    hints=[
        "merge(..., indicator=True) adds a '_merge' column labeling each row 'left_only', "
        "'right_only', or 'both' -- filter on that to isolate unmatched rows. validate='m:1' "
        "raises an error instead of silently letting an unexpected duplicate key through.",
    ],
    solution='''
audited = pd.merge(
    orders, customers, on="customer_id", how="left", indicator=True
)
orphans = audited[audited["_merge"] == "left_only"]
print("Orders with no matching customer:", len(orphans))

try:
    pd.merge(orders, customers, on="customer_id", how="left", validate="m:1")
    print("validate passed: customer_id is unique in customers")
except Exception as e:
    print("validate caught a problem:", e)
''',
    explanation=(
        "indicator=True turns an invisible problem (rows quietly dropped or filled with NaN) "
        "into something you can filter, count, and report on directly."
    ),
    reasoning=(
        "validate='m:1' asserts that the right-hand table's key is unique -- exactly the "
        "assumption merge() makes silently. If customers ever contained duplicate customer_id "
        "values, an ordinary merge would multiply your order rows without any warning; validate "
        "turns that into a loud, immediate error instead."
    ),
)

TASKS[27] = dict(
    phase="learning", difficulty="medium", title="Joining on the Index with join()",
    hints=[
        "join() combines DataFrames using their index rather than a named key column. Set the "
        "join key as the index on both sides first with set_index().",
    ],
    solution='''
products_by_id = products.set_index("product_id")

item_qty = order_items.groupby("product_id")["quantity"].sum().rename("total_units_sold")
item_qty_df = item_qty.to_frame()

result = products_by_id.join(item_qty_df, how="left")
print(result[["product_name", "total_units_sold"]].head())
''',
    explanation=(
        "join() is really just merge() with left_index=True (and right_index=True unless you "
        "pass on=). It reads more naturally when both pieces of data are already indexed by the "
        "same key, which is common right after a groupby()."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 7 - Time Series
# ---------------------------------------------------------------------------

TASKS[28] = dict(
    phase="learning", difficulty="medium", title="Parsing Messy Date Strings",
    hints=[
        "pd.to_datetime(series, errors='coerce') turns unparseable strings into NaT instead of "
        "raising an exception. A few order_date values use DD/MM/YYYY instead of YYYY-MM-DD -- "
        "check what dayfirst=True does.",
    ],
    solution='''
orders["order_date_parsed"] = pd.to_datetime(
    orders["order_date"], format="mixed", dayfirst=True, errors="coerce"
)
print(orders["order_date_parsed"].isna().sum(), "unparseable dates")
print(orders[["order_date", "order_date_parsed"]].sample(5, random_state=1))
''',
    explanation=(
        "format='mixed' tells pandas each row may use a different date layout and to infer per "
        "row rather than assuming one format for the whole column -- necessary here because most "
        "dates are YYYY-MM-DD but a few are DD/MM/YYYY or include a timestamp."
    ),
    reasoning=(
        "errors='coerce' is the honest choice for messy real-world input: it converts what it "
        "can and marks the rest NaT, letting you measure and decide what to do with failures "
        "rather than crashing the whole pipeline or silently guessing."
    ),
)

TASKS[29] = dict(
    phase="learning", difficulty="easy", title="Extracting Date Parts",
    hints=[
        "Once a column is a real datetime dtype, the .dt accessor exposes .year, .month, "
        "'.day_name()', and comparisons like .dayofweek >= 5 for weekends.",
    ],
    solution='''
d = orders["order_date_parsed"]
orders["order_year"] = d.dt.year
orders["order_month"] = d.dt.month
orders["order_day_name"] = d.dt.day_name()
orders["is_weekend"] = d.dt.dayofweek >= 5

print(orders[["order_date_parsed", "order_year", "order_month",
              "order_day_name", "is_weekend"]].head())
''',
    explanation=(
        "The .dt accessor is the datetime equivalent of .str -- it only works on a Series that "
        "is genuinely datetime64 dtype, which is exactly why Task 28 had to run first."
    ),
)

TASKS[30] = dict(
    phase="learning", difficulty="medium", title="Resampling a Time Series",
    hints=[
        "resample() only works on a DataFrame (or Series) with a DatetimeIndex, so set the "
        "parsed date as the index first. Then resample('ME') groups by calendar month, similar "
        "in spirit to groupby() but for time buckets.",
    ],
    solution='''
completed = orders[orders["order_status"] == "Completed"].copy()
completed = completed.set_index("order_date_parsed").sort_index()

monthly_orders = completed.resample("ME")["order_id"].count()
print(monthly_orders)

weekly_discount = completed.resample("W")["discount_pct"].mean()
print(weekly_discount.head())
''',
    explanation=(
        "resample('ME') buckets every row into the calendar month its index falls in, then "
        "applies the aggregation you chain on afterward -- functionally a groupby() where the "
        "group key is 'which month is this timestamp in' instead of a categorical column."
    ),
)

TASKS[31] = dict(
    phase="learning", difficulty="medium", title="Rolling and Expanding Windows",
    hints=[
        "rolling(window=N) looks at a moving window of the last N rows and applies an aggregation "
        "(commonly .mean()). expanding() does the same but the window grows to include everything "
        "from the start up to the current row.",
    ],
    solution='''
daily_revenue = (
    order_items.merge(orders[["order_id", "order_date_parsed", "order_status"]], on="order_id")
    .query("order_status == 'Completed'")
    .assign(item_total=lambda d: d["quantity"] * d["unit_price_at_purchase"])
    .groupby("order_date_parsed")["item_total"].sum()
    .sort_index()
)

rolling_7d = daily_revenue.rolling(window=7).mean()
cumulative = daily_revenue.expanding().sum()

print(rolling_7d.tail())
print(cumulative.tail())
''',
    explanation=(
        "rolling(7).mean() smooths out day-to-day noise by averaging each day with the six "
        "before it -- the first 6 values are NaN because there aren't yet 7 days of history to "
        "average. expanding().sum() is a running total from the very first day onward."
    ),
)

TASKS[32] = dict(
    phase="learning", difficulty="medium", title="Period-over-Period Change",
    hints=[
        "shift(1) moves every value down by one period so you can compare 'this period' to 'the "
        "previous period' on the same row. diff() gives you the raw difference directly; "
        "pct_change() gives you the same comparison as a percentage.",
    ],
    solution='''
completed = orders[orders["order_status"] == "Completed"].copy()
monthly = (
    completed.set_index("order_date_parsed").sort_index()
    .resample("ME")["order_id"].count()
)

monthly_df = monthly.to_frame(name="order_count")
monthly_df["previous_month"] = monthly_df["order_count"].shift(1)
monthly_df["change"] = monthly_df["order_count"].diff()
monthly_df["pct_change"] = monthly_df["order_count"].pct_change().round(3)

print(monthly_df)
''',
    explanation=(
        "diff() is literally current_value - shift(1); pct_change() is "
        "diff() / shift(1). Knowing that shift() is the primitive underneath both makes it much "
        "easier to build custom period-over-period logic when the built-ins don't quite fit."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 8 - Apply/Map & Bucketing
# ---------------------------------------------------------------------------

TASKS[33] = dict(
    phase="learning", difficulty="medium", title="Row-wise and Column-wise apply()",
    hints=[
        "DataFrame.apply(func, axis=1) calls func once per row, passing the whole row as a "
        "Series -- useful when a calculation needs more than one column at once. axis=0 (the "
        "default) calls func once per column instead.",
    ],
    solution='''
def order_flag(row):
    if row["order_status"] == "Completed" and row["discount_pct"] >= 30:
        return "Big Discount Win"
    if row["order_status"] == "Cancelled":
        return "Lost Sale"
    return "Standard"

orders["order_flag"] = orders.apply(order_flag, axis=1)
print(orders["order_flag"].value_counts())

numeric_products = products[["unit_price"]]
print(numeric_products.apply(lambda col: col.max() - col.min(), axis=0))
''',
    explanation=(
        "apply(axis=1) is flexible -- your function can reference any column of the row -- but "
        "it calls a Python function once per row, so on a large DataFrame it's noticeably slower "
        "than a vectorized alternative. You'll measure exactly how much slower in Task 39/67."
    ),
)

TASKS[34] = dict(
    phase="learning", difficulty="easy", title="Element-wise Mapping with map()",
    hints=[
        "Series.map() applies a function or a dictionary to every element of a single Series, "
        "one value at a time.",
    ],
    solution='''
tier_rank = {"Bronze": 1, "Silver": 2, "Gold": 3, "Platinum": 4}
customers["tier_rank"] = customers["membership_tier"].map(tier_rank)
print(customers[["membership_tier", "tier_rank"]].drop_duplicates())

customers["email_lower"] = customers["email"].map(
    lambda x: x.lower() if isinstance(x, str) else x
)
''',
    explanation=(
        "map() only ever sees one Series and hands back one Series of the same length -- it "
        "can't look at other columns the way apply(axis=1) can. When a dict is used, any value "
        "with no matching key becomes NaN."
    ),
)

TASKS[35] = dict(
    phase="learning", difficulty="medium", title="Bucketing Continuous Values",
    hints=[
        "pd.cut(series, bins=[...], labels=[...]) slices a numeric column into named ranges in "
        "one vectorized call -- no loop or apply() needed for this kind of multi-condition "
        "bucketing.",
    ],
    solution='''
products["price_tier"] = pd.cut(
    products["unit_price"],
    bins=[0, 500, 2000, 5000, float("inf")],
    labels=["Budget", "Mid-range", "Premium", "Luxury"],
)
print(products["price_tier"].value_counts())
''',
    explanation=(
        "pd.cut() is purpose-built for turning a continuous variable into ordered categories and "
        "is both faster and more readable than the equivalent nested apply(lambda x: ...) with "
        "if/elif chains."
    ),
    alternative=(
        "np.select([cond1, cond2, ...], [choice1, choice2, ...], default=...) is the vectorized "
        "tool of choice when your bucketing logic depends on more than one column at once, which "
        "pd.cut() can't handle since it only looks at a single Series."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 9 - Industry Practices
# ---------------------------------------------------------------------------

TASKS[36] = dict(
    phase="learning", difficulty="medium", title="Building Readable Pipelines with pipe()",
    hints=[
        "pipe(func) passes the whole DataFrame into func and returns func's result, letting you "
        "chain custom steps with the same dot-chaining style as built-in methods like "
        ".dropna().sort_values(...).",
    ],
    solution='''
def add_revenue(df):
    return df.assign(revenue=df["quantity"] * df["unit_price_at_purchase"])

def keep_positive_revenue(df):
    return df[df["revenue"] > 0]

result = (
    order_items
    .pipe(add_revenue)
    .pipe(keep_positive_revenue)
    .sort_values("revenue", ascending=False)
    .head(10)
)
print(result[["order_id", "product_id", "revenue"]])
''',
    explanation=(
        "Without pipe(), applying custom functions in sequence means nesting them "
        "(step3(step2(step1(df)))), which reads inside-out. pipe() lets each step read "
        "top-to-bottom in the order it actually runs."
    ),
)

TASKS[37] = dict(
    phase="learning", difficulty="medium", title="Reducing Memory Footprint",
    hints=[
        "memory_usage(deep=True).sum() gives an accurate total for object (string) columns, "
        "unlike the default memory_usage() which underestimates them. astype('category') and "
        "smaller numeric dtypes (e.g. downcasting int64 to int32) usually shrink it a lot.",
    ],
    solution='''
before = customers.memory_usage(deep=True).sum()

optimized = customers.copy()
optimized["membership_tier"] = optimized["membership_tier"].astype("category")
optimized["city"] = optimized["city"].astype("category")

after = optimized.memory_usage(deep=True).sum()
print(f"Before: {before / 1024:.1f} KB, After: {after / 1024:.1f} KB")
print(f"Reduction: {(1 - after / before) * 100:.1f}%")
''',
    explanation=(
        "A category dtype stores each unique string once and represents every row as a small "
        "integer code pointing back to it -- a huge win specifically for low-cardinality text "
        "columns like city or membership_tier, and a poor choice for something like email where "
        "almost every value is unique."
    ),
)

TASKS[38] = dict(
    phase="learning", difficulty="medium", title="Reading Large Files Efficiently",
    hints=[
        "read_csv() accepts usecols= to skip columns you don't need, dtype= to avoid pandas' "
        "type-guessing pass, and chunksize= to return an iterator of smaller DataFrames instead "
        "of loading the whole file into memory at once.",
    ],
    solution='''
cols_needed = ["weekly_self_study_hours", "attendance_percentage", "total_score", "grade"]
subset = pd.read_csv(
    "data/student_performance.csv",
    usecols=cols_needed,
    dtype={"grade": "category"},
)
print(subset.shape)
print(subset.dtypes)

total_rows = 0
grade_counts = None
for chunk in pd.read_csv("data/student_performance.csv", usecols=["grade"], chunksize=200_000):
    total_rows += len(chunk)
    counts = chunk["grade"].value_counts()
    grade_counts = counts if grade_counts is None else grade_counts.add(counts, fill_value=0)

print(total_rows)
print(grade_counts)
''',
    explanation=(
        "usecols= avoids reading and parsing columns you're about to drop anyway -- the cost of "
        "parsing is paid per column during the read, not after. chunksize= turns read_csv into an "
        "iterator: each chunk is processed and can be discarded before the next one loads, so "
        "peak memory usage stays bounded regardless of total file size."
    ),
    reasoning=(
        "This matters specifically for student_performance.csv, which has a million rows -- "
        "comfortably fits in memory here, but the same technique is what lets you process files "
        "that don't."
    ),
)

TASKS[39] = dict(
    phase="learning", difficulty="hard", title="Vectorized Operations vs apply(): A Performance Comparison",
    hints=[
        "Time both approaches on the same million-row column with %timeit or manual "
        "time.perf_counter() calls: one using series.apply(lambda x: ...), the other using a "
        "direct arithmetic/comparison expression on the whole Series.",
    ],
    solution='''
import time

df = pd.read_csv("data/student_performance.csv", usecols=["total_score"])

start = time.perf_counter()
via_apply = df["total_score"].apply(lambda x: "Pass" if x >= 40 else "Fail")
apply_time = time.perf_counter() - start

start = time.perf_counter()
via_vectorized = np.where(df["total_score"] >= 40, "Pass", "Fail")
vector_time = time.perf_counter() - start

print(f"apply():     {apply_time:.3f}s")
print(f"vectorized:  {vector_time:.3f}s")
print(f"speedup:     {apply_time / vector_time:.1f}x")
''',
    explanation=(
        "apply() calls a genuine Python function once per row -- a million individual Python "
        "function calls, each with normal Python-level overhead. The vectorized version pushes "
        "the whole comparison down into NumPy's compiled C loop, doing the equivalent work with "
        "almost no per-element Python overhead."
    ),
    reasoning=(
        "As a rule of thumb: if what you're doing inside apply() could be written as a plain "
        "arithmetic expression, comparison, or a NumPy/pandas built-in, it almost always should "
        "be -- apply() is a fallback for genuinely row-dependent logic that has no vectorized "
        "equivalent, not a default habit."
    ),
)


# ---------------------------------------------------------------------------
# PHASE 1 - LEARNING: Stage 10 - MultiIndex, Reshaping, and Applied Practice
# ---------------------------------------------------------------------------

TASKS[40] = dict(
    phase="learning", difficulty="medium", title="Working with MultiIndex Results",
    hints=[
        "Grouping by two columns at once (groupby(['col1', 'col2'])) produces a result indexed "
        "by both -- a MultiIndex. .loc[] with a tuple selects a specific combination; unstack() "
        "pivots the inner index level into columns.",
    ],
    solution='''
grouped = products.groupby(["category", "is_active"])["unit_price"].mean()
print(grouped)

print(grouped.loc[("Electronics", True)])

wide = grouped.unstack()
print(wide.round(2))
''',
    explanation=(
        "unstack() moves the innermost row index level to become columns -- it's the inverse of "
        "stack(), and it's exactly how pivot_table() gets its grid shape under the hood."
    ),
)

TASKS[41] = dict(
    phase="learning", difficulty="medium", title="Reshaping Wide to Long with melt()",
    hints=[
        "melt(id_vars=[...], value_vars=[...]) takes several columns and stacks them into two "
        "columns: one naming which original column each value came from, one holding the value "
        "itself.",
    ],
    solution='''
wide = products.groupby("category").agg(
    avg_price=("unit_price", "mean"),
    max_price=("unit_price", "max"),
).reset_index()

long = wide.melt(
    id_vars="category", value_vars=["avg_price", "max_price"],
    var_name="metric", value_name="value"
)
print(long.head(10))
''',
    explanation=(
        "melt() is the inverse of pivot(): it converts several value-bearing columns into "
        "name/value pairs on separate rows. It's especially useful before plotting with libraries "
        "that expect one row per (category, metric) combination rather than one column per metric."
    ),
)

TASKS[42] = dict(
    phase="learning", difficulty="medium", title="Ranking and Top-N Selection",
    hints=[
        "nlargest(n, 'col') is a direct, efficient way to get the top N rows by a column without "
        "sorting the whole DataFrame first. rank() assigns each value its rank within the whole "
        "Series (or, combined with groupby, within each group).",
    ],
    solution='''
print(products.nlargest(5, "unit_price")[["product_name", "unit_price"]])
print(products.nsmallest(5, "unit_price")[["product_name", "unit_price"]])

products["price_rank_in_category"] = (
    products.groupby("category")["unit_price"].rank(ascending=False)
)
print(products.sort_values(["category", "price_rank_in_category"]).head(8)
      [["category", "product_name", "unit_price", "price_rank_in_category"]])
''',
    explanation=(
        "nlargest()/nsmallest() are more efficient than sort_values().head(n) on big data "
        "because pandas doesn't have to fully sort every row, only find the top N."
    ),
)

TASKS[43] = dict(
    phase="learning", difficulty="medium", title="Avoiding the SettingWithCopyWarning",
    hints=[
        "Filtering a DataFrame (df[condition]) can return a view or a copy depending on "
        "internals you don't control -- assigning into it afterward is ambiguous to pandas. Call "
        ".copy() right after filtering, before you assign anything new.",
    ],
    solution='''
completed_orders = orders[orders["order_status"] == "Completed"].copy()
completed_orders["discounted_flag"] = completed_orders["discount_pct"] > 0
print(completed_orders["discounted_flag"].value_counts())
''',
    explanation=(
        "orders[orders['order_status'] == 'Completed'] may return a view into the original "
        "DataFrame's memory rather than an independent copy. Assigning a new column onto that "
        "result is exactly the pattern that triggers SettingWithCopyWarning -- pandas can't tell "
        "if you meant to modify the original orders or a separate table."
    ),
    reasoning=(
        "Calling .copy() immediately after any filter you intend to modify removes the ambiguity "
        "entirely and costs very little for datasets of this size -- it's cheap insurance against "
        "a genuinely confusing bug class."
    ),
)

TASKS[44] = dict(
    phase="learning", difficulty="hard", title="End-to-End: Monthly Revenue by Category",
    hints=[
        "This needs every table: order_items has quantity/price, products has category, orders "
        "has date and status. Merge them together first, filter to Completed orders, engineer a "
        "revenue column, parse the date, then group by month and category.",
    ],
    solution='''
full = (
    order_items
    .merge(products[["product_id", "category"]], on="product_id", how="left")
    .merge(orders[["order_id", "order_date", "order_status"]], on="order_id", how="left")
)
full = full[full["order_status"] == "Completed"].copy()
full["order_date"] = pd.to_datetime(full["order_date"], format="mixed", dayfirst=True, errors="coerce")
full["revenue"] = full["quantity"] * full["unit_price_at_purchase"]
full["order_month"] = full["order_date"].dt.to_period("M")

monthly_by_category = full.groupby(["order_month", "category"])["revenue"].sum().unstack()
print(monthly_by_category.round(0))
''',
    explanation=(
        "Each merge brings in exactly the columns needed from that table (via a column subset) "
        "rather than joining entire wide tables together, which keeps the intermediate result "
        "manageable and makes it obvious which column came from where."
    ),
    reasoning=(
        ".dt.to_period('M') collapses a full timestamp down to just its calendar month, which is "
        "a cleaner grouping key than the raw date when you want one bucket per month rather than "
        "per exact day."
    ),
)


# ===========================================================================
# PHASE 2 - TESTING
# ===========================================================================

# ---- Easy (45-52) ----------------------------------------------------------

TASKS[45] = dict(
    phase="testing", difficulty="easy", title="Cancelled Order Count",
    hints=[
        "You need a count of rows matching one specific condition on one column -- there are at "
        "least two one-line ways to get it.",
        "orders['order_status'].value_counts() gives you every status count at once; or filter "
        "with a boolean mask and check len()/shape.",
    ],
    solution='''
print((orders["order_status"] == "Cancelled").sum())
# equivalently:
print(orders["order_status"].value_counts()["Cancelled"])
''',
    explanation=(
        "Summing a boolean Series counts the True values directly, since True behaves as 1 and "
        "False as 0 in arithmetic contexts."
    ),
)

TASKS[46] = dict(
    phase="testing", difficulty="easy", title="Most Expensive Products",
    hints=[
        "You want the top rows by one numeric column -- no full sort of the whole table is "
        "necessary for just the top 5.",
    ],
    solution='''
print(products.nlargest(5, "unit_price")[["product_name", "category", "unit_price"]])
''',
    explanation=(
        "nlargest() is the direct tool for a 'top N by column' question -- sort_values().head() "
        "works too but does more work than necessary by sorting the entire table first."
    ),
)

TASKS[47] = dict(
    phase="testing", difficulty="easy", title="Missing Data Audit",
    hints=[
        "One method call summarizes missing counts per column across the whole DataFrame.",
    ],
    solution='''
print(customers.isna().sum())
''',
    explanation=(
        "isna() flags every cell, and .sum() collapses each column's flags into one count -- the "
        "standard first move on any new DataFrame."
    ),
)

TASKS[48] = dict(
    phase="testing", difficulty="easy", title="Customers Who Joined in 2023",
    hints=[
        "signup_date is currently a plain string column. Think about what has to happen to it "
        "before you can reliably filter by year.",
        "Convert with pd.to_datetime() first, then compare the .dt.year, or use string slicing "
        "on the original ISO-formatted text as a shortcut.",
    ],
    solution='''
signup_dt = pd.to_datetime(customers["signup_date"])
joined_2023 = customers[signup_dt.dt.year == 2023]
print(len(joined_2023))

# shortcut valid specifically because signup_date is consistently YYYY-MM-DD text:
joined_2023_alt = customers[customers["signup_date"].str.startswith("2023")]
print(len(joined_2023_alt))
''',
    explanation=(
        "Comparing a raw string column to a year only works safely when every value follows the "
        "exact same text format -- which happens to be true here, but wouldn't be for "
        "order_date's mixed formats. Converting to a real datetime first is the approach that "
        "generalizes."
    ),
)

TASKS[49] = dict(
    phase="testing", difficulty="easy", title="Standardizing City Names",
    hints=[
        "Recall the .str accessor tools from the Learning Phase for whitespace and casing, "
        "applied before you count anything.",
    ],
    solution='''
clean_city = customers["city"].str.strip().str.title()
print(clean_city.value_counts(dropna=True))
''',
    explanation=(
        "Cleaning before counting matters here: value_counts() treats 'Mumbai', ' mumbai ', and "
        "'MUMBAI' as three different strings unless you normalize them first, which would "
        "silently fragment a single real city into several undercounted entries."
    ),
)

TASKS[50] = dict(
    phase="testing", difficulty="easy", title="Category Dtype Memory Savings",
    hints=[
        "You need a memory measurement before and after a dtype conversion, then compare them.",
    ],
    solution='''
before = orders["order_status"].memory_usage(deep=True)
after = orders["order_status"].astype("category").memory_usage(deep=True)
print(f"Before: {before} bytes, After: {after} bytes")
print(f"Saved: {(1 - after / before) * 100:.1f}%")
''',
    explanation=(
        "order_status only has 4 distinct values repeated across 15,000+ rows, which is exactly "
        "the low-cardinality, high-repetition pattern where category dtype pays off most."
    ),
)

TASKS[51] = dict(
    phase="testing", difficulty="easy", title="Duplicate Customers by Identity",
    hints=[
        "An exact full-row duplicate check misses customers who appear twice with a different "
        "customer_id but the same name/email -- restrict which columns count as 'the same "
        "record'.",
    ],
    solution='''
identity_dupes = customers[
    customers.duplicated(subset=["first_name", "last_name", "email"], keep=False)
]
print(identity_dupes.sort_values("email").head(10))
print("Total involved rows:", len(identity_dupes))
''',
    explanation=(
        "subset=[...] narrows duplicated() to only compare the columns you specify, ignoring "
        "customer_id entirely -- necessary here since the customer_id itself is never repeated, "
        "but the underlying person might be."
    ),
    reasoning=(
        "keep=False marks every row involved in a duplicate group (not just the 2nd, 3rd, ...), "
        "which is what you want when you're trying to inspect the duplicates rather than just "
        "drop them."
    ),
)

TASKS[52] = dict(
    phase="testing", difficulty="easy", title="Most Frequent Customers",
    hints=[
        "Count orders per customer_id, then find the largest value(s) in that count.",
    ],
    solution='''
order_counts = orders.groupby("customer_id")["order_id"].count()
print(order_counts.sort_values(ascending=False).head(5))
''',
    explanation=(
        "groupby('customer_id')['order_id'].count() gives one row per customer with how many "
        "orders they placed; sorting that result descending surfaces the most frequent buyers."
    ),
)


# ---- Medium (53-62) ---------------------------------------------------------

TASKS[53] = dict(
    phase="testing", difficulty="medium", title="Each Line Item's Share of Its Order",
    hints=[
        "The output needs to be the same length as order_items -- every line item keeps its own "
        "row with an added percentage column. Which groupby operation preserves row count instead "
        "of collapsing to one row per group?",
        "transform('sum') broadcasts a per-group total back onto every original row.",
    ],
    solution='''
oi = order_items.copy()
oi["line_total"] = oi["quantity"] * oi["unit_price_at_purchase"]
order_total = oi.groupby("order_id")["line_total"].transform("sum")
oi["pct_of_order"] = (oi["line_total"] / order_total * 100).round(1)
print(oi[["order_id", "line_total", "pct_of_order"]].head(8))
print(len(oi) == len(order_items))
''',
    explanation=(
        "This is the same transform() pattern from the Learning Phase, applied without being "
        "told which function to use -- the tell is the requirement to keep every original row."
    ),
)

TASKS[54] = dict(
    phase="testing", difficulty="medium", title="Orders With No Matching Customer",
    hints=[
        "A plain inner merge would just drop these rows without telling you anything went "
        "wrong. You need a merge option that lets you see what didn't match.",
    ],
    solution='''
audited = orders.merge(customers[["customer_id"]], on="customer_id", how="left", indicator=True)
orphans = audited[audited["_merge"] == "left_only"]
print("Orphan orders:", len(orphans))
print(f"That's {len(orphans) / len(orders) * 100:.2f}% of all orders.")
''',
    explanation=(
        "how='inner' (the default) would simply exclude these rows from the result -- the "
        "resulting DataFrame would look completely normal, with no error, no warning, and a row "
        "count that's just quietly smaller than the original orders table. indicator=True is the "
        "only way to see the problem instead of losing it silently."
    ),
    reasoning=(
        "In a revenue report, an inner join here would understate total order volume by however "
        "many orphan rows exist -- a mistake that could easily go unnoticed for months."
    ),
)

TASKS[55] = dict(
    phase="testing", difficulty="medium", title="Revenue by Category and Quarter",
    hints=[
        "You need product category (from products), order date and status (from orders), and "
        "quantity/price (from order_items) all in one table before any grouping can happen.",
        "Merge the three tables, filter to Completed, engineer revenue and a quarter column, "
        "then pivot category against quarter.",
    ],
    solution='''
full = (
    order_items
    .merge(products[["product_id", "category"]], on="product_id")
    .merge(orders[["order_id", "order_date", "order_status"]], on="order_id")
)
full = full[full["order_status"] == "Completed"].copy()
full["order_date"] = pd.to_datetime(full["order_date"], format="mixed", dayfirst=True, errors="coerce")
full["revenue"] = full["quantity"] * full["unit_price_at_purchase"]
full["quarter"] = full["order_date"].dt.to_period("Q")

pivot = full.pivot_table(values="revenue", index="category", columns="quarter", aggfunc="sum")
print(pivot.round(0))
''',
    explanation=(
        "Three tables, three pieces of information needed (who/what category, when, how much) -- "
        "the shape of the question determines which tables must be joined before any aggregation "
        "makes sense."
    ),
)

TASKS[56] = dict(
    phase="testing", difficulty="medium", title="Debug: SettingWithCopyWarning",
    hints=[
        "The bug is in how the filtered subset is created, not in the arithmetic itself. Compare "
        "against the pattern from the Learning Phase task on this exact warning.",
    ],
    solution='''
# Buggy version (raises SettingWithCopyWarning):
#   discounted = orders[orders["discount_pct"] > 20]
#   discounted["net_note"] = "high discount"

# Fixed version:
discounted = orders[orders["discount_pct"] > 20].copy()
discounted["net_note"] = "high discount"
print(discounted[["order_id", "discount_pct", "net_note"]].head())
''',
    explanation=(
        "orders[orders['discount_pct'] > 20] may return a view rather than an independent copy. "
        "Assigning a new column onto that ambiguous result is what triggers the warning -- adding "
        ".copy() right after the filter removes the ambiguity."
    ),
)

TASKS[57] = dict(
    phase="testing", difficulty="medium", title="Weekend Orders and Customer Tenure",
    hints=[
        "is_weekend needs the parsed order_date. days_since_signup needs both order_date and "
        "signup_date on the same row, which means orders and customers must be merged first.",
    ],
    solution='''
merged = orders.merge(customers[["customer_id", "signup_date"]], on="customer_id", how="left")
merged["order_date"] = pd.to_datetime(merged["order_date"], format="mixed", dayfirst=True, errors="coerce")
merged["signup_date"] = pd.to_datetime(merged["signup_date"])

merged["is_weekend"] = merged["order_date"].dt.dayofweek >= 5
merged["days_since_signup"] = (merged["order_date"] - merged["signup_date"]).dt.days

print(merged[["order_date", "signup_date", "is_weekend", "days_since_signup"]].head())
''',
    explanation=(
        "Subtracting one datetime Series from another produces a Timedelta Series; .dt.days "
        "pulls out the whole-number day count, which is what 'days since' questions usually want."
    ),
)

TASKS[58] = dict(
    phase="testing", difficulty="medium", title="Choosing a Join Type for Customer Spend",
    hints=[
        "Think about what happens to a customer who has never placed an order under each join "
        "type, versus what happens to an order that references a nonexistent customer_id.",
    ],
    solution='''
# left merge, customers as the left table, keeps every customer even with zero orders
spend = customers[["customer_id"]].merge(
    orders.groupby("customer_id")["order_id"].count().rename("order_count"),
    on="customer_id", how="left"
)
spend["order_count"] = spend["order_count"].fillna(0).astype(int)
print(spend["order_count"].describe())
print("Customers with zero orders:", (spend["order_count"] == 0).sum())
''',
    explanation=(
        "how='left' with customers as the left table is correct here: every customer should "
        "appear in a 'total spend per customer' report, including the ones with zero orders, "
        "which should show up as 0 rather than being dropped."
    ),
    reasoning=(
        "how='inner' would silently exclude every customer who hasn't ordered yet, which "
        "understates the customer base and would misrepresent something like an "
        "'average orders per customer' metric by inflating the denominator's floor."
    ),
)

TASKS[59] = dict(
    phase="testing", difficulty="medium", title="Best 7-Day Revenue Window",
    hints=[
        "Build a daily completed-order revenue series first, then apply a moving window "
        "aggregation, then find the maximum of that windowed result.",
    ],
    solution='''
full = (
    order_items.merge(orders[["order_id", "order_date", "order_status"]], on="order_id")
    .query("order_status == 'Completed'")
)
full = full.copy()
full["order_date"] = pd.to_datetime(full["order_date"], format="mixed", dayfirst=True, errors="coerce")
full["revenue"] = full["quantity"] * full["unit_price_at_purchase"]

daily = full.groupby("order_date")["revenue"].sum().sort_index()
rolling_7d = daily.rolling(7).sum()

best_window_end = rolling_7d.idxmax()
print("Best 7-day window ends on:", best_window_end)
print("Revenue in that window:", round(rolling_7d.max(), 2))
''',
    explanation=(
        "idxmax() returns the index label of the maximum value rather than the value itself -- "
        "useful when the question is 'which period' rather than 'how much'."
    ),
)

TASKS[60] = dict(
    phase="testing", difficulty="medium", title="Each Customer's Most Recent Order",
    hints=[
        "You want one row per customer, so a straight groupby().max() on the date works for the "
        "date itself -- but to keep the whole row, rank within the group first and filter to "
        "rank 1.",
    ],
    solution='''
o = orders.copy()
o["order_date_parsed"] = pd.to_datetime(o["order_date"], format="mixed", dayfirst=True, errors="coerce")
o["recency_rank"] = o.groupby("customer_id")["order_date_parsed"].rank(method="first", ascending=False)

most_recent = o[o["recency_rank"] == 1]
print(most_recent[["customer_id", "order_id", "order_date_parsed"]].head())
''',
    explanation=(
        "rank(ascending=False) gives the newest date within each customer's group a rank of 1. "
        "method='first' breaks exact date ties by row order so every row gets a distinct rank, "
        "guaranteeing exactly one 'most recent' row per customer even if two orders share a date."
    ),
)

TASKS[61] = dict(
    phase="testing", difficulty="medium", title="Debug: A Misleading Average Discount",
    hints=[
        "discount_pct has real missing values (Task 6/47). Think about what a missing "
        "discount_pct actually represents versus what filling it with 0 would imply.",
    ],
    solution='''
# What the colleague did:
wrong = orders["discount_pct"].fillna(0).mean()

# Correct: let mean() skip missing values on its own (the default), since a missing
# discount_pct means "we don't know", not "the discount was zero"
correct = orders["discount_pct"].mean()

print("fillna(0) then mean:", round(wrong, 2))
print("mean() with NaN skipped:", round(correct, 2))
''',
    explanation=(
        "fillna(0) before averaging silently treats every 'unknown' discount as if it were "
        "confirmed to be zero, which drags the average down. mean()'s default skipna=True simply "
        "excludes missing values from both the sum and the count, which is the statistically "
        "honest choice when a missing value truly means 'not recorded' rather than 'zero'."
    ),
    reasoning=(
        "The fix here isn't a different function -- it's recognizing that the 'obvious' cleaning "
        "step (fillna) was the bug, not a solution. Always ask what a missing value means before "
        "deciding how to fill it."
    ),
)

TASKS[62] = dict(
    phase="testing", difficulty="medium", title="Cancellation Rate by Payment Method",
    hints=[
        "You want, for each payment method, what fraction of its orders were Cancelled -- a "
        "crosstab with row-wise normalization gets you there in one call.",
    ],
    solution='''
ct = pd.crosstab(orders["payment_method"], orders["order_status"], normalize="index")
print(ct["Cancelled"].sort_values(ascending=False).round(4))
''',
    explanation=(
        "normalize='index' turns each row into percentages that sum to 1 across that row's "
        "categories, which is exactly 'rate' -- the fraction of that payment method's orders "
        "falling into each status."
    ),
    alternative=(
        "The same answer can be built manually with "
        "orders.groupby('payment_method')['order_status'].apply(lambda s: (s == 'Cancelled')."
        "mean()) -- crosstab is just a more direct route to the same number."
    ),
)


# ---- Hard (63-70) -----------------------------------------------------------

TASKS[63] = dict(
    phase="testing", difficulty="hard", title="Debug: A Merge That Multiplied Rows",
    hints=[
        "Check whether the join key is actually unique on both sides of each merge involved. A "
        "many-to-many relationship anywhere in the chain multiplies rows combinatorially.",
    ],
    solution='''
# The buggy chain merges order_items (many rows per order_id) with orders on order_id,
# which is fine (order_items:orders is many:1) -- but if orders itself had duplicate
# order_id rows (as it did before de-duplication in Task 10), each order_items row would
# be matched against every duplicate, multiplying the result.

print("Duplicate order_id values in orders:", orders["order_id"].duplicated().sum())

orders_dedup = orders.drop_duplicates(subset="order_id")
safe_merge = order_items.merge(orders_dedup, on="order_id", how="left")
print("Row count after fix:", len(safe_merge), "vs original order_items:", len(order_items))
''',
    explanation=(
        "merge() matches every row on the left with every row on the right that shares the same "
        "key -- if the 'one' side of what should be a many-to-one relationship secretly contains "
        "duplicate keys, each of those duplicates produces its own copy of every matching left "
        "row, inflating the row count without any error being raised."
    ),
    reasoning=(
        "This is exactly what validate='m:1' from Task 26 is designed to catch automatically -- "
        "it would have raised an error the moment this merge ran, instead of leaving you to "
        "notice the row count was wrong after the fact."
    ),
)

TASKS[64] = dict(
    phase="testing", difficulty="hard", title="Flagging Suspicious Line-Item Prices",
    hints=[
        "You need each line item's unit_price_at_purchase next to the product's current "
        "unit_price on the same row, then compare the two.",
    ],
    solution='''
merged = order_items.merge(
    products[["product_id", "unit_price"]].rename(columns={"unit_price": "current_price"}),
    on="product_id", how="left"
)
merged["pct_deviation"] = (
    (merged["unit_price_at_purchase"] - merged["current_price"]).abs() / merged["current_price"]
)
suspicious = merged[merged["pct_deviation"] > 0.20]
print(f"{len(suspicious)} line items deviate more than 20% from current price")
print(suspicious[["order_id", "product_id", "unit_price_at_purchase", "current_price",
                   "pct_deviation"]].sort_values("pct_deviation", ascending=False).head())
''',
    explanation=(
        "A meaningful deviation threshold like 20% is a business judgment call, not a pandas "
        "concept -- the pandas part is just the merge-and-compare. Note that some deviation is "
        "expected here since unit_price_at_purchase intentionally reflects a discount applied at "
        "purchase time, so not every flagged row is actually an error."
    ),
    reasoning=(
        "This is a genuine engineering judgment task: the 'right' threshold depends on how much "
        "price movement is normal for this business, something you'd calibrate against real "
        "history rather than guess."
    ),
)

TASKS[65] = dict(
    phase="testing", difficulty="hard", title="Sharpest Monthly Revenue Decline",
    hints=[
        "Build the monthly revenue series, then compute the period-over-period percentage change "
        "using the tool from the Learning Phase's Task 32, then find the most negative value.",
    ],
    solution='''
full = (
    order_items.merge(orders[["order_id", "order_date", "order_status"]], on="order_id")
    .query("order_status == 'Completed'")
)
full = full.copy()
full["order_date"] = pd.to_datetime(full["order_date"], format="mixed", dayfirst=True, errors="coerce")
full["revenue"] = full["quantity"] * full["unit_price_at_purchase"]

monthly = full.set_index("order_date").resample("ME")["revenue"].sum()
monthly_change = monthly.pct_change()

worst_month = monthly_change.idxmin()
print("Sharpest decline in:", worst_month)
print(f"Change: {monthly_change.min() * 100:.1f}%")
''',
    explanation=(
        "idxmin() on the pct_change() series finds the month whose revenue dropped the most "
        "relative to the month before it -- note this is different from finding the month with "
        "the lowest absolute revenue."
    ),
)

TASKS[66] = dict(
    phase="testing", difficulty="hard", title="90-Day Cohort Order Frequency",
    hints=[
        "First define each customer's signup month as their cohort. Then, for each order, "
        "compute whether it fell within 90 days of that customer's signup. Then count qualifying "
        "orders per customer, and average that within each cohort.",
    ],
    solution='''
merged = orders.merge(customers[["customer_id", "signup_date"]], on="customer_id", how="inner")
merged = merged.copy()
merged["order_date"] = pd.to_datetime(merged["order_date"], format="mixed", dayfirst=True, errors="coerce")
merged["signup_date"] = pd.to_datetime(merged["signup_date"])
merged["cohort"] = merged["signup_date"].dt.to_period("M")

merged["days_since_signup"] = (merged["order_date"] - merged["signup_date"]).dt.days
early_orders = merged[merged["days_since_signup"].between(0, 90)]

orders_per_customer = early_orders.groupby("customer_id").size()
# customers with zero early orders must still count as 0, so reindex against every customer
all_customers_in_cohort = merged.drop_duplicates("customer_id").set_index("customer_id")["cohort"]
full_counts = orders_per_customer.reindex(all_customers_in_cohort.index, fill_value=0)

cohort_avg = full_counts.groupby(all_customers_in_cohort).mean()
print(cohort_avg.sort_index())
''',
    explanation=(
        "The subtlety is the reindex step: a naive groupby on early_orders alone would silently "
        "omit customers who placed zero orders in their first 90 days, inflating the average for "
        "every cohort. Reindexing against the full customer list first, with fill_value=0, is "
        "what keeps those zeros in the average."
    ),
    reasoning=(
        "This is the classic 'missing rows aren't missing values' trap in groupby analysis -- a "
        "customer who did nothing doesn't appear in early_orders at all, so there's no NaN to "
        "catch; you have to explicitly bring them back in."
    ),
)

TASKS[67] = dict(
    phase="testing", difficulty="hard", title="Timing apply() on a Million Rows",
    hints=[
        "Reuse the same student_performance.csv comparison style from the Learning Phase, but "
        "this time explain, in your own words, why the gap exists rather than just measuring it.",
    ],
    solution='''
import time

df = pd.read_csv("data/student_performance.csv", usecols=["attendance_percentage"])

start = time.perf_counter()
flag_apply = df["attendance_percentage"].apply(lambda x: x < 75)
t_apply = time.perf_counter() - start

start = time.perf_counter()
flag_vector = df["attendance_percentage"] < 75
t_vector = time.perf_counter() - start

print(f"apply(): {t_apply:.3f}s  |  vectorized: {t_vector:.3f}s  |  speedup: {t_apply / t_vector:.1f}x")
''',
    explanation=(
        "apply() invokes the Python interpreter once per row -- a million times, each carrying "
        "Python's normal per-call overhead (bytecode dispatch, object boxing/unboxing). The "
        "vectorized comparison instead runs as a single call into NumPy, which loops over a "
        "contiguous block of memory in compiled C with no per-element Python involvement at all."
    ),
    reasoning=(
        "The mechanism, not just the measurement, is the point: any time an operation can be "
        "expressed as array-level math/comparison instead of per-row Python logic, it should be, "
        "specifically because it avoids paying Python's interpreter overhead millions of times "
        "over."
    ),
)

TASKS[68] = dict(
    phase="testing", difficulty="hard", title="Debug: Pivot Table Silently Dropping Rows",
    hints=[
        "Check whether the column you're using as an index or columns key in pivot_table "
        "contains any missing values, and consider what pivot_table's default aggfunc/dropna "
        "behavior does with a NaN group key.",
    ],
    solution='''
# pivot_table drops any row whose index/columns key is NaN by default
print("Rows with missing membership_tier:", customers["membership_tier"].isna().sum())

broken = customers.pivot_table(values="customer_id", index="membership_tier", aggfunc="count")
print(broken.sum(), "vs total customers:", len(customers))

# Fix 1: fill the missing key with an explicit label before pivoting
fixed = customers.copy()
fixed["membership_tier"] = fixed["membership_tier"].fillna("Unknown")
fixed_pivot = fixed.pivot_table(values="customer_id", index="membership_tier", aggfunc="count")
print(fixed_pivot.sum())

# Fix 2: pass dropna=False directly (keeps unused category combinations, not missing keys --
# for missing key values themselves, filling is still the more explicit fix)
''',
    explanation=(
        "A group key of NaN can't be represented as a row/column label in the output grid, so "
        "pivot_table (like groupby, by default) simply excludes those rows -- the resulting "
        "total silently undercounts customers instead of raising any error."
    ),
    reasoning=(
        "The two fixes address the problem at different points: filling the missing key with an "
        "explicit label ('Unknown') keeps those rows visible in the output; dropna=False on "
        "pivot_table controls whether unused category combinations are shown, which is a related "
        "but distinct issue -- worth knowing the difference between the two in an interview."
    ),
)

TASKS[69] = dict(
    phase="testing", difficulty="hard", title="Top 2 Orders per Customer Without apply()",
    hints=[
        "rank() within a groupby, computed on order value, lets you filter directly instead of "
        "calling apply() with a per-group sort-and-slice.",
    ],
    solution='''
order_value = (
    order_items.assign(line_total=order_items["quantity"] * order_items["unit_price_at_purchase"])
    .groupby("order_id")["line_total"].sum()
    .rename("order_value")
    .reset_index()
    .merge(orders[["order_id", "customer_id"]], on="order_id", how="left")
)

order_value["rank_in_customer"] = (
    order_value.groupby("customer_id")["order_value"].rank(method="first", ascending=False)
)

top2 = order_value[order_value["rank_in_customer"] <= 2]
print(top2.sort_values(["customer_id", "rank_in_customer"]).head(10))
''',
    explanation=(
        "groupby(...).rank() is a vectorized, per-group ranking computed in one pass -- it "
        "achieves the same 'top N per group' result as "
        "groupby().apply(lambda g: g.nlargest(2, 'order_value')) without invoking a Python "
        "function once per group."
    ),
)

TASKS[70] = dict(
    phase="testing", difficulty="hard", title="Halving the Footprint of a Million-Row File",
    hints=[
        "Check the dtype and range of every numeric column -- int64 and float64 are often far "
        "wider than the actual data needs. grade is a small set of repeated letters.",
    ],
    solution='''
df = pd.read_csv("data/student_performance.csv")
before = df.memory_usage(deep=True).sum()

optimized = df.copy()
optimized["student_id"] = pd.to_numeric(optimized["student_id"], downcast="integer")
for col in ["weekly_self_study_hours", "attendance_percentage", "class_participation", "total_score"]:
    optimized[col] = pd.to_numeric(optimized[col], downcast="float")
optimized["grade"] = optimized["grade"].astype("category")

after = optimized.memory_usage(deep=True).sum()
print(f"Before: {before / 1e6:.1f} MB, After: {after / 1e6:.1f} MB")
print(f"Reduction: {(1 - after / before) * 100:.1f}%")
''',
    explanation=(
        "pd.to_numeric(..., downcast='integer'/'float') automatically picks the smallest dtype "
        "that can still hold every value in the column without loss -- e.g. int64 down to int32 "
        "or even int8 if the values are small enough -- instead of you having to inspect ranges "
        "and choose types by hand."
    ),
    reasoning=(
        "Combined with astype('category') for the low-cardinality grade column, this typically "
        "gets well past a 50% reduction on a file shaped like this one, because the original "
        "read_csv call defaulted every numeric column to the widest safe type (int64/float64) "
        "without knowing your actual value ranges."
    ),
)


# ---- Advanced / Interview (71-74) -------------------------------------------

TASKS[71] = dict(
    phase="testing", difficulty="advanced", title="Interview: merge() vs join() vs concat()",
    hints=[
        "Think about what each one aligns on (a key column vs the index vs nothing at all) and "
        "what happens if that assumption is violated.",
    ],
    solution='''
"""
No code required -- this is a verbal/written reasoning question.
Sketch your answer, then compare it to the explanation below.
"""
''',
    explanation=(
        "merge() aligns rows on one or more named key columns and lets you choose how="
        "'inner'/'left'/'right'/'outer' to control unmatched rows. join() does the same thing but "
        "aligns on the index by default, which is convenient right after a groupby() or "
        "set_index() but easy to misuse if the two DataFrames' indexes don't mean the same thing. "
        "concat() doesn't align on a key at all -- it just stacks DataFrames along an axis, "
        "matching purely by column name (axis=0) or row position (axis=1)."
    ),
    reasoning=(
        "The classic silent failure: using concat(axis=1) on two DataFrames that both have a "
        "default RangeIndex but are not actually row-aligned (e.g. one was filtered and the "
        "other wasn't) will paste rows together based on position, not identity -- producing a "
        "table that looks fine but pairs the wrong rows together with no error at all."
    ),
)

TASKS[72] = dict(
    phase="testing", difficulty="advanced", title="Interview: A File Too Large to Fit in Memory",
    hints=[
        "You already used one of these strategies directly in the Learning Phase -- think about "
        "what else besides chunksize= could help, including reading fewer columns or changing "
        "engine/library entirely.",
    ],
    solution='''
"""
No code required -- this is a verbal/written reasoning question.
Sketch your answer, then compare it to the explanation below.
"""
''',
    explanation=(
        "Two pandas-native strategies: (1) chunksize= turns read_csv into an iterator of smaller "
        "DataFrames, letting you process and discard each piece (e.g. accumulating an aggregate) "
        "without ever holding the full file in memory; (2) usecols= and appropriate dtype= "
        "(including category for repeated strings) reduce the memory footprint of each row "
        "enough that the full file might fit after all."
    ),
    reasoning=(
        "Trade-offs: chunksize works for aggregations and row-by-row processing but makes "
        "operations that need the whole dataset at once (a global sort, a merge against the full "
        "table) much more awkward, often requiring a different tool entirely (a database, or a "
        "library like Dask/Polars built for out-of-core or parallel processing). usecols/dtype "
        "tuning is simpler but has a ceiling -- it only helps if the file was genuinely "
        "over-typed to begin with, and won't rescue a file that's too big no matter how it's typed."
    ),
)

TASKS[73] = dict(
    phase="testing", difficulty="advanced", title="Interview: agg() vs apply() in Production",
    hints=[
        "Think back to the performance comparison from Task 39/67, and how it extends to "
        "per-group processing.",
    ],
    solution='''
"""
No code required -- this is a verbal/written reasoning question.
Sketch your answer, then compare it to the explanation below.
"""
''',
    explanation=(
        "groupby().agg() with named, built-in aggregation functions ('sum', 'mean', or a small "
        "custom function that reduces a group to a single number) can use pandas' optimized, "
        "often Cython-backed group aggregation paths. groupby().apply(custom_func) calls a "
        "genuine Python function once per group and offers total flexibility (the function can "
        "return anything, including multiple rows), at the cost of the same per-call Python "
        "overhead discussed for row-wise apply()."
    ),
    reasoning=(
        "For a production job on a large dataset, prefer agg() whenever the logic can be "
        "expressed as a standard aggregation -- it's faster and the intent is clearer to the next "
        "person reading the code. Reach for groupby().apply() only when the per-group logic "
        "genuinely can't be expressed as a simple reduction (e.g. it needs to look at multiple "
        "columns' relationship within the group, or return more than one row per group), and "
        "treat the performance cost as a deliberate trade-off, not an accident."
    ),
)

TASKS[74] = dict(
    phase="testing", difficulty="advanced", title="Capstone Query: Category Health Snapshot",
    hints=[
        "Break it into pieces: (1) the most recent full month present in the data, (2) completed"
        "-order revenue by category for that month and the month before, (3) month-over-month "
        "change, (4) unique customers per category in that month. Build each piece, then join "
        "them together.",
    ],
    solution='''
full = (
    order_items
    .merge(products[["product_id", "category"]], on="product_id")
    .merge(orders[["order_id", "order_date", "order_status", "customer_id"]], on="order_id")
)
full = full[full["order_status"] == "Completed"].copy()
full["order_date"] = pd.to_datetime(full["order_date"], format="mixed", dayfirst=True, errors="coerce")
full["revenue"] = full["quantity"] * full["unit_price_at_purchase"]
full["month"] = full["order_date"].dt.to_period("M")

latest_month = full["month"].max()
previous_month = latest_month - 1

by_month_cat = full.groupby(["month", "category"])["revenue"].sum()

current = by_month_cat.loc[latest_month].rename("revenue_this_month")
previous = by_month_cat.loc[previous_month].rename("revenue_last_month")

report = pd.concat([current, previous], axis=1)
report["mom_change_pct"] = (
    (report["revenue_this_month"] - report["revenue_last_month"]) / report["revenue_last_month"] * 100
).round(1)

unique_customers = (
    full[full["month"] == latest_month].groupby("category")["customer_id"].nunique()
)
report["unique_customers"] = unique_customers

print(report.round(2))
''',
    explanation=(
        "The query is really four smaller, familiar operations (merge, groupby+sum, pct-change "
        "style comparison, nunique) stitched together on a shared 'month' and 'category' "
        "grouping key -- exactly the kind of multi-step business question a single pandas one"
        "-liner can't answer, but a short readable pipeline can."
    ),
    reasoning=(
        "One real limitation: 'the most recent full month' isn't actually guaranteed to be "
        "complete if the underlying data was pulled mid-month -- this report would understate "
        "the current month's revenue in that case. A production version should explicitly check "
        "whether the latest month has a full set of days before treating it as comparable to "
        "prior, complete months."
    ),
)


# ===========================================================================
# FINAL CHALLENGE
# ===========================================================================

TASKS[75] = dict(
    phase="final", difficulty="advanced", title="Customer Value & Retention Report",
    hints=[
        "Break the report into three pieces you already know how to build: (1) a per-customer "
        "RFM-style summary -- recency (days since last order), frequency (completed order count), "
        "monetary (total revenue); (2) each customer's membership_tier and city, cleaned; "
        "(3) a segment label built from simple thresholds on the RFM numbers. Merge/assign your "
        "way there step by step rather than trying to write it in one expression.",
        "For recency, you need 'today' -- use the maximum order_date_parsed in the whole dataset "
        "as your reference point instead of the real current date, since the data itself ends in "
        "the past. Use pd.cut() or np.select() for the segment labels once you have the three "
        "numeric columns.",
    ],
    solution='''
# 1) Clean the pieces we need
cust = customers.drop_duplicates(subset="customer_id").copy()
cust["city"] = cust["city"].str.strip().str.title()
cust["membership_tier"] = cust["membership_tier"].fillna("Unknown")

o = orders.drop_duplicates(subset="order_id").copy()
o["order_date"] = pd.to_datetime(o["order_date"], format="mixed", dayfirst=True, errors="coerce")
completed = o[o["order_status"] == "Completed"]

oi = order_items.copy()
oi["line_total"] = oi["quantity"] * oi["unit_price_at_purchase"]

# 2) Build revenue and frequency per customer (completed orders only)
order_rev = oi.groupby("order_id")["line_total"].sum().rename("order_revenue")
completed_rev = completed.merge(order_rev, on="order_id", how="left")

monetary = completed_rev.groupby("customer_id")["order_revenue"].sum().rename("monetary")
frequency = completed_rev.groupby("customer_id")["order_id"].count().rename("frequency")

reference_date = o["order_date"].max()
last_order = completed_rev.groupby("customer_id")["order_date"].max().rename("last_order_date")
recency = (reference_date - last_order).dt.days.rename("recency_days")

# 3) Combine into one customer-level table, keeping every customer (zero-order customers included)
rfm = cust.set_index("customer_id")[["city", "membership_tier"]].join(
    [monetary, frequency, recency]
)
rfm[["monetary", "frequency"]] = rfm[["monetary", "frequency"]].fillna(0)
# recency_days stays NaN for never-ordered customers -- that's meaningfully different from 0

# 4) Segment customers with simple, explainable thresholds
def segment(row):
    if row["frequency"] == 0:
        return "Never Ordered"
    if row["recency_days"] <= 60 and row["frequency"] >= 3:
        return "Loyal & Active"
    if row["recency_days"] > 180:
        return "At Risk"
    return "Regular"

rfm["segment"] = rfm.apply(segment, axis=1)

print(rfm["segment"].value_counts())
print(rfm.groupby("segment")[["monetary", "frequency", "recency_days"]].mean().round(1))
''',
    explanation=(
        "This is an RFM (Recency, Frequency, Monetary) summary, one of the most common customer"
        "-analytics constructs in industry -- the pandas mechanics are all things you've already "
        "practiced (groupby aggregation, merge, datetime arithmetic, row-wise labeling); the "
        "capstone is assembling them into one coherent, business-readable table."
    ),
    reasoning=(
        "Two judgment calls worth noticing: (1) reference_date is taken from the data itself "
        "rather than the real 'today', since this is a static historical dataset -- using the "
        "real current date would make every customer look far more 'at risk' than they are; "
        "(2) recency_days is deliberately left as NaN rather than filled for customers who never "
        "ordered, because 'no orders yet' and 'ordered exactly 0 days ago' are different facts, "
        "and the segment() function handles that case explicitly rather than letting a filled "
        "value produce a misleading label."
    ),
)


# ---------------------------------------------------------------------------
# Captured expected output for each task's solution -- generated by actually
# running every solution against the real dataset, in task order, once.
# answer(n) prints this alongside the code so you can check your own output
# against it without having to run the solution yourself.
# ---------------------------------------------------------------------------

OUTPUTS = {
    1: 'customers (3015, 7)\nproducts (152, 7)\norders (15030, 7)\norder_items (22964, 6)\n',
    2: '0    199.0\n1    449.0\n2    899.0\nName: sample_price, dtype: float64\n  product_name  unit_price\n0   Headphones       199.0\n1   Smartwatch       449.0\n2       Tablet       899.0\n',
    3: "   customer_id first_name  last_name  ...       city signup_date membership_tier\n0         1099     Vivaan  Fernandes  ...     Mumbai  2024-01-04          Bronze\n1         1793     Ananya     Kapoor  ...    Lucknow  2024-07-24            Gold\n2         1703       Liam      Mehta  ...      DELHI  2021-06-08          Bronze\n3         2098     Sophia       Khan  ...    Lucknow  2024-12-22        Platinum\n4         1382    Krishna      Gupta  ...   Lucknow   2023-06-15            Gold\n\n[5 rows x 7 columns]\n      customer_id first_name  ... signup_date membership_tier\n3010         2764     Vivaan  ...  2023-11-03          Silver\n3011          906       Noah  ...  2021-09-15          Bronze\n3012         1097     Sophia  ...  2021-02-23          Silver\n3013          236       Noah  ...  2022-04-03          Bronze\n3014         1062       Liam  ...  2022-12-20          Silver\n\n[5 rows x 7 columns]\n<class 'pandas.DataFrame'>\nRangeIndex: 3015 entries, 0 to 3014\nData columns (total 7 columns):\n #   Column           Non-Null Count  Dtype\n---  ------           --------------  -----\n 0   customer_id      3015 non-null   int64\n 1   first_name       3015 non-null   str  \n 2   last_name        3015 non-null   str  \n 3   email            2915 non-null   str  \n 4   city             2907 non-null   str  \n 5   signup_date      3015 non-null   str  \n 6   membership_tier  2951 non-null   str  \ndtypes: int64(1), str(6)\nmemory usage: 165.0 KB\n(3015, 7)\ncustomer_id        int64\nfirst_name           str\nlast_name            str\nemail                str\ncity                 str\nsignup_date          str\nmembership_tier      str\ndtype: object\nIndex(['customer_id', 'first_name', 'last_name', 'email', 'city',\n       'signup_date', 'membership_tier'],\n      dtype='str')\n",
    4: "Index(['customer_id', 'given_name', 'surname', 'email', 'city', 'signup_date',\n       'membership_tier'],\n      dtype='str')\n          customer_id  order_date  ... discount_pct shipping_city\norder_id                           ...                           \n14577           180.0  2024-12-07  ...         35.0       Kolkata\n5249            981.0  2024-03-31  ...         10.0       KOLKATA\n10797          1683.0  2023-03-13  ...          NaN    Bengaluru \n9241            702.0  2023-01-04  ...          NaN         Pune \n6161           1909.0  2023-09-10  ...          NaN          Pune\n\n[5 rows x 6 columns]\n   order_id  customer_id  order_date  ... order_status discount_pct  shipping_city\n0     14577        180.0  2024-12-07  ...    Completed         35.0        Kolkata\n1      5249        981.0  2024-03-31  ...    Cancelled         10.0        KOLKATA\n2     10797       1683.0  2023-03-13  ...    Cancelled          NaN     Bengaluru \n3      9241        702.0  2023-01-04  ...    Completed          NaN          Pune \n4      6161       1909.0  2023-09-10  ...    Completed          NaN           Pune\n\n[5 rows x 7 columns]\n",
    5: '0    Completed\n1    Cancelled\n2    Cancelled\n3    Completed\n4    Completed\nName: order_status, dtype: str\n   order_id order_status  discount_pct\n0     14577    Completed          35.0\n1      5249    Cancelled          10.0\n2     10797    Cancelled           NaN\n3      9241    Completed           NaN\n4      6161    Completed           NaN\nCompleted\n   order_id order_status\n0     14577    Completed\n1      5249    Cancelled\n2     10797    Cancelled\n3      9241    Completed\n4      6161    Completed\norder_id               14577\ncustomer_id            180.0\norder_date        2024-12-07\npayment_method    Debit Card\norder_status       Completed\ndiscount_pct            35.0\nshipping_city        Kolkata\nName: 0, dtype: object\n   order_id  customer_id  order_date\n0     14577        180.0  2024-12-07\n1      5249        981.0  2024-03-31\n2     10797       1683.0  2023-03-13\n3      9241        702.0  2023-01-04\n4      6161       1909.0  2023-09-10\n',
    6: 'customer_id          0\nfirst_name           0\nlast_name            0\nemail              100\ncity               108\nsignup_date          0\nmembership_tier     64\ndtype: int64\n(2907, 7) (3015, 7)\n',
    7: 'category\nInt64\n0      35\n1      10\n2    <NA>\n3    <NA>\n4    <NA>\n5       5\n6       0\n7      40\n8      20\n9       0\nName: discount_pct, dtype: Int64\n',
    8: '   order_status status_label\n0     Completed      Success\n1     Cancelled       Failed\n6      Returned     Refunded\n26      Pending  In Progress\n',
    9: "Index(['order_id', 'customer_id', 'order_date', 'payment_method',\n       'order_status', 'discount_pct', 'status_label'],\n      dtype='str')\n15027 15030\n",
    10: 'Exact duplicate rows in customers: 15\n(3000, 7) (3015, 7)\nDuplicate orders: 30\n(15000, 8) (15030, 8)\n',
    11: "(10548, 8)\n<StringArray>\n['Completed']\nLength: 1, dtype: str\n",
    12: "(4414, 8)\n<StringArray>\n['Completed', 'Cancelled', 'Returned']\nLength: 3, dtype: str\n(8899, 8)\n",
    13: '(4414, 8)\n(3790, 8)\n',
    14: 'city\nbengaluru    321\nahmedabad    300\npune         298\nlucknow      293\nkolkata      290\nmumbai       289\ndelhi        288\nhyderabad    285\nchennai      275\njaipur       268\nName: count, dtype: int64\nMalformed emails: 49\nemail\nyahoo.com      749\noutlook.com    736\nhotmail.com    703\ngmail.com      678\nName: count, dtype: int64\n',
    15: '             product_name  unit_price\n22      Charger - Model 2   425946.00\n145  Board Game - Model 3    25417.00\n107    Cookbook - Model 1     8870.00\n13   Smartwatch - Model 2     7227.75\n25       Camera - Model 1     4885.77\n   category        product_name  unit_price\n77   Beauty   Perfume - Model 1       75.83\n76   Beauty  Lipstick - Model 5       86.99\n72   Beauty  Lipstick - Model 1      139.19\n74   Beauty  Lipstick - Model 3      155.22\n81   Beauty   Shampoo - Model 3      168.57\n   order_id  customer_id  order_date  ... discount_pct shipping_city  status_label\n0     14577        180.0  2024-12-07  ...         35.0       Kolkata       Success\n1      5249        981.0  2024-03-31  ...         10.0       KOLKATA        Failed\n2     10797       1683.0  2023-03-13  ...          NaN    Bengaluru         Failed\n3      9241        702.0  2023-01-04  ...          NaN         Pune        Success\n4      6161       1909.0  2023-09-10  ...          NaN          Pune       Success\n\n[5 rows x 8 columns]\n',
    16: '4113.177302631579\n629.7750000000001\n34525.33237792365\n       product_id     unit_price\ncount  152.000000     152.000000\nmean    76.500000    4113.177303\nstd     44.022721   34525.332378\nmin      1.000000      61.700000\n25%     38.750000     311.570000\n50%     76.500000     629.775000\n75%    114.250000    1479.912500\nmax    152.000000  425946.000000\n',
    17: 'order_status\nCompleted    10548\nPending       1795\nCancelled     1499\nReturned      1188\nName: count, dtype: int64\norder_status\nCompleted    0.702\nPending      0.119\nCancelled    0.100\nReturned     0.079\nName: proportion, dtype: float64\npayment_method\nUPI                 4752\nCredit Card         4147\nDebit Card          2732\nNet Banking         1878\nCash on Delivery    1362\nNaN                  159\nName: count, dtype: int64\n',
    18: '                discount_pct  quantity_total\ndiscount_pct        1.000000       -0.007068\nquantity_total     -0.007068        1.000000\n-1.5349869536543408\n',
    19: 'category\nBeauty              354.978889\nBooks               882.566000\nElectronics       18761.327407\nFashion             898.419048\nGrocery             301.970556\nHome & Kitchen     1200.481111\nSports             1140.371176\nToys               1873.431111\nName: unit_price, dtype: float64\norder_status\nCancelled     1499\nCompleted    10548\nPending       1795\nReturned      1188\nName: order_id, dtype: int64\n',
    20: '                   avg_price  min_price  max_price  n_products\ncategory                                                      \nBeauty            354.978889      75.83     838.50          18\nBooks             882.566000     115.43    8870.00          15\nElectronics     18761.327407     462.28  425946.00          27\nFashion           898.419048     118.84    2206.26          21\nGrocery           301.970556      61.70     624.47          18\nHome & Kitchen   1200.481111     201.74    2908.47          18\nSports           1140.371176     335.47    2740.31          17\nToys             1873.431111      69.27   25417.00          18\n',
    21: '   order_id  item_total  pct_of_order\n0     14577      502.82        100.00\n1      5249      215.98        100.00\n2     10797      716.02        100.00\n3      9241      441.25        100.00\n4      6161      659.38         13.32\n5      6161     3959.40         80.00\n6      6161      330.77          6.68\n7      5816     1115.35         27.41\n22964\n',
    22: 'is_active          False    True \ncategory                         \nBeauty            504.90   346.16\nBooks             204.10  1052.18\nElectronics     87703.42  3092.67\nFashion              NaN   898.42\nGrocery           280.21   303.25\nHome & Kitchen   1375.12  1150.58\nSports           1348.92  1127.34\nToys             6607.08   520.96\n',
    23: 'payment_method  Cash on Delivery  Credit Card  Debit Card  Net Banking   UPI\norder_status                                                                \nCancelled                    126          433         268          188   471\nCompleted                    974         2853        1910         1317  3376\nPending                      163          528         307          228   554\nReturned                      99          333         247          145   351\npayment_method  Cash on Delivery  Credit Card  Debit Card  Net Banking    UPI\norder_status                                                                 \nCancelled                  0.085        0.291       0.180        0.127  0.317\nCompleted                  0.093        0.274       0.183        0.126  0.324\nPending                    0.092        0.297       0.172        0.128  0.311\nReturned                   0.084        0.283       0.210        0.123  0.299\n',
    24: '(42, 7) 42\n',
    25: 'inner: 14728\nleft : 15109\nouter: 15135\n',
    26: 'Orders with no matching customer: 381\nvalidate caught a problem: Merge keys are not unique in right dataset; not a many-to-one merge\n\nDuplicates in right:\n  customer_id\n         347\n        2870\n         437\n        1327\n         102 ...\n',
    27: '                    product_name  total_units_sold\nproduct_id                                        \n1           Headphones - Model 1               267\n2           Headphones - Model 2               221\n3           Headphones - Model 3               615\n4           Smartphone - Model 1               248\n5           Smartphone - Model 2               190\n',
    28: '0 unparseable dates\n       order_date order_date_parsed\n7883   2023-11-02        2023-02-11\n8096   2023-04-25        2023-04-25\n13069  2024-10-10        2024-10-10\n8347   2024-05-29        2024-05-29\n1955   2023-02-27        2023-02-27\n',
    29: '  order_date_parsed  order_year  order_month order_day_name  is_weekend\n0        2024-07-12        2024            7         Friday       False\n1        2024-03-31        2024            3         Sunday        True\n2        2023-03-13        2023            3         Monday       False\n3        2023-04-01        2023            4       Saturday        True\n4        2023-10-09        2023           10         Monday       False\n',
    30: 'order_date_parsed\n2023-01-31    379\n2023-02-28    300\n2023-03-31    367\n2023-04-30    384\n2023-05-31    379\n2023-06-30    343\n2023-07-31    409\n2023-08-31    394\n2023-09-30    360\n2023-10-31    618\n2023-11-30    629\n2023-12-31    671\n2024-01-31    430\n2024-02-29    374\n2024-03-31    398\n2024-04-30    370\n2024-05-31    353\n2024-06-30    381\n2024-07-31    397\n2024-08-31    398\n2024-09-30    388\n2024-10-31    615\n2024-11-30    597\n2024-12-31    614\nFreq: ME, Name: order_id, dtype: int64\norder_date_parsed\n2023-01-01    23.333333\n2023-01-08    21.627907\n2023-01-15    21.105263\n2023-01-22    20.327869\n2023-01-29    18.306452\nFreq: W-SUN, Name: discount_pct, dtype: float64\n',
    31: 'order_date_parsed\n2024-12-27    227424.035714\n2024-12-28    119388.408571\n2024-12-29    122899.157143\n2024-12-30    119389.614286\n2024-12-31    124848.958571\nName: item_total, dtype: float64\norder_date_parsed\n2024-12-27    1.021863e+08\n2024-12-28    1.022856e+08\n2024-12-29    1.023724e+08\n2024-12-30    1.024184e+08\n2024-12-31    1.024898e+08\nName: item_total, dtype: float64\n',
    32: '                   order_count  previous_month  change  pct_change\norder_date_parsed                                                 \n2023-01-31                 379             NaN     NaN         NaN\n2023-02-28                 300           379.0   -79.0      -0.208\n2023-03-31                 367           300.0    67.0       0.223\n2023-04-30                 384           367.0    17.0       0.046\n2023-05-31                 379           384.0    -5.0      -0.013\n2023-06-30                 343           379.0   -36.0      -0.095\n2023-07-31                 409           343.0    66.0       0.192\n2023-08-31                 394           409.0   -15.0      -0.037\n2023-09-30                 360           394.0   -34.0      -0.086\n2023-10-31                 618           360.0   258.0       0.717\n2023-11-30                 629           618.0    11.0       0.018\n2023-12-31                 671           629.0    42.0       0.067\n2024-01-31                 430           671.0  -241.0      -0.359\n2024-02-29                 374           430.0   -56.0      -0.130\n2024-03-31                 398           374.0    24.0       0.064\n2024-04-30                 370           398.0   -28.0      -0.070\n2024-05-31                 353           370.0   -17.0      -0.046\n2024-06-30                 381           353.0    28.0       0.079\n2024-07-31                 397           381.0    16.0       0.042\n2024-08-31                 398           397.0     1.0       0.003\n2024-09-30                 388           398.0   -10.0      -0.025\n2024-10-31                 615           388.0   227.0       0.585\n2024-11-30                 597           615.0   -18.0      -0.029\n2024-12-31                 614           597.0    17.0       0.028\n',
    33: 'order_flag\nStandard            10890\nBig Discount Win     2641\nLost Sale            1499\nName: count, dtype: int64\nunit_price    425884.3\ndtype: float64\n',
    34: '    membership_tier  tier_rank\n0            Bronze        1.0\n1              Gold        3.0\n3          Platinum        4.0\n7            Silver        2.0\n109             NaN        NaN\n',
    35: 'price_tier\nMid-range    63\nBudget       62\nPremium      23\nLuxury        4\nName: count, dtype: int64\n',
    36: '       order_id  product_id     revenue\n10015     14883          14  2970935.44\n7138       6867           8  2407357.92\n14746      8729          23  2065049.25\n9867        538          23  1996279.15\n12375      2321          23  1814974.90\n21311      9397          23  1685995.40\n20293     10429          23  1641671.56\n20542      1857          23  1604186.68\n22840     13089          23  1601454.76\n22871     12795          23  1575137.08\n',
    37: 'Before: 1290.8 KB, After: 976.7 KB\nReduction: 24.3%\n',
    38: '(1000000, 4)\nweekly_self_study_hours     float64\nattendance_percentage       float64\ntotal_score                 float64\ngrade                      category\ndtype: object\n1000000\ngrade\nA    548644\nB    258174\nC    141980\nD     44998\nF      6204\nName: count, dtype: int64\n',
    39: 'apply():     0.254s\nvectorized:  0.018s\nspeedup:     14.3x\n',
    40: 'category        is_active\nBeauty          False          504.900000\n                True           346.160000\nBooks           False          204.100000\n                True          1052.182500\nElectronics     False        87703.418000\n                True          3092.670455\nFashion         True           898.419048\nGrocery         False          280.210000\n                True           303.250588\nHome & Kitchen  False         1375.122500\n                True          1150.583571\nSports          False         1348.920000\n                True          1127.336875\nToys            False         6607.085000\n                True           520.958571\nName: unit_price, dtype: float64\n3092.6704545454545\nis_active          False    True \ncategory                         \nBeauty            504.90   346.16\nBooks             204.10  1052.18\nElectronics     87703.42  3092.67\nFashion              NaN   898.42\nGrocery           280.21   303.25\nHome & Kitchen   1375.12  1150.58\nSports           1348.92  1127.34\nToys             6607.08   520.96\n',
    41: '         category     metric         value\n0          Beauty  avg_price    354.978889\n1           Books  avg_price    882.566000\n2     Electronics  avg_price  18761.327407\n3         Fashion  avg_price    898.419048\n4         Grocery  avg_price    301.970556\n5  Home & Kitchen  avg_price   1200.481111\n6          Sports  avg_price   1140.371176\n7            Toys  avg_price   1873.431111\n8          Beauty  max_price    838.500000\n9           Books  max_price   8870.000000\n',
    42: '             product_name  unit_price\n22      Charger - Model 2   425946.00\n145  Board Game - Model 3    25417.00\n107    Cookbook - Model 1     8870.00\n13   Smartwatch - Model 2     7227.75\n25       Camera - Model 1     4885.77\n             product_name  unit_price\n116    Rice 5kg - Model 1       61.70\n147  Board Game - Model 5       69.27\n77      Perfume - Model 1       75.83\n121   Atta 10kg - Model 1       85.78\n76     Lipstick - Model 5       86.99\n   category           product_name  unit_price  price_rank_in_category\n73   Beauty     Lipstick - Model 2      838.50                     1.0\n70   Beauty  Moisturizer - Model 2      674.58                     2.0\n78   Beauty      Perfume - Model 2      567.54                     3.0\n69   Beauty  Moisturizer - Model 1      552.93                     4.0\n71   Beauty  Moisturizer - Model 3      504.90                     5.0\n83   Beauty      Shampoo - Model 5      448.32                     6.0\n75   Beauty     Lipstick - Model 4      414.50                     7.0\n80   Beauty      Shampoo - Model 2      402.47                     8.0\n',
    43: 'discounted_flag\nTrue     7060\nFalse    3488\nName: count, dtype: int64\n',
    44: 'category       Beauty     Books  ...    Sports      Toys\norder_month                      ...                    \n2023-01       25045.0  348847.0  ...   85891.0  200667.0\n2023-02       20864.0   27161.0  ...  107290.0  269337.0\n2023-03       36611.0   51136.0  ...  111279.0   68140.0\n2023-04       37442.0   41262.0  ...   99890.0  162673.0\n2023-05       39159.0   63296.0  ...   92376.0  163471.0\n2023-06       35483.0   57965.0  ...  137552.0  179539.0\n2023-07       37820.0  225632.0  ...  701465.0  228232.0\n2023-08       50543.0   71729.0  ...  103875.0  201875.0\n2023-09       44790.0   52668.0  ...  107210.0  248185.0\n2023-10       68413.0  175505.0  ...  135390.0  602338.0\n2023-11       55278.0  205145.0  ...  193717.0  329674.0\n2023-12       72866.0  105944.0  ...  202896.0  446883.0\n2024-01       39950.0   89126.0  ...  105960.0  142621.0\n2024-02       33066.0   82693.0  ...   84917.0  173137.0\n2024-03       35570.0  106385.0  ...  112230.0  236384.0\n2024-04       25737.0   27729.0  ...  115405.0  374739.0\n2024-05      272510.0  133677.0  ...   91006.0  366206.0\n2024-06       31962.0   35461.0  ...   86880.0  153278.0\n2024-07       34820.0   88309.0  ...  158847.0  257027.0\n2024-08       40278.0   96025.0  ...  130323.0  521445.0\n2024-09       49269.0   42987.0  ...   95543.0   75726.0\n2024-10       70108.0  151587.0  ...  136581.0  162560.0\n2024-11       47349.0   99973.0  ...  160510.0  341092.0\n2024-12       64920.0  206891.0  ...  135067.0  293765.0\n\n[24 rows x 8 columns]\n',
    45: '1499\n1499\n',
    46: '             product_name     category  unit_price\n22      Charger - Model 2  Electronics   425946.00\n145  Board Game - Model 3         Toys    25417.00\n107    Cookbook - Model 1        Books     8870.00\n13   Smartwatch - Model 2  Electronics     7227.75\n25       Camera - Model 1  Electronics     4885.77\n',
    47: 'customer_id          0\nfirst_name           0\nlast_name            0\nemail              100\ncity               108\nsignup_date          0\nmembership_tier     64\ntier_rank           64\nemail_lower        100\ndtype: int64\n',
    48: '763\n763\n',
    49: 'city\nBengaluru    321\nAhmedabad    300\nPune         298\nLucknow      293\nKolkata      290\nMumbai       289\nDelhi        288\nHyderabad    285\nChennai      275\nJaipur       268\nName: count, dtype: int64\n',
    50: 'Before: 867094 bytes, After: 15391 bytes\nSaved: 98.2%\n',
    51: '      customer_id first_name  ... tier_rank                    email_lower\n945           756     Aadhya  ...       2.0     aadhya.khan990@hotmail.com\n2257          756     Aadhya  ...       2.0     aadhya.khan990@hotmail.com\n1806          354     Aadhya  ...       2.0  aadhya.kulkarni95@hotmail.com\n1124          354     Aadhya  ...       2.0  aadhya.kulkarni95@hotmail.com\n1345          437      Anika  ...       1.0        anika.nair283@gmail.com\n1482          437      Anika  ...       1.0        anika.nair283@gmail.com\n832          2935        Ava  ...       2.0        ava.pillai492@yahoo.com\n1845         2935        Ava  ...       2.0        ava.pillai492@yahoo.com\n877          1012       Emma  ...       2.0        emma.shettyat gmail.com\n610          1469       Emma  ...       4.0        emma.shettyat gmail.com\n\n[10 rows x 9 columns]\nTotal involved rows: 63\n',
    52: 'customer_id\n1095.0    14\n2581.0    13\n1127.0    13\n1085.0    12\n2784.0    12\nName: order_id, dtype: int64\n',
    53: '   order_id  line_total  pct_of_order\n0     14577      502.82         100.0\n1      5249      215.98         100.0\n2     10797      716.02         100.0\n3      9241      441.25         100.0\n4      6161      659.38          13.3\n5      6161     3959.40          80.0\n6      6161      330.77           6.7\n7      5816     1115.35          27.4\nTrue\n',
    54: "Orphan orders: 381\nThat's 2.53% of all orders.\n",
    55: 'quarter            2023Q1     2023Q2  ...     2024Q3      2024Q4\ncategory                              ...                       \nBeauty            82520.0   112084.0  ...   124367.0    182378.0\nBooks            427144.0   162524.0  ...   227321.0    458451.0\nElectronics     9991924.0  6006107.0  ...  8130903.0  15566832.0\nFashion          335176.0   830133.0  ...   313301.0   1178889.0\nGrocery           81756.0    78653.0  ...    79294.0    135162.0\nHome & Kitchen   348954.0   293700.0  ...   651122.0    544407.0\nSports           304460.0   329817.0  ...   384713.0    432157.0\nToys             538144.0   505683.0  ...   854198.0    797417.0\n\n[8 rows x 8 columns]\n',
    56: '    order_id  discount_pct       net_note\n0      14577          35.0  high discount\n7       5721          40.0  high discount\n10       617          35.0  high discount\n14      9585          35.0  high discount\n18      8401          25.0  high discount\n',
    57: '  order_date signup_date  is_weekend  days_since_signup\n0 2024-07-12  2024-02-12       False              151.0\n1 2024-03-31  2022-08-29        True              580.0\n2 2023-03-13  2023-02-17       False               24.0\n3 2023-04-01  2023-01-19        True               72.0\n4 2023-10-09  2024-09-18       False             -345.0\n',
    58: 'count    3015.000000\nmean        4.884909\nstd         2.198439\nmin         0.000000\n25%         3.000000\n50%         5.000000\n75%         6.000000\nmax        14.000000\nName: order_count, dtype: float64\nCustomers with zero orders: 26\n',
    59: 'Best 7-day window ends on: 2024-11-19 00:00:00\nRevenue in that window: 4700619.2\n',
    60: '    customer_id  order_id order_date_parsed\n5        1991.0      5816        2024-04-21\n8         797.0     14317        2024-04-11\n10       2813.0       617        2024-09-23\n13       2139.0      1471        2024-09-21\n14       2764.0      9585        2024-09-06\n',
    61: 'fillna(0) then mean: 15.06\nmean() with NaN skipped: 20.02\n',
    62: 'payment_method\nCredit Card         0.1044\nNet Banking         0.1001\nUPI                 0.0991\nDebit Card          0.0981\nCash on Delivery    0.0925\nName: Cancelled, dtype: float64\n',
    63: 'Duplicate order_id values in orders: 30\nRow count after fix: 22964 vs original order_items: 22964\n',
    64: '45 line items deviate more than 20% from current price\n       order_id  product_id  ...  current_price  pct_deviation\n17727      5938          63  ...        1032.21       1.164046\n3124       4007          37  ...         901.00       1.143085\n17901      3157         113  ...         337.47       1.136575\n8056       3324          53  ...        2206.26       1.120099\n1564        968          92  ...         416.33       1.093532\n\n[5 rows x 5 columns]\n',
    65: 'Sharpest decline in: 2023-03-31 00:00:00\nChange: -58.1%\n',
    66: 'cohort\n2021-01    0.000000\n2021-02    0.000000\n2021-03    0.000000\n2021-04    0.000000\n2021-05    0.000000\n2021-06    0.000000\n2021-07    0.000000\n2021-08    0.000000\n2021-09    0.000000\n2021-10    0.000000\n2021-11    0.000000\n2021-12    0.000000\n2022-01    0.000000\n2022-02    0.000000\n2022-03    0.000000\n2022-04    0.000000\n2022-05    0.000000\n2022-06    0.000000\n2022-07    0.000000\n2022-08    0.000000\n2022-09    0.000000\n2022-10    0.095238\n2022-11    0.314286\n2022-12    0.460317\n2023-01    0.563380\n2023-02    0.540000\n2023-03    0.500000\n2023-04    0.500000\n2023-05    0.469697\n2023-06    0.515625\n2023-07    0.656250\n2023-08    0.760563\n2023-09    0.561404\n2023-10    0.779661\n2023-11    0.935484\n2023-12    0.826087\n2024-01    0.640625\n2024-02    0.500000\n2024-03    0.428571\n2024-04    0.596774\n2024-05    0.462963\n2024-06    0.610169\n2024-07    0.569231\n2024-08    0.660000\n2024-09    0.960000\n2024-10    0.906250\n2024-11    0.578125\n2024-12    0.151515\nFreq: M, dtype: float64\n',
    67: 'apply(): 0.251s  |  vectorized: 0.001s  |  speedup: 284.6x\n',
    68: 'Rows with missing membership_tier: 64\ncustomer_id    2951\ndtype: int64 vs total customers: 3015\ncustomer_id    3015\ndtype: int64\n',
    69: '       order_id  order_value  customer_id  rank_in_customer\n9742       9732      8572.16          1.0               1.0\n1640       1639      5237.50          1.0               2.0\n10129     10118      4753.27          2.0               1.0\n13372     13349      3043.89          2.0               2.0\n888         889      2560.00          3.0               1.0\n8483       8474      1523.99          3.0               2.0\n7757       7748     94842.64          4.0               1.0\n4166       4163     13441.71          4.0               2.0\n4351       4348     22638.51          5.0               1.0\n11376     11360      2014.84          5.0               2.0\n',
    70: 'Before: 90.0 MB, After: 21.0 MB\nReduction: 76.7%\n',
    71: '',
    72: '',
    73: '',
    74: '                revenue_this_month  ...  unique_customers\ncategory                            ...                  \nBeauty                    64919.96  ...               108\nBooks                    206891.17  ...               101\nElectronics             4629026.50  ...               153\nFashion                  196767.70  ...               124\nGrocery                   44717.67  ...                89\nHome & Kitchen           180392.34  ...                97\nSports                   135066.51  ...                89\nToys                     293765.36  ...                96\n\n[8 rows x 4 columns]\n',
    75: 'segment\nRegular           1065\nAt Risk           1042\nLoyal & Active     796\nNever Ordered       97\nName: count, dtype: int64\n                monetary  frequency  recency_days\nsegment                                          \nAt Risk          22982.5        2.7         355.3\nLoyal & Active   46467.0        4.7          25.4\nNever Ordered        0.0        0.0           NaN\nRegular          36044.0        3.5          95.8\n',
}

for _n, _out in OUTPUTS.items():
    if _n in TASKS:
        TASKS[_n]["output"] = _out

_validate()
