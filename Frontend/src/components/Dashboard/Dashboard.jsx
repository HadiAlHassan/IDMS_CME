import React from "react";
import WordCloud from "./WordCloud";
import PieChartComponent from "./PieChart";
import { Card, CardContent } from "@mui/material";
import classes from "./Dashboard.module.css";
import { UpdateContext } from "../Context/UpdateContext";
import { useContext, useState, useEffect } from "react";
function Dashboard() {
  const { updateWordCloud } = useContext(UpdateContext);
  const [imageUrl, setImageUrl] = useState("/wordcloud.svg");

  useEffect(() => {
    // Update the image URL to trigger a re-fetch
    setImageUrl(`/wordcloud.svg?timestamp=${new Date().getTime()}`);
  }, [updateWordCloud]);

  return (
    <div className={classes.dashboardBackground}>
      <Card className={classes.column}>
        <CardContent>
          <WordCloud imageUrl={imageUrl} />
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
