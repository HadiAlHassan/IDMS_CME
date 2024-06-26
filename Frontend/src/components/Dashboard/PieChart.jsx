import React from "react";
import classes from "./PieChart.module.css";
import { PieChart } from "@mui/x-charts/PieChart";

function PieChartComponent() {
  const data = [
    { id: 0, value: 10, label: "Agreements", color: "#2E86C1" },
    { id: 1, value: 15, label: "Court Cases", color: "#1ABC9C" },
    { id: 2, value: 20, label: "Contracts", color: "#8E44AD" },
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
          height={200}
        />
      </div>
    </>
  );
}
export default PieChartComponent;
