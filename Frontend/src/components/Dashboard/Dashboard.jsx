import React from "react";
import WordCloud from "./WordCloud";
import PieChartComponent from "./PieChart";
import { Card, CardContent } from "@mui/material";
import classes from "./Dashboard.module.css";

function Dashboard() {
  return (
    <div className={classes.dashboardBackground}>
      <Card className={classes.column}>
        <CardContent>
          <WordCloud />
        </CardContent>
      </Card>
      <Card className={classes.column}>
        <CardContent>
          <PieChartComponent />
        </CardContent>
      </Card>
    </div>
  );
}

export default Dashboard;
