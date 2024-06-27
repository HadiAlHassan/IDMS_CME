import React from "react";
import classes from "./PieChart.module.css";
import { PieChart } from "@mui/x-charts/PieChart";

function PieChartComponent() {
  const data = [
    { id: 0, value: 20, label: "Agreement", color: "#2E86C1" },
    { id: 1, value: 20, label: "Court Case", color: "#1ABC9C" },
    { id: 2, value: 10, label: "Contract", color: "#8E44AD" },
    { id: 3, value: 10, label: "Technology" },
    { id: 4, value: 10, label: "Politics" },
    { id: 5, value: 10, label: "Sport" },
    { id: 6, value: 19, label: "Business" },
  ];

  return (
    <>
      <h2 className={classes.title}>Documents Category</h2>
      <div className={classes.pieChartContainer}>
        <PieChart
          series={[
            {
              data,
              highlightScope: { faded: "global", highlighted: "item" },
              faded: { innerRadius: 30, additionalRadius: -30, color: "gray" },
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
      </div>
    </>
  );
}
export default PieChartComponent;
