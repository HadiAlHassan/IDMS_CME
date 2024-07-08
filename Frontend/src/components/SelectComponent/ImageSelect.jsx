import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import classes from "./ImageSelect.module.css";

export default function SelectImage({ onImageChange }) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [imagePath, setImagePath] = React.useState("/wordcloud.png");
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = (newPath) => {
    if (newPath) {
      setImagePath(newPath);
      onImageChange(newPath); // Notify parent component of the change
    }
    setAnchorEl(null);
  };

  return (
    <Box className={classes.selectBox}>
      <Button
        id="basic-button"
        aria-controls={open ? "basic-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        onClick={handleClick}
        className={classes.menuButton}
      >
        Select Image
      </Button>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={() => handleClose(null)}
        MenuListProps={{
          "aria-labelledby": "basic-button",
        }}
      >
        <MenuItem onClick={() => handleClose("/wordcloud.png")}>
          Latest Wordcloud
        </MenuItem>
        <MenuItem onClick={() => handleClose("/general_wordcloud.png")}>
          General Wordcloud
        </MenuItem>
      </Menu>
    </Box>
  );
}
