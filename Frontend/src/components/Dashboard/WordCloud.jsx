import React from "react";
import classes from "./WordCloud.module.css";
export default function WordCloud() {
  return (
    <>
      <h2 className={classes.title}>Most Used Words</h2>
      <div className={classes.wordCloudContainer}>
        <img
          src="/wordcloud.svg"
          alt="Word Cloud"
          className={classes.wordCloudImage}
        />
      </div>
    </>
  );
}
