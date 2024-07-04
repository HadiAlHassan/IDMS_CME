import React from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/joy/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import htmlReactParser from "html-react-parser";
import classes from "./SideBarDrawer.module.css";
import axios from "axios";
import { useState, useEffect } from "react";

function SideBarDrawer() {
  const [open, setOpen] = useState(false);
  const [newsHTML, setNewsHTML] = useState("");

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/get-news");
        setNewsHTML(response.data.news);
      } catch (error) {
        console.error("Error fetching news:", error);
      }
    };

    fetchNews();
  }, []);

  const DrawerList = (
    <Box
      className={classes.sideBar}
      role="presentation"
      onClick={toggleDrawer(false)}
    >
      <h2 className={classes.sideBarHeader}>What's New?</h2>
      {htmlReactParser(newsHTML)}
    </Box>
  );

  return (
    <div>
      <IconButton
        className={classes.sideBarButton}
        variant="outlined"
        color="inherit"
        onClick={toggleDrawer(true)}
      >
        <MenuIcon />
      </IconButton>
      <Drawer open={open} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>
    </div>
  );
}

export default SideBarDrawer;

//   const newsHtml = `
// <div>
//   <div class="${classes.newsItem}">
//     <a href='https://www.reuters.com/legal/cancer-victims-lose-bid-block-proposed-jj-talc-bankruptcy-2024-06-29/' target='_blank'>Cancer victims lose bid to block proposed J&J talc bankruptcy</a>
//     <br><img src='https://cloudfront-us-east-2.images.arcpublishing.com/reuters/MRWARSMVCVMCNNOHSEIMY5FLHE.jpg' alt='Image for Cancer victims lose bid to block proposed J&J talc bankruptcy'>
//   </div>
//   <div class="${classes.newsItem}">
//     <a href='https://www.reuters.com/legal/government/texas-justices-revive-lawsuit-by-judge-censured-over-same-sex-marriage-stance-2024-06-28/' target='_blank'>Texas justices revive lawsuit by judge censured over same-sex marriage stance</a>
//     <br><img src='https://cloudfront-us-east-2.images.arcpublishing.com/reuters/WGKMI6HJWVODHMPEWCVDNQPRGU.jpg' alt='Image for Texas justices revive lawsuit by judge censured over same-sex marriage stance'>
//   </div>
//   <div class="${classes.newsItem}">
//     <a href='https://www.reuters.com/sustainability/biden-tailpipe-emission-rules-shakier-ground-after-supreme-court-ruling-2024-07-01/' target='_blank'>Biden tailpipe emission rules on shakier ground after Supreme Court ruling</a>
//     <br><img src='https://cloudfront-us-east-2.images.arcpublishing.com/reuters/Y6I7VMDGXFI5PC472WVYV6WNA4.jpg' alt='Image for Biden tailpipe emission rules on shakier ground after Supreme Court ruling'>
//   </div>
//   <div class="${classes.newsItem}">
//     <a href='https://www.reuters.com/technology/meta-charged-with-failing-comply-with-eu-tech-rules-2024-07-01/' target='_blank'>Meta's pay or consent model in crosshairs for breaching EU tech rules</a>
//     <br><img src='https://cloudfront-us-east-2.images.arcpublishing.com/reuters/ZQJM7DIJDBPNTP7RS3M636OF3M.jpg' alt='Image for Meta's pay or consent model in crosshairs for breaching EU tech rules'>
//   </div>
// </div>
// `;
