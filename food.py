import pandas as pd
from IPython.display import display

# food.csv row values represent 100g worth of the row's food
food = pd.read_csv("food.csv")
food_renamed_columns = {
    "Category": "category",
    "Description": "description",
    "Nutrient Data Bank Number": "nut_db_num",
    "Data.Alpha Carotene": "alpha_carotene",
    "Data.Ash": "ash",
    "Data.Beta Carotene": "beta_carotene",
    "Data.Beta Cryptoxanthin": "beta_cryptoxanthin",
    "Data.Carbohydrate": "carbohydrate",
    "Data.Cholesterol": "cholesterol",
    "Data.Choline": "choline",
    "Data.Fiber": "fiber",
    "Data.Kilocalories": "calories",
    "Data.Lutein and Zeaxanthin": "lutein_and_zeaxanthin",
    "Data.Lycopene": "lycopene",
    "Data.Manganese": "manganese",
    "Data.Niacin": "niacin",
    "Data.Pantothenic Acid": "pantothenic_acid",
    "Data.Protein": "protein",
    "Data.Refuse Percentage": "pct_refuse",
    "Data.Retinol": "retinol",
    "Data.Riboflavin": "riboflavin",
    "Data.Selenium": "selenium",
    "Data.Sugar Total": "sugar",
    "Data.Thiamin": "thiamin",
    "Data.Water": "water",
    "Data.Fat.Monosaturated Fat": "fat_monounsaturated",
    "Data.Fat.Polysaturated Fat": "fat_polyunsaturated",
    "Data.Fat.Saturated Fat": "fat_saturated",
    "Data.Fat.Total Lipid": "fat_total",
    "Data.Household Weights.1st Household Weight": "first_weight",
    "Data.Household Weights.1st Household Weight Description": "first_weight_desc",
    "Data.Household Weights.2nd Household Weight": "second_weight",
    "Data.Household Weights.2nd Household Weight Description": "second_weight_desc",
    "Data.Major Minerals.Calcium": "calcium",
    "Data.Major Minerals.Copper": "copper",
    "Data.Major Minerals.Iron": "iron",
    "Data.Major Minerals.Magnesium": "magnesium",
    "Data.Major Minerals.Phosphorus": "phosphorus",
    "Data.Major Minerals.Potassium": "potassium",
    "Data.Major Minerals.Sodium": "sodium",
    "Data.Major Minerals.Zinc": "zinc",
    "Data.Vitamins.Vitamin A - IU": "v_a_iu",
    "Data.Vitamins.Vitamin A - RAE": "v_a_rae",
    "Data.Vitamins.Vitamin B12": "v_b12",
    "Data.Vitamins.Vitamin B6": "v_b6",
    "Data.Vitamins.Vitamin C": "v_c",
    "Data.Vitamins.Vitamin E": "v_e",
    "Data.Vitamins.Vitamin K": "v_k",
}
food = food.rename(columns=food_renamed_columns)
food["calories_per_gram"] = food["calories"] / 100

rdi = pd.read_csv("rdi.csv")
micronutrients = rdi[rdi.nutrient.isin(food)].nutrient

POUND_IN_GRAMS = 453.592

CATEGORY_EXCLUDES = [
    "ALLSPICE",
    "BABYFOOD",
    "BEVERAGE",
    "CELERY FLAKES",
    "CEREALS RTE",
    "CEREALS",
    "CHERVIL",
    "CHILD FORMULA",
    "CHIVES",
    "CINNAMON",
    "CLOVES",
    "COCOA MIX",
    "CORIANDER LEAF",
    "DESSERTS",
    "DILL WEED",
    "Form Bar",
    "FORM BAR",
    "FORM",
    "INF FORM",
    "LEAVENING AGENTS",
    "LEMONADE",
    "MARGARINE-LIKE SPRD",
    "MARJORAM",
    "MUSTARD SEED",
    "No Category",
    "OIL",
    "PARSLEY",
    "PEPPER",
    "PUDDINGS",
    "ROSEMARY",
    "SAGE",
    "SAVORY",
    "SESAME BUTTER",
    "SEASAME FLOUR",
    "SEASAME MEAL",
    "SESAME SEEDS",
    "SISYMBRIUM SP. SEEDS",
    "SNACKS",
    "SPEARMINT",
    "SPICES",
    "TURMERIC",
    "VANILLA EXTRACT",
    "VITASOY USA",
    "WHEY",
]

# ~ is bitwise negate, functionally this is "give me all data frames that are not in the category excludes list"
food = food[~food.category.isin(CATEGORY_EXCLUDES)]
# Exclude any category with DRK in it -> some kind of BS "drink"
food = food[~food.category.str.contains("DRK")]
# Maybe powdered milk is nutritionally amazing, I don't care
food = food[~food.description.str.contains("MILK,DRY")]

# Create some derived columns:
for nutrient in micronutrients:
    food["{}_pct_rdi".format(nutrient)] = (
        food[nutrient] / rdi[rdi.nutrient == nutrient].rdi.values[0]
    ) * 100
    food["{}_grams_100_pct_rdi".format(nutrient)] = (
        100.0 / food["{}_pct_rdi".format(nutrient)]
    ) * 100
    food["{}_calories_100_pct_rdi".format(nutrient)] = (
        food["{}_grams_100_pct_rdi".format(nutrient)] * food["calories_per_gram"]
    )

food["total_pct_rdi"] = (
    food["calcium_pct_rdi"]
    + food["choline_pct_rdi"]
    + food["copper_pct_rdi"]
    + food["iron_pct_rdi"]
    + food["magnesium_pct_rdi"]
    + food["manganese_pct_rdi"]
    + food["niacin_pct_rdi"]
    + food["pantothenic_acid_pct_rdi"]
    + food["phosphorus_pct_rdi"]
    + food["potassium_pct_rdi"]
    + food["riboflavin_pct_rdi"]
    + food["selenium_pct_rdi"]
    + food["thiamin_pct_rdi"]
    + food["v_a_rae_pct_rdi"]
    + food["v_b12_pct_rdi"]
    + food["v_b6_pct_rdi"]
    + food["v_c_pct_rdi"]
    + food["v_e_pct_rdi"]
    + food["v_k_pct_rdi"]
    + food["zinc_pct_rdi"]
)
food["pct_rdi_per_calorie"] = food["total_pct_rdi"] / food["calories"]

table = {}
for nutrient in micronutrients:
    table[nutrient] = food[
        (food["pct_rdi_per_calorie"] > 1.5)
        & (food["{}_grams_100_pct_rdi".format(nutrient)] < POUND_IN_GRAMS / 2)
        & (food["{}_calories_100_pct_rdi".format(nutrient)] < 500)
    ][
        [
            "{}_calories_100_pct_rdi".format(nutrient),
            "{}_grams_100_pct_rdi".format(nutrient),
            "pct_rdi_per_calorie",
            "{}_pct_rdi".format(nutrient),
            "description",
            "category",
        ]
    ].sort_values(
        by=["{}_calories_100_pct_rdi".format(nutrient)], ascending=True
    )


def main(max_rows=100):
    pd.options.display.max_rows = max_rows
    for t in table:
        display(table[t][:max_rows])
