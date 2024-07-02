import React from "react";
import classes from "./WordCloud.module.css";
export default function WordCloud({ imageUrl }) {
  return (
    <>
      <h2 className={classes.title}>
        Most Used Words In The Latest Document Added
      </h2>
      <div className={classes.wordCloudContainer}>
        <img
          src={imageUrl}
          alt="Word Cloud"
          className={classes.wordCloudImage}
        />
      </div>
    </>
  );
}
