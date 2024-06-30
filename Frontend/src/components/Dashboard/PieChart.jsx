import React, { useState, useEffect, useContext } from "react";
import classes from "./PieChart.module.css";
import { PieChart } from "@mui/x-charts/PieChart";
import axios from "axios";
import { UpdateContext } from "../Context/UpdateContext";
import { Typography } from "@mui/material";
function PieChartComponent() {
  const [data, setData] = useState([]);
  const { updatePieChart } = useContext(UpdateContext);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/category-document-count"
        );
        const fetchedData = response.data.map((item, index) => ({
          id: index,
          value: item.document_count,
          label: item.category,
        }));
        setData(fetchedData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [updatePieChart]); // Re-fetch data when updatePieChart changes

  return (
    <>
      <h2 className={classes.title}>Documents Category</h2>
      <div className={classes.pieChartContainer}>
        {data.length === 0 ? (
          <Typography className={classes.noData}>No data inserted</Typography>
        ) : (
          <PieChart
            series={[
              {
                data,
                highlightScope: { faded: "global", highlighted: "item" },
                faded: {
                  innerRadius: 30,
                  additionalRadius: -30,
                  color: "gray",
                },
              },
            ]}
            slotProps={{
              legend: {
                labelStyle: {
                  fontSize: 14,
                  fill: "white",
                },
              },
            }}
            height={250}
          />
        )}
      </div>
    </>
  );
}

export default PieChartComponent;
