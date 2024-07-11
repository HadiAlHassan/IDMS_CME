import React from "react";
import WordCloud from "./WordCloud";
import PieChartComponent from "./PieChart";
import { Card, CardContent } from "@mui/material";
import classes from "./Dashboard.module.css";
import { UpdateContext } from "../Context/UpdateContext";
import { useContext, useState, useEffect } from "react";
import UpcomingTrialsCard from "./UpcomingTrialsCard";
// import CasesStatusCard from "./CasesStatusCard";
// import CasesBarGraph from "./CasesBarGraph";
// import ClientsListCard from "./ClientsListCard";
import SelectImage from "../SelectComponent/ImageSelect";

function Dashboard() {
  const { updateWordCloud } = useContext(UpdateContext);
  const [imageUrl, setImageUrl] = useState("/wordcloud.png");

  useEffect(() => {
    // Update the image URL to trigger a re-fetch
    setImageUrl(
      (prevUrl) => `${prevUrl.split("?")[0]}?timestamp=${new Date().getTime()}`
    );
  }, [updateWordCloud]);

  const handleImageChange = (newImagePath) => {
    setImageUrl(newImagePath);
  };

  return (
    <div className={classes.dashboardBackground}>
      <Card className={classes.column}>
        <CardContent>
          <WordCloud imageUrl={imageUrl} />
          <SelectImage onImageChange={handleImageChange} />
        </CardContent>
      </Card>
      <Card className={classes.column}>
        <CardContent>
          <PieChartComponent />
        </CardContent>
      </Card>
      <Card className={classes.column}>
        <CardContent>
          <UpcomingTrialsCard />
        </CardContent>
      </Card>

      {/* <CasesStatusCard />
      <CasesBarGraph />
      <ClientsListCard /> */}
    </div>
  );
}

export default Dashboard;
