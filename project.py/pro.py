import streamlit as st
import pandas as pd
 
st.title("Electricity Bill Calculator", width="stretch")

noOfUnits = 0

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
   status = st.radio("select an option:", ['Reading', 'No of Units'], horizontal=True)

if status == "Readings":
        preReading = st.number_input("Enter last month reading", key="pre",
        min_value=0, step=1, format="%d")
        curReading = st.number_input("Enter this month reading", key="cur",
        min_value=0, step=1, format="%d")

        if preReading and curReading:
           preReading = int(preReading)
           curReading = int(curReading)

           if curReading >= preReading:
            noOfUnits = curReading - preReading

           else:
                st.warning("Current reading must be greater than or equal to previous reading")

elif status == "No of Units":
        noOfUnits = st.number_input("Enter number of units used", key="units",
                   min_value=0, step=1, format="%d")
            
if st.button("Calculate") and noOfUnits > 0:
        try:
            row = []

            fixed_charge = round(350.00,2)
            unit_cost = 0.00
            units_remaining = noOfUnits

            if units_remaining > 0:
                units = min(20, units_remaining)
                cost = round(5.00 * units, 2)
                row.append(["First 20 units", units, 5.00, cost])
                unit_cost += cost
                units_remaining -= units

            if units_remaining > 0:
                units = min(50, units_remaining)
                cost = round(7.00 * units,2)
                row.append(["Second 50 units", units, 7.00, cost])
                unit_cost += cost
                units_remaining -= units

            if units_remaining > 0:
                cost = round(units_remaining * 10.00, 2)
                row.append(["Remaining units", units_remaining, 10.00, cost])
                unit_cost += cost

            total_cost = fixed_charge + unit_cost

            st.info(f"Total charge: Rs.{total_cost:.2f}")

            row.append(["First 20 units", units, 5.00, cost])

            row.append(["Fixed charge", "- -", "- -", fixed_charge])

            total_cost = round(unit_cost + fixed_charge,2)
            row.append(["Total charge", "- -", "- -", total_cost])

            

            df = pd.DataFrame(row,columns=["Description","Units(kwh)","Rate (Rs.)",
                                               "cost(Rs.)"])
                
            df["Rate (Rs.)"] = df["Rate (Rs.)"].apply(lambda x: f"{x:.2f}" if
                                                          isinstance(x, (int, float)) else x)
                
            df["cost (Rs.)"] = df["cost (Rs.)"].apply(lambda x: f"{x:.2f}" if
                                                          isinstance(x, (int, float)) else x)
                
            st.table(df)

        except Exception as e:
                st.error(f"Error calculating bill: {e}")