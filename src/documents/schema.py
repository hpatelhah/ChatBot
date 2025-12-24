from langchain_core.documents import Document


l1 = Document(
    page_content="""
Business Logic: Client Census Week Definition

Description:
A full client census week runs from **Sunday to Saturday**. All metrics and queries using `period_begin_date` in `dw_prod_report.vw_hours_and_client_census_weekly` should reference **last full week ending Saturday** using the logic:

`CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7)`

This ensures data consistency and avoids partial week bias.

Applies To:
- Metrics: Client Census, Count Change in Client Census, Percent Change in Client Census
- Table: dw_prod_report.vw_hours_and_client_census_weekly
""",
    metadata={"type": "business_logic", "name": "Client Census Week Logic"}
)

l2 = Document(
    page_content="""
Business Logic: Active Client

Description:
A client is considered **active** if `active_client_flag = TRUE` in the `DW_PROD_INTEGRATION.dim_client_merged` table. This flag is required for all the analaysis unless asked otherwise.

Applies To:
- Table: dw_prod_integration.dim_client_merged
""",
    metadata={"type": "business_logic", "name": "Active Client Definition"}
)




l3 = Document(
    page_content="""
Business Logic: Authorized vs Served Hours

Description:
- `AUTH_AMOUNT_VALID` refers to the **total number of authorized hours** for a client.
- `HOURS_UNITS_SERVED_VALID_AUTHS` refers to the **number of authorized hours that were actually served**.
- `hours_served_all` includes **both authorized and potentially unauthorized hours**.

Use Case:
To assess underutilization or overutilization, compare `HOURS_UNITS_SERVED_VALID_AUTHS` to `AUTH_AMOUNT_VALID`.

Applies To:
- Tables: dw_prod_report.vw_hours_and_client_census_monthly, dw_prod_report.vw_hours_and_client_census_weekly
""",
    metadata={"type": "business_logic", "name": "Authorized vs Served Hours"}
)

l4 = Document(
    page_content="""
Business Logic: Branch Attribution

Description:
A client is attributed to a branch using `branch_key`, which links census tables to branch metadata. Branch-level analyses (e.g., regional counts, client distribution by branch) must ensure this join:

`branch_key` - `dw_prod_integration.DIM_BRANCH_MRGED.branch_key`

Ensure null-safe joins to avoid dropping clients with missing branch attribution.

Applies To:
- Joins involving  dw_prod_report.vw_hours_and_client_census_monthly, dw_prod_report.vw_hours_and_client_census_weekly tables and dw_prod_integration.DIM_BRANCH_MRGED
- Metrics grouped by branch or region
""",
    metadata={"type": "business_logic", "name": "Branch Attribution"}
)

l5 = Document(
    page_content="""
Business Logic: Demographics Lookup

Description:
When enriching census data with demographics (e.g., gender, DOB, age), use `client_key` to join `dw_prod_integration.dim_client_merged`.

Important: Apply filters like `active_client_flag = TRUE` when generating metrics about the current population to avoid skew from inactive clients.

Applies To:
- All queries involving demographics (e.g., age, gender distributions, state)
""",
    metadata={"type": "business_logic", "name": "Demographics Lookup Handling"}
)

l6 = Document(
    page_content="""
Business Logic: Client Served Flag

Description:
A client is considered served if `CLIENT_SERVED_FLAG  = TRUE` in 'dw_prod_report.vw_hours_and_client_census_weekly' or 'dw_prod_report.vw_hours_and_client_census_monthly' tables. This flag should be set to 'TRUE' in all the analysis unless asked otherwise.

Applies To:
- Table: dw_prod_report.vw_hours_and_client_census_weekly, dw_prod_report.vw_hours_and_client_census_monthly
""",
    metadata={"type": "business_logic", "name": "Client Served Flag Definition"}
)

l7 = Document(
    page_content="""
Business Logic: Finance Data monthly vs weekly levels

Description: When asked about finance data relating to revenue, invoice, payrate, billing,etc, there are two tables with different levels, monthly level is data_science.finance_monthly_summary_by_state or data_science.finance_monthly_summary_by_state_and_PBL and weekly level is data_science.finance_weekly_summary. Use them accordingly and try not to use them interchangably


Applies To:
- Table: data_science.finance_monthly_summary_by_state_and_PBL, data_science.finance_monthly_summary_by_state,  data_science.finance_weekly_summary
    """,
    metadata={"type": "business_logic", "name": "Finance Data monthly vs weekly levels"}
    
)

l8 = Document(
    page_content="""
Business Logic: Month Definition 

Description:

A month is defined as full complete month as of current date, do not sure current month for analysis when asked for month level analysis. So for columns like monthstart or period_begin_date that is at month level then always cut it off at the last complete month. 

This ensures data consistency and avoids partial month bias.

Applies To:
- Metrics: Finance data monthly
- Table: dw_prod_report.vw_hours_and_client_census_weekly
""",
    metadata={"type": "business_logic", "name": "Monthly Analysis and Month Definition"}
)



l9 = Document(
    page_content="""
Business Logic: Rate calculation

Description:

When including rates in the analysis which requies regrouping, recalculate the weighted avgerage rates rather than using avg(rate).


Applies To:
- Metrics: Rate Calculation

""",
    metadata={"type": "business_logic", "name": "Rate Calculation"}
)





m1 = Document(page_content = """  
Name: Client Census
Description: count of all the client for a given week from sunday to saturday
SQL: SELECT COUNT(DISTINCT client_key) FROM dw_prod_report.vw_hours_and_client_census_weekly WHERE period_begin_date = (SELECT CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7) AS last_full_week_sunday) AND CLIENT_SERVED_FLAG = TRUE AND client_key IS NOT NULL
""",
         metadata={"type": "metric", "name": "Client Census"})


m2 = Document(
    page_content="""
Name: Change in Client Census Count
Description: difference in count of client census from between two full weeks
SQL: SELECT (SELECT COUNT(DISTINCT client_key) FROM dw_prod_report.vw_hours_and_client_census_weekly WHERE period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7) AND CLIENT_SERVED_FLAG = TRUE AND client_key IS NOT NULL) - (SELECT COUNT(DISTINCT client_key) FROM dw_prod_report.vw_hours_and_client_census_weekly WHERE period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 14) AND CLIENT_SERVED_FLAG = TRUE AND client_key IS NOT NULL) AS client_count_difference
""",
    metadata={"type": "metric", "name": "Change in Client Census Count"}
)

m3 = Document(
    page_content="""
Name: Percent Change in Client Census Count
Description: percent difference in count of client census from between two full weeks
SQL: SELECT CASE WHEN prev_week_count = 0 THEN NULL ELSE ROUND(100.0 * (last_week_count - prev_week_count) / prev_week_count, 1) END AS percent_change FROM ( SELECT (SELECT COUNT(DISTINCT client_key) FROM dw_prod.report.vw_hours_and_client_census_weekly WHERE period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7) AND CLIENT_SERVED_FLAG = TRUE AND client_key IS NOT NULL) AS last_week_count, (SELECT COUNT(DISTINCT client_key) FROM dw_prod.report.vw_hours_and_client_census_weekly WHERE period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 14) AND CLIENT_SERVED_FLAG = TRUE AND client_key IS NOT NULL) AS prev_week_count ) counts;
""",
    metadata={"type": "metric", "name": "Percent Change in Client Census Count"}
)

m4 = Document(
    page_content="""
Name: Percent Change in Client Census Count
Description: percent difference in count of client census from between two full weeks
SQL: SELECT CASE WHEN prev_week_count = 0 THEN NULL ELSE ROUND(100.0 * (last_week_count - prev_week_count) / prev_week_count, 1) END AS percent_change FROM ( SELECT (SELECT COUNT(DISTINCT client_key) FROM dw_prod.report.vw_hours_and_client_census_weekly WHERE period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7) AND CLIENT_SERVED_FLAG = TRUE AND client_key IS NOT NULL) AS last_week_count, (SELECT COUNT(DISTINCT client_key) FROM dw_prod.report.vw_hours_and_client_census_weekly WHERE period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 14) AND CLIENT_SERVED_FLAG = TRUE AND client_key IS NOT NULL) AS prev_week_count ) counts;
""",
    metadata={"type": "metric", "name": "Percent Change in Client Census Count"}
)


m5 =  Document(
    page_content = """
Name: Client Census Week-over-Week Comparison
Description: Count of distinct clients served per state for the last two full weeks (Sunday to Saturday), and the change in client count between those two weeks.
SQL: WITH census_counts AS (
  SELECT 
    state,
    period_begin_date,
    COUNT(DISTINCT client_key) AS client_count
  FROM dw_prod_report.vw_hours_and_client_census_weekly_partitioned
  WHERE CLIENT_SERVED_FLAG = TRUE
    AND client_key IS NOT NULL
    AND state IS NOT NULL
    AND period_begin_date IN (
      CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7),
      CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 14)
    )
  GROUP BY state, period_begin_date
),
pivoted_counts AS (
  SELECT
    state,
    MAX(CASE WHEN period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7)
             THEN client_count END) AS last_week_count,
    MAX(CASE WHEN period_begin_date = CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 14)
             THEN client_count END) AS prev_week_count
  FROM census_counts
  GROUP BY state
)
SELECT 
  state,
  last_week_count,
  prev_week_count,
  (last_week_count - COALESCE(prev_week_count, 0)) AS client_count_change
FROM pivoted_counts
ORDER BY client_count_change DESC
""",
    metadata = {
        "type": "metric_comparison",
        "name": "Client Census Week-over-Week Change",
        "optimized": True,
        "topic": "census",
        "granularity": "weekly",
        "dimension": "state"
    }
)

m6 = Document(
    page_content="""
Name: Financial Analysis
Description: For investigating factors impacting finance invoice and payroll data or any other trend, first level of factors to investigate 1. invoice rate, 2. pay rate, 3. hours served, and 4. client census. 
Next steps for invoice rate to dig into is 1a. business line level and program level invoice rate trend. For pay rate dig into 2a. emplpoyement type level pay trend if avalible.
For hours served dig into 3a. authorized hours trend, ratio of served to authoized hours, over and under served hours and all of this by business, program and county.
For client census dig into client churn rate and new client rate by business line, program name and county
""",
    metadata={"type": "metric", "name": "Financial Analysis"}
)

m7 = Document(
    page_content="""
Name: Adjusted daily invoice amount
Description: Adjusted daily invoice amount takes into account that # of days in a month differ month over month, as do the number of weekdays, number of weekends, and number of holidays. This is important since home care services are less on weekends and holidays.
The adjusted days takes into account that variation in days, weekdays, weekends, and holidays per month as well as differences in service intensity by state on these different types of days. This should always be used when the prompt includes a request for month over month invoice trends even it is not explicitly requested.
The "adjusted_days" value which is included in the finance monthly summary tables by state (data_science.finance_monthly_summary_by_state) and by parent business line (data_science.finance_monthly_summary_by_state_and_PBL) both include an "adjusted days" which should be used in the calculating the adjusted daily invoice amount as:

sum(P_SUM_INVOICE_AMOUNT)/max(adjusted_days) as total_adjusted_invoice_amount_by_day

Please report this as a $ amount rounded to the nearest $
""",
    metadata={"type": "metric", "name": "Adjusted Invoice Amount"}
)

m8 = Document(
    page_content="""
Name: Adjusted daily visit cost
Description: Adjusted daily visit cost takes into account that # of days in a month differ month over month, as do the number of weekdays, number of weekends, and number of holidays. This is important since home care services are less on weekends and holidays.
The adjusted days takes into account that variation in days, weekdays, weekends, and holidays per month as well as differences in service intensity by state on these different types of days. This should always be used when the prompt includes a request for month over month visit cost trends even it is not explicitly requested.
The "adjusted_days" value which is included in the finance monthly summary tables by state (data_science.finance_monthly_summary_by_state) and by parent business line (data_science.finance_monthly_summary_by_state_and_PBL) both include an "adjusted days" which should be used in the calculating the adjusted daily visit cost by day as:

sum(P_SUM_VISIT_COST)/max(adjusted_days) as total_adjusted_visit_cost_by_day

Please report this as a $ amount rounded to the nearest $
 
""",
    metadata={"type": "metric", "name": "Adjusted Visit Cost"}
)

m9 = Document(
    page_content="""
Name: Invoice amount by month or monthly invoice amount
Description: Any analysis that involves month over month change or month over month trends in invoice amount should use the adjusted daily invoice amount rather than the total invoice amount. 
Ajusted daily invoice amounttakes into account that # of days in a month differ month over month, as do the number of weekdays, number of weekends, and number of holidays. This is important since home care services are less on weekends and holidays.
The adjusted days takes into account that variation in days, weekdays, weekends, and holidays per month as well as differences in service intensity by state on these different types of days. This should always be used when the prompt includes a request for month over month invoice trends even it is not explicitly requested.
The "adjusted_days" value which is included in the finance monthly summary tables by state (data_science.finance_monthly_summary_by_state) and by parent business line (data_science.finance_monthly_summary_by_state_and_PBL) both include an "adjusted days" which should be used in the calculating the adjusted daily invoice amount as:

sum(P_SUM_INVOICE_AMOUNT)/max(adjusted_days) as total_adjusted_invoice_amount_by_day

Please report this as a $ amount rounded to the nearest $
""",
    metadata={"type": "metric", "name": "Invoice amount by month"}
)

m10 = Document(
    page_content="""
Name: Monthly visit cost or visit cost by month
Description: Any analysis that involves month over month change or month over month trends should use the adjusted daily visit cost rather than the actual visit cost.
Adjusted daily visit cost takes into account that # of days in a month differ month over month, as do the number of weekdays, number of weekends, and number of holidays. This is important since home care services are less on weekends and holidays.
The adjusted days takes into account that variation in days, weekdays, weekends, and holidays per month as well as differences in service intensity by state on these different types of days. This should always be used when the prompt includes a request for month over month visit cost trends even it is not explicitly requested.
The "adjusted_days" value which is included in the finance monthly summary tables by state (data_science.finance_monthly_summary_by_state) and by parent business line (data_science.finance_monthly_summary_by_state_and_PBL) both include an "adjusted days" which should be used in the calculating the adjusted daily visit cost by day as:

sum(P_SUM_VISIT_COST)/max(adjusted_days) as total_adjusted_visit_cost_by_day

Please report this as a $ amount rounded to the nearest $
 
""",
    metadata={"type": "metric", "name": "Monthly Visit Cost"}
)

m11 = Document(
    page_content="""
Name: Gross margin
Description: Gross margin is defined as the invoice amount less than visit cost.


sum(P_SUM_INVOICE_AMOUNT)-sum(P_SUM_VISIT_COST) as GROSS_MARGIN

Please report this as a $ amount rounded to the nearest $
 
""",
    metadata={"type": "metric", "name": "Gross Margin"}
)

m12 = Document(
    page_content="""
Name: Adjusted daily gross margin
Description: Adjusted daily gross margin is defined as the adjusted invoice amount per day less than adjusted visit cost per day.


sum(P_SUM_INVOICE_AMOUNT)/max(adjusted_days)-sum(P_SUM_VISIT_COST)/max(adjusted_days)  as ADJUSTED_DAILY_GROSS_MARGIN

Please report this as a $ amount rounded to the nearest $
 
""",
    metadata={"type": "metric", "name": "Adjusted daily Gross Margin"}
)



m13 = Document(
    page_content="""
Name: Utilization

Description: Utilization is the % of the authorized hours which are served

It is calculated as sum(HOURS_UNITS_SERVED_VALID_AUTHS)/sum(AUTH_AMOUNT_VALID) 

Use Case:
When asked to assess utilization or utilization ratio

Applies To:
- Tables: dw_prod_report.vw_hours_and_client_census_monthly, dw_prod_report.vw_hours_and_client_census_weekly
""",
    metadata={"type": "business_logic", "name": "Utilization"}
)


m14 = Document(
    page_content="""
Name: Overserved hours

Description: Sum of hours which are served over what was authorized

It is calculated as 
SUM(
        CASE 
            WHEN HOURS_SERVED_ALL - AUTH_AMOUNT_VALID  > 0 
            THEN HOURS_SERVED_ALL - AUTH_AMOUNT_VALID 
            ELSE 0 
        END
    ) AS over_served_hours


Applies To:
- Tables: dw_prod_report.vw_hours_and_client_census_monthly, dw_prod_report.vw_hours_and_client_census_weekly
""",
    metadata={"type": "business_logic", "name": "Overserved hours"}
)



m15 = Document(
    page_content="""
Name: Underserved hours

Description: Sum of hours which are served under what was authorized

It is calculated as 
SUM(
        CASE 
            WHEN HOURS_SERVED_ALL - AUTH_AMOUNT_VALID  < 0 
            THEN HOURS_SERVED_ALL - AUTH_AMOUNT_VALID 
            ELSE 0 
        END
    ) AS under_served_hours


Applies To:
- Tables: dw_prod_report.vw_hours_and_client_census_monthly, dw_prod_report.vw_hours_and_client_census_weekly
""",
    metadata={"type": "business_logic", "name": "Underserved hours"}
)

m16 = Document(
    page_content="""
Name: Margin loss due to overservice

Description: When we have overserved hours (hours served that exceed hours that are authorized), we pay our caregivers but we cannot bill for these hours.
This results in a lower gross margin as our visit costs increase to pay for these hours while our invoice or billed amount is 0 for these hours.

To calculate the margin loss: 

over_served_hours * pcal_pay_rate = margin loss due to overservice


Applies To:
- Tables: dw_prod_report.vw_hours_and_client_census_monthly, dw_prod_report.vw_hours_and_client_census_weekly, data_science.finance_monthly_summary_by_state, data_science.finance_monthly_summary_by_state_and_PBL
""",
    metadata={"type": "business_logic", "name": "Margin loss due to overservice"}
)

m17 = Document(
    page_content="""
Name: Margin loss due to underservice

Description: When we have underserved hours (hours served that are less than hours that are authorized), we lose an opportunity to bill for these hours.
This results in a lower gross margin than our potential as we cannot bill for hours we did not serve.

To calculate the margin loss due to underservice: 
under_served_hours * (pcal_bill_rate - pcal_pay_rate) = margin loss due to underservice


Applies To:
- Tables: dw_prod_report.vw_hours_and_client_census_monthly, dw_prod_report.vw_hours_and_client_census_weekly, data_science.finance_monthly_summary_by_state, data_science.finance_monthly_summary_by_state_and_PBL
""",
    metadata={"type": "business_logic", "name": "Margin loss due to underservice"}
)






j1 = Document(
    page_content="""
Join: dw_prod_report.vw_hours_and_client_census_weekly - dw_prod_integration.dim_client_merged
Keys:
- client_key = client_key

Description:
Join client census weekly data with demographic information about clients. This join allows enrichment of weekly service records with client attributes such as gender, DOB, city, and active status.
""",
    metadata={"type": "join", "name": "vw_hours_and_client_census_weekly - dim_client_merged"}
)

j2 = Document(
    page_content="""
Join: dw_prod_report.vw_hours_and_client_census_monthly - dw_prod_integration.dim_client_merged
Keys:
- client_key = client_key

Description:
Join client census monthly data with client demographic data to analyze monthly service trends alongside personal attributes such as age, gender, or branch association.
""",
    metadata={"type": "join", "name": "vw_hours_and_client_census_monthly - dim_client_merged"}
)

j3 = Document(
    page_content="""
Join: dw_prod_report.vw_hours_and_client_census_weekly - DW_PROD_INTEGRATION.DIM_BRANCH_MERGED
Keys:
- branch_key = branch_key

Description:
Combine weekly client census with branch-level metadata such as branch name, state code, and region manager to perform geographic queries.
""",
    metadata={"type": "join", "name": "vw_hours_and_client_census_weekly - DIM_BRANCH_MERGED"}
)


j4 = Document(
    page_content="""
Join: dw_prod_report.vw_hours_and_client_census_monthly - DW_PROD_INTEGRATION.DIM_BRANCH_MERGED
Keys:
- branch_key = branch_key

Description:
Join monthly service utilization data with branch details for deeper analysis of service delivery by location or managerial queries.
""",
    metadata={"type": "join", "name": "vw_hours_and_client_census_monthly - DIM_BRANCH_MERGED"}
)

j5 = Document(
    page_content="""
Join: dw_prod_report.vw_hours_and_client_census_monthly - data_science.finance_contract_details_mapping
Keys:
- contract_service_key = contract_service_key

Description:
Join monthly hours and client census information with contract details mapping table to break down hours and census information by program name, business line name and parent business line name.

""",
    metadata={"type": "join", "name": "vw_hours_and_client_census_monthly - finance_contract_details_mapping"}
)


j6 = Document(
    page_content="""
Join: dw_prod_report.vw_hours_and_client_census_weekly - data_science.finance_contract_details_mapping
Keys:
- contract_service_key = contract_service_key

Description:
Join weekly hours and client census information with contract details mapping table to break down hours and census information by program name, business line name and parent business line name.

""",
    metadata={"type": "join", "name": "vw_hours_and_client_census_weekly - finance_contract_details_mapping"}
)

t1 = Document(
    page_content="""
Table: dw_prod_report.vw_hours_and_client_census_weekly
Description: This table stores monthly information all the clients enrolled along with their demographics and numbers of hours utilized.
Columns:
- period_begin_date (date): week identifier. Synonyms: week
- client_key (string): unique id per client. Synonyms: client id
- CLIENT_SERVED_FLAG (Boolean): True or False flag to identify active clients
- branch_key (string): unique id for the branch that the client belongs to. Synonyms: branch id, branch key, branch
- state (string): client's state abbreviation as two letter. Synonyms: client_state, state code, US state abbreviation
- hours_served_all (numeric): number of hours served or used by the client for that week. Synonyms: hours, used_hours, served hours
- ABSOLUTE_FIRST_SERVICE_DATE (date): very first service date, start date, or joining date of the client. Synonyms: first service date, start absolute date, joined company date
- ABSOLUTE_LAST_SERVICE_DATE (date): very last service date, latest date, or most recent date of the client. Synonyms: last service date, recent date
- HOURS_UNITS_SERVED_VALID_AUTHS (numeric): hours served from the authorized hours. Synonyms: valid served, valid hours
- AUTH_AMOUNT_VALID (numeric): authorized hours. Synonyms: auth hours
- contract_service_key (string): contract service key used to join on data_science.finance_contract_details_mapping to get program name, business line name and parent business line name
- css_name: name of the client services supervisor, each client is assigned to a css who manages the clinet's schedules, auth hours, preferences, etc. When searching for the name, exact name might not be present so the feild might have middle name which user doesnt know about so use LIKE and LOWER in sql for the name matching. Synonyms: supervisor, client supervisor
Sample Query:
- top 5 clients with most hours in the week of march 2024: select client_key, sum(hours_served_all) from dw_prod_report.vw_hours_and_client_census_weekly where period_begin_date >='2024-03-01' and  period_begin_date <='2024-03-31' group by 1 order by sum(hours_served_all) desc limit 5
- count number of clients per date by which state they came from: select period_begin_date, state, count(distinct client_key) from dw_prod.report.vw_hours_and_client_census_weekly group by 1, 2  order by period_begin_date desc
""",
    metadata={"type": "table", "name": "dw_prod_report.vw_hours_and_client_census_weekly"}
)



t2 = Document(
    page_content="""
Table: dw_prod_report.vw_hours_and_client_census_monthly
Description: This table stores monthly information all the clients enrolled along with their demographics and numbers of hours utilized.
Columns:
- period_begin_date (date): month identifier. Synonyms: month
- client_key (string): unique id per client. Synonyms: client id
- CLIENT_SERVED_FLAG (Boolean): True or False flag to identify active clients
- branch_key (string): unique id of the branch that the client belongs to. Synonyms: branch id, branch, client's branch
- state (string): client's state abbreviation as two letter. Synonyms: client_state, state code, US state abbreviation
- hours_served_all (numeric): number of hours served or used by the client for that month. Synonyms: hours, used_hours, served hours
- contract_name (string): N/A
- ABSOLUTE_FIRST_SERVICE_DATE (date): very first service date, start date, or joining date of the client. Synonyms: first service date, start absolute date, joined company date
- ABSOLUTE_LAST_SERVICE_DATE (date): very last service date, latest date, or most recent date of the client. Synonyms: last service date, recent date
- HOURS_UNITS_SERVED_VALID_AUTHS (numeric): hours served from the authorized hours. Synonyms: valid served, valid hours
- AUTH_AMOUNT_VALID (numeric): authorized hours. Synonyms: auth hours
- contract_service_key (string): contract service key used to join on data_science.finance_contract_details_mapping to get program name, business line name and parent business line name

Sample Query:
- top 5 clients with most hours in the month of march 2024: select client_key, sum(hours_served_all) from dw_prod_report.vw_hours_and_client_census_monthly where period_begin_date = '2024-03-01' group by 1 order by sum(hours_served_all) desc limit 5
- count number of clients per month by which state they came from: select period_begin_date, state, count(distinct client_key) from dw_prod_report.vw_hours_and_client_census_monthly group by 1, 2
""",
    metadata={"type": "table", "name": "dw_prod_report.vw_hours_and_client_census_monthly"}
)

t3 = Document(
    page_content="""
Table: dw_prod_integration.dim_client_merged
Description: This table stores client demographic information and whether the client is active or not.
Columns:
- client_key (string): unique id per client. Synonyms: client id
- client_dob (timestamp): client's date of birth. Synonyms: dob, birth date, date of birth
- client_gender (string): gender of the client. Synonyms: client gender, gender, male, female
- client_state_code (string): client's state abbreviation as two letter. Synonyms: client_state, state code, US state abbreviation
- client_first_name (string): client's first name
- client_last_name (string): client's last name
- client_std_city (string): client city
- primary_branch_name (string): name of the client's primary branch

Sample Query:
- top 5 clients with most hours in the month of march 2024: select client_key, sum(hours_served_all) from dw_prod_report.vw_hours_and_client_census_monthly where period_begin_date = '2024-03-01' group by 1 order by sum(hours_served_all) desc limit 5
- count number of clients per month by which state they came from: select period_begin_date, state, count(distinct client_key) from dw_prod_report.vw_hours_and_client_census_monthly group by 1, 2
- find top 5 cities with oldest average client age (for active clients only): SELECT client_std_city, AVG(EXTRACT(YEAR FROM AGE(current_date, client_dob))) AS avg_age FROM dw_prod_integration WHERE active_client_flag = TRUE GROUP BY client_std_city ORDER BY avg_age DESC LIMIT 5;
""",
    metadata={"type": "table", "name": "dw_prod_integration.dim_client_merged"}
)




t4 = Document(
    page_content="""
Table: DW_PROD_INTEGRATION.DIM_BRANCH_MERGED
Description: This table stores branch information
Columns:
- branch_key (string): week identifier. Synonyms: branch id, branch key, branch
- branch_name (string): name of the branch. Synonyms: branch name
- office_state_code (string): branch's state abbreviation as two letter. Synonyms: branch state, state code, US state abbreviation
- hours_served_all (numeric): N/A
- region_manager (string): manager of the branch. Synonyms: manager, region manager

Sample Query:
- count number of branches being managed by manager in IL: select distinct region_manager, count(distinct branch_key) from DW_PROD_INTEGRATION.DIM_BRANCH_MERGED where office_state_code = 'IL' and region_manager is not null group by 1 order by count(distinct branch_key) desc
""",
    metadata={"type": "table", "name": "DW_PROD_INTEGRATION.DIM_BRANCH_MERGED"}
)


t5 = Document(
    page_content="""
Table: data_science.finance_monthly_summary_by_state
Description: This table contains aggregated payroll information at the month and state level. It includes total hours served, billed hours, costs, invoice amounts, visit counts, client counts, and key calculated metrics for reconciliation and rate analysis. Use this table when asked about month level finance data that is at the state or total enterprise level.
Columns:
- period_name (date): month-start date identifier. Synonyms: start of month, payroll month, month
- office_state_code (string): two-letter state code of the office, e.g., NY, PA. Synonyms: state code, branch state
- p_sum_hours_served (numeric): total hours served for the month. Synonyms: served hours, hours worked
- p_sum_visit_cost (numeric): total visit cost for the month. Synonyms: cost of visits, visit expense, payroll cost, wage cost
- p_sum_hours_billed (numeric): total billed hours for the month. Synonyms: billed hours
- p_sum_invoice_amount (numeric): total invoice amount issued for the month. Synonyms: invoice amt, billed amount
- p_sum_reg_cost (numeric): total regular labor cost. Synonyms: regular cost, base cost
- p_sum_ot_hours (numeric): total overtime hours. Synonyms: overtime, OT hrs
- p_sum_ot_cost (numeric): total overtime labor cost. Synonyms: OT cost, extra hours cost

- p_count_visit (numeric): total number of visits in the month. Synonyms: visit count
- p_count_client_key (numeric): total number of client records. Synonyms: client count
- p_count_distinct_client_key (numeric): total number of distinct clients. Synonyms: unique clients, client diversity

- pcal_pay_rate (numeric): calculated pay rate. Synonyms: pay per hour, wages per hour, visit cost per hour
- pcal_bill_rate (numeric): calculated bill rate. Synonyms: billing rate per hour, invoice rate per hour
- pcal_reg_rate (numeric): calculated regular rate. Synonyms: base hourly rate
- pcal_ot_rate (numeric): calculated overtime rate. Synonyms: OT hourly rate
- adjusted days (numeric): these are the count of days in the month adjusted for lower service hours that occur on weekends and holidays. All month over month or year over year reporting on invoice and visit cost amounts should use the adjusted days to calculate  and report on adjusted invoice amount and adjusted cost, even if it is not specifically requested.
- total days (numeric): total days in the month

Sample Queries:
- find states with highest monthly invoice amounts in July 2025:
  select office_state_code, sum(P_SUM_INVOICE_AMOUNT) as total_invoice_amount
  from data_science.finance_monthly_summary_by_state
  where period_name = '2025-07-01'
  group by office_state_code;

- calculate total hours served vs hours billed per state in July 2025:
  select office_state_code, sum(p_sum_hours_served) as total_served, sum(p_sum_hours_billed) as total_billed
  from data_science.finance_monthly_summary_by_state
  where period_name = '2025-07-01'
  group by office_state_code;

- calculate the month over month actual and adjusted daily invoice amounts for PA in 2025
  select period_name, sum(P_SUM_INVOICE_AMOUNT)/max(total_days) as total_invoice_amount_by_day,
  sum(P_SUM_INVOICE_AMOUNT)/max(adjusted_days) as total_adjusted_invoice_amount_by_day
  from data_science.finance_monthly_summary_by_state
  where office_state_code = 'PA' and period_name >= '2025-01-01'
  group by period_name

""",
    metadata={"type": "table", "name": "finance_monthly_summary_by_state"}
)

t8 = Document(
    page_content="""
Table: data_science.finance_monthly_summary_by_state_and_PBL
Description: This table contains aggregated payroll and invoice information at the month, state, and parent business line level. It includes total hours served, billed hours, costs, invoice amounts, visit counts, client counts, and key calculated metrics for reconciliation and rate analysis. Use this table when asked about month level finance data that is at the business line level.
Columns:
- period_name (date): month-start date identifier. Synonyms: start of month, payroll month, month
- office_state_code (string): two-letter state code of the office, e.g., NY, PA. Synonyms: state code, branch state
- parent_business_line_name (string): name of the parent business line. all states can be further broken down by business line for financial reporting
- p_sum_hours_served (numeric): total hours served for the month. Synonyms: served hours, hours worked
- p_sum_visit_cost (numeric): total visit cost for the month. Synonyms: cost of visits, visit expense, payroll cost, wage cost
- p_sum_hours_billed (numeric): total billed hours for the month. Synonyms: billed hours
- p_sum_invoice_amount (numeric): total invoice amount issued for the month. Synonyms: invoice amt, billed amount
- p_sum_reg_cost (numeric): total regular labor cost. Synonyms: regular cost, base cost
- p_sum_ot_hours (numeric): total overtime hours. Synonyms: overtime, OT hrs
- p_sum_ot_cost (numeric): total overtime labor cost. Synonyms: OT cost, extra hours cost

- p_count_visit (numeric): total number of visits in the month. Synonyms: visit count
- p_count_client_key (numeric): total number of client records. Synonyms: client count
- p_count_distinct_client_key (numeric): total number of distinct clients. Synonyms: unique clients, client diversity

- pcal_pay_rate (numeric): calculated pay rate. Synonyms: pay per hour, wage rate per hour, visit cost per hour
- pcal_bill_rate (numeric): calculated bill rate. Synonyms: billing rate per hour, invoice rate per hour
- pcal_reg_rate (numeric): calculated regular rate. Synonyms: base hourly rate
- pcal_ot_rate (numeric): calculated overtime rate. Synonyms: OT hourly rate
- adjusted days (numeric): these are the count of days in the month adjusted for lower service hours that occur on weekends and holidays. All month over month or year over year reporting on invoice and visit cost amounts should use the adjusted days to calculate  and report on adjusted invoice amount and adjusted cost, even if it is not specifically requested.
- total days (numeric): total days in the month


Sample Queries:
- find invoice amount by business line for PA in July 2025:
  select  parent_business_line_name, sum(P_SUM_INVOICE_AMOUNT) as total_invoice_amount
  from data_science.finance_monthly_summary_by_state_and_PBL
  where period_name = '2025-07-01' and office_state_code = 'PA'
  group by office_state_code;

- calculate the month over month actual and adjusted daily invoice amounts for PA business lines in 2025
  select period_name, parent_business_line_name, sum(P_SUM_INVOICE_AMOUNT)/max(total_days) as total_invoice_amount_by_day,
  sum(P_SUM_INVOICE_AMOUNT)/max(adjusted_days) as total_adjusted_invoice_amount_by_day
  from data_science.finance_monthly_summary_by_state_and_PBL
  where office_state_code = 'PA' and period_name >= '2025-01-01'
  group by period_name, parent_business_line_name
""",
    metadata={"type": "table", "name": "finance_monthly_summary_by_state_and_PBL"}
)


t6 = Document(
    page_content="""
Table: data_science.finance_weekly_summary
Description: This table contains aggregated payroll, hours and finance information at the week, program, state, and county level. It includes total hours served, billed hours, costs, invoice amounts, visit counts, client counts, over and under served hours and cost and other key calculated metrics finance related analysis. Use this table when asked at weekly level.
Columns:
- weekending (date): end of the week date (sunday). Synonyms: week, payroll week
- office_state_code (string): two-letter state code of the office, e.g., NY, PA. Synonyms: state code, branch state
- program_name (string): name of the client program. Synonyms: program, service program, program name
- client_std_county (string): client county. Synonyms: county, client county
- business_line_name (string): name of the business line 
- parent_business_line_name (string): name of the parent business line
- p_sum_hours_served (numeric): total hours served for the week. Synonyms: served hours, hours worked
- p_sum_visit_cost (numeric): total visit cost for the week. Synonyms: cost of visits, visit expense
- p_sum_hours_billed (numeric): total billed hours for the week. Synonyms: billed hours
- p_sum_invoice_amount (numeric): total invoice amount issued for the week. Synonyms: invoice amt, billed amount
- p_sum_reg_cost (numeric): total regular labor cost. Synonyms: regular cost, base cost
- p_sum_ot_hours (numeric): total overtime hours. Synonyms: overtime, OT hrs
- p_sum_ot_cost (numeric): total overtime labor cost. Synonyms: OT cost, extra hours cost

- p_count_visit (numeric): total number of visits in the week. Synonyms: visit count
- p_count_client_key (numeric): total number of client records. Synonyms: client count
- p_count_distinct_client_key (numeric): total number of distinct clients. Synonyms: unique clients, client diversity

- pcal_pay_rate (numeric): calculated pay rate. Synonyms: pay per hour
- pcal_bill_rate (numeric): calculated bill rate. Synonyms: billing rate per hour
- pcal_reg_rate (numeric): calculated regular rate. Synonyms: base hourly rate
- pcal_ot_rate (numeric): calculated overtime rate. Synonyms: OT hourly rate
- pcal_rev (numeric): calculated revenue. Synonyms: revenue, total earnings

- p_wkend_sum_hours_served (numeric): total hours served for the weekend. Synonyms: served hours, hours worked
- p_wkend_sum_visit_cost (numeric): total visit cost for the weekend. Synonyms: cost of visits, visit expense
- p_wkend_sum_hours_billed (numeric): total billed hours for the weekend. Synonyms: billed hours
- p_wkend_sum_invoice_amount (numeric): total invoice amount issued for the weekend. Synonyms: invoice amt, billed amount
- p_wkend_sum_reg_cost (numeric): total regular labor cost from the weekend. Synonyms: regular cost, base cost
- p_wkend_sum_ot_hours (numeric): total overtime hours fromt the weekend. Synonyms: overtime, OT hrs
- p_wkend_sum_ot_cost (numeric): total overtime labor cost from the weekend. Synonyms: OT cost, extra hours cost

- p_wkend_count_visit (numeric): total number of visits in the weekend. Synonyms: visit count
- p_wkend_count_client_key (numeric): total number of client records from the weekend. Synonyms: client count
- p_wkend_count_distinct_client_key (numeric): total number of distinct clients from the weekend. Synonyms: unique clients, client diversity

- pcal_wkend_pay_rate (numeric): calculated pay rate for the weekend. Synonyms: pay per hour
- pcal_wkend_bill_rate (numeric): calculated bill rate for the weekend. Synonyms: billing rate per hour
- pcal_wkend_reg_rate (numeric): calculated regular rate for the weekend. Synonyms: base hourly rate
- pcal_wkend_ot_rate (numeric): calculated overtime rate for the weekend. Synonyms: OT hourly rate
- pcal_wkend_rev (numeric): calculated revenue for the weekend. Synonyms: revenue, total earnings

- over_served_hours (numeric): totoal numver of served hours compare to what was authorized that are over
- under_served_hours (numeric): total under served hours compare to what was authorized that are under

- overserved_outofpocket_cost (numeric): money paid out of pocket for over served hours.
- underserved_missed_rev (numeric): money lost that could have been made in revenue if of all

Sample Queries:


- calculate total hours served  for the last six weeks:
WITH weekly_hours_served AS (
  SELECT 
    w.weekending,
    w.state,
    sum( w.p_sum_hours_served) as total_hours_served
  FROM data_science.finance_weekly_summary w
  WHERE w.weekending >= CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 42)
    AND w.weekending <= CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::integer + 7)
  GROUP BY w.weekending, w.state
)

- identify counties with highest visit counts:
  select client_std_county, sum(p_count_visit) as total_visits
  from data_science.finance_weekly_summary
  group by client_std_county
  order by total_visits desc
  limit 5;
""",
    metadata={"type": "table", "name": "finance_weekly_summary"}
)


t7 = Document(
    page_content="""
Table: data_science.finance_contract_details_mapping
Description: This table contains mapping to go from contract_service_key to program_name, business line name and the parent business line name.  
Columns:

- contract_service_key (string): unique contract service key identifier
- program_name (string): name of the client program. Synonyms: program, service program, program name
- business_line_name (string): name of the business line 
- parent_business_line_name (string): name of the parent business

Sample Queries:


- calculate client census monthly by program
select program_name, period_begin_date, count(distinct client_key) from dw_prod_report.vw_hours_and_client_census_monthly c join 
data_science.finance_contract_details_mapping m on c.contract_service_key = m.contract_service_key group by program_name, period_begin_date


""",
    metadata={"type": "table", "name": "finance_contract_details_mapping"}
)


all_docs = [l1,l2,l3,l4,l5,l6,l7,l8,l9,
            m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,
            j1,j2,j3,j4,j5,j6,
            t1,t2,t3,t4,t5,t6,t7,t8]