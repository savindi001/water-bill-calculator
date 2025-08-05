import streamlit as st
import pandas as pd

st.title("Water Bill Calculator", width="stretch")

# Initialize variables
noOfUnits = 0

# Create Columns to Control layout
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    

    # Input logic
   
        iniReading = st.number_input("Enter initial meter reading", key="ini",
        min_value=0, step=1, format="%d")
        finReading = st.number_input("Enter final meter reading", key="fin",
        min_value=0, step=1, format="%d")

        if iniReading and finReading:
            iniReading = int(iniReading)
            finReading = int(finReading)

            if iniReading >= finReading:
             noOfUnits = iniReading - finReading

            else:
               st.warning("final meter reading must be greater than or initial meter reading")

 
  
    # Calculate button
if st.button("Calculate") and noOfUnits > 0:
    try:
          row = []

          # monthly charge
          monthly_charge = round(100.00,2)
          unit_cost = 0.00
          units_remaining = noOfUnits

          # For first 25 units
          if units_remaining > 0:
             units = min(25, units_remaining)
             cost = round(5.00 * units, 2)
             row.append(["First 25 units", units, 5.00, cost])
             unit_cost += cost
             units_remaining -= units

          # For second 25 units
          if units_remaining > 0:
             units = min(25, units_remaining)
             cost = round(7.00 * units,2)
             row.append(["Second 25 units", units, 7.00,cost])
             unit_cost += cost
             units_remaining -= units

          # Remaining units
          if units_remaining > 0:
             cost = round(units_remaining * 15.00, 2)
             row.append(["Remaining units", units_remaining, 15.00, cost])
             unit_cost += cost

          total_cost = monthly_charge + unit_cost

          # Add monthly charge
          row.append(["Monthly charge", "- -", "- -", monthly_charge])

          total_cost = round(unit_cost + monthly_charge, 2)
          row.append(["Total charge", "- -", "- -", total_cost])

          # show result
          st.info(f"Total charge: Rs.{total_cost:.2f}")

          # convert to dataframe and show table
          df=pd.DataFrame(row,columns=["Description", "Units(KWh)", "Rate (Rs.)","cost (Rs.)"])

             #format the rate and cost columns
          df["Rate (Rs.)"] = df["Rate (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
          df["Cost (Rs.)"] = df["Cost (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
          st.table(df)

    except Exception as e:
            st.error(f"Error calculating bill:{e}")