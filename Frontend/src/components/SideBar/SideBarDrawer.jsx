import React, { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import ArticleIcon from "@mui/icons-material/Article";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import axios from "axios";
import classes from "./SideBarDrawer.module.css";
import { Button } from "@mui/material";

function SideBarDrawer() {
  const [open, setOpen] = useState(false);
  const [newsItems, setNewsItems] = useState([]);

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/get-news");
        setNewsItems(response.data.news);
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
      {newsItems.map((newsItem, index) => (
        <Card key={index} className={classes.newsCard}>
          <CardContent>
            <Link
              href={newsItem.link}
              target="_blank"
              className={classes.newsLink}
            >
              <Typography variant="h6" component="div">
                {newsItem.title}
              </Typography>
            </Link>
            <Typography variant="body2" color="textSecondary">
              {newsItem.description}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );

  return (
    <div>
      <Button
        className={classes.sideBarButton}
        variant="outlined"
        color="inherit"
        onClick={toggleDrawer(true)}
        sx={{ paddingLeft: 0, paddingRight: 0 }}
      >
        <img
          src="/icons/newspaper.png"
          alt="News"
          className={classes.iconImage}
        />
      </Button>
      <Drawer anchor="right" open={open} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>
    </div>
  );
}

export default SideBarDrawer;
