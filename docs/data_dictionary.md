# Data Dictionary

## Source Dataset
Sample Superstore Dataset from Kaggle

## Original Columns
| Column | Type | Description |
|---|---|---|
| Row ID | Integer | Unique row identifier |
| Order ID | String | Unique order identifier |
| Order Date | Date | Date order was placed |
| Ship Date | Date | Date order was shipped |
| Ship Mode | String | Shipping method selected |
| Customer ID | String | Unique customer identifier |
| Customer Name | String | Full name of customer |
| Segment | String | Customer segment: Consumer, Corporate, Home Office |
| Country | String | Country of order |
| City | String | City of order |
| State | String | State of order |
| Postal Code | Integer | Postal code of delivery |
| Region | String | Region: Central, East, South, West |
| Product ID | String | Unique product identifier |
| Category | String | Product category: Furniture, Office Supplies, Technology |
| Sub-Category | String | Product sub-category |
| Product Name | String | Full product name |
| Sales | Float | Revenue from transaction in dollars |
| Quantity | Integer | Number of units ordered |
| Discount | Float | Discount rate applied between 0 and 1 |
| Profit | Float | Profit from transaction in dollars |

## Engineered Columns Added During Cleaning
| Column | Type | Formula | Description |
|---|---|---|---|
| Order Year | Integer | Extracted from Order Date | Year of order |
| Order Month | Integer | Extracted from Order Date | Month number of order |
| Order Month Name | String | Extracted from Order Date | Month name of order |
| Order Quarter | Integer | Extracted from Order Date | Quarter of order |
| Gross Margin % | Float | Profit divided by Sales multiplied by 100 | Margin percentage per transaction |
| Cost | Float | Sales minus Profit | Estimated cost of goods sold |
| Discount Amount | Float | Original Price multiplied by Discount Rate | Dollar value of discount given |
| Is Low Margin | Boolean | Gross Margin % below 10 | True if transaction margin is below 10% |
| Is Loss | Boolean | Profit below 0 | True if transaction lost money |
| Is High Discount | Boolean | Discount above 0.30 | True if discount exceeded 30% |

## Business Assumptions
- Cost is derived as Sales minus Profit since COGS is not directly available
- Discount Amount is calculated from the discount rate and original price
- Low margin threshold is set at 10% based on standard retail benchmarks
- High discount threshold is set at 30% based on analysis findings